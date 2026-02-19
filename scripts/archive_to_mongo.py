import json
from pymongo import MongoClient

def archive():
    # Connection string for archival
    client = MongoClient('mongodb://localhost:27017/')
    db = client['quickcart_archive']
    
    with open('quickcart_data/raw_data.jsonl', 'r') as f:
        logs = [json.loads(line) for line in f]
        if logs:
            db.raw_logs.insert_many(logs)
            print(f"Archived {len(logs)} logs to MongoDB.")

if __name__ == "__main__":
    archive()
