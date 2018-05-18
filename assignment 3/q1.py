import numpy as np
import pandas as pd

###############
# question one
###############

# load excel file
energy = pd.read_excel('Energy Indicators.xls')

#drop header and footer
energy = energy.loc[16:242, :]

# drop unnecessary columns
energy.drop(energy.iloc[:, 0:2], axis=1, inplace=True)

# rename columns
names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy.columns = names

# convert to gigajoules
energy['Energy Supply'] *= 1000000

# rename certain rows
countries = {
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
}
energy['Country'] = energy['Country'].replace(countries, regex=True)

# remove numbers
energy['Country'] = energy['Country'].str.replace('\d+', '')

# remove text in parentheses
energy['Country'] = energy['Country'].replace(" +\(.*\)", '', regex=True)

# load gdp file
GDP = pd.read_csv('world_bank.csv', skiprows=4)

# rename countries
countries2 = {
    "Korea, Rep.": "South Korea",
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
}
GDP['Country Name'] = GDP['Country Name'].replace(countries2, regex=True)

# load journal contribution file
ScimEn = pd.read_excel('scimagojr-3.xlsx')

# remove unused columns
GDP = GDP[[
    'Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
    '2013', '2014', '2015'
]]

# take top 15 rows
ScimEn_m = ScimEn[:15]

# merge dataframes
merged = pd.merge(energy, GDP, left_on='Country', right_on='Country Name')
merged1 = merged
merged = pd.merge(ScimEn, merged, left_on='Country', right_on='Country')
merged2 = merged
# only keep top 15 countries
merged = merged[:15]

# set index to country name
merged = merged.set_index('Country')

# print(energy['Country'].sort_values()[80:150])
print(merged)