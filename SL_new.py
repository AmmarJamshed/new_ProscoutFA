import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Updated list of 25 Saudi players data
players_data = [
    {"name": "Cristiano Ronaldo", "club": "Al Nassr", "position": "Forward", "market_value": 50000000, "age": 38, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Cristiano_Ronaldo_2018.jpg"},
    {"name": "Karim Benzema", "club": "Al-Ittihad", "position": "Forward", "market_value": 30000000, "age": 35, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/8/85/Karim_Benzema_2019.jpg"},
    {"name": "Neymar Jr.", "club": "Al Hilal", "position": "Forward", "market_value": 45000000, "age": 31, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Neymar_2018.jpg"},
    {"name": "Sadio Mane", "club": "Al Nassr", "position": "Forward", "market_value": 70000000, "age": 31, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/3/31/Sadio_Mane_2019.jpg"},
    {"name": "Riyad Mahrez", "club": "Al Ahli", "position": "Winger", "market_value": 25000000, "age": 32, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/3/32/Riyad_Mahrez_2020.jpg"},
    {"name": "Marcelo Brozović", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 30, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Marcelo_Brozovic_-_2018.jpg"},
    {"name": "Kalidou Koulibaly", "club": "Al Hilal", "position": "Defender", "market_value": 35000000, "age": 32, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Kalidou_Koulibaly_2019.jpg"},
    {"name": "César Azpilicueta", "club": "Al Hilal", "position": "Defender", "market_value": 8000000, "age": 34, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Cesar_Azpilicueta_2021.jpg"},
    {"name": "Anderson Talisca", "club": "Al Nassr", "position": "Midfielder", "market_value": 25000000, "age": 29, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Talisca_2021.jpg"},
    {"name": "Alvaro Morata", "club": "Al Hilal", "position": "Forward", "market_value": 30000000, "age": 31, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Alvaro_Morata_2021.jpg"},
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

# Function to display player information and avatars
def display_player(player):
    st.image(player['avatar_url'], width=80, use_column_width=True)
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
st.title("Football Analytics Dashboard")
st.sidebar.header("Player Filter")
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

# Show summary table
st.header("Summary of Selected Players")
summary_data = [
    {"Name": player["name"], "Position": player["position"], "Age": player["age"], "Market Value": f"${player['market_value']:,.2f}"}
    for player in filtered_players if player['market_value'] <= selected_budget * 1000000
]

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary)
