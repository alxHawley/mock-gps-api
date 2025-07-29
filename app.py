from flask import Flask, jsonify, request
import threading
import time
import gpxpy
import os
from functools import wraps

app = Flask(__name__)

# --- Security Config ---
API_KEY = os.environ.get('GPS_API_KEY', 'your-secret-api-key-change-this')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# --- Config ---
GPX_FILE = 'route.gpx'  
UPDATE_INTERVAL = 1     # seconds between updates
DOG_AHEAD_DELAY = 15    # seconds ahead of user (dog will be 15 points ahead)

# --- State ---
route_points = []  # List of (lat, lon)
dog_index = 0
user_index = 0
show_dog = False  # Controls whether dog location is visible
dog_thread = None
user_thread = None

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_host():
    """Check if request is from allowed host"""
    client_ip = request.remote_addr
    # For now, allow all local connections (we'll configure this properly later)
    return True

@app.before_request
def before_request():
    """Security middleware"""
    # Temporarily disabled host checking for testing
    # if not check_host():
    #     return jsonify({'error': 'Access denied'}), 403
    pass

@app.after_request
def after_request(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

def load_gpx():
    global route_points
    try:
        with open(GPX_FILE) as f:
            gpx = gpxpy.parse(f)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        route_points.append((point.latitude, point.longitude))
        print(f"Loaded {len(route_points)} route points")
    except Exception as e:
        print(f"Error loading GPX file: {e}")
        route_points = []

@app.route('/user_location')
@require_api_key
def user_location():
    """Always return current user position from GPX loop"""
    if len(route_points) > 0:
        lat, lon = route_points[user_index]
        return jsonify({'lat': lat, 'lon': lon})
    return jsonify({'lat': None, 'lon': None})

@app.route('/start_tracking', methods=['POST'])
@require_api_key
def start_tracking():
    global show_dog
    print(f"start_tracking called - showing dog: {show_dog}")
    show_dog = True
    print(f"start_tracking - set show_dog to: {show_dog}")
    return jsonify({'status': 'tracking started'})

@app.route('/stop_tracking', methods=['POST'])
@require_api_key
def stop_tracking():
    global show_dog
    print(f"stop_tracking called - showing dog: {show_dog}")
    show_dog = False
    print(f"stop_tracking - set show_dog to: {show_dog}")
    return jsonify({'status': 'tracking stopped'})

@app.route('/dog_location')
@require_api_key
def dog_location():
    print(f"dog_location called - show_dog: {show_dog}, dog_index: {dog_index}, route_points: {len(route_points)}")
    if len(route_points) > 0:
        if show_dog:
            # Ensure dog_index is within bounds
            actual_dog_index = dog_index % len(route_points)
            lat, lon = route_points[actual_dog_index]
            print(f"Returning dog location: lat={lat}, lon={lon} (index: {actual_dog_index})")
            return jsonify({'lat': lat, 'lon': lon})
        else:
            # Return None when dog is hidden
            print(f"Returning None - dog hidden")
            return jsonify({'lat': None, 'lon': None})
    print(f"Returning None - no route points loaded")
    return jsonify({'lat': None, 'lon': None})

@app.route('/user_follow_location')
@require_api_key
def user_follow_location():
    """Always return current user position from GPX loop (same as user_location)"""
    if len(route_points) > 0:
        lat, lon = route_points[user_index]
        print(f"Returning user follow location: lat={lat}, lon={lon}")
        return jsonify({'lat': lat, 'lon': lon})
    print(f"Returning None - no route points loaded")
    return jsonify({'lat': None, 'lon': None})

@app.route('/health')
def health():
    """Health check endpoint (no auth required)"""
    return jsonify({'status': 'healthy', 'route_points': len(route_points)})

def simulate_dog():
    global dog_index
    print(f"simulate_dog started - dog_index: {dog_index}")
    # Start dog ahead of user by the delay amount
    dog_index = DOG_AHEAD_DELAY
    print(f"simulate_dog - initialized dog_index to: {dog_index} (ahead of user)")
    while True:
        time.sleep(UPDATE_INTERVAL)
        dog_index += 1
        # Use modulo to keep dog_index within bounds
        dog_index = dog_index % len(route_points)
        print(f"simulate_dog - updated dog_index to: {dog_index}")

def simulate_user():
    global user_index
    print(f"simulate_user started - user_index: {user_index}")
    while True:
        time.sleep(UPDATE_INTERVAL)
        user_index += 1
        # Use modulo to keep user_index within bounds
        user_index = user_index % len(route_points)
        print(f"simulate_user - updated user_index to: {user_index}")

if __name__ == '__main__':
    try:
        load_gpx()
        # Start both simulation threads immediately
        if route_points:
            dog_thread = threading.Thread(target=simulate_dog, daemon=True)
            user_thread = threading.Thread(target=simulate_user, daemon=True)
            dog_thread.start()
            user_thread.start()
            print("Started both dog and user simulation threads")
    except Exception as e:
        print(f"Warning: Could not load GPX file: {e}")
    app.run(host='0.0.0.0', port=5001, debug=False) 