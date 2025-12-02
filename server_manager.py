"""
Server manager module for starting and stopping the Minecraft server.
"""

import subprocess
import time
import os
import signal
import sys

import config


class MinecraftServerManager:
    """Manages the Minecraft server process."""

    def __init__(self):
        self.process = None

    def start_server(self):
        """Start the Minecraft server."""
        if self.is_running():
            print("Server is already running.")
            return False

        print(f"Starting Minecraft server in {config.SERVER_DIR}...")

        try:
            # Change to server directory and start the server
            self.process = subprocess.Popen(
                config.SERVER_START_COMMAND,
                shell=True,
                cwd=config.SERVER_DIR,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            print(f"Server started with PID: {self.process.pid}")
            return True
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False

    def stop_server(self):
        """Stop the Minecraft server gracefully."""
        if not self.is_running():
            print("Server is not running.")
            return False

        print("Stopping Minecraft server...")

        try:
            # Send the stop command to the server
            if self.process and self.process.stdin:
                self.process.stdin.write("stop\n")
                self.process.stdin.flush()
                print("Sent 'stop' command to server.")

            # Wait for graceful shutdown
            print(f"Waiting up to {config.SHUTDOWN_TIMEOUT} seconds for server to stop...")
            try:
                self.process.wait(timeout=config.SHUTDOWN_TIMEOUT)
                print("Server stopped gracefully.")
            except subprocess.TimeoutExpired:
                print("Server did not stop in time, forcing termination...")
                self.process.terminate()
                time.sleep(5)
                if self.process.poll() is None:
                    self.process.kill()
                print("Server forcefully terminated.")

            self.process = None
            return True
        except Exception as e:
            print(f"Error stopping server: {e}")
            return False

    def is_running(self):
        """Check if the server is currently running."""
        if self.process is None:
            return False
        return self.process.poll() is None

    def get_status(self):
        """Get the current server status."""
        if self.is_running():
            return f"Running (PID: {self.process.pid})"
        return "Stopped"
