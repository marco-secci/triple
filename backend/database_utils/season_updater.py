from datetime import datetime
from db_connector import connect_to_db as conn

# Get the current year
current_year = datetime.now().year

# Connect to MariaDB
conn = conn()
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS seasons (
    season INT NOT NULL PRIMARY KEY (season)
) AUTO_INCREMENT=1946;
"""
)

# Insert new season if it's not already there
cursor.execute("INSERT IGNORE INTO seasons (season) VALUES (%s);", (current_year,))

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
