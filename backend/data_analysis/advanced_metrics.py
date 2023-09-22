# Imports
import pandas as pd
import numpy as np
from backend import connect_to_db


# ====================== #
# ADVANCED METRICS CLASS #
# ====================== #
class AdvancedMetrics:
    # =========== #
    # INIT METHOD #
    # =========== #
    def __init__(self, player_id):
        # Defining variables:
        self.player_id = player_id
        self.conn = connect_to_db()  # connection to the database
        # Takes the player's stats from the database, so it's ready to work with them
        self.basic_stats = self.fetch_basic_stats_from_db()

    # ======================== #
    # FETCH BASIC STATS METHOD #
    # ======================== #
    def fetch_basic_stats_from_db(self):
        cur = self.conn.cursor()
        query = f"SELECT * FROM players_stats_table WHERE player_id = {self.player_id};"
        cur.execute(query)
        basic_stats = cur.fetchone()
        cur.close()
        return basic_stats if basic_stats else {}
