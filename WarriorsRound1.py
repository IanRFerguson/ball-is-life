import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pandas import Series,DataFrame
from scipy import stats

%matplotlib inline

# Let's talk Warriors / Spurs

gsw = pd.read_html('https://sports.yahoo.com/nba/teams/golden-state/stats/')
gsw = gsw[0]

sas = pd.read_html('https://sports.yahoo.com/nba/teams/san-antonio/stats/')
sas = sas[0]

sns.set_style('white')
plt.figure(figsize= (20,20))
fig, axes = plt.subplots(1,2, sharey= False)

warriors = sns.stripplot(x = gsw['FG%'], y = gsw['Pts'],
              orient = 'h', size = 10, palette = 'Blues', ax = axes[0],
                        jitter = True)
warriors.set_xlabel('Golden State Warriors FG%')
warriors.set_ylabel('Player PPG')
warriors.invert_yaxis()


spurs = sns.stripplot(x = sas['FG%'], y = sas['Pts'],
                      orient = 'h', size = 10, palette = 'Reds', ax = axes[1],
                      jitter = True)
spurs.set_xlabel('San Antonio Spurs FG%')
spurs.set_ylabel('Player PPG')
spurs.invert_yaxis()

fig.subplots_adjust(wspace = 0.6)
