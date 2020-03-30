import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
from numpy import savetxt
import re
import shutil

sample_plots = [
    'Afghanistan',
    'China-Hubei',
    'Italy',
    'US-NewYork',
    'US-NorthCarolina'
]

def plot(df, region, state, logy=False):
    
    # Remove internal white space because Markdown doesn't like filename with spaces.
    if state:
        state = state.replace(" ", "") 
        title = "{}-{}".format(region, state)
        if logy:
            png_name = "{}-{}-logy.png".format(region, state)
            title = title + " Log Y"
        else:
            png_name = "{}-{}.png".format(region, state)

        filename = os.path.join("./plots/{}".format(png_name))
    else:
        title = "{}".format(region)
        if logy:
            png_name = "{}-logy.png".format(region)
            title = title + " Log Y"
        else:
            png_name = "{}.png".format(region)

        filename = os.path.join("./plots/{}".format(png_name))

    if logy:
        ax = df.plot(logy=True, kind='line',x='Date',y=['ConfirmedCases','Fatalities'],title=title)
    else:
        ax = df.plot(kind='line',x='Date',y=['ConfirmedCases','Fatalities'],title=title)

    try:
        ax.set_xlabel("Date")
        # Display grid
        plt.grid(True, which="both")
        plt.xticks(rotation=70)
        plt.savefig(filename)
        plt.close()
    except Exception as exp:
        print(exp)

    print(png_name)
    if logy:
        if png_name[0:-9] in sample_plots:
            shutil.copyfile(filename,  os.path.join("./samples/{}".format(png_name)))
    else:
        if png_name[0:-4] in sample_plots:
            shutil.copyfile(filename,  os.path.join("./samples/{}".format(png_name)))

def main():
    train = pd.read_csv("./data/train.csv")

    # Clean Ups
    # 1. Transform '"Korea, South"' to 'South Korea'
    # 2. Transform 'Taiwan*' to 'Taiwan'
    train['Country_Region'] = train['Country_Region'].replace('Korea, South', 'South Korea')
    train['Country_Region'] = train['Country_Region'].replace('Taiwan*', 'Taiwan')

    regions = train['Country_Region'].unique()

    regions_df = pd.DataFrame(data=regions, columns=["country_region"])
    filename = os.path.join("./processed_data/regions.csv")
    regions_df.to_csv(filename, header=False, index=False, index_label=False)

    states = train['Province_State'].unique()

    states_tmp = []

    for value in states:
        if type(value)==str:
            if len(value)>0:
                states_tmp.append(value)

    states = states_tmp

    states_df = pd.DataFrame(data=states, columns=["states"])

    filename = os.path.join("./processed_data/states.csv")
    states_df.to_csv(filename, header=False, index=False, index_label=False)

    for index, region in enumerate(regions):
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
            for state in states:
                where2 =  df['Province_State']==state
                df2 = df[where2]
                plot(df2, region, state, logy=False)
                plot(df2, region, state, logy=True)
        else:
            title = "{}".format(region)
            plot(df, region, state=None, logy=False)
            plot(df, region, state=None, logy=True)

if __name__== "__main__":
  main()
