import requests
import csv
import time
import os

url = 'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-IN,en;q=0.9,en-US;q=0.8,hi;q=0.7,ne;q=0.6',
    'origin': 'https://bdggame3.com',
    'priority': 'u=1, i',
    'referer': 'https://bdggame3.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

csv_file = 'wingo_live_data.csv'
fetched_ids = set()

# Load or create CSV file
if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['issueNumber', 'bigOrSmall', 'color', 'premium', 'sum'])
    print("📁 New CSV file created.")
else:
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row:
                fetched_ids.add(row[0])

print(f"📄 Loaded {len(fetched_ids)} existing outcomes")

# 🔁 Run infinitely
while True:
    try:
        ts = int(time.time() * 1000)
        response = requests.get(f"{url}?ts={ts}", headers=headers)
        if response.status_code == 200:
            latest_item = response.json()['data']['list'][0]
            issue_id = latest_item['issueNumber']
            if issue_id not in fetched_ids:
                number = int(latest_item['number'])
                big_or_small = 'Small' if number <= 4 else 'Big'

                with open(csv_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        issue_id,
                        big_or_small,
                        latest_item['color'],
                        latest_item['premium'],
                        latest_item['sum']
                    ])
                fetched_ids.add(issue_id)
                print(f"✅ Added {big_or_small} | 🔢 Total: {len(fetched_ids)} | ID: {issue_id}")
            else:
                print(f"⏸️ Waiting... No new outcome yet | Latest: {issue_id}")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
    except Exception as e:
        print(f"⚠️ Exception: {e}")

    time.sleep(60)  # ⏲️ Wait 1 minute before checking again
