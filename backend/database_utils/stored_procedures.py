from backend import connect_to_db


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

    # ================== #
    # PLAYER AVG METHOD #
    # ================= #
    def get_player_avg(self, player_id, season=None):
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

    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
    # ====================================================== TEAM SINGLE STAT AVERAGE ====================================================== #
    # ====================================================================================================================================== #
    # ====================================================================================================================================== #
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
            cur.callproc("fetch_team_career_pts", (team_id))

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
            cur.callproc("fetch_team_career_ast", (team_id))

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
            cur.callproc("fetch_team_career_dreb", (team_id))

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
            cur.callproc("fetch_team_career_oreb", (team_id))

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
            cur.callproc("fetch_team_career_treb", (team_id))

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
            cur.callproc("fetch_team_career_stl", (team_id))

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
            cur.callproc("fetch_team_career_blk", (team_id))

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
            cur.callproc("fetch_team_career_fgm", (team_id))

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
            cur.callproc("fetch_team_career_fga", (team_id))

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
            cur.callproc("fetch_team_career_ftm", (team_id))

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
            cur.callproc("fetch_team_career_fta", (team_id))

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
            cur.callproc("fetch_team_career_3pm", (team_id))

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
            cur.callproc("fetch_team_career_3pa", (team_id))

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
            cur.callproc("fetch_team_career_to", (team_id))

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
            cur.callproc("fetch_league_career_pts", (league_id))

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
            cur.callproc("fetch_league_career_ast", (league_id))

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
            cur.callproc("fetch_league_career_dreb", (league_id))

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
            cur.callproc("fetch_league_career_oreb", (league_id))

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
            cur.callproc("fetch_league_career_treb", (league_id))

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
            cur.callproc("fetch_league_career_stl", (league_id))

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
            cur.callproc("fetch_league_career_blk", (league_id))

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
            cur.callproc("fetch_league_career_fgm", (league_id))

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
            cur.callproc("fetch_league_career_fga", (league_id))

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
            cur.callproc("fetch_league_career_ftm", (league_id))

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
            cur.callproc("fetch_league_career_fta", (league_id))

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
            cur.callproc("fetch_league_career_3pm", (league_id))

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
            cur.callproc("fetch_league_career_3pa", (league_id))

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
            cur.callproc("fetch_league_career_to", (league_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()
        return result
