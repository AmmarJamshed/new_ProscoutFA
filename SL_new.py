import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Set up page configuration
st.set_page_config(page_title="Football Analytics", layout="wide")

# Static player data (Updated with actual player names from Saudi clubs)
@st.cache_data
def load_static_player_data():
    np.random.seed(42)
    # Real player names and their clubs
    player_data = [
        {"Player Name": "Cristiano Ronaldo", "Club": "Al Nassr", "Position": "Forward", "Nationality": "Portugal"},
        {"Player Name": "Sadio Mané", "Club": "Al Nassr", "Position": "Forward", "Nationality": "Senegal"},
        {"Player Name": "Roberto Firmino", "Club": "Al Ahli", "Position": "Forward", "Nationality": "Brazil"},
        {"Player Name": "Riyad Mahrez", "Club": "Al Ahli", "Position": "Midfielder", "Nationality": "Algeria"},
        {"Player Name": "Karim Benzema", "Club": "Al Ittihad", "Position": "Forward", "Nationality": "France"},
        {"Player Name": "N'Golo Kanté", "Club": "Al Ittihad", "Position": "Midfielder", "Nationality": "France"},
        {"Player Name": "Odion Ighalo", "Club": "Al Hilal", "Position": "Forward", "Nationality": "Nigeria"},
        {"Player Name": "Luciano Vietto", "Club": "Al Hilal", "Position": "Midfielder", "Nationality": "Argentina"},
        {"Player Name": "Cristiano Ronaldo", "Club": "Al Nassr", "Position": "Forward", "Nationality": "Portugal"},
        {"Player Name": "Marcelo Brozović", "Club": "Al Nassr", "Position": "Midfielder", "Nationality": "Croatia"},
        {"Player Name": "Matheus Pereira", "Club": "Al Hilal", "Position": "Midfielder", "Nationality": "Brazil"},
    ]

    # Add the predicted values, transfer chance, and avatars
    for player in player_data:
        player["Predicted_Market_Value_2026"] = np.round(np.random.uniform(10, 40), 2)
        player["Transfer_Chance (%)"] = np.random.randint(10, 95)
        player["Best_Fit_Club"] = np.random.choice(["Al Nassr", "Al Hilal", "Al Ahli", "Al Ittihad"])
        player["Market_Value_SAR"] = np.round(player["Predicted_Market_Value_2026"] * 3.75, 2)

        # Generate avatar (cartoon-style)
        player["Image"] = f"https://robohash.org/{player['Player Name'].replace(' ', '')}.png?set=set2"
    
    return pd.DataFrame(player_data)

# Load Data
df = load_static_player_data()

# Sidebar filters
st.sidebar.header("Filter Players")
clubs = st.sidebar.multiselect("Club", options=df["Club"].unique(), default=df["Club"].unique())
positions = st.sidebar.multiselect("Position", options=df["Position"].unique(), default=df["Position"].unique())
filtered_df = df[(df["Club"].isin(clubs)) & (df["Position"].isin(positions))]

# Dashboard UI
st.title("🌍 Football Player Analytics Dashboard")

# Custom CSS for styling
st.markdown("""
    <style>
        .player-card {
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f4f4f4;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .player-card img {
            border-radius: 50%;
            width: 80px;
            height: 80px;
            margin-right: 20px;
        }
        .player-info {
            display: flex;
            flex-direction: column;
        }
        .player-info h3 {
            margin: 0;
            font-size: 16px;
            font-weight: bold;
        }
        .player-info p {
            margin: 2px 0;
            font-size: 14px;
            color: #333;
        }
        .player-stats {
            display: flex;
            flex-direction: column;
            justify-content: space-around;
        }
        .player-stats p {
            margin: 2px 0;
            font-size: 14px;
            font-weight: bold;
            color: #333;
        }
        .player-stats span {
            color: #0066cc;
        }
    </style>
""", unsafe_allow_html=True)

# Display players in a dynamic, attractive layout
for i, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"""
            <div class="player-card">
                <img src="{row['Image']}" alt="Player Avatar">
                <div class="player-info">
                    <h3>{row['Player Name']}</h3>
                    <p><strong>Position:</strong> {row['Position']}</p>
                    <p><strong>Nationality:</strong> {row['Nationality']}</p>
                    <p><strong>Club:</strong> {row['Club']}</p>
                </div>
                <div class="player-stats">
                    <p><strong>Predicted Value:</strong> <span>${row['Predicted_Market_Value_2026']}M</span></p>
                    <p><strong>Transfer Chance:</strong> <span>{row['Transfer_Chance (%)']}%</span></p>
                    <p><strong>Best Fit Club:</strong> <span>{row['Best_Fit_Club']}</span></p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# KPIs Section
st.markdown("### ⚽ Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", len(filtered_df))
col2.metric("Avg Market Value ($M)", f"{filtered_df['Predicted_Market_Value_2026'].mean():.2f}")
col3.metric("Avg Transfer Chance (%)", f"{filtered_df['Transfer_Chance (%)'].mean():.1f}")

# Scatter Plot
st.markdown("### 📊 Performance Comparison")
chart = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x='Predicted_Market_Value_2026',
    y='Transfer_Chance (%)',
    color='Club',
    tooltip=['Player Name', 'Predicted_Market_Value_2026', 'Transfer_Chance (%)']
).interactive()
st.altair_chart(chart, use_container_width=True)

# Bar Chart of Future Value
st.markdown("### 📈 Predicted Market Value in 2026")
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x='Player Name',
    y='Predicted_Market_Value_2026',
    color='Transfer_Chance (%)',
    tooltip=[
        'Player Name', 'Market_Value_SAR', 'Predicted_Market_Value_2026',
        'Transfer_Chance (%)', 'Best_Fit_Club'
    ]
).properties(height=400).interactive()
st.altair_chart(bar_chart, use_container_width=True)

# Detailed Table
st.markdown("### 📋 Player Details (2026 Predictions)")
st.dataframe(filtered_df[[
    'Player Name', 'Position', 'Club', 'Nationality', 
    'Predicted_Market_Value_2026', 'Transfer_Chance (%)', 'Best_Fit_Club', 
    'Market_Value_SAR'
]].reset_index(drop=True), use_container_width=True)
