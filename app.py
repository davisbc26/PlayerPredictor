from flask import Flask, jsonify, request
from flask_cors import CORS  # To handle CORS errors between React and Python
from crawler.webcrawler import get_search_results, extract_stats_from_url, get_player_stats # Import function from the crawler package (via __init__.py)
from crawler.clean import process_player_data, clean_and_save_stats
import json
import io
import csv



app = Flask(__name__)
CORS(app)  # Allow all origins to communicate with the API

@app.route('/api/search', methods=['GET']) #GET vs POST: Look at docs for detail. Get better for retrieving data
def get_stats():

    player = request.args.get("player")
    team = request.args.get("team")
    keywords = request.args.getList("keywords")  #instead of keywords, we use stat_specifier to expect an array of keywords instead of just a single stat specifier (like "3PT Percentage").

    if not player or not team or not keywords:
        return jsonify({"error": "Missing required fields: player, team, keywords"}), 400

     # Get search results (URLs)
    search_results = get_search_results(player, team)

    # Initialize results list
    results = []
    
    # Loop through URLs and extract stats based on keywords
    for url in search_results:
        stats = extract_stats_from_url(url, keywords)
        if stats:
            results.append({
                "url": url,
                "player": player,
                "team": team,
                "stats": stats
            })
 # Create CSV output
    if results:
        return generate_csv_response(results)
    else:
        return jsonify({"error": "No data found"}), 404

def generate_csv_response(results):
    # Create a StringIO object to hold CSV data in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["url", "player", "team", "stats"])
    
    # Write the header
    writer.writeheader()

    # Write data rows
    for result in results:
        # Flatten the stats dict for CSV format
        result_row = {
            "url": result["url"],
            "player": result["player"],
            "team": result["team"],
            "stats": json.dumps(result["stats"])  # Save stats as a JSON string for easy parsing
        }
        writer.writerow(result_row)

    # Move to the beginning of the StringIO buffer
    output.seek(0)

    # Return the CSV data as a response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=player_stats.csv"}
    )
    return jsonify(results)

# Route to predict game outcome based on player stats
@app.route('/predict_game', methods=['POST'])
def predict():
    # Get player stats from the POST request's JSON body
    data = request.get_json()
    
    if 'player_stats' not in data:
        return jsonify({'error': 'player_stats missing from request'}), 400

    player_stats = data['player_stats']
    
    # Call the prediction model to predict the game outcome
    try:
        prediction = predict_game_outcome(player_stats)  # Call function from models
        return jsonify({'prediction': prediction}), 200  # Return prediction (Win/Loss)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Error handling
    
if __name__ == '__main__':
    app.run(port=5000)  # Flask app will run on http://localhost:5000

