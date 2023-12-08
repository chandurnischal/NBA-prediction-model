-- processing abbreviation table

ALTER TABLE abbrev CHANGE COLUMN Nicknames Nickname text;
alter table abbrev modify Team text not null;
alter table abbrev modify Nickname text not null;
update abbrev set Team = trim(Team), Nickname = trim(Nickname);
alter table abbrev modify Nickname varchar(3);
ALTER TABLE abbrev ADD COLUMN ID INT AUTO_INCREMENT PRIMARY KEY;
alter table abbrev add column franchise varchar(20);
update abbrev set franchise = SUBSTRING_INDEX(Team, ' ', -1);
CREATE table franchises (franchiseID int AUTO_INCREMENT PRIMARY KEY, franchise varchar(20)) as (select DISTINCT(franchise) from abbrev);
alter table abbrev add column franchiseID int;
update abbrev a join franchises b on a.franchise = b.franchise set a.franchiseID = b.franchiseID;
drop table franchises;
drop table team_v_team;

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
update team_total set `FT` = null where `FT` = '';            
update team_total set `FTA` = null where `FTA` = '';              
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
alter table team_total modify `G` INTEGER;
alter table team_total modify `MP` INTEGER;
alter table team_total modify `FG` INTEGER;
alter table team_total modify `FGA` INTEGER;
alter table team_total modify `FG%` DECIMAL(10, 2);
alter table team_total modify `3P` INTEGER;
alter table team_total modify `3PA` INTEGER;
alter table team_total modify `3P%` DECIMAL(10, 2);
alter table team_total modify `2P` INTEGER;
alter table team_total modify `2PA` INTEGER;
alter table team_total modify `2P%` DECIMAL(10, 2);
alter table team_total modify `FT` INTEGER;
alter table team_total modify `FTA` INTEGER;
alter table team_total modify `FT%` DECIMAL(10, 2);
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
update team_total set `Team` = `Tm` where `Team` is null and `Tm` is not null;

alter table team_total drop column `Tm`;

update team_total set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_total add column `nickname` varchar(3) not null;
update team_total a join abbrev b on a.Team = b.Team set a.Nickname = b.Nickname;
alter table team_total drop column `Tm`;
alter table team_total add column `team_id` integer not null;
update team_total a join abbrev b on a.Team = b.Team set a.team_id = b.ID;
alter table team_total add column `franchise_id` integer not null;
update team_total a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;
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
update team_per_game set `FT` = null where `FT` = '';              
update team_per_game set `FTA` = null where `FTA` = '';              
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
alter table team_per_game modify `G` INTEGER;
alter table team_per_game modify `MP` INTEGER;
alter table team_per_game modify `FG` INTEGER;
alter table team_per_game modify `FGA` INTEGER;
alter table team_per_game modify `FG%` DECIMAL(10, 2);
alter table team_per_game modify `3P` INTEGER;
alter table team_per_game modify `3PA` INTEGER;
alter table team_per_game modify `3P%` DECIMAL(10, 2);
alter table team_per_game modify `2P` INTEGER;
alter table team_per_game modify `2PA` INTEGER;
alter table team_per_game modify `2P%` DECIMAL(10, 2);
alter table team_per_game modify `FT` INTEGER;
alter table team_per_game modify `FTA` INTEGER;
alter table team_per_game modify `FT%` DECIMAL(10, 2);
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
update team_per_game set `Team` = `Tm` where `Team` is null and `Tm` is not null;

alter table team_per_game drop column `Tm`;


