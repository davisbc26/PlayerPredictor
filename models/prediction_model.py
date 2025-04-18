from sklearn.ensemble import RandomForestRegressor
import pandas as pd

# Example model for predicting game outcome (win/loss)
def predict_game_outcome(player_stats):
    # Example historical data for training the model
    data = pd.DataFrame({
        'points': [25, 18, 30, 22, 24],
        'assists': [5, 7, 8, 6, 6],
        'rebounds': [10, 12, 8, 9, 11],
        '3_pointers': [2, 1, 4, 3, 2],
        'team_win': [1, 0, 1, 1, 0],  # 1 = win, 0 = loss
    })

    # Features (player stats) and target (game outcome)
    X = data[['points', 'assists', 'rebounds', '3_pointers']]
    y = data['team_win']

    # Train a Random Forest model
    model = RandomForestRegressor()
    model.fit(X, y)

    # Predict game outcome based on the current player's stats
    prediction = model.predict([[
        player_stats['points'],
        player_stats['assists'],
        player_stats['rebounds'],
        player_stats['3_pointers']
    ]])

    return prediction[0]  # 0 = loss, 1 = win