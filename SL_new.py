import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Add custom CSS for a Summer Sports Vibes theme
st.markdown("""
    <style>
    .stApp {
        background-color: #ffefd5;  /* Summer light background (cream) */
        color: #000000;  /* Black text for readability */
    }
    .stButton>button {
        background-color: #ff8c00; /* Orange button for sunny vibes */
        color: white;
        border-radius: 12px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff6a00;
    }
    .stMarkdown {
        font-size: 20px;
        font-weight: bold;
        color: #000000;
    }
    .stSelectbox, .stSlider, .stRadio, .stTextInput {
        background-color: #ffeb3b;  /* Yellow background for dropdowns */
        color: #000000;
        border-radius: 8px;
    }
    .stSelectbox>div>div {
        background-color: #ffeb3b;
    }
    .stTextInput>div>div {
        background-color: #ffeb3b;
    }
    .player-card {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        padding: 20px;
        margin-bottom: 20px;
        max-width: 300px;
        display: inline-block;
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #333;
        border: 3px solid #ff8c00; /* Orange border for Summer feel */
    }
    .player-card h2 {
        font-size: 22px;
        color: #ff8c00; /* Orange for player names */
        margin-bottom: 10px;
    }
    .player-card .position {
        font-size: 16px;
        color: #ff8c00;
    }
    .player-card .market-value {
        font-size: 18px;
        color: #009e4d;  /* Green for market value */
        margin-top: 10px;
    }
    .player-card .age {
        font-size: 14px;
        color: #888;
    }
    .player-card .card-footer {
        margin-top: 15px;
        font-size: 14px;
        color: #ff8c00;
    }
    .player-card .transfer-chance {
        font-size: 14px;
        color: #f44336; /* Red for transfer chance */
    }
    .ksa-flag {
        display: block;
        margin: 0 auto 20px;
        width: 100px;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample player data with style of playing, age, and market value
players_data = [
    {"name": "Cristiano Ronaldo", "club": "Al Nassr", "position": "Forward", "market_value": 50000000, "age": 38, "style": "Attacking"},
    {"name": "Karim Benzema", "club": "Al-Ittihad", "position": "Forward", "market_value": 30000000, "age": 35, "style": "Attacking"},
    {"name": "Neymar Jr.", "club": "Al Hilal", "position": "Forward", "market_value": 45000000, "age": 31, "style": "Attacking"},
    {"name": "Sadio Mane", "club": "Al Nassr", "position": "Forward", "market_value": 70000000, "age": 31, "style": "Balanced"},
    {"name": "Riyad Mahrez", "club": "Al Ahli", "position": "Winger", "market_value": 25000000, "age": 32, "style": "Balanced"},
    {"name": "Marcelo Brozović", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 30, "style": "Defensive"},
    {"name": "Kalidou Koulibaly", "club": "Al Hilal", "position": "Defender", "market_value": 35000000, "age": 32, "style": "Defensive"},
    {"name": "César Azpilicueta", "club": "Al Hilal", "position": "Defender", "market_value": 8000000, "age": 34, "style": "Defensive"},
    {"name": "Anderson Talisca", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 29, "style": "Balanced"},
    {"name": "Alvaro Morata", "club": "Al Hilal", "position": "Forward", "market_value": 30000000, "age": 31, "style": "Attacking"},
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

# Function to filter and display player cards based on selected criteria
def display_filtered_players(style, min_age, max_age, budget_range):
    filtered_players = [player for player in players_data if 
                        (player['style'] == style) and
                        (min_age <= player['age'] <= max_age) and
                        (budget_range == 'Low' and player['market_value'] <= 20000000 or
                         budget_range == 'Medium' and 20000000 < player['market_value'] <= 50000000 or
                         budget_range == 'High' and player['market_value'] > 50000000)]
    
    for player in filtered_players:
        # Generate historical data for the player
        historical_data = generate_historical_data(player['market_value'])
        predicted_values = forecast_market_value(historical_data)
        transfer_chance = calculate_transfer_chance(player)
        
        # Display player card
        st.markdown(f"""
            <div class="player-card">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Saudi_Arabia.svg" class="ksa-flag" alt="KSA Flag">
                <h2>{player['name']}</h2>
                <p class="position">{player['position']} - {player['club']}</p>
                <p class="market-value">Current Market Value: ${player['market_value']:,.2f}</p>
                <p class="age">Age: {player['age']}</p>
                <p class="transfer-chance">Transfer Chance: {transfer_chance}%</p>
                <p class="card-footer">Market Value Forecast:</p>
                <p class="market-value">{current_year+1}: ${predicted_values[0]:,.2f}</p>
                <p class="market-value">{current_year+2}: ${predicted_values[1]:,.2f}</p>
                <p class="market-value">{current_year+3}: ${predicted_values[2]:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)

# Add dropdowns to select filter criteria
style_of_play = st.selectbox("Style of Playing:", ["Attacking", "Balanced", "Defensive"])
age_range = st.slider("Age Range:", 18, 40, (18, 30))
budget_range = st.selectbox("Budget Range:", ["Low", "Medium", "High"])

# Display filtered players based on dropdown selections
display_filtered_players(style_of_play, age_range[0], age_range[1], budget_range)
