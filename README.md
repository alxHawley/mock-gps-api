# Mock GPS API

A Flask application that provides mock GPS data with Docker deployment for 24/7 operation.

## Features
- **Continuous GPX Route Simulation**: Both user and dog continuously loop through the GPX route
- **Realistic Tracking Scenario**: Dog stays ahead of user by 15 seconds, creating a natural following effect
- **Simple Visibility Control**: Start/Stop tracking just controls dog visibility on the map
- **Real-time Updates**: 1-second intervals for smooth movement
- **Docker Deployment**: Containerized for easy 24/7 operation
- **Auto-restart**: Built-in resilience with automatic restart on failure

## How It Works
- **User Position**: Always shows current GPX route position (continuously moving)
- **Dog Position**: Always 15 seconds ahead of user on the same GPX route
- **Start Tracking**: Shows dog icon on map and enables distance display
- **Stop Tracking**: Hides dog icon and distance display, user continues moving

## Quick Start (Docker - Recommended)

### Prerequisites
- Docker and Docker Compose installed
- `route.gpx` file in the project directory

### Deployment
```bash
# Build and start the service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Management Scripts
```bash
# Start/stop/restart
./manage.sh start
./manage.sh stop
./manage.sh restart

# Check health
./monitor.sh
```

## Manual Setup (Development)

### Prerequisites
- Python 3.11+
- `route.gpx` file in the project directory

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python app.py
   ```
3. The API will be available at `http://localhost:5001`

## API Endpoints
- `GET /user_location` — Get current user position from GPX route
- `GET /user_follow_location` — Same as user_location (for compatibility)
- `GET /dog_location` — Get current dog position (returns None when hidden)
- `POST /start_tracking` — Show dog on map and enable distance tracking
- `POST /stop_tracking` — Hide dog from map and disable distance tracking

## Configuration
- `UPDATE_INTERVAL = 1` — Seconds between position updates
- `DOG_AHEAD_DELAY = 15` — Seconds ahead of user (dog will be 15 points ahead)
- `GPX_FILE = 'route.gpx'` — GPX file to use for route simulation
- `PORT = 5001` — API server port

## 24/7 Deployment

For production deployment with auto-startup, see [SETUP.md](SETUP.md) for detailed instructions including:
- Systemd service configuration
- Auto-restart policies
- Health monitoring
- Troubleshooting guide

## Development vs Production

- **Development**: Use `python app.py` for local development
- **Production**: Use Docker with `docker-compose up -d` for 24/7 operation

---

**Both user and dog continuously loop through the GPX route, creating a seamless demo experience.**
