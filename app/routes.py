from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hero/<hero_name>")
def hero_stats(hero_name):
    # Fetch data from Dota API
    data = requests.get(f"https://api.opendota.com/api/heroStats").json()
    hero_data = next(h for h in data if h['localized_name'] == hero_name)
    return render_template("hero.html", hero=hero_data)

if __name__ == "__main__":
    app.run(debug=True)