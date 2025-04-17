import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

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
    {"name": "Fabinho", "club": "Al-Ittihad", "position": "Midfielder", "market_value": 25000000, "age": 29, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Fabinho_2019.jpg"},
    {"name": "Mason Mount", "club": "Al-Ittihad", "position": "Midfielder", "market_value": 40000000, "age": 26, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Mason_Mount_2022.jpg"},
    {"name": "Fábio Vieira", "club": "Al Nassr", "position": "Midfielder", "market_value": 18000000, "age": 23, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Fabio_Vieira_2022.jpg"},
    {"name": "James Rodríguez", "club": "Al Rayyan", "position": "Midfielder", "market_value": 15000000, "age": 32, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/4/49/James_Rodríguez_2018.jpg"},
    {"name": "Angelo Ogbonna", "club": "Al Ahli", "position": "Defender", "market_value": 8000000, "age": 35, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Angelo_Ogbonna_2019.jpg"},
    {"name": "Sergio Ramos", "club": "Al Nassr", "position": "Defender", "market_value": 15000000, "age": 38, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Sergio_Ramos_2020.jpg"},
    {"name": "David Ospina", "club": "Al Nassr", "position": "Goalkeeper", "market_value": 5000000, "age": 35, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/5/58/David_Ospina_2018.jpg"},
    {"name": "Abdullah Al-Muaiouf", "club": "Al Hilal", "position": "Goalkeeper", "market_value": 1000000, "age": 34, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Abdullah_Al-Muaiouf_2016.jpg"},
    {"name": "Yasser Al-Shahrani", "club": "Al Hilal", "position": "Defender", "market_value": 8000000, "age": 30, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Yasser_Al_Shahrani_2018.jpg"},
    {"name": "Salman Al-Faraj", "club": "Al Hilal", "position": "Midfielder", "market_value": 5000000, "age": 34, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Salman_Al-Faraj_2021.jpg"},
    {"name": "Mohammad Al-Dosari", "club": "Al Nassr", "position": "Midfielder", "market_value": 3000000, "age": 32, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Mohammad_Al-Dosari_2020.jpg"},
    {"name": "Abdulrahman Al-Obaid", "club": "Al Ahli", "position": "Defender", "market_value": 2000000, "age": 30, "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/1/12/Abdulrahman_Al-Obaid_2016.jpg"},
]

# Get the current year
current_year = datetime.now().year

# Function to calculate predicted market value
def predict_market_value(current_value, years_from_now):
    growth_rate = random.uniform(0.05, 0.15)  # 5% to 15% growth per year
    predicted_value = current_value * (1 + growth_rate) ** years_from_now
    return round(predicted_value, 2)

# Function to display player information and avatars
def display_player(player):
    st.image(player['avatar_url'], width=80, use_column_width=True)
    st.write(f"**{player['name']}** - {player['position']} - Age: {player['age']}")
    
    # Market value predictions for next 3 years
    years = [1, 2, 3]
    market_values = [predict_market_value(player['market_value'], year) for year in years]
    
    # Display predicted market values
    for i, year in enumerate(years):
        st.write(f"**Market Value in {current_year + year}:** ${market_values[i]:,} USD")
    
    # Display best fit club
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
    display_player(player)

# Show a table of players with their market values for the next 3 years
st.subheader("Player Market Value Predictions")
table_data = []
for player in filtered_players:
    market_values = [predict_market_value(player['market_value'], year) for year in years]
    table_data.append({
        "Player": player['name'],
        "Current Market Value": f"${player['market_value']:,} USD",
        f"Market Value in {current_year + 1}": f"${market_values[0]:,} USD",
        f"Market Value in {current_year + 2}": f"${market_values[1]:,} USD",
