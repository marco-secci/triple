# Imports
import pandas as pd
import numpy as np
from database_utils.stored_procedures import StoredProcedures as sp


# ====================== #
# ADVANCED METRICS CLASS #
# ====================== #
class AdvancedMetrics:
    # =========== #
    # INIT METHOD #
    # =========== #
    def __init__(self, id, season=None):
        """
        ### __INIT__

        ========================

        Parameters:

        #### `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its averages will be fetched\n
            if `2000000 <= id < 3000000`, it's a player's ID so its averages will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league averages will be fetched\n

        #### `season = None`: `int`
            if a value for season is inserted as a parameter of the method, averages for that specific season
            will be fetched; otherwise, career/all-time averages will be fetched.
        """

        # If there's a season, that season's average will be fetched:
        if season is not None:
            # Checking which type of ID the method is dealing with:
            if isinstance(id, str):
                with sp():
                    # Takes the league's stats from the database, so it's ready to work with them:
                    self.basic_stats = sp.get_league_avg(id, season)
            elif id >= 1000000 and id < 2000000:
                # Takes the team's stats from the database, so it's ready to work with them:
                with sp():
                    self.basic_stats = sp.get_team_avg(id, season)
            elif id >= 2000000 and id < 3000000:
                # Takes the player's stats from the database, so it's ready to work with them:
                with sp():
                    self.basic_stats = sp.get_player_avg(id, season)
        else:
            # Checking which type of ID the method is dealing with:
            if isinstance(id, str):
                with sp():
                    # Takes the league's stats from the database, so it's ready to work with them:
                    self.basic_stats = sp.get_league_avg(id, None)
            elif id >= 1000000 and id < 2000000:
                # Takes the team's stats from the database, so it's ready to work with them:
                with sp():
                    self.basic_stats = sp.get_team_avg(id, None)
            elif id >= 2000000 and id < 3000000:
                # Takes the player's stats from the database, so it's ready to work with them:
                with sp():
                    self.basic_stats = sp.get_player_avg(id, None)

    # =========================== #
    # ASSIST OVER TURNOVER METHOD #
    # =========================== #
    def ast_over_to(self, ast, to):
        return ast / to

    # =============================== #
    # PLAYER EFFICIENCY RATING METHOD #
    # =============================== #
    def per(self):
        """TODO I need to have queries for league average and team average to calculate per"""
