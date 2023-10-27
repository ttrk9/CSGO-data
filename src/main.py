import os
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time


main_df = None

def get_data():
    global main_df
    try:
         main_df = pd.read_csv('main_data.csv')
    except FileNotFoundError:
        print("File not found, creating new file")
        main_df = pd.DataFrame() 
 
    # Get data from API
    url = "https://www.csgo.com.cn/api/lotteryHistory"
    response = requests.get(url)
    data = response.json()

    # Create dataframe
    df = pd.json_normalize(data, record_path="result")

    # Drop timestamp and out column, rename src to case
    df = df.drop(["timestamp", "out"], axis=1)
    df = df.rename(columns={"src": "case"})

    return df

# get data every 30 minutes, if new data is available
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Starting at " + time_str)

for i in range(20):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    df = get_data()

    # add to main dataframe, drop duplicates
    main_df = pd.concat([main_df, df], ignore_index=True)

    if(main_df.duplicated().any()):
        print("No new data " + time_str)
        main_df = main_df.drop_duplicates()
    else:
        print("New data available at " + time_str)

    main_df.to_csv('main_data.csv', index=False)

    time.sleep(1800)
