import requests
import pandas as pd
import time
import logging
import logging.handlers


main_df = None


def get_data():
    global main_df
    try:
        main_df = pd.read_csv("main_data.csv")
    except FileNotFoundError:
        print("File not found, creating new file")
        main_df = pd.DataFrame()

    # Get data from API
    try:
        url = "https://www.csgo.com.cn/api/lotteryHistory"
        response = requests.get(url)
        data = response.json()
    except:
        print("ERROR: Could not get data from API")
        return None

    # Create dataframe
    df = pd.json_normalize(data, record_path="result")
    if df.empty:
        return None

    # Drop timestamp and out column, rename src to case
    df = df.drop(["timestamp", "out"], axis=1)
    df = df.rename(columns={"src": "case"})

    return df


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

if __name__ == "__main__":
    df = None
    try:
        df = get_data()
    except df is None:
        logger.info("No data found")
        # wait 5 minutes and execute script again

    # add to main dataframe, drop duplicates
    main_df = pd.concat([main_df, df], ignore_index=True)

    if main_df.duplicated().any():
        logger.info("No new data")
        main_df = main_df.drop_duplicates()
    else:
        logger.info("New data available")

    main_df.to_csv("main_data.csv", index=False)


"""# get data every 1 hour, if new data is available
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Starting at " + time_str)

for i in range(20):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    try:
        df = get_data()
    except df is None:
        print("No data found " + time_str)
        time.sleep(900)
        continue

    # add to main dataframe, drop duplicates
    main_df = pd.concat([main_df, df], ignore_index=True)

    if main_df.duplicated().any():
        print("No new data " + time_str)
        main_df = main_df.drop_duplicates()
    else:
        print("New data available " + time_str)

    main_df.to_csv("main_data.csv", index=False)

    time.sleep(3600)"""
