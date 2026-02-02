import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
opening = user_df[user_df.groupby('convo_index').cumcount() == 0]['content_trunc'].dropna()

print(f"Clustering {len(opening)} opening prompts.")

vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X = vectorizer.fit_transform(opening)

kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
kmeans.fit(X)

clusters = pd.Series(kmeans.labels_)
top_terms = vectorizer.get_feature_names_out()

print("\nTop 10 clusters (5 top terms each):")
for i in range(10):
    terms = [top_terms[j] for j in kmeans.cluster_centers_[i].argsort()[-5:][::-1]]
    count = (clusters == i).sum()
    print(f"Cluster {i} ({count} prompts): {', '.join(terms)}")

print("\nExample prompts per cluster:")
for i in range(10):
    cluster_mask = clusters == i
    cluster_opening = opening.reset_index(drop=True)[cluster_mask.reset_index(drop=True)]
    examples = cluster_opening.head(3).tolist()
    print(f"Cluster {i}:")
    for ex in examples:
        print(f" - {ex}")
    print()