update team_per_game set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_per_game add column `nickname` varchar(3) not null;
update team_per_game a join abbrev b on a.Team = b.Team set a.Nickname = b.Nickname;
alter table team_per_game drop column `Tm`;
alter table team_per_game add column `team_id` integer not null;
update team_per_game a join abbrev b on a.Team = b.Team set a.team_id = b.ID;
alter table team_per_game add column `franchise_id` integer not null;
update team_per_game a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


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
update team_per_possession set `FT` = null where `FT` = '';              
update team_per_possession set `FTA` = null where `FTA` = '';              
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
alter table team_per_possession modify `G` INTEGER;
alter table team_per_possession modify `MP` INTEGER;
alter table team_per_possession modify `FG` INTEGER;
alter table team_per_possession modify `FGA` INTEGER;
alter table team_per_possession modify `FG%` DECIMAL(10, 2);
alter table team_per_possession modify `3P` INTEGER;
alter table team_per_possession modify `3PA` INTEGER;
alter table team_per_possession modify `3P%` DECIMAL(10, 2);
alter table team_per_possession modify `2P` INTEGER;
alter table team_per_possession modify `2PA` INTEGER;
alter table team_per_possession modify `2P%` DECIMAL(10, 2);
alter table team_per_possession modify `FT` INTEGER;
alter table team_per_possession modify `FTA` INTEGER;
alter table team_per_possession modify `FT%` DECIMAL(10, 2);
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
update team_per_possession set `Team` = `Tm` where `Team` is null and `Tm` is not null;

alter table team_per_possession drop column `Tm`;


update team_per_possession set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
alter table team_per_possession add column `nickname` varchar(3) not null;
update team_per_possession a join abbrev b on a.Team = b.Team set a.Nickname = b.Nickname;
alter table team_per_possession drop column `Tm`;
alter table team_per_possession add column `team_id` integer not null;
update team_per_possession a join abbrev b on a.Team = b.Team set a.team_id = b.ID;
alter table team_per_possession add column `franchise_id` integer not null;
update team_per_possession a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;

CREATE INDEX idx_team_id ON team_per_possession(team_id);

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
alter table player_total  MODIFY `FG%` DECIMAL(10, 2);
alter table player_total  MODIFY `3P` INTEGER;
alter table player_total  MODIFY `3PA` INTEGER;
alter table player_total  MODIFY `3P%` DECIMAL(10, 2);
alter table player_total  MODIFY `2P` INTEGER;
alter table player_total  MODIFY `2PA` INTEGER;
alter table player_total  MODIFY `2P%` DECIMAL(10, 2);
alter table player_total  MODIFY `eFG%` DECIMAL(10, 2);
alter table player_total  MODIFY `FT` INTEGER;
alter table player_total  MODIFY `FTA` INTEGER;
alter table player_total  MODIFY `FT%` DECIMAL(10, 2);
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
update player_total pt join abbrev up on pt.Tm = up.Nickname set pt.team_id = up.id;

alter table player_total add column `franchise_id` integer not null;
update player_total a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


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
alter table player_per_game  MODIFY `FG%` DECIMAL(10, 2);
alter table player_per_game  MODIFY `3P` INTEGER;
alter table player_per_game  MODIFY `3PA` INTEGER;
alter table player_per_game  MODIFY `3P%` DECIMAL(10, 2);
alter table player_per_game  MODIFY `2P` INTEGER;
alter table player_per_game  MODIFY `2PA` INTEGER;
alter table player_per_game  MODIFY `2P%` DECIMAL(10, 2);
alter table player_per_game  MODIFY `eFG%` DECIMAL(10, 2);
alter table player_per_game  MODIFY `FT` INTEGER;
alter table player_per_game  MODIFY `FTA` INTEGER;
alter table player_per_game  MODIFY `FT%` DECIMAL(10, 2);
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
update player_per_game pt join abbrev up on pt.Tm = up.Nickname set pt.team_id = up.id;


