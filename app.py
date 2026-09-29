import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Analysis", layout="wide")
st.title("⚽ football-analysis - La Liga Betting AI")

@st.cache_data
def load():
    try:
        df = pd.read_csv("SP1.csv")
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df['TotalGoals'] = df['FTHG'] + df['FTAG']
        return df
    except:
        return None

df = load()

if df is None:
    st.warning("Upload SP1.csv first - then reload. App is ready.")
else:
    tab1, tab2, tab3 = st.tabs(["Match Viewer", "Over 2.5 Model", "Team Form"])
    
    with tab1:
        st.dataframe(df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HS','AS','HST','AST']].sort_values('Date', ascending=False).head(30))
    
    with tab2:
        df['Over25'] = df['TotalGoals'] > 2.5
        st.metric("La Liga Over 2.5 %", f"{df['Over25'].mean()*100:.1f}%")
        team_over = df.groupby('HomeTeam')['Over25'].mean().sort_values(ascending=False)*100
        st.bar_chart(team_over)
        st.write(team_over.round(1))
    
    with tab3:
        team = st.selectbox("Select Team", sorted(df['HomeTeam'].unique()))
        t = df[(df['HomeTeam']==team) | (df['AwayTeam']==team)].sort_values('Date', ascending=False).head(10)
        st.dataframe(t[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']])
