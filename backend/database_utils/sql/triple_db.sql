CREATE DATABASE triple;
USE triple;
-- Table containing seasons:
CREATE TABLE seasons(
    season INT NOT NULL PRIMARY KEY AUTO_INCREMENT
) AUTO_INCREMENT = 1946;
-- Table containing all countries hosting one or more basketball tournament:
CREATE TABLE countries(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    alfa CHAR(3),
    season_id INT NOT NULL,
    start DATE NOT NULL,
end DATE NOT NULL,
FOREIGN KEY (season_id) REFERENCES seasons(season)
);
-- Table containing all tournaments in the world:
CREATE TABLE tournaments(
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    country_id INT NOT NULL,
    -- Level of the national tournament (higher level closer to 0):
    level INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
-- Table containing all teams in the world:
CREATE TABLE teams(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    country_id INT NOT NULL,
    tournament_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
) AUTO_INCREMENT = 1000000;
-- Table containing all players in the world:
CREATE TABLE players(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    season_id INT NOT NULL,
    shirt_num TINYINT,
    name VARCHAR(150),
    age TINYINT,
    height VARCHAR(10),
    weight VARCHAR(10),
    nationality CHAR(3),
    experience VARCHAR(40),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (season_id) REFERENCES seasons(season)
) AUTO_INCREMENT = 2000000;
-- Table containing every game ever played:
CREATE TABLE games(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    season INT NOT NULL,
    tournament CHAR(10) NOT NULL,
    home INT NOT NULL,
    home_score TINYINT,
    away INT NOT NULL,
    away_score TINYINT,
    date DATE,
    time TIME,
    FOREIGN KEY (season) REFERENCES seasons(season),
    FOREIGN KEY (tournament) REFERENCES tournaments(id),
    FOREIGN KEY (home, away) REFERENCES teams(id)
) AUTO_INCREMENT = 3000000;
-- Table containing all individual statline ever produced:
CREATE TABLE statlines(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    mp FLOAT,
    pts INT,
    ast INT,
    dreb INT,
    oreb INT,
    treb INT,
    stl INT,
    blk INT,
    fgm INT,
    fga INT,
    ftm INT,
    fta INT,
    `3pm` INT,
    `3pa` INT,
    `to` INT,
    pf INT,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (game_id) REFERENCES games(id)
);
-- ======================================== STORED PROCEDURES, TRIGGERS, ETC ======================================== --
-- Trigger to create an easy-recognizable tournament ID (eg: NBA.id = USA1, NBL.id = AUS1, LegaSerieA2.id = ITA2)
DELIMITER $$ CREATE TRIGGER set_tournament_id BEFORE
INSERT ON tournaments FOR EACH ROW BEGIN
DECLARE country_alfa CHAR(3);
SELECT alfa INTO country_alfa
FROM countries
WHERE countries.id = NEW.country_id;
SET NEW.id = CONCAT(country_alfa, NEW.level);
END $$ DELIMITER;
-- Trigger to calculate total rebounds:
DELIMITER $$ CREATE TRIGGER calculate_treb BEFORE
INSERT ON statlines FOR EACH ROW BEGIN
SET NEW.treb = NEW.oreb + NEW.dreb;
END $$ DELIMITER;
-- ================================================ SEASON AVERAGES ================================================ --
-- Calculating averages for a single player during a single season:
DELIMITER $$ CREATE PROCEDURE player_season_avg(IN p_player_id INT, IN p_season INT) BEGIN
DECLARE total_games INT;
DECLARE avg_mp FLOAT;
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND mp IS NOT NULL;
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND pts IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND fga IS NOT NULL;
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND fta IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND `3pm` IS NOT NULL;
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
-- Calculating a team averages for a single season:
DELIMITER $$ CREATE PROCEDURE team_season_avg(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE total_games INT;
DECLARE avg_mp FLOAT;
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND mp IS NOT NULL;
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND pts IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND fga IS NOT NULL;
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND fta IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND `3pm` IS NOT NULL;
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
-- Calculating league averages for a single season:
DELIMITER $$ CREATE PROCEDURE league_season_avg(IN p_tournament VARCHAR(10), p_season INT) BEGIN
DECLARE total_games INT;
DECLARE avg_mp FLOAT;
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND mp IS NOT NULL;
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND pts IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND fga IS NOT NULL;
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND fta IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND `3pm` IS NOT NULL;
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season
    AND g.tournament = p_tournament
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
-- =============================================== ALL-TIME AVERAGES =============================================== --
DELIMITER $$ CREATE PROCEDURE player_career_avg(IN p_player_id INT) BEGIN -- Declaring variables where the averages are going to be stored:
DECLARE total_games INT;
DECLARE avg_mp FLOAT;
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
-- Calculating total number of games the player played in his career
SELECT COUNT(*) INTO total_games
FROM statlines
WHERE player_id = p_player_id;
-- Calculating averages from the player's available statlines:
SELECT AVG(mp) INTO avg_mp
FROM statlines
WHERE player_id = p_player_id
    AND mp IS NOT NULL;
SELECT AVG(pts) INTO avg_pts
FROM statlines
WHERE player_id = p_player_id
    AND pts IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines
WHERE player_id = p_player_id
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines
WHERE player_id = p_player_id
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines
WHERE player_id = p_player_id
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines
WHERE player_id = p_player_id
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines
WHERE player_id = p_player_id
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines
WHERE player_id = p_player_id
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines
WHERE player_id = p_player_id
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines
WHERE player_id = p_player_id
    AND fga IS NOT NULL;
SELECT (ftm) INTO avg_ftm
FROM statlines
WHERE player_id = p_player_id
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines
WHERE player_id = p_player_id
    AND fta IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines
WHERE player_id = p_player_id
    AND `3pm` IS NOT NULL;
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines
WHERE player_id = p_player_id
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines
WHERE player_id = p_player_id
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines
WHERE player_id = p_player_id
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
DELIMITER $$ CREATE PROCEDURE team_alltime_averages(IN p_team_id VARCHAR(10)) BEGIN
DECLARE total_games INT;
DECLARE avg_mp FLOAT;
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND pts IS NOT NULL;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND mp IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fga IS NOT NULL;
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fta IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND blk IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `3pm` IS NOT NULL;
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
-- Stored procedure to fetch league all-time averages:
DELIMITER $$ CREATE PROCEDURE league_alltime_averages(IN p_league_id VARCHAR(10)) BEGIN
DECLARE total_games INT;
DECLARE avg_mp FLOAT
DECLARE avg_pts FLOAT;
DECLARE avg_ast FLOAT;
DECLARE avg_dreb FLOAT;
DECLARE avg_oreb FLOAT;
DECLARE avg_treb FLOAT;
DECLARE avg_stl FLOAT;
DECLARE avg_blk FLOAT;
DECLARE avg_fgm FLOAT;
DECLARE avg_fga FLOAT;
DECLARE avg_ftm FLOAT;
DECLARE avg_fta FLOAT;
DECLARE avg_3pm FLOAT;
DECLARE avg_3pa FLOAT;
DECLARE avg_to FLOAT;
DECLARE avg_pf FLOAT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND pts IS NOT NULL;
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND mp IS NOT NULL;
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND ast IS NOT NULL;
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND dreb IS NOT NULL;
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND oreb IS NOT NULL;
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND treb IS NOT NULL;
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND stl IS NOT NULL;
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND blk IS NOT NULL;
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND fgm IS NOT NULL;
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND fga IS NOT NULL;
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND ftm IS NOT NULL;
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND fta IS NOT NULL;
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND `3pm` IS NOT NULL;
SELECT AVG(3pa) INTO avg_3pa
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND `3pa` IS NOT NULL;
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND `to` IS NOT NULL;
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
WHERE g.tournament = p_league_id
    AND s.game_id = g.id
    AND pf IS NOT NULL;
SELECT avg_mp,
    avg_pts,
    avg_ast,
    avg_dreb,
    avg_oreb,
    avg_treb,
    avg_stl,
    avg_blk,
    avg_fgm,
    avg_fga,
    avg_ftm,
    avg_fta,
    avg_3pm,
    avg_3pa,
    avg_to,
    avg_pf;
END $$ DELIMITER;
-- =============================================== SINGLE STATS AVERAGES =============================================== --
-- ==========================================PLAYER SINGLE SEASON AVERAGES ========================================== --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_mp(IN p_player_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the minutes played by the player in a single season:
SELECT AVG(mp) INTO avg_mp
FROM statlines s
WHERE p.player_id = p_player_id
    AND season = p_season
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_pts(IN p_player_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the points per game scored by the player in the specified season:
SELECT AVG(pts) INTO avg_pts
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND pts IS NOT NULL;
-- Return the result:
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_ast(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the total ast made per game by the player in the specified season:
SELECT AVG(ast) INTO avg_ast
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND ast IS NOT NULL;
-- Return the result:
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_dreb(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the total defensive boards grabbed per game by the player in the specified season:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND dreb IS NOT NULL;
-- Return the result:
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_oreb(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the total offensive boards grabbed per game by the player in the specified season:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND oreb IS NOT NULL;
-- Return the result:
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_treb(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the total boards grabbed per game by the player in the specified season:
SELECT AVG(treb) INTO avg_treb
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND treb IS NOT NULL;
-- Return the result:
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_stl(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the steals per game made by the player in the specified season:
SELECT AVG(stl) INTO avg_stl
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND stl IS NOT NULL;
-- Return the result:
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_blk(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the steals per game made by the player in the specified season:
SELECT AVG(blk) INTO avg_blk
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND blk IS NOT NULL;
-- Return the result:
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_fgm(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the field goals made per game by the player in the specified season:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND fgm IS NOT NULL;
-- Return the result:
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_fga(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the field goal attempts per game by the player in the specified season:
SELECT AVG(fga) INTO avg_fga
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND fga IS NOT NULL;
-- Return the result:
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_ftm(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the free throws made per game by the player in the specified season:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND ftm IS NOT NULL;
-- Return the result:
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_fta(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the free throw attempts per game by the player in the specified season:
SELECT AVG(fta) INTO avg_fta
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND fta IS NOT NULL;
-- Return the result:
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_3pm(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the three pointers made per game by the player in the specified season:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND `3pm` IS NOT NULL;
-- Return the result:
SELECT avg_3pm;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_3pa(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the three pointer attempts per game by the player in the specified season:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND `3pa` IS NOT NULL;
-- Return the result:
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_to(IN p_season INT, IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the turnovers per game by the player in the specified season:
SELECT AVG(`to`) INTO avg_to
FROM statlines
WHERE player_id = p_player_id
    AND season = p_season
    AND `to` IS NOT NULL;
-- Return the result:
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_season_pf(IN p_player_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id
    AND season = p_season;
-- Calculate the fouls made by the player in a single season:
SELECT AVG(pf) INTO avg_pf
FROM statlines s
WHERE p.player_id = p_player_id
    AND season = p_season
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ========================================== PLAYER CAREER AVERAGES ========================================== --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_mp(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the minutes played by the player in a single season:
SELECT AVG(mp) INTO avg_mp
FROM statlines
WHERE p.player_id = p_player_id
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_pts(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the points per game scored by the player in their career:
SELECT AVG(pts) INTO avg_pts
FROM statlines
WHERE player_id = p_player_id
    AND pts IS NOT NULL;
-- Return the result:
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_ast(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the total ast made per game by the player in their career:
SELECT AVG(ast) INTO avg_ast
FROM statlines
WHERE player_id = p_player_id
    AND ast IS NOT NULL;
-- Return the result:
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_dreb(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the total defensive boards grabbed per game by the player in their career:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines
WHERE player_id = p_player_id
    AND dreb IS NOT NULL;
-- Return the result:
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_oreb(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the total offensive boards grabbed per game by the player in their career:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines
WHERE player_id = p_player_id
    AND oreb IS NOT NULL;
-- Return the result:
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_treb(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the total boards grabbed per game by the player in their career:
SELECT AVG(treb) INTO avg_treb
FROM statlines
WHERE player_id = p_player_id
    AND treb IS NOT NULL;
-- Return the result:
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_stl(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the steals per game made by the player in their career:
SELECT AVG(stl) INTO avg_stl
FROM statlines
WHERE player_id = p_player_id
    AND stl IS NOT NULL;
-- Return the result:
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_blk(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the steals per game made by the player in their career:
SELECT AVG(blk) INTO avg_blk
FROM statlines
WHERE player_id = p_player_id
    AND blk IS NOT NULL;
-- Return the result:
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_fgm(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the field goals made per game by the player in their career:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines
WHERE player_id = p_player_id
    AND fgm IS NOT NULL;
-- Return the result:
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_fga(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the field goal attempts per game by the player in their career:
SELECT AVG(fga) INTO avg_fga
FROM statlines
WHERE player_id = p_player_id
    AND fga IS NOT NULL;
-- Return the result:
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_ftm(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the free throws made per game by the player in their career:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines
WHERE player_id = p_player_id
    AND ftm IS NOT NULL;
-- Return the result:
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_fta(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the free throw attempts per game by the player in their career:
SELECT AVG(fta) INTO avg_fta
FROM statlines
WHERE player_id = p_player_id
    AND fta IS NOT NULL;
-- Return the result:
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_3pm(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the three pointers made per game by the player in their career:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines
WHERE player_id = p_player_id
    AND `3pm` IS NOT NULL;
-- Return the result:
SELECT avg_3pm;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_3pa(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the three pointer attempts per game by the player in their career:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines
WHERE player_id = p_player_id
    AND `3pa` IS NOT NULL;
-- Return the result:
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_to(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the turnovers per game by the player in their career:
SELECT AVG(`to`) INTO avg_to
FROM statlines
WHERE player_id = p_player_id
    AND `to` IS NOT NULL;
-- Return the result:
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_player_career_pf(IN p_player_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE player_id = p_player_id;
-- Calculate the fouls made by the player in a single season:
SELECT AVG(pf) INTO avg_pf
FROM statlines
WHERE player_id = p_player_id
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ================================ TEAM SINGLE SEASON AVERAGE ================================ --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_mp(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season;
-- Calculate the fouls made by the team in its history:
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_pts(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season;
-- Calculate the points per game scored by the team in a single season:
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND pts IS NOT NULL;
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_ast(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the total ast made per game by the team in a single season:
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND ast IS NOT NULL;
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_dreb(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the total defensive boards grabbed per game by the team in a single season:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND dreb IS NOT NULL;
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_oreb(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the total offensive boards grabbed per game by the team in a single season:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND oreb IS NOT NULL;
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_treb(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the total boards grabbed per game by the team in a single season:
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND treb IS NOT NULL;
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_stl(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the steals per game made by the team in a single season:
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND stl IS NOT NULL;
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_blk(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the steals per game made by the team in a single season:
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND blk IS NOT NULL;
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_fgm(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the field goals made per game by the team in a single season:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND fgm IS NOT NULL;
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_fga(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the field goal attempts per game by the team in a single season:
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND fga IS NOT NULL;
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_ftm(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the free throws made per game by the team in a single season:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND ftm IS NOT NULL;
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_fta(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the free throw attempts per game by the team in a single season:
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND fta IS NOT NULL;
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_3pm(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the three pointers made per game by the team in a single season:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND `3pm` IS NOT NULL;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_3pa(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the three pointer attempts per game by the team in a single season:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND `3pa` IS NOT NULL;
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_to(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the turnovers per game by the team in a single season:
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND `to` IS NOT NULL;
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_season_pf(IN p_team_id INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id
    AND season = p_season;
-- Calculate the points per game scored by the team in a single season:
SELECT AVG(pf) INTO avg_pf
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND season = p_season
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ================================ TEAM HISTORY AVERAGES ================================ --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_mp(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id;
-- Calculate the fouls made by the team in its history:
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_pts(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id -- Calculate the points per game scored by the team in its history:
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND pts IS NOT NULL;
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_ast(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the total ast made per game by the team in its history:
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND ast IS NOT NULL;
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_dreb(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the total defensive boards grabbed per game by the team in its history:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND dreb IS NOT NULL;
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_oreb(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the total offensive boards grabbed per game by the team in its history:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND oreb IS NOT NULL;
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_treb(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the total boards grabbed per game by the team in its history:
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND treb IS NOT NULL;
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_stl(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the steals per game made by the team in its history:
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND stl IS NOT NULL;
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_blk(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the steals per game made by the team in its history:
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND blk IS NOT NULL;
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_fgm(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the field goals made per game by the team in its history:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fgm IS NOT NULL;
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_fga(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the field goal attempts per game by the team in its history:
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fga IS NOT NULL;
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_ftm(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the free throws made per game by the team in its history:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND ftm IS NOT NULL;
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_fta(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the free throw attempts per game by the team in its history:
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND fta IS NOT NULL;
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_3pm(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the three pointers made per game by the team in its history:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `3pm` IS NOT NULL;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_3pa(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the three pointer attempts per game by the team in its history:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `3pa` IS NOT NULL;
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_to(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id -- Calculate the turnovers per game by the team in its history:
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND `to` IS NOT NULL;
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_team_history_pf(IN p_team_id INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s
WHERE team_id = p_team_id;
-- Calculate the fouls made by the team in a single season:
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
    JOIN players p ON s.player_id = p.id
WHERE p.team_id = p_team_id
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ================================ LEAGUE SINGLE SEASON ================================ --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_mp(IN p_tournament VARCHAR(10), IN season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season;
-- Calculate the minutes played per game by the league in a single season: (prolly dont make sense)
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_pts(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season;
-- Calculate the points per game scored by the league in a single season:
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND pts IS NOT NULL;
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_ast(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the total ast made per game by the league in a single season:
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND ast IS NOT NULL;
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_dreb(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the total defensive boards grabbed per game by the league in a single season:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND dreb IS NOT NULL;
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_oreb(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the total offensive boards grabbed per game by the league in a single season:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND oreb IS NOT NULL;
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_treb(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the total boards grabbed per game by the league in a single season:
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND treb IS NOT NULL;
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_stl(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the steals per game made by the league in a single season:
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND stl IS NOT NULL;
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_blk(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the steals per game made by the league in a single season:
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND blk IS NOT NULL;
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_fgm(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the field goals made per game by the league in a single season:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND fgm IS NOT NULL;
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_fga(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the field goal attempts per game by the league in a single season:
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND fga IS NOT NULL;
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_ftm(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the free throws made per game by the league in a single season:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND ftm IS NOT NULL;
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_fta(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the free throw attempts per game by the league in a single season:
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND fta IS NOT NULL;
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_3pm(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the three pointers made per game by the league in a single season:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND `3pm` IS NOT NULL;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_3pa(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the three pointer attempts per game by the league in a single season:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND `3pa` IS NOT NULL;
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_to(IN p_tournament VARCHAR(10), IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the turnovers per game by the league in a single season:
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND `to` IS NOT NULL;
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_season_pf(IN p_tournament INT, IN p_season INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament
    AND season = p_season;
-- Calculate the points per game scored by the league in a single season:
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND season = p_season
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ================================ LEAGUE HISTORY AVERAGES ================================ --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_mp(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_mp FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament -- Calculate the minutes played per game by the league in its history:
SELECT AVG(mp) INTO avg_mp
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND mp IS NOT NULL;
SELECT avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_pts(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_pts FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament -- Calculate the points per game scored by the league in its history:
SELECT AVG(pts) INTO avg_pts
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND pts IS NOT NULL;
SELECT avg_pts;
END $$ DELIMITER;
-- =============== ASSIST =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_ast(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_ast FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the total ast made per game by the league in its history:
SELECT AVG(ast) INTO avg_ast
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND ast IS NOT NULL;
SELECT avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_dreb(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_dreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the total defensive boards grabbed per game by the league in its history:
SELECT AVG(dreb) INTO avg_dreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND dreb IS NOT NULL;
SELECT avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_oreb(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_oreb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the total offensive boards grabbed per game by the league in its history:
SELECT AVG(oreb) INTO avg_oreb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND oreb IS NOT NULL;
SELECT avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_treb(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_treb FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the total boards grabbed per game by the league in its history:
SELECT AVG(treb) INTO avg_treb
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND treb IS NOT NULL;
SELECT avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_stl(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_stl FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the steals per game made by the league in its history:
SELECT AVG(stl) INTO avg_stl
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND stl IS NOT NULL;
SELECT avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_blk(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_blk FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the steals per game made by the league in its history:
SELECT AVG(blk) INTO avg_blk
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND blk IS NOT NULL;
SELECT avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOAL MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_fgm(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_fgm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the field goals made per game by the league in its history:
SELECT AVG(fgm) INTO avg_fgm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND fgm IS NOT NULL;
SELECT avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_fga(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_fga FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the field goal attempts per game by the league in its history:
SELECT AVG(fga) INTO avg_fga
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND fga IS NOT NULL;
SELECT avg_fga;
END $$ DELIMITER;
-- =============== FREE THROWS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_ftm(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_ftm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the free throws made per game by the league in its history:
SELECT AVG(ftm) INTO avg_ftm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND ftm IS NOT NULL;
SELECT avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_fta(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_fta FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the free throw attempts per game by the league in its history:
SELECT AVG(fta) INTO avg_fta
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND fta IS NOT NULL;
SELECT avg_fta;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_3pm(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pm FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the three pointers made per game by the league in its history:
SELECT AVG(`3pm`) INTO avg_3pm
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND `3pm` IS NOT NULL;
END $$ DELIMITER;
-- =============== THREE POINTER ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_3pa(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_3pa FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the three pointer attempts per game by the league in its history:
SELECT AVG(`3pa`) INTO avg_3pa
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND `3pa` IS NOT NULL;
SELECT avg_3pa;
END $$ DELIMITER;
-- =============== TURNOVERS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_to(IN p_tournament VARCHAR(10)) BEGIN -- Declare a variable to store the result:
DECLARE avg_to FLOAT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the turnovers per game by the league in its history:
SELECT AVG(`to`) INTO avg_to
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND `to` IS NOT NULL;
SELECT avg_to;
END $$ DELIMITER;
-- =============== FOULS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_league_history_pf(IN p_tournament INT) BEGIN -- Declare a variable to store the result:
DECLARE avg_pf INT;
-- Declare a variable where to count the total games:
DECLARE total_games INT;
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE g.tournament = p_tournament;
-- Calculate the fouls made by the league in a single season:
SELECT AVG(pf) INTO avg_pf
FROM statlines s,
    games g
WHERE game_id = g.id
    AND g.tournament = p_tournament
    AND pf IS NOT NULL;
SELECT avg_pf;
END $$ DELIMITER;
-- ========================================== OPPONENTS SEASON AVERAGES ========================================== --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_mp(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_mp FLOAT;
SELECT AVG(s.mp) INTO opp_avg_mp
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.mp IS NOT NULL;
SELECT opp_avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_pts(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_pts FLOAT;
SELECT AVG(s.pts) INTO opp_avg_pts
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.pts IS NOT NULL;
SELECT opp_avg_pts;
END $$ DELIMITER;
-- =============== ASSISTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_ast(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_ast FLOAT;
SELECT AVG(s.ast) INTO opp_avg_ast
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.ast IS NOT NULL;
SELECT opp_avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE calc_season_opp_dreb(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_dreb FLOAT;
SELECT AVG(s.dreb) INTO opp_avg_dreb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.dreb IS NOT NULL;
SELECT opp_avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_oreb(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_oreb FLOAT;
SELECT AVG(s.oreb) INTO opp_avg_oreb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.oreb IS NOT NULL;
SELECT opp_avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_treb(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_treb FLOAT;
SELECT AVG(s.treb) INTO opp_avg_treb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.treb IS NOT NULL;
SELECT opp_avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_stl(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_stl FLOAT;
SELECT AVG(s.stl) INTO opp_avg_stl
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.stl IS NOT NULL;
SELECT opp_avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_blk(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_blk FLOAT;
SELECT AVG(s.blk) INTO opp_avg_blk
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.blk IS NOT NULL;
SELECT opp_avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOALS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_fgm(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_fgm FLOAT;
SELECT AVG(s.fgm) INTO opp_avg_fgm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.fgm IS NOT NULL;
SELECT opp_avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_fga(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_fga FLOAT;
SELECT AVG(s.fga) INTO opp_avg_fga
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.fga IS NOT NULL;
SELECT opp_avg_fga;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_3pm(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_3pm FLOAT;
SELECT AVG(s.3pm) INTO opp_avg_3pm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.3pm IS NOT NULL;
SELECT opp_avg_3pm;
END $$ DELIMITER;
-- =============== THREE POINTERS ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_3pa(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_3pa FLOAT;
SELECT AVG(s.3pa) INTO opp_avg_3pa
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.3pa IS NOT NULL;
SELECT opp_avg_3pa;
END $$ DELIMITER;
-- =============== FREE THROW MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_ftm(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_ftm FLOAT;
SELECT AVG(s.ftm) INTO opp_avg_ftm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.ftm IS NOT NULL;
SELECT opp_avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_fta(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_fta FLOAT;
SELECT AVG(s.fta) INTO opp_avg_fta
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.fta IS NOT NULL;
SELECT opp_avg_fta;
END $$ DELIMITER;
-- =============== TURNOVER =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_to(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_to FLOAT;
SELECT AVG(s.to) INTO opp_avg_to
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.to IS NOT NULL;
SELECT opp_avg_to;
END $$ DELIMITER;
-- =============== PERSONAL FOULS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_season_opp_pf(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE opp_avg_pf FLOAT;
SELECT AVG(s.pf) INTO opp_avg_pf
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND g.season = p_season
    AND s.pf IS NOT NULL;
SELECT opp_avg_pf;
END $$ DELIMITER;
-- ========================================== OPPONENTS HISTORY AVERAGES ========================================== --
-- =============== MINUTES PLAYED =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_mp(IN p_team_id INT) BEGIN
DECLARE opp_avg_mp FLOAT;
SELECT AVG(s.mp) INTO opp_avg_mp
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.mp IS NOT NULL;
SELECT opp_avg_mp;
END $$ DELIMITER;
-- =============== POINTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_pts(IN p_team_id INT) BEGIN
DECLARE opp_avg_pts FLOAT;
SELECT AVG(s.pts) INTO opp_avg_pts
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.pts IS NOT NULL;
SELECT opp_avg_pts;
END $$ DELIMITER;
-- =============== ASSISTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_ast(IN p_team_id INT) BEGIN
DECLARE opp_avg_ast FLOAT;
SELECT AVG(s.ast) INTO opp_avg_ast
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.ast IS NOT NULL;
SELECT opp_avg_ast;
END $$ DELIMITER;
-- =============== DEFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE calc_history_opp_dreb(IN p_team_id INT) BEGIN
DECLARE opp_avg_dreb FLOAT;
SELECT AVG(s.dreb) INTO opp_avg_dreb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.dreb IS NOT NULL;
SELECT opp_avg_dreb;
END $$ DELIMITER;
-- =============== OFFENSIVE REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_oreb(IN p_team_id INT) BEGIN
DECLARE opp_avg_oreb FLOAT;
SELECT AVG(s.oreb) INTO opp_avg_oreb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.oreb IS NOT NULL;
SELECT opp_avg_oreb;
END $$ DELIMITER;
-- =============== TOTAL REBOUNDS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_treb(IN p_team_id INT) BEGIN
DECLARE opp_avg_treb FLOAT;
SELECT AVG(s.treb) INTO opp_avg_treb
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.treb IS NOT NULL;
SELECT opp_avg_treb;
END $$ DELIMITER;
-- =============== STEALS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_stl(IN p_team_id INT) BEGIN
DECLARE opp_avg_stl FLOAT;
SELECT AVG(s.stl) INTO opp_avg_stl
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.stl IS NOT NULL;
SELECT opp_avg_stl;
END $$ DELIMITER;
-- =============== BLOCKS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_blk(IN p_team_id INT) BEGIN
DECLARE opp_avg_blk FLOAT;
SELECT AVG(s.blk) INTO opp_avg_blk
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.blk IS NOT NULL;
SELECT opp_avg_blk;
END $$ DELIMITER;
-- =============== FIELD GOALS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_fgm(IN p_team_id INT) BEGIN
DECLARE opp_avg_fgm FLOAT;
SELECT AVG(s.fgm) INTO opp_avg_fgm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.fgm IS NOT NULL;
SELECT opp_avg_fgm;
END $$ DELIMITER;
-- =============== FIELD GOAL ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_fga(IN p_team_id INT) BEGIN
DECLARE opp_avg_fga FLOAT;
SELECT AVG(s.fga) INTO opp_avg_fga
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.fga IS NOT NULL;
SELECT opp_avg_fga;
END $$ DELIMITER;
-- =============== THREE POINTERS MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_3pm(IN p_team_id INT) BEGIN
DECLARE opp_avg_3pm FLOAT;
SELECT AVG(s.3pm) INTO opp_avg_3pm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.3pm IS NOT NULL;
SELECT opp_avg_3pm;
END $$ DELIMITER;
-- =============== THREE POINTERS ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_3pa(IN p_team_id INT) BEGIN
DECLARE opp_avg_3pa FLOAT;
SELECT AVG(s.3pa) INTO opp_avg_3pa
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.3pa IS NOT NULL;
SELECT opp_avg_3pa;
END $$ DELIMITER;
-- =============== FREE THROW MADE =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_ftm(IN p_team_id INT) BEGIN
DECLARE opp_avg_ftm FLOAT;
SELECT AVG(s.ftm) INTO opp_avg_ftm
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.ftm IS NOT NULL;
SELECT opp_avg_ftm;
END $$ DELIMITER;
-- =============== FREE THROW ATTEMPTS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_fta(IN p_team_id INT) BEGIN
DECLARE opp_avg_fta FLOAT;
SELECT AVG(s.fta) INTO opp_avg_fta
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.fta IS NOT NULL;
SELECT opp_avg_fta;
END $$ DELIMITER;
-- =============== TURNOVER =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_to(IN p_team_id INT) BEGIN
DECLARE opp_avg_to FLOAT;
SELECT AVG(s.to) INTO opp_avg_to
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.to IS NOT NULL;
SELECT opp_avg_to;
END $$ DELIMITER;
-- =============== PERSONAL FOULS =============== --
DELIMITER $$ CREATE PROCEDURE fetch_history_opp_pf(IN p_team_id INT) BEGIN
DECLARE opp_avg_pf FLOAT;
SELECT AVG(s.pf) INTO opp_avg_pf
FROM statlines s
    JOIN players p ON s.player_id = p.id
    JOIN games g ON s.game_id = g.id
WHERE p.team_id != p_team_id
    AND s.pf IS NOT NULL;
SELECT opp_avg_pf;
END $$ DELIMITER;