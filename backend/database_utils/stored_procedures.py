from backend import connect_to_db
from datetime import datetime as dt

# ======================= #
# STORED PROCEDURES CLASS #
# ======================= #
class StoredProcedures:
    """# StoredProcedures class
    This class contains all methods that run stored procedures inside the database.

    The class is built as a context manager, so it has` __enter__` and `__exit__` methods
    that make possible to use this class with the `with` statement:
    - When invoked, the `with` keyword runs `__enter__`;
    - When the execution leaves the `with` block, it runs `__exit__`instead
    """

    # =========== #
    # INIT METHOD #
    # =========== #
    def __init__(self):
        """The `__init__` method here has the simple task to run the script in the `db_connector.py` file
        to connect to the database."""
        self.conn = connect_to_db()

    # ================ #
    # __ENTER__ METHOD #
    # ================ #
    def __enter__(self):
        """Ran when the class is initialized using `with`."""
        return self

    # =============== #
    # __EXIT__ METHOD #
    # =============== #
    def __exit__(self, exc_type, exc_value, traceback):
        """Ran when the class is initialized using `with` and the execution is leaving the block."""
        self.conn.close()

    # ===================================================================================================================================== #
    # ===================================================================================================================================== #
    # ========================================================= AVERAGE STATLINES ========================================================= #
    # ===================================================================================================================================== #
    # ===================================================================================================================================== #

    # ================= #
    # PLAYER AVG METHOD #
    # ================= #
    def get_player_avg(self, player_id: int, season: int=None) -> list: 
        """### Parameters:
        -`player_id`: `int`
        - `season = None`: `int` >= 1946
        This method returns as a `list` the averages in every base stat of a single player during a single season or their entire
        career, if a `season` parameter is not provided.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()

        # Get the current year - to check that the inserted season is valid:
        current_year = dt.now().year
        if season > current_year:
            raise ValueError(f"Please insert a valid season value [value inserted '{season}' is greater than the current year, {current_year}].")
        elif season < 1946:
            raise ValueError(f"Please insert a valid season value [value inserted '{season}' is lower than the first ever season, 1946].")
        if season is not None:
            cur.callproc("player_season_avg", (player_id, season))
        else:
            cur.callproc("player_career_avg", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =============== #
    # TEAM AVG METHOD #
    # =============== #
    def get_team_avg(self, team_id, season=None):
        """### Parameters:
        - `team_id`: `int`
        - `season = None` `int` >= 1946
        This method returns as a `list` the averages in every base stat of the given team during the course of the selected season,
        or for its entire existence if a `season` parameter is not provided.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """

        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("team_season_avg", (team_id, season))
        else:
            cur.callproc("team_alltime_avg", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ================= #
    # LEAGUE AVG METHOD #
    # ================= #
    def get_league_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` similar to ITA1, SPA3, etc. matching the national level
        - `season = None`: `int` >= 1946
        This method returns as a `list` the averages in every base stat of a league during a single season or its entire
        existence if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("league_season_avg", (league_id, season))
        else:
            cur.callproc("league_alltime_avg", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
    # ===================================================== PLAYER SINGLE STAT AVERAGE ===================================================== #
    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
    # ====================== #
    # MINUTES PLAYED AVERAGE #
    # ====================== #
    def get_player_mp_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average minutes played by a player in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_mp", (player_id, season))
        else:
            cur.callproc("fetch_player_career_mp", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # POINTS AVERAGE #
    # ============== #
    def get_player_pts_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average points scored by a player in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_pts", (player_id, season))
        else:
            cur.callproc("fetch_player_career_pts", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =============== #
    # ASSISTS AVERAGE #
    # =============== #
    def get_player_ast_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average assists given by a player in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_ast", (player_id, season))
        else:
            cur.callproc("fetch_player_career_ast", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # DEFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_player_dreb_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average defensive rebounds grabbed by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_dreb", (player_id, season))
        else:
            cur.callproc("fetch_player_career_dreb", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # OFFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_player_oreb_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average offensive rebounds grabbed by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_oreb", (player_id, season))
        else:
            cur.callproc("fetch_player_career_oreb", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ====================== #
    # TOTAL REBOUNDS AVERAGE #
    # ====================== #
    def get_player_treb_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average total rebounds grabbed by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_treb", (player_id, season))
        else:
            cur.callproc("fetch_player_career_treb", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # STEALS AVERAGE #
    # ============== #
    def get_player_stl_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average steals made by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_stl", (player_id, season))
        else:
            cur.callproc("fetch_player_career_stl", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # BLOCKS AVERAGE #
    # ============== #
    def get_player_blk_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average block made by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_blk", (player_id, season))
        else:
            cur.callproc("fetch_player_career_blk", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =================== #
    # FIELD GOALS AVERAGE #
    # =================== #
    def get_player_fgm_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals made by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_fgm", (player_id, season))
        else:
            cur.callproc("fetch_player_career_fgm", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # FIELD GOAL ATTEMPTS AVERAGE #
    # =========================== #
    def get_player_fga_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals attempted by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_fga", (player_id, season))
        else:
            cur.callproc("fetch_player_career_fga", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================== #
    # FREE THROW AVERAGE #
    # ================== #
    def get_player_ftm_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws made by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_ftm", (player_id, season))
        else:
            cur.callproc("fetch_player_career_ftm", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================ #
    # FREE THROWS ATTEMPTS AVERAGE #
    # ============================ #
    def get_player_fta_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws attempted  by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_fta", (player_id, season))
        else:
            cur.callproc("fetch_player_career_fta", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================= #
    # THREES POINTERS AVERAGE #
    # ======================= #
    def get_player_3pm_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average three pointers made by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_3pm", (player_id, season))
        else:
            cur.callproc("fetch_player_career_3pm", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================= #
    # THREE POINTS ATTEMPTS AVERAGE #
    # ============================= #
    def get_player_3pa_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average threes attempted by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_3pa", (player_id, season))
        else:
            cur.callproc("fetch_player_career_3pa", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================ #
    # TURNOVER AVERAGE #
    # ================ #
    def get_player_to_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average turnover given by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_to", (player_id, season))
        else:
            cur.callproc("fetch_player_career_to", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================== #
    # PERSONAL FOULS AVERAGE #
    # ====================== #
    def get_player_pf_avg(self, player_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average fouls committed by a player in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_player_season_pf", (player_id, season))
        else:
            cur.callproc("fetch_player_career_pf", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
    # ====================================================== TEAM SINGLE STAT AVERAGE ====================================================== #
    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
    # ====================== #
    # MINUTES PLAYED AVERAGE #
    # ====================== #
    def get_team_mp_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average minutes played by the average player of a team in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_history_mp", (team_id, season))
        else:
            cur.callproc("fetch_team_history_mp", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # POINTS AVERAGE #
    # ============== #
    def get_team_pts_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average points scored by a team in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_pts", (team_id, season))
        else:
            cur.callproc("fetch_team_history_pts", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =============== #
    # ASSISTS AVERAGE #
    # =============== #
    def get_team_ast_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average assists given by a team in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_ast", (team_id, season))
        else:
            cur.callproc("fetch_team_history_ast", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # DEFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_team_dreb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average defensive rebounds grabbed by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_dreb", (team_id, season))
        else:
            cur.callproc("fetch_team_history_dreb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # OFFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_team_oreb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average offensive rebounds grabbed by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_oreb", (team_id, season))
        else:
            cur.callproc("fetch_team_history_oreb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ====================== #
    # TOTAL REBOUNDS AVERAGE #
    # ====================== #
    def get_team_treb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average total rebounds grabbed by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_treb", (team_id, season))
        else:
            cur.callproc("fetch_team_history_treb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # STEALS AVERAGE #
    # ============== #
    def get_team_stl_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average steals made by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_stl", (team_id, season))
        else:
            cur.callproc("fetch_team_history_stl", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # BLOCKS AVERAGE #
    # ============== #
    def get_team_blk_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average block made by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_blk", (team_id, season))
        else:
            cur.callproc("fetch_team_history_blk", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =================== #
    # FIELD GOALS AVERAGE #
    # =================== #
    def get_team_fgm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals made by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_fgm", (team_id, season))
        else:
            cur.callproc("fetch_team_history_fgm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # FIELD GOAL ATTEMPTS AVERAGE #
    # =========================== #
    def get_team_fga_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals attempted by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_fga", (team_id, season))
        else:
            cur.callproc("fetch_team_history_fga", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================== #
    # FREE THROW AVERAGE #
    # ================== #
    def get_team_ftm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws made by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_ftm", (team_id, season))
        else:
            cur.callproc("fetch_team_history_ftm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================ #
    # FREE THROWS ATTEMPTS AVERAGE #
    # ============================ #
    def get_team_fta_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws attempted  by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_fta", (team_id, season))
        else:
            cur.callproc("fetch_team_history_fta", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================= #
    # THREES POINTERS AVERAGE #
    # ======================= #
    def get_team_3pm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average three pointers made by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_3pm", (team_id, season))
        else:
            cur.callproc("fetch_team_history_3pm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================= #
    # THREE POINTS ATTEMPTS AVERAGE #
    # ============================= #
    def get_team_3pa_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average threes attempted by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_3pa", (team_id, season))
        else:
            cur.callproc("fetch_team_history_3pa", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================ #
    # TURNOVER AVERAGE #
    # ================ #
    def get_team_to_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average turnover given by a team in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_to", (team_id, season))
        else:
            cur.callproc("fetch_team_history_to", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================== #
    # PERSONAL FOULS AVERAGE #
    # ====================== #
    def get_team_pf_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average fouls committed by a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_team_season_pf", (team_id, season))
        else:
            cur.callproc("fetch_team_history_pf", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================================================================================================================================== #
    # ======================================================================================================================================== #
    # ====================================================== LEAGUE SINGLE STAT AVERAGE ====================================================== #
    # ======================================================================================================================================== #
    # ======================================================================================================================================== #
    # ====================== #
    # MINUTES PLAYED AVERAGE #
    # ====================== #
    def get_league_mp_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `player_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average minutes played by the average player of a league in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_mp", (league_id, season))
        else:
            cur.callproc("fetch_league_history_mp", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # POINTS AVERAGE #
    # ============== #
    def get_league_pts_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average points scored by the league in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_pts", (league_id, season))
        else:
            cur.callproc("fetch_league_history_pts", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =============== #
    # ASSISTS AVERAGE #
    # =============== #
    def get_league_ast_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average assists given by the league in a single season, or during their
        entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_ast", (league_id, season))
        else:
            cur.callproc("fetch_league_history_ast", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # DEFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_league_dreb_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average defensive rebounds grabbed by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_dreb", (league_id, season))
        else:
            cur.callproc("fetch_league_history_dreb", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ========================== #
    # OFFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_league_oreb_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average offensive rebounds grabbed by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_oreb", (league_id, season))
        else:
            cur.callproc("fetch_league_history_oreb", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ====================== #
    # TOTAL REBOUNDS AVERAGE #
    # ====================== #
    def get_league_treb_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average total rebounds grabbed by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_treb", (league_id, season))
        else:
            cur.callproc("fetch_league_history_treb", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # STEALS AVERAGE #
    # ============== #
    def get_league_stl_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average steals made by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_stl", (league_id, season))
        else:
            cur.callproc("fetch_league_history_stl", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # ============== #
    # BLOCKS AVERAGE #
    # ============== #
    def get_league_blk_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average block made by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_blk", (league_id, season))
        else:
            cur.callproc("fetch_league_history_blk", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return results

    # =================== #
    # FIELD GOALS AVERAGE #
    # =================== #
    def get_league_fgm_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals made by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_fgm", (league_id, season))
        else:
            cur.callproc("fetch_league_history_fgm", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # FIELD GOAL ATTEMPTS AVERAGE #
    # =========================== #
    def get_league_fga_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals attempted by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_fga", (league_id, season))
        else:
            cur.callproc("fetch_league_history_fga", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================== #
    # FREE THROW AVERAGE #
    # ================== #
    def get_league_ftm_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws made by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_ftm", (league_id, season))
        else:
            cur.callproc("fetch_league_history_ftm", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================ #
    # FREE THROWS ATTEMPTS AVERAGE #
    # ============================ #
    def get_league_fta_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws attempted  by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_fta", (league_id, season))
        else:
            cur.callproc("fetch_league_history_fta", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================= #
    # THREES POINTERS AVERAGE #
    # ======================= #
    def get_league_3pm_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average three pointers made by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_3pm", (league_id, season))
        else:
            cur.callproc("fetch_league_history_3pm", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================= #
    # THREE POINTS ATTEMPTS AVERAGE #
    # ============================= #
    def get_league_3pa_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average threes attempted by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_3pa", (league_id, season))
        else:
            cur.callproc("fetch_league_history_3pa", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================ #
    # TURNOVER AVERAGE #
    # ================ #
    def get_league_to_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `str` like ITA1, ITA2, SPA1, etc.
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average turnover given by the league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_to", (league_id, season))
        else:
            cur.callproc("fetch_league_history_to", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================== #
    # PERSONAL FOULS AVERAGE #
    # ====================== #
    def get_league_pf_avg(self, league_id, season=None):
        """
        ### Parameters:
        - `league_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average fouls committed by a league in
        a single season, or during their entire career if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_league_season_pf", (league_id, season))
        else:
            cur.callproc("fetch_league_history_pf", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ========================================================================================================================================== #
    # ========================================================================================================================================== #
    # ====================================================== OPPONENT SINGLE STAT AVERAGE ====================================================== #
    # ========================================================================================================================================== #
    # ========================================================================================================================================== #
    # ====================== #
    # MINUTES PLAYED AVERAGE #
    # ====================== #
    def get_opp_mp_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average minutes played against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_mp", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_mp", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ===================== #
    # POINTS SCORED AVERAGE #
    # ===================== #
    def get_opp_pts_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average points scored against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_pts", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_pts", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =============== #
    # ASSISTS AVERAGE #
    # =============== #
    def get_opp_ast_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average assists made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_ast", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_ast", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ========================== #
    # DEFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_opp_dreb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average defensive rebounds grabbed against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_dreb", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_dreb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ========================== #
    # OFFENSIVE REBOUNDS AVERAGE #
    # ========================== #
    def get_opp_oreb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average offensive rebounds grabbed against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_oreb", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_oreb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================== #
    # TOTAL REBOUNDS AVERAGE #
    # ====================== #
    def get_opp_treb_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average total rebounds grabbed against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_treb", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_treb", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============== #
    # STEALS AVERAGE #
    # ============== #
    def get_opp_stl_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average steals got against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_stl", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_stl", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============== #
    # BLOCKS AVERAGE #
    # ============== #
    def get_opp_blk_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average blocked shots against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_blk", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_blk", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================== #
    # FIELD GOALS MADE AVERAGE #
    # ======================== #
    def get_opp_fgm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goals made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_fgm", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_fgm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # FIELD GOAL ATTEMPTS AVERAGE #
    # =========================== #
    def get_opp_fga_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average field goal attempts against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_fga", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_fga", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # THREE POINTERS MADE AVERAGE #
    # =========================== #
    def get_opp_3pm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average three pointers made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_3pm", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_3pm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ============================ #
    # THREE POINT ATTEMPTS AVERAGE #
    # ============================ #
    def get_opp_3pa_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average three pointers attempted against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_3pa", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_3pa", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ======================== #
    # FREE THROWS MADE AVERAGE #
    # ======================== #
    def get_opp_ftm_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throws made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_ftm", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_ftm", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # =========================== #
    # FREE THROW ATTEMPTS AVERAGE #
    # =========================== #
    def get_opp_fta_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average free throw attempted against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_fta", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_fta", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ================ #
    # TURNOVER AVERAGE #
    # ================ #
    def get_opp_to_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average turnovers made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_to", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_to", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result

    # ====================== #
    # PERSONAL FOULS AVERAGE #
    # ====================== #
    def get_opp_pf_avg(self, team_id, season=None):
        """
        ### Parameters:
        - `team_id`: `int`
        - `season = None`: `int` >= 1946
        Returns a `list` parameter with the average turnovers made against a team in
        a single season, or during their entire history if `season = None`.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        if season is not None:
            cur.callproc("fetch_opp_season_pf", (team_id, season))
        else:
            cur.callproc("fetch_opp_history_pf", (team_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result
