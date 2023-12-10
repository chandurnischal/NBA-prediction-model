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

alter table elo add column home_fgm int, add column home_stl int, add column home_3p int, add column home_ft int, add column home_blk int, add column home_orb int, add column home_ast int, add column home_drb int, add column home_pf int, add column home_ftm int, add column home_tov int, add column home_mp int, add column visitor_fgm int, add column visitor_stl int, add column visitor_3p int, add column visitor_ft int, add column visitor_blk int, add column visitor_orb int, add column visitor_ast int, add column visitor_drb int, add column visitor_pf int, add column visitor_ftm int, add column visitor_tov int, add column visitor_mp int;

update elo a join conference_standings b on a.home_id = b.team_id and a.season = b.year set a.home_ppg = b.`PS/G`, a.home_pag = b.`PA/G`;
update elo a join conference_standings b on a.visitor_id = b.team_id and a.season and b.year set a.visitor_ppg = b.`PS/G`, a.visitor_pag = b.`PA/G`;
alter table elo add column home_victory text;
update elo a join team_total b on a.home_id = b.team_id and a.season = b.year set a.home_fgm = b.FGA - b.FG, a.home_stl = b.STL, a.home_3p = b.3P, a.home_ft = b.FT, a.home_blk = b.BLK, a.home_orb = b.ORB, a.home_ast = b.AST, a.home_drb = b.DRB, a.home_pf = b.PF, a.home_ftm = b.FTA - b.FT, a.home_tov = b.TOV, a.home_mp = b.MP;
update elo a join team_total b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_fgm = b.FGA - b.FG, a.visitor_stl = b.STL, a.visitor_3p = b.3P, a.visitor_ft = b.FT, a.visitor_blk = b.BLK, a.visitor_orb = b.ORB, a.visitor_ast = b.AST, a.visitor_drb = b.DRB, a.visitor_pf = b.PF, a.visitor_ftm = b.FTA - b.FT, a.visitor_tov = b.TOV, a.visitor_mp = b.MP;
update elo set home_victory = 'YES' where mov > 0;
update elo set home_victory = 'NO' where mov < 0;