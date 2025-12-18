import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

SIMULATION_MODE = os.getenv("SIMULATION_MODE", "true").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'monitor.db'}")
API_KEY = os.getenv("API_KEY", "change-me")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
ALERT_SMS_TO = os.getenv("ALERT_SMS_TO")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "alerts@example.com")
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80"))
PACKET_LOSS_THRESHOLD = float(os.getenv("PACKET_LOSS_THRESHOLD", "5"))

DEVICES = [
    {
        "id": "aruba-s2500-48p",
        "name": "Aruba S2500-48P Switch",
        "host": os.getenv("DEVICE1_HOST", "192.0.2.10"),
        "username": os.getenv("DEVICE1_USER", "admin"),
        "password": os.getenv("DEVICE1_PASS", "password"),
        "device_type": "aruba_os",  # netmiko device type
        "snmp_community": os.getenv("DEVICE1_COMMUNITY", "public"),
    },
    {
        "id": "core-switch-2",
        "host": os.getenv("DEVICE2_HOST", "192.0.2.20"),
        "username": os.getenv("DEVICE2_USER", "admin"),
        "password": os.getenv("DEVICE2_PASS", "password"),
        "device_type": "aruba_os",
        "snmp_community": os.getenv("DEVICE2_COMMUNITY", "public"),
    },
]
