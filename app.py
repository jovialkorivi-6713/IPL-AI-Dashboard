import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ----------------------------
# LOAD DATA
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("IPL_Matches_2008_2022.csv")

    # Clean data
    df = df.drop_duplicates()
    df = df.dropna(subset=["WinningTeam"])

    return df

df = load_data()

# ----------------------------
# TITLE
# ----------------------------

st.title("🏏 IPL Analytics Dashboard")
st.markdown("### IPL Match Analysis (2008–2022)")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------

st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    sorted(df["Season"].unique())
)

teams = sorted(
    pd.concat([df["Team1"], df["Team2"]]).unique()
)

team_filter = st.sidebar.selectbox(
    "Select Team",
    teams
)

# ----------------------------
# FILTER DATA
# ----------------------------

filtered_df = df[df["Season"] == season]

# ----------------------------
# KPIs
# ----------------------------

total_matches = len(filtered_df)

total_teams = len(
    pd.concat(
        [filtered_df["Team1"], filtered_df["Team2"]]
    ).unique()
)

total_venues = filtered_df["Venue"].nunique()

total_winners = filtered_df["WinningTeam"].nunique()

st.subheader("📊 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Matches", total_matches)
c2.metric("Teams", total_teams)
c3.metric("Venues", total_venues)
c4.metric("Winning Teams", total_winners)

# ----------------------------
# CHART 1 TEAM WINS
# ----------------------------

team_wins = (
    filtered_df["WinningTeam"]
    .value_counts()
    .reset_index()
)

team_wins.columns = ["Team", "Wins"]

fig1 = px.bar(
    team_wins,
    x="Team",
    y="Wins",
    title="Team-wise Wins"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# CHART 2 MATCHES PER SEASON
# ----------------------------

season_matches = (
    df["Season"]
    .value_counts()
    .sort_index()
    .reset_index()
)

season_matches.columns = ["Season", "Matches"]

fig2 = px.line(
    season_matches,
    x="Season",
    y="Matches",
    markers=True,
    title="Matches Per Season"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# CHART 3 + 4
# ----------------------------

left, right = st.columns(2)

with left:

    toss = (
        filtered_df["TossDecision"]
        .value_counts()
        .reset_index()
    )

    toss.columns = ["Decision", "Count"]

    fig3 = px.pie(
        toss,
        names="Decision",
        values="Count",
        title="Toss Decision Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

with right:

    pom = (
        filtered_df["Player_of_Match"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pom.columns = ["Player", "Awards"]

    fig4 = px.bar(
        pom,
        x="Player",
        y="Awards",
        title="Top 10 Player of Match Winners"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# CHART 5 TOP VENUES
# ----------------------------

venue = (
    filtered_df["Venue"]
    .value_counts()
    .head(10)
    .reset_index()
)

venue.columns = ["Venue", "Matches"]

fig5 = px.bar(
    venue,
    x="Matches",
    y="Venue",
    orientation="h",
    title="Top Venues"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# CHART 6 TEAM TREND
# ----------------------------

team_df = df[
    (df["Team1"] == team_filter)
    |
    (df["Team2"] == team_filter)
]

team_trend = (
    team_df.groupby("Season")
    .size()
    .reset_index(name="Matches")
)

fig6 = px.line(
    team_trend,
    x="Season",
    y="Matches",
    markers=True,
    title=f"{team_filter} Participation Trend"
)

st.plotly_chart(fig6, use_container_width=True)

# ----------------------------
# AI INSIGHTS
# ----------------------------

st.subheader("🤖 AI Generated Insights")

if st.button("Generate Insights"):

    best_team = (
        df["WinningTeam"]
        .value_counts()
        .idxmax()
    )

    top_player = (
        df["Player_of_Match"]
        .value_counts()
        .idxmax()
    )

    st.success(f"""
🏆 Most Successful Team: {best_team}

⭐ Most Player of Match Awards: {top_player}

🎯 Teams generally prefer fielding after winning the toss.

📈 IPL has grown significantly over the years.

🏟️ Certain venues consistently host the most matches.
""")

# ----------------------------
# DATASET OVERVIEW
# ----------------------------

st.subheader("📄 Dataset Overview")

st.dataframe(filtered_df.head(20))