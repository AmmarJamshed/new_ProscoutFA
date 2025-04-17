import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import altair as alt
import random

# App configuration
st.set_page_config(page_title="Football Analytics", layout="wide")

# Add a football-themed background to the app
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1560366719-30f918c9a755');
        background-size: cover;
        background-position: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Static player data for 50 players from Saudi clubs
players_data = [
    {"Player Name": "Salem Al-Dawsari", "Age": 31, "Nationality": "Saudi", "Position": "Forward", "Club": "Al Hilal", "xG": 0.7, "Assists": 5, "Dribbles": 10, "Tackles": 1, "Interceptions": 2, "PassingAccuracy": 80, "Previous_Season_Goals": 7, "Previous_Season_Assists": 5, "Market_Value": 8.0},
    {"Player Name": "Anderson Talisca", "Age": 29, "Nationality": "Brazilian", "Position": "Midfielder", "Club": "Al Nassr", "xG": 0.9, "Assists": 4, "Dribbles": 12, "Tackles": 3, "Interceptions": 1, "PassingAccuracy": 85, "Previous_Season_Goals": 12, "Previous_Season_Assists": 6, "Market_Value": 12.5},
    {"Player Name": "Cristiano Ronaldo", "Age": 38, "Nationality": "Portuguese", "Position": "Forward", "Club": "Al Nassr", "xG": 0.8, "Assists": 6, "Dribbles": 7, "Tackles": 2, "Interceptions": 1, "PassingAccuracy": 87, "Previous_Season_Goals": 22, "Previous_Season_Assists": 7, "Market_Value": 25.0},
    {"Player Name": "Matheus Pereira", "Age": 28, "Nationality": "Brazilian", "Position": "Midfielder", "Club": "Al Hilal", "xG": 0.5, "Assists": 8, "Dribbles": 15, "Tackles": 4, "Interceptions": 3, "PassingAccuracy": 84, "Previous_Season_Goals": 4, "Previous_Season_Assists": 8, "Market_Value": 6.0},
    {"Player Name": "Odion Ighalo", "Age": 34, "Nationality": "Nigerian", "Position": "Forward", "Club": "Al Hilal", "xG": 0.6, "Assists": 3, "Dribbles": 6, "Tackles": 1, "Interceptions": 1, "PassingAccuracy": 78, "Previous_Season_Goals": 10, "Previous_Season_Assists": 3, "Market_Value": 7.0},
    # Add more players as before...
]

# Convert to DataFrame
df = pd.DataFrame(players_data)

# Static avatar generation (using simple image URL pattern, can be improved)
df['Image'] = df['Player Name'].apply(lambda name: f"https://robohash.org/{name.replace(' ', '')}.png?set=set2")

# Add predicted values for each player
df['Predicted_Market_Value'] = df['Market_Value'] * random.uniform(1.05, 1.3)  # Simulating future predicted values
df['Transfer_Chance'] = df['Market_Value'].apply(lambda x: random.uniform(0.6, 0.9))  # Random transfer chance
df['Best_Fit_Club'] = df['Club'].apply(lambda x: random.choice(['Barcelona', 'Manchester United', 'Paris Saint-Germain', 'Bayern Munich', 'Chelsea']))  # Random best-fit clubs

# Market Value Prediction for the next three years
growth_factor = 1.1  # 10% market value growth per year
df['Predicted_Market_Value_Year_1'] = df['Predicted_Market_Value'] * growth_factor
df['Predicted_Market_Value_Year_2'] = df['Predicted_Market_Value_Year_1'] * growth_factor
df['Predicted_Market_Value_Year_3'] = df['Predicted_Market_Value_Year_2'] * growth_factor

# Convert market value to SAR (for display in Saudi Arabia)
df['Market_Value_SAR'] = df['Market_Value'] * 3.75
df['Predicted_Market_Value_SAR'] = df['Predicted_Market_Value'] * 3.75
df['Predicted_Market_Value_Year_1_SAR'] = df['Predicted_Market_Value_Year_1'] * 3.75
df['Predicted_Market_Value_Year_2_SAR'] = df['Predicted_Market_Value_Year_2'] * 3.75
df['Predicted_Market_Value_Year_3_SAR'] = df['Predicted_Market_Value_Year_3'] * 3.75

