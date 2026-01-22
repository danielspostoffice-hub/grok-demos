# 01 - Minimal Flask API

First real code commit.

## Endpoints
- GET / → {"message": "Hello from Grok demo #01"}
- GET /health → {"status": "healthy"}

## Run
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
