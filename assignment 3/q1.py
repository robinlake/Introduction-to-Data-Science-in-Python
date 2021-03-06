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
merged = pd.merge(ScimEn, merged, left_on='Country', right_on='Country')
merged2 = merged  # for use in second question
# only keep top 15 countries
merged = merged[:15]

# set index to country name
merged = merged.set_index('Country')

# test if pandas is displaying correct information
# print(merged)

###############
# question two
###############

# takes the count of the largest data set (found by examining all three with shape)
# and subtracting the the count of the merged data set
# print(GDP.shape[0] - merged2.shape[0])

################
# question three
################

# add avgGDP to initial dataframe
merged['avgGDP'] = merged[[
    '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
    '2015'
]].mean(axis=1)

# create sorted avgGDP series
avgGDP = merged['avgGDP'].sort_values(ascending=False)

# print(avgGDP[:])

################
# question four
################

# find country with sixth highest average gdp
gdp6 = merged.sort_values(by=['avgGDP'], ascending=False)
gdp6 = gdp6[5:6]

# get gdp for selected years
gdpYears = gdp6[[
    '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
    '2015'
]]

# find difference between max and min values
change = gdpYears.max(axis=1) - gdpYears.min(axis=1)

# print(change[0])

################
# question five
################

# get the mean per capita energy supply
meanSupply = merged.loc[:, 'Energy Supply per Capita'].mean()

# print(meanSupply)

################
# question six
################

renewable = merged.loc[:, '% Renewable']

# print(renewable.max())

################
# question seven
################

# create self citations to total citations ratio
merged['self/cite'] = merged['Self-citations'] / merged['Citations']

highest = merged.sort_values(by="self/cite", ascending=False)
highest = highest.iloc[0]
country = highest['Country Name']
cite = highest['self/cite']
answer = [country, cite]
# highest = highest.loc[['Country', 'self/cite']]
print(answer)