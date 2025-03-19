import os

# Basic Flask Configuration
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'os.urandom(24)')  # Replace with a strong secret key for production
    SESSION_COOKIE_SECURE = True  # Set to True if using https
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Database Configurations (Example)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')  # Database URI (SQLite in this case)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary overhead

# SocketIO Configurations
class SocketIOConfig:
    """SocketIO configurations."""
    MESSAGE_QUEUE = os.environ.get('REDIS_URL', 'redis://localhost:6379')  # Redis server for managing the message queue
    SESSION_PROVIDERS = {
        'redis': {
            'url': MESSAGE_QUEUE
        }
    }
    # Set the logging level for socket events (optional)
    SOCKETIO_LOGGING_LEVEL = 'DEBUG'  # 'DEBUG', 'INFO', or 'ERROR'

# Extend the Config class
class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration with debugging disabled."""
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Should be set securely in production

# Select the appropriate configuration based on the environment
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
