-- processing abbreviation table

alter table abbrev modify Team text not null;
alter table abbrev modify Nicknames text not null;
update abbrev set Team = trim(Team), Nicknames = time(Nicknames);
alter table abbrev modify Nicknames varchar(3);
ALTER TABLE abbrev ADD COLUMN ID INT AUTO_INCREMENT PRIMARY KEY;

-- processing team_total

update team_total set `Rk` = null where `Rk` = '';              
update team_total set `Team` = null where `Team` = '';              
update team_total set `G` = null where `G` = '';              
update team_total set `MP` = null where `MP` = '';              
update team_total set `FG` = null where `FG` = '';              
update team_total set `FGA` = null where `FGA` = '';              
update team_total set `FG%` = null where `FG%` = '';              
update team_total set `3P` = null where `3P` = '';              
update team_total set `3PA` = null where `3PA` = '';              
update team_total set `3P%` = null where `3P%` = '';              
update team_total set `2P` = null where `2P` = '';              
update team_total set `2PA` = null where `2PA` = '';              
update team_total set `2P%` = null where `2P%` = '';              
update team_total set `FTA` = null where `FT` = '';              
update team_total set `FT%` = null where `FT%` = '';              
update team_total set `ORB` = null where `ORB` = '';              
update team_total set `DRB` = null where `DRB` = '';              
update team_total set `TRB` = null where `TRB` = '';              
update team_total set `AST` = null where `AST` = '';              
update team_total set `STL` = null where `STL` = '';              
update team_total set `BLK` = null where `BLK` = '';              
update team_total set `TOV` = null where `TOV` = '';              
update team_total set `PF` = null where `PF` = '';              
update team_total set `PTS` = null where `PTS` = '';              
update team_total set `Tm` = null where `Tm` = '';

alter table team_total modify `Rk` INTEGER;
alter table team_total modify `Team` text;
alter table team_total modify `G` INTEGER;
alter table team_total modify `MP` INTEGER;
alter table team_total modify `FG` INTEGER;
alter table team_total modify `FGA` INTEGER;
alter table team_total modify `FG%` DECIMAL;
alter table team_total modify `3P` INTEGER;
alter table team_total modify `3PA` INTEGER;
alter table team_total modify `3P%` DECIMAL;
alter table team_total modify `2P` INTEGER;
alter table team_total modify `2PA` INTEGER;
alter table team_total modify `2P%` DECIMAL;
alter table team_total modify `FT` INTEGER;
alter table team_total modify `FTA` INTEGER;
alter table team_total modify `FT%` DECIMAL;
alter table team_total modify `ORB` INTEGER;
alter table team_total modify `DRB` INTEGER;
alter table team_total modify `TRB` INTEGER;
alter table team_total modify `AST` INTEGER;
alter table team_total modify `STL` INTEGER;
alter table team_total modify `BLK` INTEGER;
alter table team_total modify `TOV` INTEGER;
alter table team_total modify `PF` INTEGER;
alter table team_total modify `PTS` INTEGER;
alter table team_total modify `Year` INTEGER;
alter table team_total drop column `Tm`;


update team_total set `Team` = `Tm` where `Team` is null and `Tm` is not null;
update team_total set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_total add column `nickname` varchar(3) not null;
update team_total a join abbrev b on a.Team = b.Team set a.Nickname = b.Nicknames;
alter table team_total drop column `Tm`;
alter table team_total add column `team_id` integer not null;
update team_total a join abbrev b on a.Team = b.Team set a.team_id = b.ID;

CREATE INDEX idx_team_id ON team_total (team_id);


-- processing team_per_game

