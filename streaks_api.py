from flask import Flask, request, render_template
from middleware import authorize_request
from handler import write_streaks, read_streaks, get_tasks_json, icon_translation

import random

app = Flask(__name__)
app.before_request(authorize_request)

@app.route("/streaks", methods=["POST"])
def import_streak_csv():
    write_streaks(request.get_json())

    return {200: "success"}

@app.route("/api/streaks-day/<date>")
def api_get_streaks_from_day(date):
    try:
        res = get_tasks_json(date)
    except:
        return {500: "server error"}
    return res

@app.route("/streaks-day/<date>")
def get_streaks_from_day(date):
    try:
        res = get_tasks_json(date)
    except:
        res = [{
            "title": "Unable to Load Streaks",
            "icon": icon_translation["none"],
            "entry_type": 0
        }]

    supported_themes = ['orange', 'pink', 'yellow', 'purple', 'green', 'hotpink', 'blue', 'red', 'lightgreen', 'cyan', 'darkred', 'brown', 'navy', 'darkgreen', 'gray', 'darkgray']
    theme = 'orange'
    if("theme" in request.args):
        theme = request.args["theme"]
        if(theme == "random"):
            theme = random.choice(supported_themes)

    return render_template('streaks.html', tasks=res, theme=theme)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)