#!/usr/bin/env python3
"""
Continuous data generator for live monitoring testing.
This script simulates real-time data collection by polling devices at regular intervals.
"""

import sys
import os
import time
import signal
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from db import SessionLocal, init_db
from monitoring import collector
import config

class DataGenerator:
    def __init__(self, interval_seconds: int = 21600):
        self.interval = interval_seconds
        self.running = True
        self.poll_count = 0
        
    def handle_signal(self, signum, frame):
        """Handle SIGINT (Ctrl+C) gracefully"""
        print("\n\n⏹️  Stopping data generator...")
        self.running = False
        
    def run(self):
        """Start the continuous data generation loop"""
        signal.signal(signal.SIGINT, self.handle_signal)
        
        init_db()
        print(f"🚀 Starting continuous data generator")
        print(f"   📊 Polling every {self.interval} seconds")
        print(f"   🎯 Devices: {', '.join([d['id'] for d in config.DEVICES])}")
        print(f"   🔄 Simulation Mode: {config.SIMULATION_MODE}")
        print(f"\n💡 Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                self.poll_count += 1
                timestamp = datetime.utcnow().strftime("%H:%M:%S")
                
                session = SessionLocal()
                try:
                    print(f"[{timestamp}] Poll #{self.poll_count}: ", end="", flush=True)
                    
                    for device in config.DEVICES:
                        result = collector.poll_device(session, device)
                        cpu = result['snmp']['cpu']
                        memory = result['snmp']['memory']
                        packet_loss = result['snmp']['packet_loss']
                        
                        status = "✅"
                        alerts = len(result.get('alerts', []))
                        if alerts > 0:
                            status = f"⚠️  ({alerts} alerts)"
                        
                        print(f"{device['id']} {status} ", end="", flush=True)
                    
                    print()
                    
                except Exception as e:
                    print(f"\n❌ Error during poll: {e}")
                finally:
                    session.close()
                
                # Wait for the next poll
                time.sleep(self.interval)
        
        except KeyboardInterrupt:
            pass
        
        print(f"\n✅ Data generator stopped after {self.poll_count} polls")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate continuous monitoring data")
    parser.add_argument("--interval", type=int, default=21600, help="Seconds between polls (default: 21600 = 6 hours)")
    
    args = parser.parse_args()
    
    generator = DataGenerator(interval_seconds=args.interval)
    generator.run()
