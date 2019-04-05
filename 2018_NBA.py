import numpy as np
import pandas as pd
from pandas import Series,DataFrame

## Convert % statistics to Float ##
def pct2flt(x):
    return float(x.strip('%')/100)


west = ['Golden State','Denver','Houston','Portland','Okla City','San Antonio',
'Utah','LA Clippers','Sacramento','Minnesota','LA Lakers','New Orleans','Memphis',
'Dallas','Phoenix']

east = ['Milwaukee','Toronto','Indiana','Philadelphia','Boston','Detroit','Brooklyn',
'Miami','Orlando','Charlotte','Washington','Atlanta','Chicago','Cleveland','New York']

conf = west + east
confw = ['West'] * 15
confe = ['East'] * 15
conf_a = confw + confe

base = pd.DataFrame(
    {'Team': conf,
     'conf': conf_a})

## Sheet One
# Baseline Team Information
games_played = pd.read_html('https://www.teamrankings.com/nba/stat/games-played')
games_played = games_played[0].loc[:,['Team','2018']]
win_per = pd.read_html('https://www.teamrankings.com/nba/stat/win-pct-all-games')
win_per = win_per[0].loc[:,['Team','2018','Home','Away']]

frame_1 = pd.merge(left = base, right = games_played, on = 'Team', how = 'outer')
frame_1 = pd.merge(left = frame_1, right = win_per, on = 'Team', how = 'outer')

## OFFENSE
# Import Offensive stats
points_per = pd.read_html('https://www.teamrankings.com/nba/stat/points-per-game')
points_per = points_per[0].loc[:,['Team','2018']]
off_eff = pd.read_html('https://www.teamrankings.com/nba/stat/offensive-efficiency')
off_eff = off_eff[0].loc[:,['Team','2018']]

off1 = pd.merge(points_per,off_eff, how = 'outer', on = 'Team')

first_half = pd.read_html('https://www.teamrankings.com/nba/stat/1st-half-points-per-game')
first_half = first_half[0].loc[:,['Team','2018']]
second_half = pd.read_html('https://www.teamrankings.com/nba/stat/2nd-half-points-per-game')
second_half = second_half[0].loc[:,['Team','2018']]

off2 = pd.merge(first_half,second_half, how = 'outer', on = 'Team')

fastbreak = pd.read_html('https://www.teamrankings.com/nba/stat/fastbreak-efficiency')
fastbreak = fastbreak[0].loc[:,['Team','2018']]
paint = pd.read_html('https://www.teamrankings.com/nba/stat/points-in-paint-per-game')
paint = paint[0].loc[:,['Team','2018']]

off3 = pd.merge(fastbreak,paint, how = 'outer', on = 'Team')

pctfrm2 = pd.read_html('https://www.teamrankings.com/nba/stat/percent-of-points-from-2-pointers')
pctfrm2 = pctfrm2[0].loc[:,['Team','2018']]
pctfrm3 = pd.read_html('https://www.teamrankings.com/nba/stat/percent-of-points-from-3-pointers')
pctfrm3 = pctfrm3[0].loc[:,['Team','2018']]

off4 = pd.merge(pctfrm2,pctfrm3, how = 'outer', on = 'Team')

off4['2018_x'] = off4['2018_x'].map(lambda x: str(x)[:-1])
off4['2018_y'] = off4['2018_y'].map(lambda x: str(x)[:-1])

off4['2018_x'] = pd.to_numeric(off4['2018_x']) / 100
off4['2018_y'] = pd.to_numeric(off4['2018_y']) / 100

shtpct = pd.read_html('https://www.teamrankings.com/nba/stat/shooting-pct')
shtpct = shtpct[0].loc[:,['Team','2018']]
efffgpct = pd.read_html('https://www.teamrankings.com/nba/stat/effective-field-goal-pct')
efffgpct = efffgpct[0].loc[:,['Team','2018']]

off5 = pd.merge(shtpct, efffgpct, how = 'outer', on = 'Team')

off5['2018_x'] = off5['2018_x'].map(lambda x: str(x)[:-1])
off5['2018_y'] = off5['2018_y'].map(lambda x: str(x)[:-1])

off5['2018_x'] = pd.to_numeric(off5['2018_x']) / 100
off5['2018_y'] = pd.to_numeric(off5['2018_y']) / 100

