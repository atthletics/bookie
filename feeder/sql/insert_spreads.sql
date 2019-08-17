insert into ud_spreads(game_id, team_id, spread)
select
g.game_id,
t.atthletics_team_id,
s.spread
from ud_spreads_espn s
left join ud_games g
on s.espn_game_id = g.espn_game_id
left join teams t
on s.espn_team_id = t.espn_team_id
;