# Displaying dashboard title and subtitle
st.title("⚽ Football Player Analytics Dashboard")
st.subheader("Explore player stats, predicted market values, transfer chances, and the best-fit clubs!")

# Sidebar filters for position, age, and budget
position_filter = st.sidebar.selectbox("Select Position", ['All'] + list(df['Position'].unique()))
age_filter = st.sidebar.slider("Select Age Range", min_value=18, max_value=40, value=(18, 40))
budget_filter = st.sidebar.slider("Select Budget (in SAR millions)", min_value=0, max_value=100, value=(0, 100))

# Filter the dataframe based on the selected criteria
filtered_df = df
if position_filter != 'All':
    filtered_df = filtered_df[filtered_df['Position'] == position_filter]

filtered_df = filtered_df[(filtered_df['Age'] >= age_filter[0]) & (filtered_df['Age'] <= age_filter[1])]
filtered_df = filtered_df[(filtered_df['Market_Value_SAR'] >= budget_filter[0] * 1e6) & (filtered_df['Market_Value_SAR'] <= budget_filter[1] * 1e6)]

# Display the table
st.write(f"Displaying players with the selected filters (Position: {position_filter}, Age Range: {age_filter}, Budget: {budget_filter[0]}M to {budget_filter[1]}M SAR):")
st.write(filtered_df[['Player Name', 'Age', 'Nationality', 'Position', 'Club', 'Market_Value_SAR', 
                      'Predicted_Market_Value_SAR', 'Predicted_Market_Value_Year_1_SAR', 'Predicted_Market_Value_Year_2_SAR', 
                      'Predicted_Market_Value_Year_3_SAR', 'Transfer_Chance', 'Best_Fit_Club']])

# Function to create player card with football icon
def player_card(player_data):
    card = f"""
    <div style="padding: 10px; background-color: rgba(0, 0, 0, 0.6); margin: 10px; border-radius: 8px; color: white; display: flex; align-items: center;">
        <img src="{player_data['Image']}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px;">
        <div>
            <h3>{player_data['Player Name']}</h3>
            <p><strong>Club:</strong> {player_data['Club']}</p>
            <p><strong>Position:</strong> {player_data['Position']}</p>
            <p><strong>Predicted Market Value (SAR):</strong> {player_data['Predicted_Market_Value_SAR']:.2f} SAR</p>
            <p><strong>Transfer Chance:</strong> {player_data['Transfer_Chance'] * 100:.1f}%</p>
            <p><strong>Best Fit Club:</strong> {player_data['Best_Fit_Club']}</p>
            <p><strong>Predicted Market Value in 1 Year:</strong> {player_data['Predicted_Market_Value_Year_1_SAR']:.2f} SAR</p>
            <p><strong>Predicted Market Value in 2 Years:</strong> {player_data['Predicted_Market_Value_Year_2_SAR']:.2f} SAR</p>
            <p><strong>Predicted Market Value in 3 Years:</strong> {player_data['Predicted_Market_Value_Year_3_SAR']:.2f} SAR</p>
        </div>
        <div style="margin-left: auto; display: flex; justify-content: center; align-items: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/57/Football_Icon.svg" style="width: 30px; height: 30px; margin-left: 10px;">
        </div>
    </div>
    """
    return card

# Display player cards for filtered players
for _, player in filtered_df.iterrows():
    st.markdown(player_card(player), unsafe_allow_html=True)

# Adding interactive graphs (Optional)
x = df['Age']
y = df['Market_Value']

# Scatter plot for Market Value vs Age
chart = alt.Chart(df).mark_circle(size=60).encode(
    x=alt.X('Age', title='Age'),
    y=alt.Y('Market_Value', title='Market Value (M)'),
    color='Position',
    tooltip=['Player Name', 'Market_Value', 'Position', 'Age']
).interactive()

st.altair_chart(chart, use_container_width=True)
