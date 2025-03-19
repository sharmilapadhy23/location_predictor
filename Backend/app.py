from flask import Flask, render_template
from flask_socketio import SocketIO
from sockets.danger_alerts import init_app, socketio

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Flask-SocketIO with the app
init_app(app)

@app.route('/')
def index():
    """Render the main page where the danger alerts pop-ups will be shown."""
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app with WebSocket support
    socketio.run(app, debug=True)
