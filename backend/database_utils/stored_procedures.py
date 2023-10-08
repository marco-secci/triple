import mysql.connector
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
            cur.callproc("player_career_avg", (player_id, None))

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
            cur.callproc("team_alltime_avg", (team_id, None))

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
        """### Parameters:
        - `league_id`: `str` similar to ITA1, SPA3, etc. matching the national level
        - `season) None`: `int` >= 1946
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
            cur.callproc("league_alltime_avg", (league_id, None))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()

        return results
