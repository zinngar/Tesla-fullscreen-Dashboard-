from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "links.json")
BACKUP_FILE = os.path.join(DATA_DIR, "links.json.bak")
TMP_FILE = os.path.join(DATA_DIR, "links.json.tmp")

DEFAULT_LINKS = [
    {
        "name": "Jellyfin",
        "url": "http://192.168.1.100:8096",
        "icon": "📺"
    },
    {
        "name": "Home Assistant",
        "url": "http://192.168.1.100:8123",
        "icon": "🏠"
    },
    {
        "name": "Plex",
        "url": "http://192.168.1.200:32400",
        "icon": "💡"
    }
]

def save_links(links):
    os.makedirs(DATA_DIR, exist_ok=True)
    # Write to temporary file first for atomic save
    with open(TMP_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    os.replace(TMP_FILE, DATA_FILE)
    # Maintain backup copy
    try:
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_links():
    os.makedirs(DATA_DIR, exist_ok=True)
    # 1. Try loading main data file
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass

    # 2. Try restoring from backup file
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    save_links(data)
                    return data
        except Exception:
            pass

    # 3. Fallback to default links if missing or corrupted
    save_links(DEFAULT_LINKS)
    return DEFAULT_LINKS

@app.route("/")
def index():
    links = load_links()
    return render_template("index.html", links=links)

@app.route("/add", methods=["POST"])
def add_link():
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    icon = request.form.get("icon", "🌐").strip()

    if icon == "custom":
        icon = request.form.get("custom_icon", "🌐").strip()
    if not icon:
        icon = "🌐"

    if name and url:
        # Check if protocol is specified, if not default to http://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        links = load_links()
        # Remove duplicate name if any (case-insensitive)
        links = [l for l in links if l.get("name", "").lower() != name.lower()]
        links.append({
            "name": name,
            "url": url,
            "icon": icon
        })
        save_links(links)
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["POST"])
def edit_link(index):
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    icon = request.form.get("icon", "🌐").strip()

    if icon == "custom":
        icon = request.form.get("custom_icon", "🌐").strip()
    if not icon:
        icon = "🌐"

    if name and url:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        links = load_links()
        if 0 <= index < len(links):
            links[index] = {
                "name": name,
                "url": url,
                "icon": icon
            }
            save_links(links)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete_link(index):
    links = load_links()
    if 0 <= index < len(links):
        links.pop(index)
        save_links(links)
    return redirect(url_for("index"))

@app.route("/reorder/<int:index>/<direction>")
def reorder_link(index, direction):
    links = load_links()
    if 0 <= index < len(links):
        if direction == "up" and index > 0:
            links[index], links[index - 1] = links[index - 1], links[index]
        elif direction == "down" and index < len(links) - 1:
            links[index], links[index + 1] = links[index + 1], links[index]
        save_links(links)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
