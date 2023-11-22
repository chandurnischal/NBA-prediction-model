create index home_idx on elo(home_id);
create index visitor_idx on elo(visitor_id); 
create index team_idx on team_efficiency(team_id); 
alter table elo add column home_per decimal(10, 2); 
update elo a join team_efficiency b on a.home_id = b.team_id and a.season = b.year set a.home_per = b.per;
alter table elo add column visitor_per decimal(10, 2);
update elo a join team_efficiency b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_per = b.per;
alter table elo add column home_victory int;
update elo set home_victory = 1 where mov > 0;,
update elo set home_victory = 0 where mov < 0;
