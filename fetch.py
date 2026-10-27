import requests
import csv
import os
from datetime import datetime, timezone, timedelta

URL = "https://allmyday.com.tw/api/product/item/46756ad6feef74d93"
CSV_PATH = "allmyday.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://allmyday.com.tw/"
}

def main():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        print("HTTP Status:", r.status_code)
        r.raise_for_status()
        data = r.json()
        
        p = data.get("data", {}).get("prod", {})
        if not p:
            print("找不到商品資料")
            return

        tw = timezone(timedelta(hours=8))
        now = datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")
        
        row = {
            "time": now,
            "sales_amount": p.get("sales_amount", 0),
            "quantity": p.get("quantity", 0),
            "title": p.get("title", "")
        }
        
        new_file = not os.path.exists(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=row.keys())
            if new_file:
                w.writeheader()
            w.writerow(row)
            
        print("Success! Data saved:", row)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
