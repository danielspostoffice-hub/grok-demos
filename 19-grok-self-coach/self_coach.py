import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

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

query = input("Self-coach query: ")
results = collection.query(query_texts=[query], n_results=20)

context = "\n\n".join(results['documents'][0])

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise ValueError("XAI_API_KEY not in .env")

grok_client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

response = grok_client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "system", "content": "You are a reflective coach. Summarize patterns/themes from user's past prompts. Be concise, insightful."},
        {"role": "user", "content": f"Query: {query}\n\nRelevant past prompts:\n{context}"}
    ],
    max_tokens=800
)

print("\nGrok self-coach:")
print(response.choices[0].message.content)