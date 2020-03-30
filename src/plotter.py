import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
from numpy import savetxt



train = pd.read_csv("./data/train.csv")

# Clean Ups
# 1. Transform '"Korea, South"' to 'South Korea'

# 2. Transform 'Taiwan*' to 'Taiwan'

#train.Country_Region = train.Country_Region.replace({'"Korea, South"': 'South Korea'})
#train.Country_Region = train.Country_Region.replace({'Taiwan*': 'Taiwan'})
train['Country_Region'] = train['Country_Region'].replace('Korea, South', 'South Korea')
train['Country_Region'] = train['Country_Region'].replace('Taiwan*', 'Taiwan')

regions = train['Country_Region'].unique()

#train.columns
#Index(['Id', 'Province_State', 'Country_Region', 'Date', 'ConfirmedCases','Fatalities'], dtype='object')
#List unique values in the train['Country_Region'] column

regions_df = pd.DataFrame(data=regions, columns=["country_region"])
filename = os.path.join("./processed_data/regions.csv")
regions_df.to_csv(filename, header=False, index=False, index_label=False)

states = train['Province_State'].unique()
#print(states[0])
#print(states.index(np.nan))
#print(states[np.isnan(states)])

#print(type(states))
#print(states[0])

# Filter nan

# array([nan, 'Australian Capital Territory', 'New South Wales',
#        'Northern Territory', 'Queensland', 'South Australia', 'Tasmania',
#        'Victoria', 'Western Australia', 'Alberta', 'British Columbia',
#        'Manitoba', 'New Brunswick', 'Newfoundland and Labrador',
#        'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec',
#        'Saskatchewan', 'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu',
#        'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei',
#        'Heilongjiang', 'Henan', 'Hong Kong', 'Hubei', 'Hunan',
#        'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning',
#        'Macau', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai',
#        'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Yunnan',
#        'Zhejiang', 'Faroe Islands', 'Greenland', 'French Guiana',
#        'French Polynesia', 'Guadeloupe', 'Martinique', 'Mayotte',
#        'New Caledonia', 'Reunion', 'Saint Barthelemy', 'St Martin',
#        'Aruba', 'Curacao', 'Sint Maarten', 'Alabama', 'Alaska', 'Arizona',
#        'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
#        'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii',
#        'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
#        'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
#        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
#        'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
#        'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
#        'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
#        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
#        'Virgin Islands', 'Virginia', 'Washington', 'West Virginia',
#        'Wisconsin', 'Wyoming', 'Bermuda', 'Cayman Islands',
#        'Channel Islands', 'Gibraltar', 'Isle of Man', 'Montserrat'],
#       dtype=object)

states_tmp = []

for value in states:
    if type(value)==str:
        if len(value)>0:
            states_tmp.append(value)

states = states_tmp

states_df = pd.DataFrame(data=states, columns=["states"])

filename = os.path.join("./processed_data/states.csv")
states_df.to_csv(filename, header=False, index=False, index_label=False)

# result = np.where(states == np.nan)
# print('result : ', result)
# result = states[np.isnan(states)]
# print('result : ', result)

# result = np.where(states == 'Australian Capital Territory')
# print('result : ', result)
# for item in result:
#     print(item[0], states[item[0]])

#result = numpy.where(states == "")
#print('result : ', result)

# type(train['Country_Region'])
#number_of_regions = len(regions)
#train.plot(kind='scatter',x='Date',y='ConfirmedCases',color='red')
#plt.show()


for index, region in enumerate(regions):
    print(index, region)

    where =  train['Country_Region']==region
    
    df = train[where]
    states = df['Province_State'].unique()

    states_tmp = []

    for value in states:
        if type(value)==str:
            if len(value)>0:
                states_tmp.append(value)

    states = states_tmp

    if len(states)>0:
        #print(states)
        #states_df = pd.DataFrame(data=states, columns=["states"])
        for state in states:
            print(state)
            where2 =  df['Province_State']==state
            df2 = df[where2]
            print(df2.head(3))
            
            df2.plot(kind='scatter',x='Date',y='ConfirmedCases',color='red')
            try:
                filename = os.path.join("./plots/{}-{}.png".format(region, state))
                print(filename)
                plt.savefig(filename)
                plt.close()
            except Exception as exp:
                print(exp)

        #sys.exit()
    else:
        continue
        #print(df.head(3))

        df.plot(kind='scatter',x='Date',y='ConfirmedCases',color='red')
        #plt.show()
        try:
            filename = os.path.join("./plots/{}.png".format(region))
            plt.savefig(filename)
            plt.close()
        except Exception as exp:
            print(exp)

