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

    # =========== #
    # INIT METHOD #
    # =========== #
    def __enter__(self):
        """Ran when the class is initialized using `with`."""
        return self

    # =========== #
    # INIT METHOD #
    # =========== #
    def __exit__(self, exc_type, exc_value, traceback):
        """Ran when the class is initialized using `with` and the execution is leaving the block."""
        self.conn.close()

    # ======================== #
    # PLAYER CAREER AVG METHOD #
    # ======================== #
    def get_player_career_avg(self, player_id):
        """### Parameters : `player_id (int)`
        The method takes as input the `id` of a player and fetches all games he or she played, all
        their statlines and calculates the average statline produced by them.

        #### IN CASE OF `NULL`:
        Every average stat is calculated on the number of statlines including that particular statistic;
        for example, Wilt Chamberlain played in an era where blocks were not tracked, but there are some
        unofficial tracked statlines of his that include blocks. His career block average will be calculated
        on the total number of statlines including blocks and not on his total number of games.

        This means that `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages.
        """

        cur = self.conn.cursor()
        cur.callproc("player_career_avg", (player_id))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()

        return results

    # ======================== #
    # PLAYER SEASON AVG METHOD #
    # ======================== #
    def get_player_season_avg(self, player_id, season):
        """### Parameters: `player_id` int, `season` int >= 1946
        This method returns as a `list` the averages in every base stat of a single player during a single season.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        cur.callproc("player_season_avg", (player_id, season))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()

        return results

    # ====================== #
    # TEAM SEASON AVG METHOD #
    # ====================== #
    def get_team_season_avg(self, team_id, season):
        """### Parameters: `team_id` int, `season` int >= 1946
        This method returns as a `list` the averages in every base stat of a single player during a single season.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.

        ###### TODO: solve some problems regarding database tables identification
        """

        cur = self.conn.cursor()
        cur.callproc("team_season_avg", (team_id, season))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()

        return results

    # ======================== #
    # LEAGUE SEASON AVG METHOD #
    # ======================== #
    def get_league_season_avg(self, league_id, season):
        """### Parameters: `league_id` str, `season` int >= 1946
        This method returns as a `list` the averages in every base stat of a single player during a single season.
        #### IN CASE OF `NULL`:
        `NULL` values are NOT treated as `0`, and statlines including `NULL` values are NOT
        automatically excluded from the calculation of the averages. Instead, every statistic average will be
        calculated with the number of available statlines containing that particular stat.
        """
        cur = self.conn.cursor()
        cur.callproc("league_season_avg", (league_id, season))

        # Initializing variable as a list where the final output will be appended:
        results = []
        for result in cur.stored_results():
            results.append(result.fetchall())

        cur.close()

        return results
