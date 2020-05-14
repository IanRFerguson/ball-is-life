import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import Series,DataFrame
from scipy import stats
from mpl_toolkits import mplot3d
%matplotlib inline

# Use Excel sheet created in "2018_NBA.py" script in this repository
data = pd.read_excel('~/NBA_Stats.xlsx')
data = data.loc[[0,7]]

# Import Golden State Warriors stats
gsw = pd.read_html('http://www.espn.com/nba/team/stats/_/name/gs')
gsw = gsw[3]

# Import Los Angeles Clippers stats
lac = pd.read_html('http://www.espn.com/nba/team/stats/_/name/lac')
lac = lac[3]

lac.drop(index=[13], columns=['GP','GS'],inplace=True)
gsw.drop(index=[14], columns= ['GP','GS'],inplace=True)

team = DataFrame(['los angeles'] * 13)
lac['team'] = team
lac

lol = DataFrame(['golden state'] * 14)
gsw['team'] = lol

total = pd.concat((lac,gsw))
total.sort_values(by = 'PER', ascending=False,inplace=True)

sns.set_style('dark')
plt.figure(figsize= (10,10))
sns.lmplot(x = 'PER', y = 'PTS', hue = 'team', data = total, height = 7,
           palette = 'Set2_r', aspect = 1, x_bins = 5)
           
plt.figure(figsize= (8,8))
sns.scatterplot(x = total['PER'], y = total['PTS'], hue = total['team'],)