update team_per_game set `Rk` = null where `Rk` = '';              
update team_per_game set `Team` = null where `Team` = '';              
update team_per_game set `G` = null where `G` = '';              
update team_per_game set `MP` = null where `MP` = '';              
update team_per_game set `FG` = null where `FG` = '';              
update team_per_game set `FGA` = null where `FGA` = '';              
update team_per_game set `FG%` = null where `FG%` = '';              
update team_per_game set `3P` = null where `3P` = '';              
update team_per_game set `3PA` = null where `3PA` = '';              
update team_per_game set `3P%` = null where `3P%` = '';              
update team_per_game set `2P` = null where `2P` = '';              
update team_per_game set `2PA` = null where `2PA` = '';              
update team_per_game set `2P%` = null where `2P%` = '';              
update team_per_game set `FTA` = null where `FT` = '';              
update team_per_game set `FT%` = null where `FT%` = '';              
update team_per_game set `ORB` = null where `ORB` = '';              
update team_per_game set `DRB` = null where `DRB` = '';              
update team_per_game set `TRB` = null where `TRB` = '';              
update team_per_game set `AST` = null where `AST` = '';              
update team_per_game set `STL` = null where `STL` = '';              
update team_per_game set `BLK` = null where `BLK` = '';              
update team_per_game set `TOV` = null where `TOV` = '';              
update team_per_game set `PF` = null where `PF` = '';              
update team_per_game set `PTS` = null where `PTS` = '';              
update team_per_game set `Tm` = null where `Tm` = '';

alter table team_per_game modify `Rk` INTEGER;
alter table team_per_game modify `Team` text;
alter table team_per_game modify `G` INTEGER;
alter table team_per_game modify `MP` INTEGER;
alter table team_per_game modify `FG` INTEGER;
alter table team_per_game modify `FGA` INTEGER;
alter table team_per_game modify `FG%` DECIMAL;
alter table team_per_game modify `3P` INTEGER;
alter table team_per_game modify `3PA` INTEGER;
alter table team_per_game modify `3P%` DECIMAL;
alter table team_per_game modify `2P` INTEGER;
alter table team_per_game modify `2PA` INTEGER;
alter table team_per_game modify `2P%` DECIMAL;
alter table team_per_game modify `FT` INTEGER;
alter table team_per_game modify `FTA` INTEGER;
alter table team_per_game modify `FT%` DECIMAL;
alter table team_per_game modify `ORB` INTEGER;
alter table team_per_game modify `DRB` INTEGER;
alter table team_per_game modify `TRB` INTEGER;
alter table team_per_game modify `AST` INTEGER;
alter table team_per_game modify `STL` INTEGER;
alter table team_per_game modify `BLK` INTEGER;
alter table team_per_game modify `TOV` INTEGER;
alter table team_per_game modify `PF` INTEGER;
alter table team_per_game modify `PTS` INTEGER;
alter table team_per_game modify `Year` INTEGER;
alter table team_per_game drop column `Tm`;


update team_per_game set `Team` = `Tm` where `Team` is null and `Tm` is not null;
update team_per_game set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_per_game add column `nickname` varchar(3) not null;
update team_per_game a join abbrev b on a.Team = b.Team set a.Nickname = b.Nicknames;
alter table team_per_game drop column `Tm`;
alter table team_per_game add column `team_id` integer not null;
update team_per_game a join abbrev b on a.Team = b.Team set a.team_id = b.ID;

CREATE INDEX idx_team_id ON team_per_game(team_id);


-- processing team_per_possession

update team_per_possession set `Rk` = null where `Rk` = '';              
update team_per_possession set `Team` = null where `Team` = '';              
update team_per_possession set `G` = null where `G` = '';              
update team_per_possession set `MP` = null where `MP` = '';              
update team_per_possession set `FG` = null where `FG` = '';              
update team_per_possession set `FGA` = null where `FGA` = '';              
update team_per_possession set `FG%` = null where `FG%` = '';              
update team_per_possession set `3P` = null where `3P` = '';              
update team_per_possession set `3PA` = null where `3PA` = '';              
update team_per_possession set `3P%` = null where `3P%` = '';              
update team_per_possession set `2P` = null where `2P` = '';              
update team_per_possession set `2PA` = null where `2PA` = '';              
update team_per_possession set `2P%` = null where `2P%` = '';              
update team_per_possession set `FTA` = null where `FT` = '';              
update team_per_possession set `FT%` = null where `FT%` = '';              
update team_per_possession set `ORB` = null where `ORB` = '';              
update team_per_possession set `DRB` = null where `DRB` = '';              
update team_per_possession set `TRB` = null where `TRB` = '';              
update team_per_possession set `AST` = null where `AST` = '';              
update team_per_possession set `STL` = null where `STL` = '';              
update team_per_possession set `BLK` = null where `BLK` = '';              
update team_per_possession set `TOV` = null where `TOV` = '';              
update team_per_possession set `PF` = null where `PF` = '';              
update team_per_possession set `PTS` = null where `PTS` = '';              
update team_per_possession set `Tm` = null where `Tm` = '';

