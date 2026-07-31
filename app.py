from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "links.json")

def load_links():
    if not os.path.exists(DATA_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_links(links):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(links, f, indent=2)

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
