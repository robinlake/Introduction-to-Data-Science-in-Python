import numpy as np
import pandas as pd

# load excel file
df = pd.read_excel('Energy Indicators.xls')

#drop header and footer
df = df.loc[16:242, :]

# drop unnecessary columns
df.drop(df.iloc[:, 0:2], axis=1, inplace=True)

# rename columns
names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
df.columns = names

# convert to gigajoules
df['Energy Supply'] *= 1000000

# rename certain rows
countries = {
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
}

# remove numbers
df['Country'] = df['Country'].str.replace('\d+', '')

# remove text in parentheses
df['Country'] = df['Country'].replace("\(.+\)", '', regex=True)

df.rename(index=countries)

print(df.loc[230:, :])