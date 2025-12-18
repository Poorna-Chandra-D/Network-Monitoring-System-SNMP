import logging
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS

import config
from db import SessionLocal, init_db
from monitoring import collector
from models.alerts import Alert

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)
init_db()


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key != config.API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return wrapper


@app.route("/api/devices", methods=["GET"])
@require_api_key
def list_devices():
    return jsonify([{"id": d["id"], "host": d["host"]} for d in config.DEVICES])


@app.route("/api/metrics/<device_id>", methods=["GET"])
@require_api_key
def get_metrics(device_id: str):
    metric_type = request.args.get("metric", "cpu")
    minutes = int(request.args.get("minutes", 60))
    with SessionLocal() as session:
        metrics = collector.recent_metrics(session, device_id, metric_type, minutes)
        return jsonify(
            [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "value": m.value,
                    "metric_type": m.metric_type,
                }
                for m in metrics
            ]
        )


@app.route("/api/alerts", methods=["GET"])
@require_api_key
def get_alerts():
    device_id = request.args.get("device_id")
    limit = int(request.args.get("limit", 50))
    with SessionLocal() as session:
        alerts = collector.recent_alerts(session, device_id, limit)
        return jsonify(
            [
                {
                    "id": a.id,
                    "device_id": a.device_id,
                    "severity": a.severity,
                    "message": a.message,
                    "metric_type": a.metric_type,
                    "value": a.value,
                    "timestamp": a.timestamp.isoformat(),
                    "acknowledged": a.acknowledged,
                }
                for a in alerts
            ]
        )


@app.route("/api/poll", methods=["POST"])
@require_api_key
def poll_now():
    summary = []
    with SessionLocal() as session:
        for device in config.DEVICES:
            result = collector.poll_device(session, device)
            summary.append(result)
    return jsonify({"polled_at": datetime.utcnow().isoformat(), "devices": summary})


@app.route("/api/alerts/<int:alert_id>/ack", methods=["POST"])
@require_api_key
def acknowledge_alert(alert_id: int):
    with SessionLocal() as session:
        alert = session.get(Alert, alert_id)
        if not alert:
            return jsonify({"error": "Not found"}), 404
        alert.acknowledged = True
        session.commit()
        return jsonify({"status": "acknowledged", "id": alert_id})


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "simulation": config.SIMULATION_MODE})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
