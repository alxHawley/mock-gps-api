from flask import Flask, jsonify, request
import threading
import time
import gpxpy

app = Flask(__name__)

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
def user_location():
    """Always return current user position from GPX loop"""
    if len(route_points) > 0:
        lat, lon = route_points[user_index]
        return jsonify({'lat': lat, 'lon': lon})
    return jsonify({'lat': None, 'lon': None})

@app.route('/start_tracking', methods=['POST'])
def start_tracking():
    global show_dog
    print(f"start_tracking called - showing dog: {show_dog}")
    show_dog = True
    print(f"start_tracking - set show_dog to: {show_dog}")
    return jsonify({'status': 'tracking started'})

@app.route('/stop_tracking', methods=['POST'])
def stop_tracking():
    global show_dog
    print(f"stop_tracking called - showing dog: {show_dog}")
    show_dog = False
    print(f"stop_tracking - set show_dog to: {show_dog}")
    return jsonify({'status': 'tracking stopped'})

@app.route('/dog_location')
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
def user_follow_location():
    """Always return current user position from GPX loop (same as user_location)"""
    if len(route_points) > 0:
        lat, lon = route_points[user_index]
        print(f"Returning user follow location: lat={lat}, lon={lon}")
        return jsonify({'lat': lat, 'lon': lon})
    print(f"Returning None - no route points loaded")
    return jsonify({'lat': None, 'lon': None})

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
    app.run(port=5001, debug=True) 