alter table team_per_possession modify `Rk` INTEGER;
alter table team_per_possession modify `Team` text;
alter table team_per_possession modify `G` INTEGER;
alter table team_per_possession modify `MP` INTEGER;
alter table team_per_possession modify `FG` INTEGER;
alter table team_per_possession modify `FGA` INTEGER;
alter table team_per_possession modify `FG%` DECIMAL;
alter table team_per_possession modify `3P` INTEGER;
alter table team_per_possession modify `3PA` INTEGER;
alter table team_per_possession modify `3P%` DECIMAL;
alter table team_per_possession modify `2P` INTEGER;
alter table team_per_possession modify `2PA` INTEGER;
alter table team_per_possession modify `2P%` DECIMAL;
alter table team_per_possession modify `FT` INTEGER;
alter table team_per_possession modify `FTA` INTEGER;
alter table team_per_possession modify `FT%` DECIMAL;
alter table team_per_possession modify `ORB` INTEGER;
alter table team_per_possession modify `DRB` INTEGER;
alter table team_per_possession modify `TRB` INTEGER;
alter table team_per_possession modify `AST` INTEGER;
alter table team_per_possession modify `STL` INTEGER;
alter table team_per_possession modify `BLK` INTEGER;
alter table team_per_possession modify `TOV` INTEGER;
alter table team_per_possession modify `PF` INTEGER;
alter table team_per_possession modify `PTS` INTEGER;
alter table team_per_possession modify `Year` INTEGER;
alter table team_per_possession drop column `Tm`;


update team_per_possession set `Team` = `Tm` where `Team` is null and `Tm` is not null;
update team_per_possession set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_per_possession add column `nickname` varchar(3) not null;
update team_per_possession a join abbrev b on a.Team = b.Team set a.Nickname = b.Nicknames;
alter table team_per_possession drop column `Tm`;
alter table team_per_possession add column `team_id` integer not null;
update team_per_possession a join abbrev b on a.Team = b.Team set a.team_id = b.ID;

CREATE INDEX idx_team_id ON team_per_possession(team_id);


-- processing team_v_team
update team_v_team a join abbrev b on a.Team = b.Team set a.Team = b.Nicknames;

-- create a new table with unique player names

create table player_unique (id INT AUTO_INCREMENT PRIMARY KEY, player_name varchar(100) NOT NULL UNIQUE);
INSERT INTO player_unique (player_name) SELECT DISTINCT Player FROM player_total;
update player_unique set player_name = trim(player_name);

-- process player_total
update player_total  set `Player` = trim(`Player`);
update player_total  set  `GS` = null where `GS` = '';
update player_total  set  `MP` = null where `MP` = '';
update player_total  set  `FG` = null where `FG` = '';
update player_total  set `FG%` = null where `FG%` = '';
update player_total  set  `3P` = null where `3P` = '';
update player_total  set `3P%` = null where `3P%` = '';
update player_total  set `3PA` = null where `3PA` = '';
update player_total  set  `2P` = null where `2P` = '';
update player_total  set  `2PA` = null where `2PA` = '';
update player_total  set `2P%` = null where `2P%` = '';
update player_total  set`eFG%` = null where `eFG%` = '';
update player_total  set  `FT` = null where `FT` = '';
update player_total  set `FTA` = null where `FTA` = '';
update player_total  set `FT%` = null where `FT%` = '';
update player_total  set `ORB` = null where `ORB` = '';
update player_total  set `DRB` = null where `DRB` = '';
update player_total  set `TRB` = null where `TRB` = '';
update player_total  set `AST` = null where `AST` = '';
update player_total  set `STL` = null where `STL` = '';
update player_total  set `BLK` = null where `BLK` = '';
update player_total  set `TOV` = null where `TOV` = '';
update player_total  set  `PF` = null where `PF` = '';
update player_total  set `PTS` = null where `PTS` = '';


