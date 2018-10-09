import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib
import plotly.plotly as py
import plotly.graph_objs as go

#loading the dataset
data = pd.read_csv('afg_pop.csv', thousands=',')

#inspecting the dataset
data.head(10)
data.describe()
data.info()
data.shape

#cleaning the dataset
data.drop(['Unnamed: 11', 'Unnamed: 12'], axis=1, inplace=True)
data.drop(['1'], axis=1, inplace=True)
data = data[data.TOTAL.notnull()]

#renaming columns
data.columns
data.columns = ['Province', 'Total', 'Male', 'Female',
                'Urban', 'Urban_Male', 'Urban_Female',
                'Rural', 'Rural_Male', 'Rural_Female']

#Changing column dtypes and replacing the comma
#data = data.iloc[:, 1:10].str.replace(',', '').astype('int64')
data.loc[data.isnull().any(axis=1), :]
data.isnull().any(axis=1)
#missing values
missing = data.isnull().sum()
missing = missing[missing > 0]
print(missing)

#dropping rows with missing values
data.dropna(axis=0, inplace=True)

#mean and total and shit
totals = pd.DataFrame({
        'totals': ['Total', 'Total Male', 'Total Female',
                  'Total Urban', 'Total Rural'],\
          'sums': [data.Total.sum(), data.Male.sum(),
                   data.Female.sum(), data.Urban.sum(),
                   data.Rural.sum()]
          })

#bar plotting
f, ax = plt.subplots(figsize = (12, 10))
sns.set(style='whitegrid', font_scale = 1.5)
sns.barplot(x='totals', y='sums', data=totals, palette='colorblind')
plt.xlabel('Categories', fontsize=20, fontweight='bold', labelpad=15) 
plt.ylabel('Sums', fontsize=20, fontweight='bold', labelpad=15)
plt.title('Population Totals', fontsize=30, fontweight='bold')

#genders in provinces
genders = data.loc[:, ['Province', 'Male', 'Female']]

genders = (
        genders.set_index('Province')
            .stack()
            .reset_index()
            .rename(columns={'level_1': 'Variable', 0: 'Sums'})
        )
sns.barplot(x='Province', y='Sums', hue='Variable', data=genders)
plt.xlabel('Province', fontsize=20, fontweight='bold', labelpad=15)
plt.ylabel('Sums', fontsize=20, fontweight='bold', labelpad=15)
plt.xticks(rotation=90)
legend = plt.legend(frameon=True, fancybox=True, 
                    framealpha=1, shadow=True, borderpad=1,
                    fontsize='large')
legend.get_frame().set_facecolor('lightgrey')

#rural vs. urban population
rural_urban = data.loc[:, ['Province', 'Male', 'Female']]

rural_urban = (
        rural_urban.set_index('Province')
            .stack()
            .reset_index()
            .rename(columns={'level_1': 'Variable', 0: 'Sums'})
        )
sns.barplot(x='Province', y='Sums', hue='Variable', data=rural_urban)
plt.xlabel('Province', fontsize=20, fontweight='bold', labelpad=15)
plt.ylabel('Sums', fontsize=20, fontweight='bold', labelpad=15)
plt.xticks(rotation=90)
legend = plt.legend(frameon=True, fancybox=True, 
                    framealpha=1, shadow=True, borderpad=1,
                    fontsize='large')
legend.get_frame().set_facecolor('lightgrey')

#on a map
import geopandas as gpd

mapdf = gpd.read_file('admin2_poly_32.shp')
mapdf.plot() ; plt.show()

#change to lowercase with the exception of first letter
mapdf['PRV_NAME'] = mapdf.PRV_NAME.str.title()

#replace names to match
replacements = {
        'PRV_NAME':{
                'Hilmand':'Helmand',
                'Hirat':'Herat',
                'Kunar': 'Kunarha',
                'Nuristan':'Nooristan',
                'Sari Pul':'Sar-e-pul',
                'Uruzgan':'Urozgan'}
        }

mapdf = mapdf.replace(replacements)

#import the pops dataset again and do the cleaning to match with mapdf
data = pd.read_csv('afg_pop.csv', thousands=',')
data.drop(['Unnamed: 11', 'Unnamed: 12'], axis=1, inplace=True)
data.drop(['1'], axis=1, inplace=True)
data = data[data.TOTAL.notnull()]
data.columns = ['Province', 'Total', 'Male', 'Female',
                'Urban', 'Urban_Male', 'Urban_Female',
                'Rural', 'Rural_Male', 'Rural_Female']
#drop the two extra provinces
data = data[(data.Province != 'Daykundi') & (data.Province != 'Panjsher')]

#join the mapdf with pops dataframe
choropleth_df = mapdf.set_index('PRV_NAME').join(data.set_index('Province'))

#plot the choropleth
fig, ax = plt.subplots(1)
hello.plot(column='Total', ax=ax, cmap='Blues', linewidth=0.8, edgecolor='0.8') ; plt.show(1)
ax.axis('off')
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=0, vmax=100))
sm._A = []
cbar = fig.colorbar(sm)
