import pandas as pd
import numpy as np

import json

with open("icon_translation.json") as f:
    icon_translation = json.load(f)

def write_streaks(request):
    with open("data/streaks.csv", "w") as f:
	    f.write(request["streaks_csv"])

    return True

def read_streaks():
    df = pd.read_csv("data/streaks.csv", header=0, parse_dates=[4], index_col=4, na_values=[-1], sep=",")
    df = df.drop(["quantity", "page"], axis=1)

    return df

def get_tasks(date):
    return read_streaks().loc[date].drop_duplicates(subset='task_id', keep="last")

def get_tasks_json(date):
    res = []

    snippet = get_tasks(date)
    for index, row in snippet.iterrows():
        res_obj = {}
        res_obj["title"] = row["title"]
        if(row["icon"] in icon_translation):
            res_obj["icon"] = icon_translation[row["icon"]]
        else:
            res_obj["icon"] = icon_translation["none"]
        res_obj["entry_timestamp"] = row["entry_timestamp"]

        if("missed" in row["entry_type"]):
            res_obj["entry_type"] = 0
        else:
            res_obj["entry_type"] = 1
        res.append(res_obj)

    return res