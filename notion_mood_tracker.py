import os
import requests

# API võtmed keskkonnamuutujatest
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

print("🚀 Skript käivitub!")
if not NOTION_API_KEY or not DATABASE_ID:
    print("❌ API võtmed puuduvad! Kontrolli GitHub Secrets.")
    exit(1)

# Notioni tuju ja värvi kaardistus
MOOD_COLORS = {
    "tänulik": "#e6fff2",
    "üksildane": "#e6ffff",
    "segaduses": "#ffebcc",
    "innustunud": "#ffffb3",
    "ärev": "#f0b3ff",
    "rahulik": "#ccffcc",
    "vihane": "#ff3333",
    "kurb": "#99e6ff",
    "rõõmus": "#ffb3ff"
}

def get_pages():
    """Küsib Notioni kirjed."""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    print(f"🔄 API vastus: {response.status_code}")
    if response.status_code != 200:
        print("❌ API error! Kontrolli API võtit ja database ID-d.")
        return []
    return response.json().get("results", [])

def update_page_color(page_id, mood):
    """Uuendab Notion kirje värvi."""
    color = MOOD_COLORS.get(mood.lower(), "#ffffff")
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    data = {
        "properties": {
            "Värv": {"rich_text": [{"text": {"content": color}}]}
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    print(f"🎨 Uuendasin {mood} värviks {color}: {response.status_code}")

# Käivitame skripti
pages = get_pages()
if pages:
    for page in pages:
        mood = page["properties"].get("Tuju", {}).get("select", {}).get("name", "").lower()
        if mood in MOOD_COLORS:
            update_page_color(page["id"], mood)
