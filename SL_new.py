import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Add custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;  /* White background for the app */
        color: #000000;  /* Black text for readability */
    }
    .stButton>button {
        background-color: #ff8c00; /* Orange button */
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
        box-shadow: 0 4px 6px rgba(0, 128, 0, 0.5);  /* Green shadow */
        padding: 20px;
        margin-bottom: 20px;
        max-width: 300px;
        display: inline-block;
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #333;
        border: 3px solid #4CAF50; /* Green border for player cards */
    }
    .player-card h2 {
        font-size: 22px;
        color: #4CAF50; /* Green for player names */
        margin-bottom: 10px;
        font-weight: bold;
    }
    .player-card .position {
        font-size: 16px;
        color: #4CAF50;
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
        color: #4CAF50;
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

# Sample player data
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

# Sidebar filter options
style_of_play = st.sidebar.selectbox("Style of Playing:", ["Attacking", "Balanced", "Defensive"])
min_age = st.sidebar.slider("Minimum Age:", 18, 40, 25)
max_age = st.sidebar.slider("Maximum Age:", 18, 40, 35)
budget_range = st.sidebar.selectbox("Budget Range:", ["Low", "Medium", "High"])

# Function to filter and display player cards
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

# Display filtered player cards
display_filtered_players(style_of_play, min_age, max_age, budget_range)
