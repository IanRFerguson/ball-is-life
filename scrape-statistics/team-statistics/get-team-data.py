# ------------------ Imports
import pandas as pd
import xlsxwriter
from tqdm import tqdm
from time import sleep

# ------------------ Set up base DataFrame
west = ['Golden State', 'Denver', 'Houston', 'Portland', 'Okla City', 'San Antonio', 'Utah', 'LA Clippers',
        'Sacramento', 'Minnesota', 'LA Lakers', 'New Orleans', 'Memphis', 'Dallas', 'Phoenix']

east = ['Milwaukee', 'Toronto', 'Indiana', 'Philadelphia', 'Boston', 'Detroit', 'Brooklyn', 'Miami', 'Orlando',
        'Charlotte', 'Washington', 'Atlanta', 'Chicago', 'Cleveland', 'New York']

conf = west + east
confw = ['West'] * 15
confe = ['East'] * 15
conf_all = confw + confe

base = pd.DataFrame({'Team': conf, 'conf': conf_all})

# ------------------ Propogate Team Data
stat_bank = ['https://www.teamrankings.com/nba/stat/games-played', 'https://www.teamrankings.com/nba/stat/win-pct-all-games',
             'https://www.teamrankings.com/nba/stat/points-per-game', 'https://www.teamrankings.com/nba/stat/offensive-efficiency',
             'https://www.teamrankings.com/nba/stat/1st-half-points-per-game', 'https://www.teamrankings.com/nba/stat/2nd-half-points-per-game',
             'https://www.teamrankings.com/nba/stat/fastbreak-efficiency', 'https://www.teamrankings.com/nba/stat/points-in-paint-per-game',
             'https://www.teamrankings.com/nba/stat/percent-of-points-from-2-pointers', 'https://www.teamrankings.com/nba/stat/percent-of-points-from-3-pointers',
             'https://www.teamrankings.com/nba/stat/shooting-pct', 'https://www.teamrankings.com/nba/stat/effective-field-goal-pct',
             'https://www.teamrankings.com/nba/stat/offensive-rebounds-per-game', 'https://www.teamrankings.com/nba/stat/defensive-rebounds-per-game',
             'https://www.teamrankings.com/nba/stat/blocks-per-game', 'https://www.teamrankings.com/nba/stat/steals-per-game',
             'https://www.teamrankings.com/nba/stat/defensive-efficiency', 'https://www.teamrankings.com/nba/stat/opponent-points-per-game',
             'https://www.teamrankings.com/nba/stat/opponent-points-in-paint-per-game', 'https://www.teamrankings.com/nba/stat/opponent-shooting-pct',
             'https://www.teamrankings.com/nba/stat/opponent-three-point-pct', 'https://www.teamrankings.com/nba/stat/opponent-two-point-pct']

print('Reading in team stats...')
for stat in tqdm(stat_bank):
    target_name = stat.split("/")[-1]                                           # Tail of URL == Relevant statistic
    temp = (pd.read_html(stat))[0].loc[:,['Team', '2019']]                      # Read in URL data with Pandas
    temp.rename(columns={'2019':target_name}, inplace=True)                     # Convert trailing column name to relevant statistic
    base = pd.merge(base, temp, on="Team", how="outer")                         # Append column to base DataFrame

base.sort_values(by='win-pct-all-games', ascending=False, inplace=True)         # Sort DF by most- to least-winning team

# ------------------ Clean Data
headers = []
convert2pct = []

print("Parsing data types...")
for var in tqdm(base.columns):
    matches = ["percent", "per"]
    if any(x in var for x in matches):                                          # Isolate % variables (e.g., shooting percentage)
        convert2pct.append(var)

    pattern = {'header': var}                                                   # Convert all column names to XLSX headers
    headers.append(pattern)
    sleep(0.25)

print("Converting percentage variables...")
for stat in tqdm(convert2pct):
    base[stat] = base[stat].map(lambda x: str(x)[:-1])                          # Strip '%' from percentage columns
    base[stat] = pd.to_numeric(base[stat]) / 100                                # Convert percentage columns to numeric and divide values by 100
    sleep(0.25)

# ------------------ Export to XLSX
cornerThree = xlsxwriter.Workbook('NBA_Stats_2019.xlsx')                        # Instantiate Excel workbook
statSheet = cornerThree.add_worksheet('Team Statistics')                        # Add worksheet to workbook
statSheet.set_column('A:X', 16)                                                 # Set column width
statSheet.add_table('A1:X31', {'data': base.stack(), 'columns':headers})        # Push base DataFrame to Excel workbook
cornerThree.close()                                                             # You're all done!
sleep(1)
print("\nAll NBA Team data has been parsed")
