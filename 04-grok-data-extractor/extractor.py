import json
from datetime import datetime
from pathlib import Path

# ROOT OF EXPORT - keep full, script filters to safe convo folder
EXPORT_ROOT = Path(r"C:\Users\Dan\Downloads\24JAN2026 Grok Data\ttl\30d\export_data\62ddaaafa-1458-4278-bb4e-0df30d49ddff5")

# Subfolder with actual convos
ASSET_FOLDER = EXPORT_ROOT / "prod-mc-asset-server"

def find_convo_jsons():
    if not ASSET_FOLDER.exists():
        raise ValueError(f"Asset folder missing: {ASSET_FOLDER} - check path")
    
    # One JSON per convo subfolder
    convo_jsons = list(ASSET_FOLDER.rglob("*.json"))
    print(f"Found {len(convo_jsons)} potential convo JSON files in asset server.")
    return convo_jsons

def load_convo(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def extract_stats(convo_jsons):
    convos = 0
    total_messages = 0
    dates = []
    user_messages = 0
    assistant_messages = 0
    
    for jp in convo_jsons:
        try:
            data = load_convo(jp)
            # Grok convo JSON usually dict with "messages" list
            if "messages" in data:
                messages = data["messages"]
                msg_count = len(messages)
                total_messages += msg_count
                convos += 1
                
                # Role split
                for msg in messages:
                    role = msg.get("role") or msg.get("author", "").lower()
                    if "user" in role:
                        user_messages += 1
                    elif "assistant" in role or "grok" in role:
                        assistant_messages += 1
                
                # Date from metadata or first message
                ct = data.get("create_time") or data.get("created_at")
                if not ct and messages:
                    ct = messages[0].get("timestamp") or messages[0].get("create_time")
                if ct:
                    if isinstance(ct, (int, float)):
                        dates.append(datetime.fromtimestamp(ct))
                    else:
                        dates.append(datetime.fromisoformat(ct.replace("Z", "+00:00")))
        except Exception as e:
            print(f"Skip bad file {jp.name}: {e}")
    
    print(f"\nExtraction complete (billing/auth skipped automatically).")
    print(f"Conversations processed: {convos}")
    print(f"Total messages: {total_messages}")
    print(f"User messages: {user_messages}")
    print(f"Assistant messages: {assistant_messages}")
    if dates:
        print(f"Date range: {min(dates)} to {max(dates)}")

if __name__ == "__main__":
    if not EXPORT_ROOT.exists():
        raise ValueError(f"Export root wrong: {EXPORT_ROOT}")
    
    convo_jsons = find_convo_jsons()
    if convo_jsons:
        print("\nSample first convo preview (truncated):")
        sample = load_convo(convo_jsons[0])
        print(json.dumps(sample, indent=2)[:2500] + ("..." if len(json.dumps(sample, indent=2)) > 2500 else ""))
        
        extract_stats(convo_jsons)
    else:
        print("Zero convo JSON - path off or export empty.")