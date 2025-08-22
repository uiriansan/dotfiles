import requests, time, sqlite3, json
from calendar import monthrange
from pathlib import Path

WIKIPEDIA_ENDPOINT = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all"
MAX_ATTEMPTS = 10
attempts = 0

DB_PATH = "./facts.db"

def get_facts_from_day(i_day, i_month, con, cur):
    for month in range(i_month, 13):
        ( _, days ) = monthrange(2012, month)
        for day in range(i_day, days + 1):
            response = requests.get(f"{WIKIPEDIA_ENDPOINT}/{month:02}/{day:02}")
            if response.status_code == 200:
                data = response.json()
                
                for key, facts in data.items():
                    for i in range(len(facts)):
                        text = facts[i].get('text')
                        year = facts[i].get('year') or 'NULL'
                        pages_raw = facts[i].get('pages')
                        pages = [
                            {
                                "title": page.get("title"),
                                "thumb": page.get("thumbnail").get("source") if page.get("thumbnail") else "",
                                "url": page.get("content_urls").get("desktop").get("page") if page.get("content_urls") and page.get("content_urls").get("desktop") else ""
                            }
                            for page in pages_raw
                        ]
                        facts[i] = (text, key, day, month, year, json.dumps(pages))

                facts = data["selected"] + data["births"] + data["deaths"] + data["events"] + data["holidays"]
                print(f"\033[32m[{day:02}/{month:02} OK] ->\033[37m Fetched {len(facts)} facts.")

                cur.executemany("INSERT INTO Facts VALUES (?, ?, ?, ?, ?, ?)", facts)
                con.commit()
            else:
                print(f"\033[31m[{day:02}/{month:02} ERROR] ->\033[37m Retrying in 10s...")
                if attempts < MAX_ATTEMPTS:
                    time.sleep(10)
                    return get_facts_from_day(day, month, con, cur)

            time.sleep(5)

if __name__ == "__main__":
    resolved_db_path = Path(DB_PATH).resolve()
    if resolved_db_path.is_file():
        try:
            # Delete DB if exists
            resolved_db_path.unlink()
        except Exception as e:
            print(f"Error: {e}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Create DB
    cur.execute("""
        CREATE TABLE Facts(
            text TEXT NOT NULL,
            type TEXT NOT NULL,
            day INT NOT NULL, 
            month INT NOT NULL, 
            year INT, 
            pages TEXT
        )
    """)

    get_facts_from_day(1, 1, con, cur)

    con.close()
