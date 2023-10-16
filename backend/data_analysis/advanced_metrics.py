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

        #### - `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its averages will be fetched\n
            if `2000000 <= id < 3000000`, it's a player's ID so its averages will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league averages will be fetched\n

        #### - `season = None`: `int`
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
    def ast_over_to(self, id, season=None):
        """
        ### AST_OVER_TO - Assist over Turnover Ratio

        ========================

        Description:
        This ratio is used to measure the efficiency of the subject in terms of dimes: if a player gets `10` assist
        but `10` turnovers, technically for every bucket they give to their team, they're giving one to the opponent.

        ========================

        Parameters:

        #### - `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its average `A/TO` will be fetched\n
            if `2000000 <= id < 3000000`, it's a player's ID so its average `A/TO` will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league average `A/TO` will be fetched\n

        #### - `season = None`: `int`
            if a value for season is inserted as a parameter of the method, average `A/TO` for that specific season
            will be fetched; otherwise, career/all-time average `A/TO` will be fetched.
        """
        # If there's a season, that season's average will be fetched:
        if season is not None:
            # Checking which type of ID the method is dealing with:
            if isinstance(id, str):
                with sp():
                    # Takes the league's stats from the database, so it's ready to work with them:
                    self.aotr = sp.get_league_ast_avg(
                        id, season
                    ) / sp.get_league_to_avg(id, season)
            if id >= 1000000 and id < 2000000:
                # Takes the team's stats from the database, so it's ready to work with them:
                with sp():
                    self.aotr = sp.get_team_ast_avg(id, season) / sp.get_team_to_avg(
                        id, season
                    )
            elif id >= 2000000 and id < 3000000:
                # Takes the player's stats from the database, so it's ready to work with them:
                with sp():
                    self.aotr = sp.get_player_ast_avg(
                        id, season
                    ) / sp.get_player_to_avg(id, season)
        else:
            # Checking which type of ID the method is dealing with:
            if isinstance(id, str):
                with sp():
                    # Takes the league's stats from the database, so it's ready to work with them:
                    self.aotr = sp.get_league_ast_avg(id, None) / sp.get_league_to_avg(
                        id, None
                    )
            if id >= 1000000 and id < 2000000:
                # Takes the team's stats from the database, so it's ready to work with them:
                with sp():
                    self.aotr = sp.get_team_ast_avg(id, None) / sp.get_player_to_avg(
                        id, None
                    )
            elif id >= 2000000 and id < 3000000:
                # Takes the player's stats from the database, so it's ready to work with them:
                with sp():
                    self.aotr = sp.get_player_ast_avg(id, None) / sp.get_player_to_avg(
                        id, None
                    )

        return self.aotr

    # ========================== #
    # VALUE OF POSSESSION METHOD #
    # ========================== #
    def vop(self, id, season=None):
        """
        ### VOP - Value of Possession

        ========================

        Description:
        The `VOP`stat is essential to understand how valuable is every possession to the subject in terms of points.
        Ideally, if a team scores a midrange with every single possession they get, that team's `VOP` would be `2`.

        ========================

        Parameters:
        #### - `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its average `VOP` will be fetched\n
            if `2000000 <= id < 3000000`, it's a player's ID so its average `VOP` will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league average `VOP`

        #### - `season = None`: `int`
            if a value for season is inserted as a parameter of the method, average `VOP` for that specific season
            will be fetched; otherwise, career/all-time average `VOP` will be fetched.

        """
        if season is not None:
            # Leagues
            if isinstance(id, str):
                # Connecting to the db using `with`:
                with sp:
                    self.tm_pts = sp.get_league_pts_avg(id, season)
                    self.tm_fga = sp.get_league_fga_avg(id, season)
                    self.tm_oreb = sp.get_league_oreb_avg(id, season)
                    self.tm_to = sp.get_league_to_avg(id, season)
                    self.tm_fta = sp.get_league_fta_avg(id, season)
                self.den = self.tm_fga - self.tm_oreb + self.tm_to + 0.44 * self.tm_fta
                self._vop = self.tm_pts / self.den
            # Teams
            elif id >= 1000000 and id < 2000000:
                # Connecting to the db using `with`:
                with sp:
                    self.lg_pts = sp.get_team_pts_avg(id, season)
                    self.lg_fga = sp.get_team_fga_avg(id, season)
                    self.lg_oreb = sp.get_team_oreb_avg(id, season)
                    self.lg_to = sp.get_team_to_avg(id, season)
                    self.lg_fta = sp.get_team_fta_avg(id, season)
                self.den = self.lg_fga - self.lg_oreb + self.lg_to + 0.44 * self.lg_fta
                self._vop = self.lg_pts / self.den
            # Players
            elif id >= 2000000 and id < 3000000:
                # Connecting to the db using `with`:
                with sp:
                    self.pl_pts = sp.get_player_pts_avg(id, season)
                    self.pl_fga = sp.get_player_fga_avg(id, season)
                    self.pl_oreb = sp.get_player_oreb_avg(id, season)
                    self.pl_to = sp.get_player_to_avg(id, season)
                    self.pl_fta = sp.get_player_fta_avg(id, season)
                self.den = self.pl_fga - self.pl_oreb + self.pl_to + 0.44 * self.pl_fta
                self._vop = self.pl_pts / self.den

        else:
            # Leagues
            if isinstance(id, str):
                # Connecting to the db using `with`:
                with sp:
                    self.lg_pts = sp.get_league_pts_avg(id, None)
                    self.lg_fga = sp.get_league_fga_avg(id, None)
                    self.lg_oreb = sp.get_league_oreb_avg(id, None)
                    self.lg_to = sp.get_league_to_avg(id, None)
                    self.lg_fta = sp.get_league_fta_avg(id, None)
                self.den = self.lg_fga - self.lg_oreb + self.lg_to + 0.44 * self.lg_fta
                self._vop = self.lg_pts / self.den
            # Teams
            elif id >= 1000000 and id < 2000000:
                # Connecting to the db using `with`:
                with sp:
                    self.self.lg_pts = sp.get_team_pts_avg(id, None)
                    self.lg_fga = sp.get_team_fga_avg(id, None)
                    self.lg_oreb = sp.get_team_oreb_avg(id, None)
                    self.lg_to = sp.get_team_to_avg(id, None)
                    self.lg_fta = sp.get_team_fta_avg(id, None)
                self.den = self.lg_fga - self.lg_oreb + self.lg_to + 0.44 * self.lg_fta
                self._vop = self.lg_pts / self.den
            # Players
            elif id >= 2000000 and id < 3000000:
                # Connecting to the db using `with`:
                with sp:
                    self.pl_pts = sp.get_player_pts_avg(id, None)
                    self.pl_fga = sp.get_player_fga_avg(id, None)
                    self.pl_oreb = sp.get_player_oreb_avg(id, None)
                    self.pl_to = sp.get_player_to_avg(id, None)
                    self.pl_fta = sp.get_player_fta_avg(id, None)
                self.den = self.pl_fga - self.pl_oreb + self.pl_to + 0.44 * self.pl_fta
                self._vop = self.pl_pts / self.den
        # Final output

        return self.vop

    # ========================= #
    # REBOUND PERCENTAGE METHOD #
    # ========================= #
    def rbp(self, id, type="t", season=None):
        """
        ### RBP - Rebound Percentage

        ========================

        Description:
        The `RBP` (usually `ORBP` for offensive rebound %, `DRBP` for defensive rebound %) is a metric
        that shows how many rebound of the chosen type that player or team grabs while available on the floor.
        If a player `DRBP` is `0.2`, it means that they grab `2` offensive rebounds every `10` offensive rebounds available
        while on the floor.

        ========================

        Parameters:
        #### - `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its average `RBP` will be fetched\n
            if `2000000 <= id < 3000000`, it's a player's ID so its average `RBP` will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league average `RBP` will be fetched

        #### - `type`: `str`
            if `type = "t"`, 1 will be printed as the % of total rebounds grabbed is always 100\n
            if `type = "d"`, `DRBP` will be fetched\n
            if `type = "o"`, `ORBP` will be fetched\n

        #### - `season = None`: `int`
            if a value for season is inserted as a parameter of the method, average `RBP` for that specific season
            will be fetched; otherwise, career/all-time average `RBP` will be fetched.

        """
        if season is not None:
            if isinstance(id, str):
                if type == "d":
                    with sp:
                        self._rbp = (
                            sp.get_league_treb_avg(id, season)
                            - sp.get_league_oreb_avg(id, season)
                        ) / sp.get_league_treb_avg(id, season)
                elif type == "o":
                    with sp:
                        self._rbp = (
                            sp.get_league_treb_avg(id, season)
                            - sp.get_league_dreb_avg(id, season)
                        ) / sp.get_league_treb_avg(id, season)
                elif type == "t":
                    return 1
                else:
                    raise ValueError(
                        """Invalid type of rebound insert: choose from the list below:
                                    - "t" for total rebounds (always 1);
                                    - "d" for defensive rebounds;
                                    - "o" for offensive rebounds. 
                                    """
                    )
        else:
            if isinstance(id, str):
                if type == "d":
                    with sp:
                        self._rbp = (
                            sp.get_league_treb_avg(id, None)
                            - sp.get_league_oreb_avg(id, None)
                        ) / sp.get_league_treb_avg(id, None)
                elif type == "o":
                    with sp:
                        self._rbp = (
                            sp.get_league_treb_avg(id, None)
                            - sp.get_league_dreb_avg(id, None)
                        ) / sp.get_league_treb_avg(id, None)
                elif type == "t":
                    return 1
                else:
                    raise ValueError(
                        """Invalid type of rebound insert: choose from the list below:
                                    - "t" for total rebounds (always 1);
                                    - "d" for defensive rebounds;
                                    - "o" for offensive rebounds. 
                                     
                                    """
                    )
                return self._rbp

    # ================== #
    # POSSESSIONS METHOD #
    # ================== #
    def poss(self, id, season=None):
        """
        ### POSS - Possessions

        ========================

        Description:
        Number of possessions a team has during a game or a season on average.

        ========================

        Parameters:
        #### - `id`: `int` or `str`
            if `1000000 <= id < 2000000`, it's a team's ID so its average possessions will be fetched\n
            if `isinstance(id, str) = True`, it's a league's ID so league average possessions will be fetched

        #### - `opp_id = None`: `int`
            this NEEDS to be input if `id` is a team's id and you want to calculate it's est. possessions in a
            single game.

        #### - `season = None`: `int`
            if a value for season is inserted as a parameter of the method, average possessions for that specific season
            will be fetched; otherwise, all-time average possessions will be fetched.

        """
        if season is not None:
            if isinstance(id, str):
                with sp:
                    self.pos = (
                        sp.get_league_fga_avg(id, season)
                        + 0.44 * sp.get_league_fta_avg(id, season)
                        - 1.07
                        * (
                            sp.get_league_oreb_avg(id, season)
                            / sp.get_league_oreb_avg(id, season)
                            + sp.get_league_dreb_avg(id, season)
                        )
                        * (
                            sp.get_league_fga_avg(id, season)
                            - sp.get_team_fgm_avg(id, season)
                        )
                        + sp.get_league_to_avg(id, season)
                    )

            else:
                with sp:
                    self.pos = (
                        sp.get_team_fga_avg(id, season)
                        + 0.44 * sp.get_team_fta_avg(id, season)
                        - 1.07
                        * (
                            sp.get_team_oreb_avg(id, season)
                            / sp.get_team_oreb_avg(id, season)
                        )
                        - sp.get_opp_dreb_avg(id, season)
                        * (
                            sp.get_team_fga_avg(id, season)
                            - sp.get_team_fgm_avg(id, season)
                        )
                        + sp.get_team_to_avg(id, season)
                    )
        else:
            if isinstance(id, str):
                with sp:
                    self.pos = (
                        sp.get_league_fga_avg(id, None)
                        + 0.44 * sp.get_league_fta_avg(id, None)
                        - 1.07
                        * (
                            sp.get_league_oreb_avg(id, None)
                            / sp.get_league_oreb_avg(id, None)
                            + sp.get_league_dreb_avg(id, None)
                        )
                        * (
                            sp.get_league_fga_avg(id, None)
                            - sp.get_team_fgm_avg(id, None)
                        )
                        + sp.get_league_to_avg(id, None)
                    )

            else:
                with sp:
                    self.pos = (
                        sp.get_team_fga_avg(id, None)
                        + 0.44 * sp.get_team_fta_avg(id, None)
                        - 1.07
                        * (
                            sp.get_team_oreb_avg(id, None)
                            / sp.get_team_oreb_avg(id, None)
                        )
                        - sp.get_opp_dreb_avg(id, None)
                        * (
                            sp.get_team_fga_avg(id, None)
                            - sp.get_team_fgm_avg(id, None)
                        )
                        + sp.get_team_to_avg(id, None)
                    )

    # =============================== #
    # PLAYER EFFICIENCY RATING METHOD #
    # =============================== #
    def uper(self, player_id, team_id, league_id, season=None):
        """TODO I need to have queries for league average and team average to calculate per"""

        with sp():
            self.factor = (2 / 3) - (
                0.5
                * sp.get_league_ast_avg(league_id, season)
                / sp.get_league_fgm_avg(league_id, season)
            ) / (
                2
                * (
                    sp.get_league_fgm_avg(league_id, season)
                    / sp.get_league_ftm_avg(league_id, season)
                )
            )
            self.ast_over_fg = sp.get_team_ast_avg(
                team_id, season
            ) / sp.get_team_fgm_avg(team_id, season)

            self.u_per = (
                1
                / sp.get_player_mp_avg(player_id, season)
                * (sp.get_player_3pm_avg(player_id, season))
                + [2 / 3 * sp.get_player_ast_avg(player_id, season)]
                + [
                    ((2 - self.factor * self.ast_over_fg))
                    * sp.get_player_fgm_avg(player_id, season)
                ]
                + [
                    0.5
                    * sp.get_player_ftm_avg(player_id, season)
                    * (2 - (1 / 3) * self.ast_over_fg)
                ]
                - [
                    self.vop(league_id, season)
                    * sp.get_player_to_avg(player_id, season)
                ]
                - [
                    self.vop(league_id, season)
                    * self.rbp(league_id, "d", season)
                    * (
                        sp.get_player_fga_avg(player_id, season)
                        * sp.get_player_fgm_avg(player_id, season)
                    )
                ]
                - [
                    self.vop(league_id, season)
                    * 0.44
                    * (0.44 + (0.56 * self.rbp(league_id, "d", season)))
                    * (
                        sp.get_player_fta_avg(player_id, season)
                        - sp.get_player_ftm_avg(player_id, season)
                    )
                ]
                + [
                    self.vop(league_id, season)
                    * (1 - self.rbp(league_id, "d", season))
                    * (
                        sp.get_player_treb_avg(player_id, season)
                        - sp.get_player_oreb_avg(player_id, season)
                    )
                ]
                + [
                    self.vop(league_id, season)
                    * self.rbp(league_id, "d", season)
                    * sp.get_player_oreb_avg(player_id, season)
                ]
                + [
                    self.vop(league_id, season)
                    * sp.get_player_stl_avg(player_id, season)
                ]
                + [
                    self.vop(league_id, season)
                    * self.rbp(league_id, "d", season)
                    * sp.get_player_blk_avg(player_id, season)
                ]
                - [
                    sp.get_player_pf_avg(player_id, season)
                    * (
                        sp.get_league_ftm_avg(league_id, season)
                        / sp.get_league_pf_avg(league_id, season)
                    )
                    - 0.44
                    * sp.get_league_fta_avg(league_id, season)
                    / sp.get_league_pf_avg(league_id, season)
                    * self.vop(league_id, season)
                ]
            )
        return self.u_per
