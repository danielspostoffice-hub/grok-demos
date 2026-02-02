import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

user_df = df[df['role'].str.contains('human|user', case=False, na=False)].copy()
user_df['length'] = user_df['content_trunc'].str.len()

features = user_df[['length']]

model = IsolationForest(contamination=0.05, random_state=42)
user_df['anomaly'] = model.fit_predict(features)

anomalies = user_df[user_df['anomaly'] == -1]

print(f"Found {len(anomalies)} anomaly prompts (5% contamination).")
print("\nAnomaly examples (length, content):")
for _, row in anomalies.head(10).iterrows():
    print(f"Length {row['length']}: {row['content_trunc']}")