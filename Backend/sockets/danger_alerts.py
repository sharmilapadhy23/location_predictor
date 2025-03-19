from flask_socketio import SocketIO, emit
from threading import Thread
import time

# Initialize the SocketIO instance
socketio = SocketIO()

# This function will simulate sending danger alerts
def send_danger_alerts():
    """Simulates sending danger alerts periodically."""
    while True:
        time.sleep(10)  # Simulate periodic alert every 10 seconds
        alert_message = "Danger alert! Please be cautious in your area."
        socketio.emit('danger_alert', {'message': alert_message}, broadcast=True)

# Function to start sending danger alerts in a separate thread
def start_danger_alert_thread():
    alert_thread = Thread(target=send_danger_alerts)
    alert_thread.daemon = True
    alert_thread.start()

# Function to initialize the Flask app and WebSocket
def init_app(app):
    socketio.init_app(app)
    start_danger_alert_thread()
