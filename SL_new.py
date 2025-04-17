import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import altair as alt
import random

# App configuration
st.set_page_config(page_title="Football Analytics", layout="wide")

# Static player data for 50 players from Saudi clubs
players_data = [
    {"Player Name": "Salem Al-Dawsari", "Age": 31, "Nationality": "Saudi", "Position": "Forward", "Club": "Al Hilal", "xG": 0.7, "Assists": 5, "Dribbles": 10, "Tackles": 1, "Interceptions": 2, "PassingAccuracy": 80, "Previous_Season_Goals": 7, "Previous_Season_Assists": 5, "Market_Value": 8.0},
    {"Player Name": "Anderson Talisca", "Age": 29, "Nationality": "Brazilian", "Position": "Midfielder", "Club": "Al Nassr", "xG": 0.9, "Assists": 4, "Dribbles": 12, "Tackles": 3, "Interceptions": 1, "PassingAccuracy": 85, "Previous_Season_Goals": 12, "Previous_Season_Assists": 6, "Market_Value": 12.5},
    {"Player Name": "Cristiano Ronaldo", "Age": 38, "Nationality": "Portuguese", "Position": "Forward", "Club": "Al Nassr", "xG": 0.8, "Assists": 6, "Dribbles": 7, "Tackles": 2, "Interceptions": 1, "PassingAccuracy": 87, "Previous_Season_Goals": 22, "Previous_Season_Assists": 7, "Market_Value": 25.0},
    {"Player Name": "Matheus Pereira", "Age": 28, "Nationality": "Brazilian", "Position": "Midfielder", "Club": "Al Hilal", "xG": 0.5, "Assists": 8, "Dribbles": 15, "Tackles": 4, "Interceptions": 3, "PassingAccuracy": 84, "Previous_Season_Goals": 4, "Previous_Season_Assists": 8, "Market_Value": 6.0},
    {"Player Name": "Odion Ighalo", "Age": 34, "Nationality": "Nigerian", "Position": "Forward", "Club": "Al Hilal", "xG": 0.6, "Assists": 3, "Dribbles": 6, "Tackles": 1, "Interceptions": 1, "PassingAccuracy": 78, "Previous_Season_Goals": 10, "Previous_Season_Assists": 3, "Market_Value": 7.0},
    # Add more players as needed...
]

# Convert to DataFrame
df = pd.DataFrame(players_data)

# Static avatar generation (using simple image URL pattern, can be improved)
df['Image'] = df['Player Name'].apply(lambda name: f"https://robohash.org/{name.replace(' ', '')}.png?set=set2")

# Add predicted values for each player
df['Predicted_Market_Value'] = df['Market_Value'] * random.uniform(1.05, 1.3)  # Simulating future predicted values
df['Transfer_Chance'] = df['Market_Value'].apply(lambda x: random.uniform(0.6, 0.9))  # Random transfer chance
df['Best_Fit_Club'] = df['Club'].apply(lambda x: random.choice(['Barcelona', 'Manchester United', 'Paris Saint-Germain', 'Bayern Munich', 'Chelsea']))  # Random best-fit clubs

# Convert market value to SAR (for display in Saudi Arabia)
df['Market_Value_SAR'] = df['Market_Value'] * 3.75
df['Predicted_Market_Value_SAR'] = df['Predicted_Market_Value'] * 3.75

# Displaying dashboard title and subtitle
st.title("🌍 Football Player Analytics Dashboard")
st.subheader("Explore player stats, predicted market values, transfer chances, and the best-fit clubs!")

# Sidebar filters for position and club
st.sidebar.header("Filter Players")
positions = st.sidebar.multiselect("Position", options=df["Position"].unique(), default=df["Position"].unique())
clubs = st.sidebar.multiselect("Club", options=df["Club"].unique(), default=df["Club"].unique())

# Filter dataframe based on sidebar selections
filtered_df = df[(df["Position"].isin(positions)) & (df["Club"].isin(clubs))]

# Display filtered player avatars and details
st.subheader("Player Avatars & Performance")
cols = st.columns(6)
for i, row in filtered_df.iterrows():
    with cols[i % 6]:
        st.image(row["Image"], width=80, caption=row["Player Name"])
        st.write(f"**Predicted Market Value**: {row['Predicted_Market_Value']:.2f}M USD")
        st.write(f"**Transfer Chance**: {row['Transfer_Chance']*100:.1f}%")
        st.write(f"**Best Fit Club**: {row['Best_Fit_Club']}")
        st.write(f"**Previous Market Value**: {row['Market_Value']}M USD")

# KPI section: Total players, average market value, etc.
st.markdown("### Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Market Value (USD)", f"{filtered_df['Market_Value'].mean():.2f}")
col3.metric("Avg Passing Accuracy (%)", f"{filtered_df['PassingAccuracy'].mean():.1f}")

# Scatter plot for player performance comparison
st.markdown("### 📊 Performance Comparison (xG vs Assists)")
chart = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x='xG',
    y='Assists',
    color='Position',
    tooltip=['Player Name', 'xG', 'Assists', 'Dribbles']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Detailed table of filtered players
st.markdown("### 📋 Player Details")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
