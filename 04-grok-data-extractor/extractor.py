import json
import csv
from datetime import datetime
from pathlib import Path

# FULL EXACT EXPORT ROOT - copy Explorer address bar when in UUID folder, Ctrl+C, paste into r""
EXPORT_ROOT = Path(r"C:\Users\Dan\Documents\grok-demos\24JAN2026-Grok-Data\ttl\30d\export_data\62ddaafa-1458-4278-bb4e-0df30d49ddf5")

def find_convo_jsons():
    all_json = list(EXPORT_ROOT.glob("*.json"))
    safe_json = [p for p in all_json if "billing" not in p.name.lower() and "auth" not in p.name.lower()]
    print(f"Found {len(all_json)} root JSON, processing {len(safe_json)} safe.")
    return safe_json

def load_convo(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def extract_and_export(convo_jsons):
    convos = 0
    total_messages = 0
    user_messages = 0
    assistant_messages = 0
    csv_rows = [["file", "convo_index", "msg_index", "role", "content_trunc", "timestamp"]]
    
    for jp in convo_jsons:
        try:
            data = load_convo(jp)
            conversations = data.get("conversations", [])
            for convo_idx, convo_wrapper in enumerate(conversations):
                convo = convo_wrapper.get("conversation", {})
                responses = convo_wrapper.get("responses", [])
                convos += 1
                total_messages += len(responses)
                
                for idx, resp_wrapper in enumerate(responses):
                    resp = resp_wrapper.get("response", {})
                    role = resp.get("sender", "unknown").lower()
                    content = resp.get("message", "")
                    content_trunc = content[:200] + "..." if len(content) > 200 else content
                    ct = resp.get("create_time", {})
                    ts = ""
                    if isinstance(ct, dict) and "$date" in ct:
                        ts = datetime.fromtimestamp(int(ct["$date"]["$numberLong"]) / 1000).isoformat()
                    elif isinstance(ct, str):
                        ts = ct
                    
                    if "human" in role or "user" in role:
                        user_messages += 1
                    elif "assistant" in role or "grok" in role:
                        assistant_messages += 1
                    
                    csv_rows.append([jp.name, convo_idx, idx, role, content_trunc, ts])
        except Exception as e:
            print(f"Skip {jp.name}: {e}")
    
    print(f"\nStats:")
    print(f"Conversations: {convos}")
    print(f"Total messages: {total_messages}")
    print(f"User/human: {user_messages}")
    print(f"Assistant: {assistant_messages}")
    
    csv_path = Path("extracted_messages.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
    print(f"\nCSV exported to {csv_path} ({len(csv_rows)-1} messages).")

if __name__ == "__main__":
    if not EXPORT_ROOT.exists():
        raise ValueError(f"Root wrong: {EXPORT_ROOT}")
    
    convo_jsons = find_convo_jsons()
    if convo_jsons:
        print("\nSample first convo preview (truncated):")
        sample = load_convo(convo_jsons[0])
        print(json.dumps(sample, indent=2)[:2500] + "...")
        
        extract_and_export(convo_jsons)
    else:
        print("Zero safe JSON.")