alter table player_total  MODIFY `Rk` INTEGER;
alter table player_total  MODIFY `Age` INTEGER; 
alter table player_total  MODIFY `G` INTEGER;
alter table player_total  MODIFY `GS` INTEGER; 
alter table player_total  MODIFY `MP` INTEGER; 
alter table player_total  MODIFY `FG` INTEGER;
alter table player_total  MODIFY `FG%` DECIMAL;
alter table player_total  MODIFY `3P` INTEGER;
alter table player_total  MODIFY `3PA` INTEGER;
alter table player_total  MODIFY `3P%` DECIMAL;
alter table player_total  MODIFY `2P` INTEGER;
alter table player_total  MODIFY `2PA` INTEGER;
alter table player_total  MODIFY `2P%` DECIMAL;
alter table player_total  MODIFY `eFG%` DECIMAL;
alter table player_total  MODIFY `FT` INTEGER;
alter table player_total  MODIFY `FTA` INTEGER;
alter table player_total  MODIFY `FT%` DECIMAL;
alter table player_total  MODIFY `ORB` INTEGER;
alter table player_total  MODIFY `DRB` INTEGER;
alter table player_total  MODIFY `TRB` INTEGER;
alter table player_total  MODIFY `AST` INTEGER;
alter table player_total  MODIFY `STL` INTEGER;
alter table player_total  MODIFY `BLK` INTEGER;
alter table player_total  MODIFY `TOV` INTEGER;
alter table player_total  MODIFY `PF` INTEGER;
alter table player_total  MODIFY `PTS` INTEGER;
alter table player_total  MODIFY `Year` INTEGER;

alter table player_total add player_id INTEGER not null;
update player_total pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;

update player_total set Tm = trim(Tm);
alter table player_total add team_id INTEGER not null;
update player_total pt join abbrev up on pt.Tm = up.Nicknames set pt.team_id = up.id;

CREATE INDEX idx_player_id ON player_total (player_id);
CREATE INDEX idx_team_id ON player_total (team_id);


-- process player_per_game

update player_per_game  set `Player` = trim(`Player`);
update player_per_game  set  `GS` = null where `GS` = '';
update player_per_game  set  `MP` = null where `MP` = '';
update player_per_game  set  `FG` = null where `FG` = '';
update player_per_game  set `FG%` = null where `FG%` = '';
update player_per_game  set  `3P` = null where `3P` = '';
update player_per_game  set `3P%` = null where `3P%` = '';
update player_per_game  set `3PA` = null where `3PA` = '';
update player_per_game  set  `2P` = null where `2P` = '';
update player_per_game  set `2P%` = null where `2P%` = '';
update player_per_minute  set `2PA` = null where `2PA` = '';
update player_per_game  set`eFG%` = null where `eFG%` = '';
update player_per_game  set  `FT` = null where `FT` = '';
update player_per_game  set `FTA` = null where `FTA` = '';
update player_per_game  set `FT%` = null where `FT%` = '';
update player_per_game  set `ORB` = null where `ORB` = '';
update player_per_game  set `DRB` = null where `DRB` = '';
update player_per_game  set `TRB` = null where `TRB` = '';
update player_per_game  set `AST` = null where `AST` = '';
update player_per_game  set `STL` = null where `STL` = '';
update player_per_game  set `BLK` = null where `BLK` = '';
update player_per_game  set `TOV` = null where `TOV` = '';
update player_per_game  set  `PF` = null where `PF` = '';
update player_per_game  set `PTS` = null where `PTS` = '';


alter table player_per_game  MODIFY `Rk` INTEGER;
alter table player_per_game  MODIFY `Age` INTEGER; 
alter table player_per_game  MODIFY `G` INTEGER;
alter table player_per_game  MODIFY `GS` INTEGER; 
alter table player_per_game  MODIFY `MP` INTEGER; 
alter table player_per_game  MODIFY `FG` INTEGER;
alter table player_per_game  MODIFY `FG%` DECIMAL;
alter table player_per_game  MODIFY `3P` INTEGER;
alter table player_per_game  MODIFY `3PA` INTEGER;
alter table player_per_game  MODIFY `3P%` DECIMAL;
alter table player_per_game  MODIFY `2P` INTEGER;
alter table player_per_game  MODIFY `2PA` INTEGER;
alter table player_per_game  MODIFY `2P%` DECIMAL;
alter table player_per_game  MODIFY `eFG%` DECIMAL;
alter table player_per_game  MODIFY `FT` INTEGER;
alter table player_per_game  MODIFY `FTA` INTEGER;
alter table player_per_game  MODIFY `FT%` DECIMAL;
alter table player_per_game  MODIFY `ORB` INTEGER;
alter table player_per_game  MODIFY `DRB` INTEGER;
alter table player_per_game  MODIFY `TRB` INTEGER;
alter table player_per_game  MODIFY `AST` INTEGER;
alter table player_per_game  MODIFY `STL` INTEGER;
alter table player_per_game  MODIFY `BLK` INTEGER;
alter table player_per_game  MODIFY `TOV` INTEGER;
alter table player_per_game  MODIFY `PF` INTEGER;
alter table player_per_game  MODIFY `PTS` INTEGER;
alter table player_per_game  MODIFY `Year` INTEGER;

