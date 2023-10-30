"""
Translates the case names from Chinese to English and saves the dictionary to src/case_dict.json
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os

# Read the data
df = pd.read_csv('main_data.csv')


translated_df = df.copy()
with open("src/case_dict.json", 'r',encoding='utf-8-sig') as f:
        case_dict = json.load(f)
for case in translated_df['case']:
        if case not in case_dict.keys():
            case_dict[case] = input("Enter the english name for " + case  + ": ")
with open('src/case_dict.json', 'w') as f:
        json.dump(case_dict, f)

translated_df['case'] = translated_df['case'].map(case_dict)


print(translated_df)