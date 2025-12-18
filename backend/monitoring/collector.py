from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.orm import Session

import config
from monitoring.netmiko_client import get_interface_stats
from monitoring.snmp_client import get_snmp_metrics
from models.metrics import Metric
from models.alerts import Alert


def poll_device(session: Session, device: Dict) -> Dict:
    snmp = get_snmp_metrics(device)
    interfaces = get_interface_stats(device)

    _persist_metric(session, device["id"], "cpu", snmp["cpu"])
    _persist_metric(session, device["id"], "memory", snmp["memory"])
    _persist_metric(session, device["id"], "packet_loss", snmp["packet_loss"])

    alerts = _generate_alerts(session, device["id"], snmp)
    return {"device": device["id"], "snmp": snmp, "interfaces": interfaces, "alerts": alerts}


def _persist_metric(session: Session, device_id: str, metric_type: str, value: float) -> None:
    metric = Metric(device_id=device_id, metric_type=metric_type, value=value)
    session.add(metric)
    session.commit()


def _generate_alerts(session: Session, device_id: str, snmp: Dict) -> List[Alert]:
    alerts: List[Alert] = []
    if snmp["cpu"] > config.CPU_THRESHOLD:
        alerts.append(_record_alert(session, device_id, "high", "CPU above threshold", "cpu", snmp["cpu"]))
    if snmp["packet_loss"] > config.PACKET_LOSS_THRESHOLD:
        alerts.append(_record_alert(session, device_id, "high", "Packet loss above threshold", "packet_loss", snmp["packet_loss"]))
    return alerts


def _record_alert(session: Session, device_id: str, severity: str, message: str, metric_type: str, value: float) -> Alert:
    alert = Alert(device_id=device_id, severity=severity, message=message, metric_type=metric_type, value=value)
    session.add(alert)
    session.commit()
    return alert


def recent_metrics(session: Session, device_id: str, metric_type: str, minutes: int = 60) -> List[Metric]:
    since = datetime.utcnow() - timedelta(minutes=minutes)
    stmt = (
        select(Metric)
        .where(Metric.device_id == device_id)
        .where(Metric.metric_type == metric_type)
        .where(Metric.timestamp >= since)
        .order_by(Metric.timestamp.desc())
    )
    return list(session.scalars(stmt).all())


def recent_alerts(session: Session, device_id: str | None = None, limit: int = 50) -> List[Alert]:
    stmt = select(Alert).order_by(Alert.timestamp.desc()).limit(limit)
    if device_id:
        stmt = stmt.where(Alert.device_id == device_id)
    return list(session.scalars(stmt).all())
