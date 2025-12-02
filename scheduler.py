#!/usr/bin/env python3
"""
Minecraft Server Scheduler

This script automatically starts and stops a Minecraft server based on
configured schedule times to save power and bandwidth.
"""

import schedule
import time
import signal
import sys
from datetime import datetime

import config
from server_manager import MinecraftServerManager


def create_scheduler():
    """Create and configure the scheduler."""
    server = MinecraftServerManager()

    def start_job():
        """Job to start the server."""
        print(f"[{datetime.now()}] Scheduled server start triggered.")
        server.start_server()

    def stop_job():
        """Job to stop the server."""
        print(f"[{datetime.now()}] Scheduled server stop triggered.")
        server.stop_server()

    def signal_handler(sig, frame):
        """Handle shutdown signals gracefully."""
        print("\nShutdown signal received. Stopping server if running...")
        server.stop_server()
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Schedule the jobs
    schedule.every().day.at(config.START_TIME).do(start_job)
    schedule.every().day.at(config.STOP_TIME).do(stop_job)

    print(f"Minecraft Server Scheduler Started")
    print(f"=" * 40)
    print(f"Server directory: {config.SERVER_DIR}")
    print(f"Start time: {config.START_TIME}")
    print(f"Stop time: {config.STOP_TIME}")
    print(f"Current server status: {server.get_status()}")
    print(f"=" * 40)
    print("Press Ctrl+C to stop the scheduler.\n")

    return server


def should_server_be_running():
    """Determine if the server should currently be running based on schedule."""
    now = datetime.now()
    current_time = now.hour * 60 + now.minute

    start_parts = config.START_TIME.split(":")
    start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])

    stop_parts = config.STOP_TIME.split(":")
    stop_minutes = int(stop_parts[0]) * 60 + int(stop_parts[1])

    # Handle overnight schedule (e.g., start at 07:00, stop at 02:00)
    if stop_minutes < start_minutes:
        # Server runs from start_time until midnight, and from midnight until stop_time
        return current_time >= start_minutes or current_time < stop_minutes
    else:
        # Normal schedule (start before stop in same day)
        return start_minutes <= current_time < stop_minutes


def main():
    """Main entry point."""
    server = create_scheduler()

    # Check if server should be running at startup
    if should_server_be_running():
        print("Based on schedule, server should be running. Starting now...")
        server.start_server()
    else:
        print("Based on schedule, server should not be running.")

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
