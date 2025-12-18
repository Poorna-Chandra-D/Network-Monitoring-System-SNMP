#!/usr/bin/env python3
"""
Test data generator for the Network Monitoring system.
Run this script to auto-generate test metrics and alerts.
"""

import sys
import os
import time
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from db import SessionLocal, init_db
from models.metrics import Metric
from models.alerts import Alert
import config

def generate_test_data(num_polls: int = 24, interval_minutes: int = 60):
    """
    Generate test metrics for the past N hours.
    
    Args:
        num_polls: Number of data points to generate (default: 24 for 24 hours)
        interval_minutes: Minutes between each data point (default: 60)
    """
    print(f"🔄 Generating test data for {num_polls} polls with {interval_minutes} minute intervals...")
    
    init_db()
    session = SessionLocal()
    
    try:
        # Generate historical data
        for i in range(num_polls):
            timestamp = datetime.utcnow() - timedelta(minutes=interval_minutes * (num_polls - i - 1))
            
            for device in config.DEVICES:
                device_id = device["id"]
                
                # Generate CPU metrics (trend with some randomness)
                cpu_base = 30 + (i / num_polls) * 40  # Trend from 30% to 70%
                cpu = cpu_base + random.uniform(-10, 10)
                cpu = max(5, min(95, cpu))  # Clamp between 5 and 95
                
                metric_cpu = Metric(
                    device_id=device_id,
                    metric_type="cpu",
                    value=cpu,
                    timestamp=timestamp
                )
                session.add(metric_cpu)
                
                # Generate Memory metrics
                memory = 40 + random.uniform(-5, 15)
                memory = max(10, min(90, memory))
                
                metric_memory = Metric(
                    device_id=device_id,
                    metric_type="memory",
                    value=memory,
                    timestamp=timestamp
                )
                session.add(metric_memory)
                
                # Generate Packet Loss metrics
                packet_loss = random.uniform(0, 3)
                if random.random() < 0.1:  # 10% chance of spike
                    packet_loss += random.uniform(5, 15)
                
                metric_loss = Metric(
                    device_id=device_id,
                    metric_type="packet_loss",
                    value=packet_loss,
                    timestamp=timestamp
                )
                session.add(metric_loss)
                
                # Generate alerts for high CPU
                if cpu > config.CPU_THRESHOLD:
                    alert = Alert(
                        device_id=device_id,
                        severity="high",
                        message=f"CPU usage above threshold: {cpu:.1f}%",
                        metric_type="cpu",
                        value=cpu,
                        timestamp=timestamp,
                        acknowledged=random.choice([True, False])
                    )
                    session.add(alert)
                
                # Generate alerts for packet loss
                if packet_loss > config.PACKET_LOSS_THRESHOLD:
                    alert = Alert(
                        device_id=device_id,
                        severity="high",
                        message=f"Packet loss above threshold: {packet_loss:.1f}%",
                        metric_type="packet_loss",
                        value=packet_loss,
                        timestamp=timestamp,
                        acknowledged=random.choice([True, False])
                    )
                    session.add(alert)
        
        session.commit()
        print(f"✅ Successfully generated test data!")
        print(f"   📊 Generated {num_polls} data points per metric per device")
        print(f"   📈 CPU metrics: 30% → 70% trend")
        print(f"   💾 Memory metrics: 40% ± 5-15%")
        print(f"   📉 Packet Loss: 0-3% baseline with occasional spikes")
        print(f"\n🔗 Access the dashboard at: http://localhost:5173")
        
    except Exception as e:
        print(f"❌ Error generating test data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate test monitoring data")
    parser.add_argument("--polls", type=int, default=24, help="Number of data points to generate (default: 24)")
    parser.add_argument("--interval", type=int, default=60, help="Minutes between data points (default: 60)")
    
    args = parser.parse_args()
    
    generate_test_data(num_polls=args.polls, interval_minutes=args.interval)
