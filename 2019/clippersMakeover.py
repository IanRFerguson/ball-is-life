import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
%matplotlib inline

from pandas import Series, DataFrame

# /////////////// 2018 Starters //////////////////
# PG - Beverley
bev = pd.read_html('https://www.basketball-reference.com/players/b/beverpa01.html')
bev = bev[0].iloc[[6]]

# SG - Gallinari
gal = pd.read_html('https://www.basketball-reference.com/players/g/gallida01.html')
gal = gal[0].iloc[[12]]

# SF - SGA
sga = pd.read_html('https://www.basketball-reference.com/players/g/gilgesh01.html')
sga = sga[0].iloc[[0]]

# PF - Shamet
sham = pd.read_html('https://www.basketball-reference.com/players/s/shamela01.html')
sham = sham[0].iloc[[2]]

# C - Zubac
zub = pd.read_html('https://www.basketball-reference.com/players/z/zubaciv01.html')
zub = zub[0].iloc[[4]]

clips18 = pd.concat((bev,gal,sga,sham,zub))
clips18.drop(columns = ['Season','Age','Tm','Lg','Pos','G','GS'], inplace=True)
clips18.dropna(inplace=True)

# This fixes the correlation problem for some reason
clips18.to_excel('explore_Clippers2018.xlsx',sheet_name='2018')
clips18_data = pd.read_excel('explore_Clippers.xlsx')
clips18_data = clips18_data.loc[:,['FG%','3P%','FT%','TRB','AST','STL','BLK','PTS']]

LAC18_c = clips18_data.corr()

mask = np.zeros_like(LAC18_c, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Plot Correlations
plt.figure(figsize=(12,10))
sns.heatmap(LAC18_c, mask = mask, linewidths=0.6, 
            cmap='RdBu_r', annot=True)
plt.title('2018 Los Angeles Clippers Starters')
plt.savefig('2018_Clippers')

# /////////////// 2019 Starters //////////////////
# PG - Beverley
bev = pd.read_html('https://www.basketball-reference.com/players/b/beverpa01.html')
bev = bev[0].iloc[[6]]

# SG - Shamet
sham = pd.read_html('https://www.basketball-reference.com/players/s/shamela01.html')
sham = sham[0].iloc[[2]]

# SF - Leonard
fun_guy = pd.read_html('https://www.basketball-reference.com/players/l/leonaka01.html')
fun_guy = fun_guy[0].iloc[[7]]

# PF - George
paul = pd.read_html('https://www.basketball-reference.com/players/g/georgpa01.html')
paul = paul[0].iloc[[8]]

# C - Harrell
mon = pd.read_html('https://www.basketball-reference.com/players/h/harremo01.html')
mon = mon[0].iloc[[3]]

clips19 = pd.concat((bev,sham,fun_guy,paul,mon))

clips19.drop(columns = ['Season','Age','Tm','Lg','Pos','G','GS'], inplace=True)
clips19.dropna(inplace=True)

clips19.to_excel('explore_Clippers2019.xlsx', sheet_name='2019')
clips19_data = pd.read_excel('explore_Clippers2019.xlsx')
clips19_data = clips19_data.loc[:,['FG%','3P%','FT%','TRB','AST','STL','BLK','PTS']]

LAC19_c = clips19_data.corr()

mask = np.zeros_like(LAC19_c, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Plot Correlations
plt.figure(figsize=(12,10))
sns.heatmap(LAC19_c, mask = mask, linewidths=0.6, 
            cmap='RdBu_r', annot=True)
plt.title('2019 Los Angeles Clippers Starters')
plt.savefig('2019_Clippers')
