import pandas as pd
from pathlib import Path
from collections import Counter

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

print(f"Loaded {len(df)} message rows.")

df['length'] = df['content_trunc'].str.len()
print("\nLength stats:")
print(df['length'].describe())

print("\nRole counts:")
print(df['role'].value_counts())

df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
daily = df.groupby(df['ts'].dt.date).size()
print("\nDaily messages:")
print(daily.to_string())

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
top_opening = user_df[user_df.groupby('convo_index').cumcount() == 0]['content_trunc'].value_counts().head(20)
print("\nTop opening user prompts:")
print(top_opening)

user_words = ' '.join(user_df['content_trunc'].dropna()).lower().split()
top_words = Counter(user_words).most_common(30)
print("\nTop user words:")
print(top_words)