from flask import Flask, request, render_template

import pandas as pd
import numpy as np

df = 0

def read_csv():
    global df
    df = pd.read_csv("data/streaks.csv", header=0, parse_dates=[4], index_col=4, na_values=[-1], sep=",")
    df = df.drop(["quantity", "page"], axis=1)

def get_tasks(date):
    return df.loc[date].drop_duplicates(subset='task_id', keep="last")

icon_translation = {
    "none": "fas fa-times",
    "ic_biceps": "fas fa-running",
    "ic_broom": "fa-solid fa-broom",
    "ic_code": "fas fa-terminal"
}

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

app = Flask(__name__)

key = "MTIzNGFzZGYxMjM0Cg"

@app.route("/streaks", methods=["POST"])
def import_streak_csv():
    auth_key = request.args.get('key')
    if(auth_key != key):
        return {401: "unauthorized"}

    args = request.data
    print(args)
    with open("data/streaks.csv", "w") as f:
	    f.write(request.get_json()["streaks_csv"])
    read_csv()
    return render_template('streaks.html', name=args)

@app.route("/api/streaks-day/<date>")
def api_get_streaks_from_day(date):
    auth_key = request.args.get('key')
    if(auth_key != key):
        return {401: "unauthorized"}
    try:
        res = get_tasks_json(date)
    except:
        return {500: "server error"}
    return res

@app.route("/streaks-day/<date>")
def get_streaks_from_day(date):
    auth_key = request.args.get('key')
    if(auth_key != key):
        return {401: "unauthorized"}
    try:
        res = get_tasks_json(date)
    except:
        res = [{
            "title": "Unable to Load Streaks",
            "icon": icon_translation["none"],
            "entry_type": 0
        }]
    return render_template('streaks.html', res=res)


app.run(host="0.0.0.0", port=4000)