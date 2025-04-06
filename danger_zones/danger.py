from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Sample function that simulates fetching danger zones
def fetch_danger_zones(location):
    # Replace with your API or method to fetch danger zones
    try:
        # Simulating an API call for example purposes
        response = requests.get(f"http://api.example.com/dangerzones?location={location}")
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()        # Assumes the response is JSON
    except Exception as e:
        print(f"Error: {e}")
        return None  # Return None if there's an error

@app.route('/', methods=['GET', 'POST'])
def index():
    danger_zones = None
    error_message = None

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            danger_zones = fetch_danger_zones(location)
            if danger_zones is None:
                error_message = "Error fetching danger zones. Please try again."
        else:
            error_message = "Please enter a valid location."

    return render_template('maps.html', danger_zones=danger_zones, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)