alter table player_per_game add player_id INTEGER not null;

update player_per_game pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;

update player_per_game set Tm = trim(Tm);
alter table player_per_game add team_id INTEGER not null;
update player_per_game pt join abbrev up on pt.Tm = up.Nicknames set pt.team_id = up.id;

CREATE INDEX idx_player_id ON player_per_game (player_id);
CREATE INDEX idx_team_id ON player_per_game (team_id);



-- process player_per_minute

update player_per_minute  set `Player` = trim(`Player`);
update player_per_minute  set  `GS` = null where `GS` = '';
update player_per_minute  set  `MP` = null where `MP` = '';
update player_per_minute  set  `FG` = null where `FG` = '';
update player_per_minute  set `FG%` = null where `FG%` = '';
update player_per_minute  set  `3P` = null where `3P` = '';
update player_per_minute  set `3P%` = null where `3P%` = '';
update player_per_minute  set `3PA` = null where `3PA` = '';
update player_per_minute  set  `2P` = null where `2P` = '';
update player_per_minute  set `2PA` = null where `2PA` = '';
update player_per_minute  set `2P%` = null where `2P%` = '';
update player_per_minute  set`eFG%` = null where `eFG%` = '';
update player_per_minute  set  `FT` = null where `FT` = '';
update player_per_minute  set `FTA` = null where `FTA` = '';
update player_per_minute  set `FT%` = null where `FT%` = '';
update player_per_minute  set `ORB` = null where `ORB` = '';
update player_per_minute  set `DRB` = null where `DRB` = '';
update player_per_minute  set `TRB` = null where `TRB` = '';
update player_per_minute  set `AST` = null where `AST` = '';
update player_per_minute  set `STL` = null where `STL` = '';
update player_per_minute  set `BLK` = null where `BLK` = '';
update player_per_minute  set `TOV` = null where `TOV` = '';
update player_per_minute  set  `PF` = null where `PF` = '';
update player_per_minute  set `PTS` = null where `PTS` = '';


alter table player_per_minute  MODIFY `Rk` INTEGER;
alter table player_per_minute  MODIFY `Age` INTEGER; 
alter table player_per_minute  MODIFY `G` INTEGER;
alter table player_per_minute  MODIFY `GS` INTEGER; 
alter table player_per_minute  MODIFY `MP` INTEGER; 
alter table player_per_minute  MODIFY `FG` INTEGER;
alter table player_per_minute  MODIFY `FG%` DECIMAL;
alter table player_per_minute  MODIFY `3P` INTEGER;
alter table player_per_minute  MODIFY `3PA` INTEGER;
alter table player_per_minute  MODIFY `3P%` DECIMAL;
alter table player_per_minute  MODIFY `2P` INTEGER;
alter table player_per_minute  MODIFY `2PA` INTEGER;
alter table player_per_minute  MODIFY `2P%` DECIMAL;
alter table player_per_minute  MODIFY `eFG%` DECIMAL;
alter table player_per_minute  MODIFY `FT` INTEGER;
alter table player_per_minute  MODIFY `FTA` INTEGER;
alter table player_per_minute  MODIFY `FT%` DECIMAL;
alter table player_per_minute  MODIFY `ORB` INTEGER;
alter table player_per_minute  MODIFY `DRB` INTEGER;
alter table player_per_minute  MODIFY `TRB` INTEGER;
alter table player_per_minute  MODIFY `AST` INTEGER;
alter table player_per_minute  MODIFY `STL` INTEGER;
alter table player_per_minute  MODIFY `BLK` INTEGER;
alter table player_per_minute  MODIFY `TOV` INTEGER;
alter table player_per_minute  MODIFY `PF` INTEGER;
alter table player_per_minute  MODIFY `PTS` INTEGER;
alter table player_per_minute  MODIFY `Year` INTEGER;

