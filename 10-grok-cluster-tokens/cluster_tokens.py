import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

# Opening prompts + rough tokens
user_df = df[df['role'].str.contains('human|user', case=False, na=False)].copy()
user_df['tokens'] = (user_df['content_trunc'].str.len() // 3) + 10  # Conservative estimate

opening = user_df[user_df.groupby('convo_index').cumcount() == 0]

vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X = vectorizer.fit_transform(opening['content_trunc'].dropna())

kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
kmeans.fit(X)

opening['cluster'] = kmeans.labels_

cluster_tokens = opening.groupby('cluster')['tokens'].sum()

print("Rough tokens per cluster:")
for cluster, tokens in cluster_tokens.items():
    print(f"Cluster {cluster}: {tokens:,} tokens")

print("\nTop terms per cluster (context):")
top_terms = vectorizer.get_feature_names_out()
for i in range(10):
    terms = [top_terms[j] for j in kmeans.cluster_centers_[i].argsort()[-5:][::-1]]
    print(f"Cluster {i}: {', '.join(terms)}")