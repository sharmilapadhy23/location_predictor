import subprocess

def create_tables():
    """Creates a table for storing predictions in PostgreSQL."""
    try:
        command = [
            "psql",
            "-U", "postgres",
            "-h", "localhost",
            "-d", "location_db",
            "-c", """
            CREATE TABLE IF NOT EXISTS location_predictions (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                predicted_latitude FLOAT NOT NULL,
                predicted_longitude FLOAT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ Predictions table created successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error creating table:", e.stderr)

create_tables()