alter table player_per_minute add player_id INTEGER not null;

update player_per_minute pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;

update player_per_minute set Tm = trim(Tm);
alter table player_per_minute add team_id INTEGER not null;
update player_per_minute pt join abbrev up on pt.Tm = up.Nicknames set pt.team_id = up.id;

CREATE INDEX idx_player_id ON player_per_minute (player_id);
CREATE INDEX idx_team_id ON player_per_minute (team_id);



-- process player_per_possession

update player_per_possession  set `Player` = trim(`Player`);
update player_per_possession  set  `GS` = null where `GS` = '';
update player_per_possession  set  `MP` = null where `MP` = '';
update player_per_possession  set  `FG` = null where `FG` = '';
update player_per_possession  set `FG%` = null where `FG%` = '';
update player_per_possession  set  `3P` = null where `3P` = '';
update player_per_possession  set `3P%` = null where `3P%` = '';
update player_per_possession  set `3PA` = null where `3PA` = '';
update player_per_possession  set  `2P` = null where `2P` = '';
update player_per_possession  set  `2PA` = null where `2PA` = '';
update player_per_possession  set `2P%` = null where `2P%` = '';
update player_per_possession  set`eFG%` = null where `eFG%` = '';
update player_per_possession  set  `FT` = null where `FT` = '';
update player_per_possession  set `FTA` = null where `FTA` = '';
update player_per_possession  set `FT%` = null where `FT%` = '';
update player_per_possession  set `ORB` = null where `ORB` = '';
update player_per_possession  set `DRB` = null where `DRB` = '';
update player_per_possession  set `TRB` = null where `TRB` = '';
update player_per_possession  set `AST` = null where `AST` = '';
update player_per_possession  set `STL` = null where `STL` = '';
update player_per_possession  set `BLK` = null where `BLK` = '';
update player_per_possession  set `TOV` = null where `TOV` = '';
update player_per_possession  set  `PF` = null where `PF` = '';
update player_per_possession  set `PTS` = null where `PTS` = '';


alter table player_per_possession  MODIFY `Rk` INTEGER;
alter table player_per_possession  MODIFY `Age` INTEGER; 
alter table player_per_possession  MODIFY `G` INTEGER;
alter table player_per_possession  MODIFY `GS` INTEGER; 
alter table player_per_possession  MODIFY `MP` INTEGER; 
alter table player_per_possession  MODIFY `FG` INTEGER;
alter table player_per_possession  MODIFY `FG%` DECIMAL;
alter table player_per_possession  MODIFY `3P` INTEGER;
alter table player_per_possession  MODIFY `3PA` INTEGER;
alter table player_per_possession  MODIFY `3P%` DECIMAL;
alter table player_per_possession  MODIFY `2P` INTEGER;
alter table player_per_possession  MODIFY `2PA` INTEGER;
alter table player_per_possession  MODIFY `2P%` DECIMAL;
alter table player_per_possession  MODIFY `eFG%` DECIMAL;
alter table player_per_possession  MODIFY `FT` INTEGER;
alter table player_per_possession  MODIFY `FTA` INTEGER;
alter table player_per_possession  MODIFY `FT%` DECIMAL;
alter table player_per_possession  MODIFY `ORB` INTEGER;
alter table player_per_possession  MODIFY `DRB` INTEGER;
alter table player_per_possession  MODIFY `TRB` INTEGER;
alter table player_per_possession  MODIFY `AST` INTEGER;
alter table player_per_possession  MODIFY `STL` INTEGER;
alter table player_per_possession  MODIFY `BLK` INTEGER;
alter table player_per_possession  MODIFY `TOV` INTEGER;
alter table player_per_possession  MODIFY `PF` INTEGER;
alter table player_per_possession  MODIFY `PTS` INTEGER;
alter table player_per_possession  MODIFY `Year` INTEGER;

