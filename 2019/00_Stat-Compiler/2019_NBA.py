import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import xlsxwriter
import time


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

# Team Stats
games_played = (pd.read_html('https://www.teamrankings.com/nba/stat/games-played'))[0].loc[:,['Team','2019']]
win_per = (pd.read_html('https://www.teamrankings.com/nba/stat/win-pct-all-games'))[0].loc[:,['Team','2019']]
points_per = (pd.read_html('https://www.teamrankings.com/nba/stat/points-per-game'))[0].loc[:,['Team','2019']]
off_eff = (pd.read_html('https://www.teamrankings.com/nba/stat/offensive-efficiency'))[0].loc[:,['Team','2019']]
first_half = (pd.read_html('https://www.teamrankings.com/nba/stat/1st-half-points-per-game'))[0].loc[:,['Team','2019']]
second_half = (pd.read_html('https://www.teamrankings.com/nba/stat/2nd-half-points-per-game'))[0].loc[:,['Team','2019']]
fastbreak = (pd.read_html('https://www.teamrankings.com/nba/stat/fastbreak-efficiency'))[0].loc[:,['Team','2019']]
paint = (pd.read_html('https://www.teamrankings.com/nba/stat/points-in-paint-per-game'))[0].loc[:,['Team','2019']]
pctfrm2 = (pd.read_html('https://www.teamrankings.com/nba/stat/percent-of-points-from-2-pointers'))[0].loc[:,['Team','2019']]
pctfrm3 = (pd.read_html('https://www.teamrankings.com/nba/stat/percent-of-points-from-3-pointers'))[0].loc[:,['Team','2019']]
shtpct = (pd.read_html('https://www.teamrankings.com/nba/stat/shooting-pct'))[0].loc[:,['Team','2019']]
efffgpct = (pd.read_html('https://www.teamrankings.com/nba/stat/effective-field-goal-pct'))[0].loc[:,['Team','2019']]
off_reb = (pd.read_html('https://www.teamrankings.com/nba/stat/offensive-rebounds-per-game'))[0].loc[:,['Team','2019']]
def_reb = (pd.read_html('https://www.teamrankings.com/nba/stat/defensive-rebounds-per-game'))[0].loc[:,['Team','2019']]
block = (pd.read_html('https://www.teamrankings.com/nba/stat/blocks-per-game'))[0].loc[:,['Team','2019']]
steal = (pd.read_html('https://www.teamrankings.com/nba/stat/steals-per-game'))[0].loc[:,['Team','2019']]
dvoa = (pd.read_html('https://www.teamrankings.com/nba/stat/defensive-efficiency'))[0].loc[:,['Team','2019']]
opp_ppg = (pd.read_html('https://www.teamrankings.com/nba/stat/opponent-points-per-game'))[0].loc[:,['Team','2019']]
opp_paint = (pd.read_html('https://www.teamrankings.com/nba/stat/opponent-points-in-paint-per-game'))[0].loc[:,['Team','2019']]
opp_shoot = (pd.read_html('https://www.teamrankings.com/nba/stat/opponent-shooting-pct'))[0].loc[:,['Team','2019']]
opp_3 = (pd.read_html('https://www.teamrankings.com/nba/stat/opponent-three-point-pct'))[0].loc[:,['Team','2019']]
opp_2 = (pd.read_html('https://www.teamrankings.com/nba/stat/opponent-two-point-pct'))[0].loc[:,['Team','2019']]

allStats = [games_played, win_per, points_per, off_eff, first_half, second_half, fastbreak, paint, pctfrm2, pctfrm3,
            shtpct, efffgpct, off_reb, def_reb, block, steal, dvoa, opp_ppg, opp_paint, opp_shoot, opp_3, opp_2]

for stat in allStats:

    base = pd.merge(base, stat, on = 'Team', how = 'outer')


skyhook = ['team','conference','games','winpct_tot',
'points','off_eff','first_half','second_half',
'fastbreak_eff','points_paint','pct_from2','pct_from3',
'shoot','fg_pct','off_reb','def_reb','blocks','steals','def_eff',
'opp_ppg','opp_paint','opp_shootpct','opp_3','opp_2']

base.columns = skyhook

base.sort_values(by = 'winpct_tot', ascending = False, inplace = True)

convertPct = ['pct_from2','pct_from3','shoot','fg_pct','opp_shootpct','opp_3','opp_2']

for stat in convertPct:

    base[stat] = base[stat].map(lambda x: str(x)[:-1])
    base[stat] = pd.to_numeric(base[stat]) / 100

headers = []

for var in skyhook:
    pattern = {'header':var}
    headers.append(pattern)

cornerThree = xlsxwriter.Workbook('NBA_Stats_2019.xlsx')
statSheet = cornerThree.add_worksheet('Team Statistics')
statSheet.set_column('A:X', 14)
statSheet.add_table('A1:X31', {'data': base.stack(), 'columns':headers})

cornerThree.close()
