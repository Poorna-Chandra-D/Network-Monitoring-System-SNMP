import random
from typing import Dict
from pysnmp.hlapi import (
    CommunityData,
    SnmpEngine,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
)
import config

# Simple SNMP OIDs for demo; replace with accurate device OIDs as needed.
CPU_OID = "1.3.6.1.4.1.9.2.1.58.0"
MEMORY_OID = "1.3.6.1.4.1.2021.4.6.0"
PKT_LOSS_OID = "1.3.6.1.4.1.9.9.48.1.1.1.6.1"


def get_snmp_metrics(device: Dict) -> Dict:
    if config.SIMULATION_MODE:
        return _fake_snmp(device)

    community = device.get("snmp_community", "public")
    host = device["host"]

    def _walk(oid):
        error_indication, error_status, error_index, var_binds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((host, 161), timeout=1, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
        )
        if error_indication or error_status:
            raise RuntimeError(f"SNMP error: {error_indication or error_status.prettyPrint()}")
        return float(var_binds[0][1])

    return {
        "cpu": _walk(CPU_OID),
        "memory": _walk(MEMORY_OID),
        "packet_loss": _walk(PKT_LOSS_OID),
    }


def _fake_snmp(device: Dict) -> Dict:
    return {
        "cpu": random.uniform(10, 95),
        "memory": random.uniform(30, 90),
        "packet_loss": random.uniform(0, 8),
    }
