import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("Grok Usage Dashboard")

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

st.header("Daily Messages")
df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
daily = df.groupby(df['ts'].dt.date).size().reset_index(name='messages')
fig1 = px.bar(daily, x='ts', y='messages', title="Daily Messages")
st.plotly_chart(fig1)

st.header("Role Counts")
st.write(df['role'].value_counts())

st.header("Length Stats")
df['length'] = df['content_trunc'].str.len()
st.write(df['length'].describe())

st.header("Top Opening Prompts")
user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
opening = user_df[user_df.groupby('convo_index').cumcount() == 0]['content_trunc']
st.write(opening.value_counts().head(20))