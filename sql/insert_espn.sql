insert into ud_games(espn_game_id, home_id, away_id, game_ts, week_id, home_score, away_score, is_final)
select
espn_game_id,
t1.atthletics_team_id home_id,
t2.atthletics_team_id away_id,
game_ts,
week_id,
home_score,
away_score,
is_final
from ud_games_espn g
left join teams t1
on g.espn_home_id = t1.espn_team_id
left join teams t2
on g.espn_away_id = t2.espn_team_id
;
