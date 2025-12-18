import random
from typing import List, Dict
from netmiko import ConnectHandler
import config


def get_interface_stats(device: Dict) -> List[Dict]:
    if config.SIMULATION_MODE:
        return _fake_interfaces(device)

    handler = ConnectHandler(
        device_type=device["device_type"],
        host=device["host"],
        username=device["username"],
        password=device["password"],
    )
    output = handler.send_command("show interface status", use_textfsm=True)
    handler.disconnect()
    # Netmiko with textfsm returns a list of dicts; normalize fields we care about.
    return [
        {
            "interface": row.get("interface") or row.get("port"),
            "status": row.get("status", "unknown"),
            "speed": row.get("speed", "unknown"),
            "duplex": row.get("duplex", "unknown"),
            "vlan": row.get("vlan"),
        }
        for row in output or []
    ]


def _fake_interfaces(device: Dict) -> List[Dict]:
    ports = ["1/1/1", "1/1/2", "1/1/3", "1/1/4"]
    return [
        {
            "interface": p,
            "status": random.choice(["up", "up", "down"]),
            "speed": random.choice(["1G", "10G"]),
            "duplex": "full",
            "vlan": random.choice([1, 10, 20, 30]),
        }
        for p in ports
    ]
