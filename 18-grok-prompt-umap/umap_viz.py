import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from umap import UMAP

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
opening = user_df[user_df.groupby('convo_index').cumcount() == 0]['content_trunc'].dropna()

vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X = vectorizer.fit_transform(opening)

reducer = UMAP(n_components=2, random_state=42)
embedding = reducer.fit_transform(X)

umap_df = pd.DataFrame(embedding, columns=['x', 'y'])
umap_df['prompt'] = opening.reset_index(drop=True)

fig = px.scatter(umap_df, x='x', y='y', hover_data=['prompt'], title="UMAP Prompt Embeddings (hover for text)")
fig.show()