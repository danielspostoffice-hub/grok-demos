import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
daily = df.groupby(df['ts'].dt.date).size().reset_index(name='messages')
fig1 = px.bar(daily, x='ts', y='messages', title="Daily Grok Messages")
fig1.show()

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
opening = user_df[user_df.groupby('convo_index').cumcount() == 0]['content_trunc'].dropna()

vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X = vectorizer.fit_transform(opening)

kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
kmeans.fit(X)

opening_df = pd.DataFrame({'prompt': opening.reset_index(drop=True), 'cluster': kmeans.labels_})
fig2 = px.scatter(opening_df, x=opening_df.index, y='cluster', hover_data=['prompt'], title="Prompt Clusters (hover for text)")
fig2.show()