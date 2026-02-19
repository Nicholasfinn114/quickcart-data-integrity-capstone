import json
import csv

def normalize_amount(val):
    if val is None or val == "": return None
    if isinstance(val, (int, float)): return float(val / 100.0) # Cents to Dollars
    if isinstance(val, str):
        # Cleans "$10.00", "USD 10.00", "1,200.00"
        clean = val.replace('$', '').replace('USD', '').replace(',', '').strip()
        try: return float(clean)
        except: return None
    return None

def main():
    cleaned_data = []
    # Assuming the file is in the root during execution
    try:
        with open('quickcart_data/raw_data.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                payload = record.get('payload', {})
                entity = record.get('entity', {})
                
                # 1. Normalization
                amount = normalize_amount(payload.get('Amount'))
                
                # 2. Filtering (Remove Test and Incomplete)
                flags = payload.get('flags') or []
                is_test = "test" in flags or "test" in (entity.get('customer', {}).get('email') or "").lower()
                
                if is_test or amount is None or not entity.get('payment', {}).get('id'):
                    continue

                cleaned_data.append({
                    'payment_id': entity['payment']['id'],
                    'order_id': entity.get('order', {}).get('id'),
                    'amount_usd': amount,
                    'status': payload.get('status'),
                    'timestamp': record.get('event', {}).get('ts')
                })
        
        # Write Result
        with open('cleaned_transactions.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_data)
        print("Cleaning Successful.")
    except FileNotFoundError:
        print("Raw data not found. Run generator first.")

if __name__ == "__main__":
    main()