alter table player_per_possession add player_id INTEGER not null;

update player_per_possession pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;


update player_per_possession set Tm = trim(Tm);
alter table player_per_possession add team_id INTEGER not null;
update player_per_possession pt join abbrev up on pt.Tm = up.Nicknames set pt.team_id = up.id;

CREATE INDEX idx_player_id ON player_per_possession (player_id);
CREATE INDEX idx_team_id ON player_per_possession (team_id);


-- process player_advanced

update player_advanced set `Rk` = null where `Rk` = '';
update player_advanced set `Player` = null where `Player` = '';
update player_advanced set `Pos` = null where `Pos` = '';
update player_advanced set `Age` = null where `Age` = '';
update player_advanced set `Tm` = null where `Tm` = '';
update player_advanced set `G` = null where `G` = '';
update player_advanced set `MP` = null where `MP` = '';
update player_advanced set `PER` = null where `PER` = '';
update player_advanced set `TS%` = null where `TS%` = '';
update player_advanced set `3PAr` = null where `3PAr` = '';
update player_advanced set `FTr` = null where `FTr` = '';
update player_advanced set `ORB%` = null where `ORB%` = '';
update player_advanced set `DRB%` = null where `DRB%` = '';
update player_advanced set `TRB%` = null where `TRB%` = '';
update player_advanced set `AST%` = null where `AST%` = '';
update player_advanced set `STL%` = null where `STL%` = '';
update player_advanced set `BLK%` = null where `BLK%` = '';
update player_advanced set `TOV%` = null where `TOV%` = '';
update player_advanced set `USG%` = null where `USG%` = '';
update player_advanced set `OWS` = null where `OWS` = '';
update player_advanced set  `DWS` = null where `DWS` = '';
update player_advanced set `WS` = null where `WS` = '';
update player_advanced set `WS/48` = null where `WS/48` = '';
update player_advanced set `OBPM` = null where `OBPM` = '';
update player_advanced set `DBPM` = null where `DBPM` = '';
update player_advanced set `BPM` = null where `BPM` = '';
update player_advanced set `VORP` = null where `VORP` = '';

alter table player_advanced  MODIFY `Rk` INTEGER;
alter table player_advanced  MODIFY `Age` INTEGER;
alter table player_advanced  MODIFY `G` INTEGER;
alter table player_advanced  MODIFY `MP` INTEGER;
alter table player_advanced  MODIFY `PER` DECIMAL;
alter table player_advanced  MODIFY `TS%` DECIMAL;
alter table player_advanced  MODIFY `3PAr` DECIMAL;
alter table player_advanced  MODIFY `FTr` DECIMAL;
alter table player_advanced  MODIFY `ORB%` DECIMAL;
alter table player_advanced  MODIFY `DRB%` DECIMAL;
alter table player_advanced  MODIFY `TRB%` DECIMAL;
alter table player_advanced  MODIFY `AST%` DECIMAL;
alter table player_advanced  MODIFY `STL%` DECIMAL;
alter table player_advanced  MODIFY `BLK%` DECIMAL;
alter table player_advanced  MODIFY `TOV%` DECIMAL;
alter table player_advanced  MODIFY `USG%` DECIMAL;
alter table player_advanced  MODIFY `OWS` DECIMAL;
alter table player_advanced  MODIFY `DWS` DECIMAL;
alter table player_advanced  MODIFY `WS` DECIMAL;
alter table player_advanced  MODIFY `WS/48` DECIMAL;
alter table player_advanced  MODIFY `OBPM` DECIMAL;
alter table player_advanced  MODIFY `DBPM` DECIMAL;
alter table player_advanced  MODIFY `BPM` DECIMAL;
alter table player_advanced  MODIFY `VORP` DECIMAL;
alter table player_advanced  MODIFY `Year` INTEGER;

alter table player_advanced add player_id INTEGER not null;

update player_advanced pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;

update player_advanced set Tm = trim(Tm);
alter table player_advanced add team_id INTEGER not null;
update player_advanced pt join abbrev up on pt.Tm = up.Nicknames set pt.team_id = up.id;

CREATE INDEX idx_player_id ON player_advanced (player_id);
CREATE INDEX idx_team_id ON player_advanced (team_id);
