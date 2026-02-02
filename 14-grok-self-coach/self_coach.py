import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
prompts = user_df['content_trunc'].dropna().tolist()

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("prompts", embedding_function=SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2"))

if collection.count() == 0:
    batch_size = 5000
    for i in range(0, len(prompts), batch_size):
        batch_prompts = prompts[i:i+batch_size]
        batch_ids = [str(j) for j in range(i, i+len(batch_prompts))]
        collection.add(documents=batch_prompts, ids=batch_ids)
    print("DB built.")
else:
    print("DB loaded.")

query = input("Self-coach query (e.g., 'what are my top themes?'): ")
results = collection.query(query_texts=[query], n_results=10)

print("\nRelevant past prompts:")
for doc in results['documents'][0]:
    print(f"- {doc}")