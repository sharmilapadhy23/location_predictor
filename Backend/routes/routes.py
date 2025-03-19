# routes/routes.py - Main route handler

from flask import Blueprint, jsonify

# Importing other routes
from .danger_zones import danger_zones_blueprint
from .emergency import emergency_blueprint
from .prediction import prediction_blueprint

# Main Blueprint
routes_blueprint = Blueprint('routes', __name__)

# Registering other routes
routes_blueprint.register_blueprint(danger_zones_blueprint, url_prefix='/danger-zones')
routes_blueprint.register_blueprint(emergency_blueprint, url_prefix='/emergency')
routes_blueprint.register_blueprint(prediction_blueprint, url_prefix='/prediction')

# Default route
@routes_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Location Predictor API!'})