alter table player_per_game add column `franchise_id` integer not null;
update player_per_game a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


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
alter table player_per_minute  MODIFY `FG%` DECIMAL(10, 2);
alter table player_per_minute  MODIFY `3P` INTEGER;
alter table player_per_minute  MODIFY `3PA` INTEGER;
alter table player_per_minute  MODIFY `3P%` DECIMAL(10, 2);
alter table player_per_minute  MODIFY `2P` INTEGER;
alter table player_per_minute  MODIFY `2PA` INTEGER;
alter table player_per_minute  MODIFY `2P%` DECIMAL(10, 2);
alter table player_per_minute  MODIFY `eFG%` DECIMAL(10, 2);
alter table player_per_minute  MODIFY `FT` INTEGER;
alter table player_per_minute  MODIFY `FTA` INTEGER;
alter table player_per_minute  MODIFY `FT%` DECIMAL(10, 2);
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
update player_per_minute pt join abbrev up on pt.Tm = up.Nickname set pt.team_id = up.id;


alter table player_per_minute add column `franchise_id` integer not null;
update player_per_minute a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


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
alter table player_per_possession  MODIFY `FG%` DECIMAL(10, 2);
alter table player_per_possession  MODIFY `3P` INTEGER;
alter table player_per_possession  MODIFY `3PA` INTEGER;
alter table player_per_possession  MODIFY `3P%` DECIMAL(10, 2);
alter table player_per_possession  MODIFY `2P` INTEGER;
alter table player_per_possession  MODIFY `2PA` INTEGER;
alter table player_per_possession  MODIFY `2P%` DECIMAL(10, 2);
alter table player_per_possession  MODIFY `eFG%` DECIMAL(10, 2);
alter table player_per_possession  MODIFY `FT` INTEGER;
alter table player_per_possession  MODIFY `FTA` INTEGER;
alter table player_per_possession  MODIFY `FT%` DECIMAL(10, 2);
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
update player_per_possession pt join abbrev up on pt.Tm = up.Nickname set pt.team_id = up.id;


alter table player_per_possession add column `franchise_id` integer not null;
update player_per_possession a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


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
alter table player_advanced  MODIFY `PER` DECIMAL(10, 2);
alter table player_advanced  MODIFY `TS%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `3PAr` DECIMAL(10, 2);
alter table player_advanced  MODIFY `FTr` DECIMAL(10, 2);
alter table player_advanced  MODIFY `ORB%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `DRB%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `TRB%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `AST%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `STL%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `BLK%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `TOV%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `USG%` DECIMAL(10, 2);
alter table player_advanced  MODIFY `OWS` DECIMAL(10, 2);
alter table player_advanced  MODIFY `DWS` DECIMAL(10, 2);
alter table player_advanced  MODIFY `WS` DECIMAL(10, 2);
alter table player_advanced  MODIFY `WS/48` DECIMAL(10, 2);
alter table player_advanced  MODIFY `OBPM` DECIMAL(10, 2);
alter table player_advanced  MODIFY `DBPM` DECIMAL(10, 2);
alter table player_advanced  MODIFY `BPM` DECIMAL(10, 2);
alter table player_advanced  MODIFY `VORP` DECIMAL(10, 2);
alter table player_advanced  MODIFY `Year` INTEGER;

alter table player_advanced add player_id INTEGER not null;

update player_advanced pt join player_unique up on pt.Player = up.player_name set pt.player_id = up.id;

update player_advanced set Tm = trim(Tm);
alter table player_advanced add team_id INTEGER not null;
update player_advanced pt join abbrev up on pt.Tm = up.Nickname set pt.team_id = up.id;


alter table player_advanced add column `franchise_id` integer not null;
update player_advanced a join abbrev b on a.Team_id = b.id set a.franchise_id = b.franchiseid;


CREATE INDEX idx_player_id ON player_advanced (player_id);
CREATE INDEX idx_team_id ON player_advanced (team_id);


-- processing games table

ALTER TABLE games CHANGE COLUMN date datetime text;
DELETE FROM games where datetime = 'Playoffs';
ALTER TABLE games ADD COLUMN day VARCHAR(3), ADD COLUMN date DATE;
UPDATE games SET day = DATE_FORMAT(STR_TO_DATE(datetime, '%a, %b %d, %Y'), '%a');
update games set date = STR_TO_DATE(datetime, '%a, %b %d, %Y');
alter table games drop column datetime;

