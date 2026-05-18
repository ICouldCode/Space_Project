from src.database.db import db

def run():
    db.execute("""
        CREATE TABLE IF NOT EXISTS tle_history (
            id         SERIAL PRIMARY KEY,
            cat_nr     INTEGER NOT NULL,
            name       VARCHAR(100) NOT NULL,
            line1      VARCHAR(100) NOT NULL,
            line2      VARCHAR(100) NOT NULL,
            fetched_at TIMESTAMP DEFAULT NOW()
        );
    """)
    print("Migrations complete.")

if __name__ == "__main__":
    run()