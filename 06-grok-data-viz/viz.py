import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from wordcloud import WordCloud

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
daily = df.groupby(df['ts'].dt.date).size()
daily.plot(kind='bar', figsize=(16,8), title="Daily Grok Messages", color='skyblue')
plt.xlabel("Date")
plt.ylabel("Messages")
plt.tight_layout()
plt.show()

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
user_text = ' '.join(user_df['content_trunc'].dropna())
wc = WordCloud(width=1200, height=600, background_color='black', colormap='viridis').generate(user_text)
plt.figure(figsize=(12,6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Your Grok Prompt Themes")
plt.show()