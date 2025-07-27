# Mock GPS API

A Flask application that provides mock GPS data

## Features
- **Continuous GPX Route Simulation**: Both user and dog continuously loop through the GPX route
- **Realistic Tracking Scenario**: Dog stays ahead of user by 15 seconds, creating a natural following effect
- **Simple Visibility Control**: Start/Stop tracking just controls dog visibility on the map
- **Real-time Updates**: 1-second intervals for smooth movement

## How It Works
- **User Position**: Always shows current GPX route position (continuously moving)
- **Dog Position**: Always 15 seconds ahead of user on the same GPX route
- **Start Tracking**: Shows dog icon on map and enables distance display
- **Stop Tracking**: Hides dog icon and distance display, user continues moving

## Endpoints
- `GET /user_location` — Get current user position from GPX route
- `GET /user_follow_location` — Same as user_location (for compatibility)
- `GET /dog_location` — Get current dog position (returns None when hidden)
- `POST /start_tracking` — Show dog on map and enable distance tracking
- `POST /stop_tracking` — Hide dog from map and disable distance tracking

## Usage
1. Place your `route.gpx` file in this directory
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   python app.py
   ```
4. The demo app will automatically connect and start displaying user movement

## Configuration
- `UPDATE_INTERVAL = 1` — Seconds between position updates
- `DOG_AHEAD_DELAY = 15` — Seconds ahead of user (dog will be 15 points ahead)
- `GPX_FILE = 'route.gpx'` — GPX file to use for route simulation

---

**Both user and dog continuously loop through the GPX route, creating a seamless demo experience.**
