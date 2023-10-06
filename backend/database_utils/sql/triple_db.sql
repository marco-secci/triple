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
END $$ DELIMITER -- Stored procedure to calculate player average:
DELIMITER $$ CREATE PROCEDURE player_career_avg(IN p_player_id INT) BEGIN -- Declaring variables where the averages are going to be stored:
DECLARE total_games INT;
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
-- Calculating total number of games the player played in his career
SELECT COUNT(*) INTO total_games
FROM statlines
WHERE player_id = p_player_id;
-- Calculating averages from the player's available statlines:
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
END $$ DELIMITER;
-- Calculating averages for a single player during a single season:
DELIMITER $$ CREATE PROCEDURE player_season_avg(IN p_player_id INT, IN p_season INT) BEGIN
DECLARE total_games INT;
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
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE player_id = p_player_id
    AND season = p_season
    AND game_id = g.id;
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
SELECT avg_pts,
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
    avg_to;
END $$ DELIMITER;
-- Calculating a team averages for a single season:
DELIMITER $$ CREATE PROCEDURE team_season_avg(IN p_team_id INT, IN p_season INT) BEGIN
DECLARE total_games INT;
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
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
    JOIN players ON s.player_id = players.id
WHERE players.team_id = p_team_id
    AND season = p_season;
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
SELECT avg_pts,
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
    avg_to;
END $$ DELIMITER;
-- Calculating league averages for a single season:
DELIMITER $$ CREATE PROCEDURE league_season_avg(IN p_season INT, p_tournament VARCHAR(10)) BEGIN
DECLARE total_games INT;
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
SELECT COUNT(*) INTO total_games
FROM statlines s,
    games g
WHERE game_id = g.id
    AND season = p_season;
-- Calculating averages for each statistic for the entire league in the specified season
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
-- (Optional) Output the calculated averages
SELECT avg_pts,
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
    avg_to;
END $$ DELIMITER;