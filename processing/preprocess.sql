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
alter table player_per_game add column per decimal(10, 2);
update player_per_game set per = (`FG` * 85.91) + (`STL` * 53.897) + (`3P` * 51.757) + (`FT` * 46.845) + (`BLK` * 39.19) + (`ORB` * 39.19) + (`AST` * 34.677) + (`DRB` * 14.707) - (`PF` * 17.174) - ((`FTA` - `FT`) * 20.091) - ((`FGA` - `FG`) * 39.190) - (`TOV` * 53.897);