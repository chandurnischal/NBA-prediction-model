update conference_standings set `Team` =  REPLACE(`Team`, '*', '') where `Team` like '%*%';
update conference_standings  set `Team` = trim(`Team`);
update conference_standings set `GB` = null WHERE `GB` like '%???%';


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
alter table conference_standings modify `GB` DECIMAL;
alter table conference_standings modify `PS/G` DECIMAL;
alter table conference_standings modify `PA/G` INTEGER;
alter table conference_standings modify `SRS` INTEGER;

alter table conference_standings add column `T` integer;
update conference_standings set `T` = `W` + `L`;

alter table conference_standings add column `W%` DECIMAL(10, 2);
update conference_standings set `W%` = CAST(`W` AS DECIMAL(10, 2)) * 100 / CAST(`T` AS DECIMAL(10, 2));

alter table conference_standings add column `nickname` varchar(3) not null;
update conference_standings a join abbrev b on a.Team = b.Team set a.Nickname = b.Nickname;
alter table conference_standings add column `team_id` integer not null;
update conference_standings a join abbrev b on a.Team = b.Team set a.team_id = b.ID;
