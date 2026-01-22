# 02 - xAI API Client

Direct integration with Grok via xAI API. Proves I can call Grok programmatically.

## Why
Highest relevance to xAI. No more toy web servers—this touches the actual product.

## Setup
1. Get API key: https://x.ai/api → links to console (likely console.grok.x.ai). Generate key.
2. Copy .env.example → .env and paste your key.
3. Models/pricing: https://docs.x.ai/docs/models

## Run
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python client.py
