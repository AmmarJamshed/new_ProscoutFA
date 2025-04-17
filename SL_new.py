import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Football Analytics", layout="wide")

# Static player data
@st.cache_data
def load_static_player_data():
    np.random.seed(42)
    positions = ["Forward", "Midfielder", "Defender"]
    leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
    nationalities = ["Brazil", "France", "Germany", "Spain", "England", "Portugal", "Argentina", "Netherlands"]
    future_year = 2026
    top_clubs = ["Real Madrid", "Manchester City", "Barcelona", "Bayern Munich", "Arsenal", "PSG", "Inter Milan"]

    data = []
    for i in range(50):
        name = f"Player {i+1}"
        age = np.random.randint(19, 34)
        nationality = np.random.choice(nationalities)
        position = np.random.choice(positions)
        league = np.random.choice(leagues)
        club = f"Club {np.random.randint(1, 20)}"
        xg = np.round(np.random.uniform(0, 10), 2)
        assists = np.random.randint(0, 15)
        dribbles = np.random.randint(0, 30)
        tackles = np.random.randint(0, 15)
        interceptions = np.random.randint(0, 10)
        pass_acc = np.round(np.random.uniform(60, 95), 1)
        prev_goals = np.random.randint(0, 15)
        prev_assists = np.random.randint(0, 15)
        market_value = np.round(np.random.uniform(10, 40), 2)

        # Prediction logic
        predicted_value = np.round(market_value * np.random.uniform(1.1, 1.5), 2)
        transfer_chance = np.random.randint(10, 95)

        # Best fit club logic: based on performance metrics
        performance_score = xg + assists + dribbles + (pass_acc / 10)
        fit_index = int(performance_score % len(top_clubs))
        best_fit_club = top_clubs[fit_index]

        image = f"https://robohash.org/{name.replace(' ', '')}.png?set=set2"

        data.append({
            "Player Name": name,
            "Age": age,
            "Nationality": nationality,
            "Position": position,
            "League": league,
            "Club": club,
            "xG": xg,
            "Assists": assists,
            "Dribbles": dribbles,
            "Tackles": tackles,
            "Interceptions": interceptions,
            "PassingAccuracy": pass_acc,
            "Previous_Season_Goals": prev_goals,
            "Previous_Season_Assists": prev_assists,
            "Market_Value": market_value,
            "Predicted_Market_Value_2026": predicted_value,
            "Predicted_Year": future_year,
            "Best_Fit_Club": best_fit_club,
            "Transfer_Chance (%)": transfer_chance,
            "Image": image,
            "Market_Value_SAR": np.round(market_value * 3.75, 2),
        })

    return pd.DataFrame(data)

# Load Data
df = load_static_player_data()

# Sidebar filters
st.sidebar.header("Filter Players")
positions = st.sidebar.multiselect("Position", options=df["Position"].unique(), default=df["Position"].unique())
leagues = st.sidebar.multiselect("League", options=df["League"].unique(), default=df["League"].unique())
filtered_df = df[(df["Position"].isin(positions)) & (df["League"].isin(leagues))]

# Dashboard UI
st.title("🌍 Football Player Analytics Dashboard")

# Avatar preview
st.subheader("Player Avatars")
cols = st.columns(6)
for i, row in filtered_df.head(6).iterrows():
    with cols[i % 6]:
        st.image(row["Image"], width=80, caption=row["Player Name"])

# KPIs
st.markdown("### ⚽ Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Market Value ($M)", f"{filtered_df['Market_Value'].mean():.2f}")
col3.metric("Avg Passing Accuracy (%)", f"{filtered_df['PassingAccuracy'].mean():.1f}")

# Scatter Plot
st.markdown("### 📊 Performance Comparison")
chart = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x='xG',
    y='Assists',
    color='Position',
    tooltip=['Player Name', 'xG', 'Assists', 'Dribbles']
).interactive()
st.altair_chart(chart, use_container_width=True)

# Bar Chart of Future Value
st.markdown("### 📈 Predicted Market Value in 2026")
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x='Player Name',
    y='Predicted_Market_Value_2026',
    color='Transfer_Chance (%)',
    tooltip=[
        'Player Name', 'Market_Value', 'Predicted_Market_Value_2026',
        'Transfer_Chance (%)', 'Best_Fit_Club'
    ]
).properties(height=400).interactive()
st.altair_chart(bar_chart, use_container_width=True)

# Detailed Table
st.markdown("### 📋 Player Details (2026 Predictions)")
st.dataframe(filtered_df[[
    'Player Name', 'Age', 'Nationality', 'Position', 'League', 'Club',
    'xG', 'Assists', 'Dribbles', 'Tackles', 'Interceptions', 'PassingAccuracy',
    'Previous_Season_Goals', 'Previous_Season_Assists',
    'Market_Value', 'Predicted_Market_Value_2026', 'Predicted_Year',
    'Best_Fit_Club', 'Transfer_Chance (%)', 'Market_Value_SAR'
]].reset_index(drop=True), use_container_width=True)