off_tot = pd.merge(off1, off2, how = 'outer', on = 'Team')
off_tot = pd.merge(off_tot, off3, how = 'outer', on = 'Team')
off_tot = pd.merge(off_tot, off4, how = 'outer', on = 'Team')
off_tot = pd.merge(off_tot, off5, how = 'outer', on = 'Team')

frame_1 = pd.merge(frame_1, off_tot, how = 'outer', on = 'Team')

## DEFENSE ##
# Import Defensive stats
off_reb = pd.read_html('https://www.teamrankings.com/nba/stat/offensive-rebounds-per-game')
off_reb = off_reb[0].loc[:,['Team','2018']]
def_reb = pd.read_html('https://www.teamrankings.com/nba/stat/defensive-rebounds-per-game')
def_reb = def_reb[0].loc[:,['Team','2018']]

def1 = pd.merge(off_reb, def_reb, how = 'outer', on = 'Team')

block = pd.read_html('https://www.teamrankings.com/nba/stat/blocks-per-game')
block = block[0].loc[:,['Team','2018']]
steal = pd.read_html('https://www.teamrankings.com/nba/stat/steals-per-game')
steal = steal[0].loc[:,['Team','2018']]

def2 = pd.merge(block, steal, how = 'outer', on = 'Team')

dvoa = pd.read_html('https://www.teamrankings.com/nba/stat/defensive-efficiency')
dvoa = dvoa[0].loc[:,['Team','2018']]
opp_ppg = pd.read_html('https://www.teamrankings.com/nba/stat/opponent-points-per-game')
opp_ppg = opp_ppg[0].loc[:,['Team','2018']]

def3 = pd.merge(dvoa, opp_ppg, how = 'outer', on = 'Team')

opp_paint = pd.read_html('https://www.teamrankings.com/nba/stat/opponent-points-in-paint-per-game')
opp_paint = opp_paint[0].loc[:,['Team','2018']]
opp_shoot = pd.read_html('https://www.teamrankings.com/nba/stat/opponent-shooting-pct')
opp_shoot = opp_shoot[0].loc[:,['Team','2018']]

def4 = pd.merge(opp_paint, opp_shoot, how = 'outer', on = 'Team')

def4['2018_y'] = def4['2018_y'].map(lambda x: str(x)[:-1])

def4['2018_y'] = pd.to_numeric(def4['2018_y']) / 100

opp_3 = pd.read_html('https://www.teamrankings.com/nba/stat/opponent-three-point-pct')
opp_3 = opp_3[0].loc[:,['Team','2018']]
opp_2 = pd.read_html('https://www.teamrankings.com/nba/stat/opponent-two-point-pct')
opp_2 = opp_2[0].loc[:,['Team','2018']]

def5 = pd.merge(opp_3, opp_2, how = 'outer', on = 'Team')

def5['2018_x'] = def5['2018_x'].map(lambda x: str(x)[:-1])
def5['2018_y'] = def5['2018_y'].map(lambda x: str(x)[:-1])

def5['2018_x'] = pd.to_numeric(def5['2018_x']) / 100
def5['2018_y'] = pd.to_numeric(def5['2018_y']) / 100

def_tot = pd.merge(def1, def2, how = 'outer', on = 'Team')
def_tot = pd.merge(def_tot, def3, how = 'outer', on = 'Team')
def_tot = pd.merge(def_tot, def4, how = 'outer', on = 'Team')
def_tot = pd.merge(def_tot, def5, how = 'outer', on = 'Team')

frame_1 = pd.merge(frame_1, def_tot, how = 'outer', on = 'Team')

## Rename DataFrame Columns ##
skyhook = ['team','conference','games','winpct_tot','winpct_home','winpct_away',
'points','off_eff','first_half','second_half',
'fastbreak_eff','points_paint','pct_from2','pct_from3',
'shoot','fg_pct','off_reb','def_reb','blocks','steals','def_eff',
'opp_ppg','opp_paint','opp_shootpct','opp_3','opp_2']

frame_1.columns = skyhook

frame_1.sort_values(by = 'winpct_tot', ascending = False, inplace = True)

frame_1.to_excel('NBA_Stats.xlsx')
