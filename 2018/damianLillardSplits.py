import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import Series,DataFrame
from scipy import stats
from mpl_toolkits import mplot3d
%matplotlib inline

# /////////////// PORTLAND WITH DAME //////////////////
portland = pd.read_html('http://www.espn.com/nba/team/stats/_/name/por')
portland = portland[3]
portland.drop(index = [13],columns= ['GP','GS'], inplace=True)
blaze = portland.corr()

mask = np.zeros_like(blaze, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

plt.figure(figsize = (10,8))
sns.heatmap(blaze, mask=mask, linewidths=0.5, cmap= 'RdBu_r',
            annot = True)
plt.title('Portland With Damian Lillard')
plt.savefig('Blazers_Wit')

# /////////////// PORTLAND WITHOUT DAME /////////////////
oregon = portland
oregon.drop(index=[0], inplace= True)
beaver = oregon.corr()

mask = np.zeros_like(beaver, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

plt.figure(figsize = (10,8))
sns.heatmap(beaver, mask=mask, linewidths=0.5, cmap= 'RdBu_r',
            annot = True)
plt.title('Portland Without Damian Lillard')
plt.savefig('Blazer_Wittout')
