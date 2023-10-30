"""
Translates the case names from Chinese to English and saves the dictionary to src/case_dict.json
"""
import pandas as pd
import json

def translate(df):
    translated = df.copy()
    with open("case_dict.json", 'r',encoding='utf-8-sig') as f:
            case_dict = json.load(f)
    for case in translated['case']:
            if case not in case_dict.keys():
                case_dict[case] = input("Enter the english name for " + case  + ": ")
    with open('case_dict.json', 'w') as f:
            json.dump(case_dict, f)

    translated['case'] = translated['case'].map(case_dict)


    return translated