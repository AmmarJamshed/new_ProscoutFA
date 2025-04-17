import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Add custom CSS for styling (FIFA-colored theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f0f0f;  /* FIFA dark background */
        color: #e5e5e5;
    }
    .stButton>button {
        background-color: #f9a826; /* FIFA yellow */
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #f79013;
    }
    .stMarkdown {
        font-size: 18px;
        font-weight: bold;
    }
    .stSelectbox, .stSlider, .stRadio, .stTextInput {
        background-color: #262626;
        color: #e5e5e5;
    }
    .stSelectbox>div>div {
        background-color: #262626;
    }
    .stTextInput>div>div {
        background-color: #262626;
    }
    .player-card {
        background-color: #1c1c1c;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        padding: 20px;
        margin-bottom: 20px;
        max-width: 300px;
        display: inline-block;
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #e5e5e5;
    }
    .player-card h2 {
        font-size: 22px;
        color: #f9a826; /* FIFA yellow */
        margin-bottom: 10px;
    }
    .player-card .position {
        font-size: 16px;
        color: #f9a826; /* FIFA yellow */
    }
    .player-card .market-value {
        font-size: 18px;
        color: #4caf50; /* Green for market value */
        margin-top: 10px;
    }
    .player-card .age {
        font-size: 14px;
        color: #888;
    }
    .player-card .card-footer {
        margin-top: 15px;
        font-size: 14px;
        color: #f9a826; /* FIFA yellow */
    }
    .player-card .transfer-chance {
        font-size: 14px;
        color: #ff5722; /* Red for transfer chance */
    }
    .ksa-flag {
        display: block;
        margin: 0 auto 20px;
        width: 100px;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Updated list of 25 Saudi players data without avatar URLs
players_data = [
    {"name": "Cristiano Ronaldo", "club": "Al Nassr", "position": "Forward", "market_value": 50000000, "age": 38},
    {"name": "Karim Benzema", "club": "Al-Ittihad", "position": "Forward", "market_value": 30000000, "age": 35},
    {"name": "Neymar Jr.", "club": "Al Hilal", "position": "Forward", "market_value": 45000000, "age": 31},
    {"name": "Sadio Mane", "club": "Al Nassr", "position": "Forward", "market_value": 70000000, "age": 31},
    {"name": "Riyad Mahrez", "club": "Al Ahli", "position": "Winger", "market_value": 25000000, "age": 32},
    {"name": "Marcelo Brozović", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 30},
    {"name": "Kalidou Koulibaly", "club": "Al Hilal", "position": "Defender", "market_value": 35000000, "age": 32},
    {"name": "César Azpilicueta", "club": "Al Hilal", "position": "Defender", "market_value": 8000000, "age": 34},
    {"name": "Anderson Talisca", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 29},
    {"name": "Alvaro Morata", "club": "Al Hilal", "position": "Forward", "market_value": 30000000, "age": 31},
    # Add more players here...
]

# Get the current year
current_year = datetime.now().year

# Function to simulate historical market values (for model training)
def generate_historical_data(initial_value, years=5):
    """Simulate historical market data for a player over the past few years."""
    historical_data = []
    for year in range(current_year - years, current_year):
        value = initial_value * (1 + random.uniform(-0.1, 0.2))  # Simulate market fluctuations (between -10% and +20%)
        historical_data.append((year, round(value, 2)))
        initial_value = value
    return historical_data

# Function to apply Linear Regression and predict future market values
def forecast_market_value(historical_data, years_to_predict=3):
    """Use Linear Regression to forecast market values."""
    # Prepare the data
    years = np.array([data[0] for data in historical_data]).reshape(-1, 1)
    values = np.array([data[1] for data in historical_data])
    
    # Create and fit the model
    model = LinearRegression()
    model.fit(years, values)
    
    # Predict future values
    future_years = np.array([current_year + i for i in range(1, years_to_predict + 1)]).reshape(-1, 1)
    predicted_values = model.predict(future_years)
    
    # Return predicted values
    return predicted_values

# Function to calculate transfer chance using regression
def calculate_transfer_chance(player):
    """Calculate transfer chance using linear regression based on player's market value and age."""
    # Prepare the data
    # We will simulate the target variable (transfer chance) for training purposes
    data = [
        {"market_value": 50000000, "age": 38, "transfer_chance": 70},
        {"market_value": 30000000, "age": 35, "transfer_chance": 50},
        {"market_value": 45000000, "age": 31, "transfer_chance": 60},
        {"market_value": 70000000, "age": 31, "transfer_chance": 80},
        {"market_value": 25000000, "age": 32, "transfer_chance": 40},
        {"market_value": 25000000, "age": 30, "transfer_chance": 55},
        {"market_value": 35000000, "age": 32, "transfer_chance": 50},
        {"market_value": 8000000, "age": 34, "transfer_chance": 20},
        {"market_value": 25000000, "age": 29, "transfer_chance": 60},
        {"market_value": 30000000, "age": 31, "transfer_chance": 65},
    ]
    
    # Convert to DataFrame for regression
    df = pd.DataFrame(data)
    
    # Create features and target variable
    X = df[["market_value", "age"]]
    y = df["transfer_chance"]
    
    # Train a regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict transfer chance for the player
    player_data = np.array([[player["market_value"], player["age"]]])
    transfer_chance = model.predict(player_data)[0]
    
    # Return the transfer chance (rounded to 2 decimal places)
    return round(min(max(transfer_chance, 0), 100), 2)

# Function to display player information as a football card
def display_player_card(player):
    historical_data = generate_historical_data(player['market_value'])
    predicted_values = forecast_market_value(historical_data)
    transfer_chance = calculate_transfer_chance(player)
    
    st.markdown(f"""
    <div class="player-card">
        <h2>{player['name']}</h2>
        <div class="position">{player['position']} | {player['club']}</div>
        <div class="market-value">Market Value: ${player['market_value'] / 1e6:.2f}M</div>
        <div class="age">Age: {player['age']}</div>
        <div class="transfer-chance">Transfer Chance: {transfer_chance}%</div>
        <div class="card-footer">
            <strong>Predicted Market Value:</strong><br>
            {current_year + 1}: ${predicted_values[0] / 1e6:.2f}M<br>
            {current_year + 2}: ${predicted_values[1] / 1e6:.2f}M<br>
            {current_year + 3}: ${predicted_values[2] / 1e6:.2f}M
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display the Saudi flag at the top
st.markdown('<img class="ksa-flag" src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg" alt="KSA Flag">', unsafe_allow_html=True)

# Create a selection for player positions and additional details
st.title("Saudi Arabian Players Transfer Predictions")
player_names = [player['name'] for player in players_data]
selected_player_name = st.selectbox("Choose a Player:", player_names)

# Display selected player's info
selected_player = next(player for player in players_data if player['name'] == selected_player_name)
display_player_card(selected_player)
