# Imports
import pandas as pd
import numpy as np
from backend import connect_to_db as conn
from database_utils.stored_procedures import StoredProcedures as sp


# ====================== #
# ADVANCED METRICS CLASS #
# ====================== #
class AdvancedMetrics:
    # =========== #
    # INIT METHOD #
    # =========== #
    def __init__(self, player_id):
        """TODO Actually there's the need to improve this class. It needs to be able to work with teams
        and leagues too, and to be more versatile rather than returning just the advanced metrics of a
        single player's career.

        """
        # Defining variables:
        self.player_id = player_id
        self.conn = conn()  # connection to the database
        # Takes the player's stats from the database, so it's ready to work with them
        self.basic_stats = sp.get_player_career_avg(self)

    # =============================== #
    # PLAYER EFFICIENCY RATING METHOD #
    # =============================== #
    def per(self):
        """TODO I need to have queries for league average and team average to calculate per"""
