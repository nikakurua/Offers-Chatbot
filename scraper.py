import requests
import json
import time

BASE_URL = "https://bankofgeorgia.ge/api/bog-b/offers-hub/get-offers"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://bankofgeorgia.ge",
    "referer": "https://bankofgeorgia.ge/ka/offers-hub/catalog",
    "user-agent": "Mozilla/5.0"
}

all_offers = []
seen_ids = set()

r = requests.post(f"{BASE_URL}?pageInfo=true&pageNumber=0&pageSize=10", headers=HEADERS, json={})
payload = r.json()

total_pages = payload["result"]["totalPageCount"]
print("Total pages:", total_pages)

for page in range(total_pages):
    print(f"Fetching page {page+1}/{total_pages}")

    r = requests.post(
        f"{BASE_URL}?pageInfo=true&pageNumber={page}&pageSize=10",
        headers=HEADERS,
        json={}
    )

    data = r.json()
    offers = data["result"]["offers"]

    for offer in offers:
        cid = offer["campaignId"]
        if cid not in seen_ids:
            seen_ids.add(cid)
            all_offers.append(offer)

    time.sleep(0.3)

print("Total unique offers:", len(all_offers))

with open("offers.json", "w", encoding="utf-8") as f:
    json.dump(all_offers, f, ensure_ascii=False, indent=2)

print("Finished")
