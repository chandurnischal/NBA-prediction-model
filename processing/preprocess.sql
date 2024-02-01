create index home_idx on elo(home_id);
create index visitor_idx on elo(visitor_id); 
create index team_idx on team_efficiency(team_id); 
alter table elo add column home_per decimal(10, 2); 
update elo a join team_efficiency b on a.home_id = b.team_id and a.season = b.year set a.home_per = b.per;
alter table elo add column visitor_per decimal(10, 2);
update elo a join team_efficiency b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_per = b.per;
alter table elo add column home_eff decimal(10, 2);
update elo a join team_efficiency b on a.home_id = b.team_id and a.season = b.year set a.home_eff = b.eff;
alter table elo add column visitor_eff decimal(10, 2);
update elo a join team_efficiency b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_eff = b.eff;
alter table elo add column home_win_perc decimal(10, 2);
update elo a join conference_standings b on a.home_id = b.team_id and a.season = b.year set a.home_win_perc = b.`W%`;
alter table elo add column visitor_win_perc decimal(10, 2);
update elo a join conference_standings b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_win_perc = b.`W%`;
alter table elo add column home_ppg decimal(10, 2), add column visitor_ppg decimal(10, 2), add column home_pag decimal(10, 2), add column visitor_pag decimal(10, 2);
update elo a join conference_standings b on a.home_id = b.team_id and a.season = b.year set a.home_ppg = b.`PS/G`, a.home_pag = b.`PA/G`;
update elo a join conference_standings b on a.visitor_id = b.team_id and a.season and b.year set a.visitor_ppg = b.`PS/G`, a.visitor_pag = b.`PA/G`;
alter table elo add column home_victory text;
update elo set home_victory = 'YES' where mov > 0;
update elo set home_victory = 'NO' where mov < 0;
alter table elo add column home_conf varchar(1), add column visitor_conf varchar(1);
update elo a join (select team_id, conf from team_total) b on a.home_id = b.team_id set a.home_conf = b.conf;
update elo a join (select team_id, conf from team_total) b on a.visitor_id = b.team_id set a.visitor_conf = b.conf;
alter table conference_standings add column home_wins int, add column home_losses int, add column visitor_wins int, add column visitor_losses int, add column conf_wins int, add column conf_losses int;
update conference_standings a join (select home_id, season, count(*) home_wins from elo where mov > 0 group by home_id, season) as b on a.team_id = b.home_id and a.year = b.season set a.home_wins = b.home_wins;
update conference_standings a join (select home_id, season, count(*) home_losses from elo where mov < 0 group by home_id, season) as b on a.team_id = b.home_id and a.year = b.season set a.home_losses = b.home_losses;
update conference_standings a join (select visitor_id, season, count(*) visitor_wins from elo where mov < 0 group by visitor_id, season) as b on a.team_id = b.visitor_id and a.year = b.season set a.visitor_wins = b.visitor_wins;
update conference_standings a join (select visitor_id, season, count(*) visitor_losses from elo where mov > 0 group by visitor_id, season) as b on a.team_id = b.visitor_id and a.year = b.season set a.visitor_losses = b.visitor_losses;

update conference_standings a join (select b.home_id as team_id, b.home_wins + c.visitor_wins conf_wins from (select home_id, season, count(*) home_wins from elo where mov > 0 and home_conf = visitor_conf group by home_id, season) as b join (select visitor_id, season, count(*) visitor_wins from elo where mov < 0 and home_conf = visitor_conf group by visitor_id, season) as c on b.home_id = c.visitor_id) as e on a.team_id = e.team_id set a.conf_wins = e.conf_wins;


alter table player_per_game add column per decimal(10, 2);
update player_per_game a join player_advanced b on a.player_id = b.player_id and a.year = b.year set a.per = b.per;