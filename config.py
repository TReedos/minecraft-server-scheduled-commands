"""
Configuration settings for the Minecraft server scheduler.
"""

# Path to your Minecraft server directory
SERVER_DIR = "/path/to/your/minecraft/server"

# Server start command (adjust for your server type)
# For vanilla: "java -Xmx1024M -Xms1024M -jar server.jar nogui"
# For Forge: "java -Xmx4G -Xms4G -jar forge-*.jar nogui"
SERVER_START_COMMAND = "java -Xmx4G -Xms4G -jar server.jar nogui"

# Schedule times (24-hour format)
# Server will start at START_TIME and stop at STOP_TIME
START_TIME = "07:00"  # 7:00 AM
STOP_TIME = "02:00"   # 2:00 AM

# Graceful shutdown timeout (seconds)
# Time to wait after sending stop command before force killing
SHUTDOWN_TIMEOUT = 60
