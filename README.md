# Minecraft Server Scheduled Commands

Automatically opens and closes a locally run Minecraft server based on a schedule to save bandwidth and electricity.

## Features

- **Scheduled Start/Stop**: Automatically start and stop your Minecraft server at configured times
- **Graceful Shutdown**: Sends the `/stop` command to the server before terminating
- **Auto-detection**: Determines if the server should be running when the scheduler starts
- **Signal Handling**: Properly shuts down the server when the scheduler is stopped

## Requirements

- Python 3.7+
- A Minecraft server (vanilla, Forge, Fabric, etc.)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/TReedos/minecraft-server-scheduled-commands.git
   cd minecraft-server-scheduled-commands
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your settings in `config.py`:
   ```python
   # Path to your Minecraft server directory
   SERVER_DIR = "/path/to/your/minecraft/server"
   
   # Server start command (adjust for your server type)
   SERVER_START_COMMAND = "java -Xmx4G -Xms4G -jar server.jar nogui"
   
   # Schedule times (24-hour format)
   START_TIME = "07:00"  # 7:00 AM - Server starts
   STOP_TIME = "02:00"   # 2:00 AM - Server stops
   ```

## Usage

Run the scheduler:
```bash
python scheduler.py
```

The scheduler will:
1. Check if the server should currently be running based on the schedule
2. Start or leave the server stopped accordingly
3. Automatically start/stop the server at the configured times
4. Run continuously until you stop it with `Ctrl+C`

### Running as a Service (Linux)

To run the scheduler as a systemd service:

1. Create a service file `/etc/systemd/system/minecraft-scheduler.service`:
   ```ini
   [Unit]
   Description=Minecraft Server Scheduler
   After=network.target
   
   [Service]
   Type=simple
   User=minecraft
   WorkingDirectory=/path/to/minecraft-server-scheduled-commands
   ExecStart=/usr/bin/python3 scheduler.py
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable minecraft-scheduler
   sudo systemctl start minecraft-scheduler
   ```

### Running on Windows

You can use Task Scheduler to run the script at startup, or run it in a terminal window.

## Configuration

Edit `config.py` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `SERVER_DIR` | Path to your Minecraft server directory | `/path/to/your/minecraft/server` |
| `SERVER_START_COMMAND` | Command to start the server | `java -Xmx4G -Xms4G -jar server.jar nogui` |
| `START_TIME` | Time to start the server (24-hour format) | `07:00` |
| `STOP_TIME` | Time to stop the server (24-hour format) | `02:00` |
| `SHUTDOWN_TIMEOUT` | Seconds to wait for graceful shutdown | `60` |

## How It Works

1. The scheduler runs continuously and checks every minute for scheduled tasks
2. At `START_TIME`, it starts the Minecraft server process
3. At `STOP_TIME`, it sends the `stop` command to the server for graceful shutdown
4. If the server doesn't stop within `SHUTDOWN_TIMEOUT` seconds, it's forcefully terminated

## License

MIT License