alter table games add column season int;
update games set season = year(date) + 1 where month(date) between 7 and 12;
update games set season = year(date) where month(date) < 7;

update games set Visitor = trim(Visitor);
update games set Home = trim(Home);

alter table games add column home_id integer;
alter table games add column home_fid int;
alter table games add column visitor_id integer;
alter table games add column visitor_fid int;

update games a join abbrev b on a.Home = b.Team set a.home_id = b.id;
update games a join abbrev b on a.Visitor = b.Team set a.visitor_id = b.id;
CREATE INDEX idx_visitor_id ON games (visitor_id);
CREATE INDEX idx_home_id ON games (home_id);

update games a join abbrev b on a.visitor_id = b.id set a.Visitor = b.Nickname;
update games a join abbrev b on a.home_id = b.id set a.Home = b.Nickname;

update games a join abbrev b on a.visitor_id = b.id set a.visitor_fid = b.franchiseID;
update games a join abbrev b on a.home_id = b.id set a.home_fid = b.franchiseID;

alter table games MODIFY `VPoints` INTEGER;
alter table games MODIFY `HPoints` INTEGER;

UPDATE games SET `Attend` = NULL WHERE `Attend` = '';
update games set `Attend` =  REPLACE(`Attend`, ',', '') where `Attend` like '%,%';
alter table games MODIFY `Attend` INTEGER;

alter table games add column `mov` integer;
update games set `mov`=Hpoints-VPoints;

alter table games add column playoff_date date;
update games a join playoffs_dates b on a.season = b.year set a.playoff_date = b.start_date;
alter table games add column is_regular int;
update games set is_regular = 1 where date < playoff_date;
update games set is_regular = 1 where playoff_date is null;
update games set is_regular = 0 where date >= playoff_date;

-- processing conference standings

update conference_standings set `Team` =  REPLACE(`Team`, '*', '');
update conference_standings set `Team` =  REGEXP_REPLACE(`Team`, '\\([0-9]+\\)', '');
UPDATE conference_standings SET `Team` = REGEXP_REPLACE(`Team`, '[^a-zA-Z0-9\/ ]', '');
update conference_standings  set `Team` = trim(`Team`);
update conference_standings set `GB` = null WHERE `GB` like '%?%';


update conference_standings set `W` = null where `W` = '';              
update conference_standings set `Team` = null where `Team` = '';              
update conference_standings set `L` = null where `L` = '';              
update conference_standings set `W/L%` = null where `W/L%` = '';              
update conference_standings set `GB` = null where `GB` = '';              
update conference_standings set `PS/G` = null where `PS/G` = '';              
update conference_standings set `PA/G` = null where `PA/G` = '';              
update conference_standings set `SRS` = null where `SRS` = '';              
update conference_standings set `conf` = null where `conf` = '';              

alter table conference_standings drop column `W/L%`;
alter table conference_standings modify `W` INTEGER;
alter table conference_standings modify `L` INTEGER;
alter table conference_standings modify `GB` DECIMAL(10, 2);
alter table conference_standings modify `PS/G` DECIMAL(10, 2);
alter table conference_standings modify `PA/G` INTEGER;
alter table conference_standings modify `SRS` INTEGER;

alter table conference_standings add column `T` integer;
update conference_standings set `T` = `W` + `L`;

alter table conference_standings add column `W%` DECIMAL(10, 2);
update conference_standings set `W%` = CAST(`W` AS DECIMAL(10, 2)) * 100 / CAST(`T` AS DECIMAL(10, 2));

alter table conference_standings add column team_id int, add column franchise_id int;
update conference_standings as a join abbrev as b on a.Team = b.Team set a.team_id = b.id;
CREATE INDEX idx_team_id ON conference_standings(team_id);
update conference_standings a join abbrev b on a.team_id = b.id set a.franchise_id = b.franchiseID;
update conference_standings a join abbrev b on a.team_id = b.id set a.Team = b.Nickname;