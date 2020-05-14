# Imports
import pandas as pd
import numpy as np
import os

print("*** \tNBA Player Data\t ***\n")

# ------------------------ READING DATA ------------------------ #

# Data from Basketball Reference
stats = ["https://www.basketball-reference.com/leagues/NBA_2014_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2014_advanced.html",
        "https://www.basketball-reference.com/leagues/NBA_2015_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2015_advanced.html",
        "https://www.basketball-reference.com/leagues/NBA_2016_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2016_advanced.html",
        "https://www.basketball-reference.com/leagues/NBA_2017_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2017_advanced.html",
        "https://www.basketball-reference.com/leagues/NBA_2018_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2018_advanced.html",
        "https://www.basketball-reference.com/leagues/NBA_2019_totals.html",
        "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"]

# Split into Total and Advanced statistics
stats_total = []
stats_advanced = []
counter = 2

for frame in stats:

    # TOTALS URLs
    if (counter % 2 == 0):
        stats_total.append(frame)

    # ADVANCED URLs
    elif (counter % 2 != 0):
        stats_advanced.append(frame)

    counter += 1

print("Data split...\n")

# ------------------------ TOTAL x ADVANCED ------------------------ #

print("Reading data from Basketball Reference...\n")

# TOTAL data frame
nba_total = pd.DataFrame()
years = ["2014", "2015", "2016", "2017", "2018", "2019"]
counter = 0

for frame in stats_total:

    temp = (pd.read_html(frame))[0] # Read in data from URL
    temp = temp[temp["Player"] != "Player"] # Remove filler rows
    temp["Year"] = years[counter] # Add in relevant year to each data table (for later comparison)
    counter +=1

    # Push formatted df to bottom of composite data frame
    nba_total = nba_total.append(temp, ignore_index = True)

# ------------------------ #

# ADVANCED data frame
nba_advanced = pd.DataFrame()

for frame in stats_advanced:

    temp = (pd.read_html(frame))[0] # Read in data from URL
    temp = temp[temp["Player"] != "Player"] # Remove filler rows
    newC = [] # Reformatting columns

    # Add 'x' to column names to avoid overwriting
    for x in temp.columns:
        form = x + "x"
        newC.append(form)

    # Replace column names
    temp.columns = newC

    # Push formatted df to bottom of composite data frame
    nba_advanced = nba_advanced.append(temp, ignore_index = True)

print("Data split...\n")

# ------------------------ #

# Join dataframes together!
data = pd.concat([nba_total, nba_advanced], axis = 1, sort = False)

print("Data joined...\n")

# ------------------------ MR. CLEAN ------------------------ #

# Drop useless + duplicate columns
badVars = ["Rkx", "Playerx", "Posx", "Agex", "Tmx", "Gx", "MPx"]

for stat in data.columns:
    if "Unnamed" in stat:
        data.drop(stat, axis=1, inplace=True)

    elif stat in badVars:
        data.drop(stat, axis=1, inplace=True)

    else:
        continue

# Reformat all column datas (remove placeholder "x" vals)
newColumns = []

for k in range(len(data.columns)):
    stat = data.columns[k]

    # Variable contains 'x' placeholder
    if (stat[-1] == "x"):
        clean = stat[:-1]
        newColumns.append(clean)

    else:
        newColumns.append(stat)

# Update dataframe columns
data.columns = newColumns

# Convert variables to numeric when applicable
for stat in data.columns:
    try:
        data[stat] = pd.to_numeric(data[stat])

    except:
        continue

print("Data cleaned...\n")

# Push to CSV in its own directory
here = os.getcwd()

try:
    os.chdir(here + "/PLAYER STATS/")

except:
    os.mkdir("PLAYER STATS")
    os.chdir(here + "/PLAYER STATS/")

data.to_csv("NBA_Player_Statistics.csv", index=False)

print("Success! " + str(data["Player"].nunique()) + " players' data logged")
