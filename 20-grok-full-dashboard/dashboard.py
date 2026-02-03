import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Grok Usage Full Dashboard")

CSV_PATH = Path("../04-grok-data-extractor/extracted_messages.csv")

df = pd.read_csv(CSV_PATH, encoding='utf-8', encoding_errors='replace')

st.header("Daily Messages")
df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
daily = df.groupby(df['ts'].dt.date).size().reset_index(name='messages')
fig1 = px.bar(daily, x='ts', y='messages')
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

st.header("Self-Coach Reflection")
query = st.text_input("Query your patterns")
if query:
    user_df = df[df['role'].str.contains('human|user', case=False, na=False)]
    prompts = user_df['content_trunc'].dropna().tolist()

    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection("prompts", embedding_function=SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2"))

    if collection.count() == 0:
        st.write("Building DB (first run)...")
        batch_size = 5000
        for i in range(0, len(prompts), batch_size):
            batch_prompts = prompts[i:i+batch_size]
            batch_ids = [str(j) for j in range(i, i+len(batch_prompts))]
            collection.add(documents=batch_prompts, ids=batch_ids)
        st.write("DB built.")
    else:
        st.write("DB loaded.")

    results = collection.query(query_texts=[query], n_results=20)
    context = "\n\n".join(results['documents'][0])

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        st.error("XAI_API_KEY missing in .env")
    else:
        grok_client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        response = grok_client.chat.completions.create(
            model="grok-4-fast",
            messages=[
                {"role": "system", "content": "Reflective coach. Summarize patterns/themes from user's past prompts. Concise, insightful."},
                {"role": "user", "content": f"Query: {query}\n\nRelevant past prompts:\n{context}"}
            ],
            max_tokens=800
        )
        st.write(response.choices[0].message.content)