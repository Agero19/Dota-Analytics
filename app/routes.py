from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

hero_data = requests.get("https://api.opendota.com/api/heroes").json()
hero_id_to_name = {hero['id']: hero['localized_name'] for hero in hero_data}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hero")
def hero_stats():
    # Get the hero name from the query parameter
    hero_name = request.args.get("hero_name")
    
    if not hero_name:
        return "Please enter a hero name.", 400

    # Fetch data from Dota API
    data = requests.get("https://api.opendota.com/api/heroStats").json()
    
    # Find the hero data
    hero_data = next((h for h in data if h['localized_name'].lower() == hero_name.lower()), None)
    
    if not hero_data:
        return f"Hero '{hero_name}' not found.", 404

    return render_template("hero.html", hero=hero_data)

@app.route("/player")
def player_stats():
    # Get the personaname from the query parameter
    personaname = request.args.get("personaname")
    
    if not personaname:
        return "Please enter a player name.", 400

    # Search for the player by personaname
    search_url = f"https://api.opendota.com/api/search?q={personaname}"
    search_results = requests.get(search_url).json()

    if not search_results:
        return f"Player '{personaname}' not found.", 404

    # Use the first result's account_id
    account_id = search_results[0]['account_id']

    # Fetch player data using the account_id
    player_data = requests.get(f"https://api.opendota.com/api/players/{account_id}").json()
    player_matches = requests.get(f"https://api.opendota.com/api/players/{account_id}/matches").json()
    player_wl = requests.get(f"https://api.opendota.com/api/players/{account_id}/wl").json()

    # Calculate top heroes
    df = pd.DataFrame(player_matches)
    top_heroes = df['hero_id'].value_counts().head(5).to_dict()

    # Map hero IDs to hero names
    top_heroes_with_names = {hero_id_to_name.get(hero_id, "Unknown"): count for hero_id, count in top_heroes.items()}

    return render_template("player.html", player=player_data, top_heroes=top_heroes_with_names, wl = player_wl)


if __name__ == "__main__":
    app.run(debug=True)