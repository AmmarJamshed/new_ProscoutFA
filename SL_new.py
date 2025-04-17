import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Add custom CSS for styling for a light-colored theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f7;
        color: black;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stMarkdown {
        font-size: 18px;
        font-weight: bold;
    }
    .stSelectbox, .stSlider, .stRadio, .stTextInput {
        background-color: #e3f2fd;
        color: black;
    }
    .stSelectbox>div>div {
        background-color: #e3f2fd;
    }
    .stTextInput>div>div {
        background-color: #e3f2fd;
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

# Function to display player information
def display_player(player):
    st.write(f"**{player['name']}** - {player['position']} - Age: {player['age']}")
    
    # Simulate historical data for the player
    historical_data = generate_historical_data(player['market_value'])
    
    # Forecast future market values
    predicted_values = forecast_market_value(historical_data)
    
    # Display predicted market values
    for i, year in enumerate(range(1, 4)):
        st.write(f"**Market Value in {current_year + year}:** ${predicted_values[i]:,.2f} USD")
    
    # Display best fit club (random for now)
    best_fit_club = random.choice(["Al Nassr", "Al Hilal", "Al-Ittihad", "Al Ahli"])  # Random choice for now
    st.write(f"**Best Fit Club:** {best_fit_club}")

# Create a selection for player positions and additional details
st.title("⚽ Football Analytics Dashboard ⚽")
st.sidebar.header("Player Filter ⚽")
positions = ["Forward", "Midfielder", "Defender", "Goalkeeper", "Winger"]
selected_position = st.sidebar.selectbox("Select Position", positions)
selected_budget = st.sidebar.slider("Budget (in millions)", 10, 100, 50)
selected_age = st.sidebar.slider("Age Range", 18, 40, (20, 35))

# Filter players by selected criteria
filtered_players = [
    player for player in players_data
    if player['position'] == selected_position and player['age'] >= selected_age[0] and player['age'] <= selected_age[1]
]

# Display players
st.header(f"Players ({selected_position}s) Available for Your Budget: ${selected_budget}M")
for player in filtered_players:
    if player['market_value'] <= selected_budget * 1000000:
        display_player(player)
        st.write("---")
