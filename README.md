# Tesla Fullscreen Dashboard

A lightweight, beautiful, dark-mode web application hosted inside a Docker container designed to easily launch any website in full screen on a Tesla browser with a single click.

## Features

- **No Logins Required:** Designed for quick convenience on phones, tablets, or the Tesla browser itself. Anyone on the local network can manage links.
- **Modern Dark-Mode Dashboard:** A responsive UI styled with Tailwind CSS, designed specifically to look stunning on the Tesla screen.
- **Interactive Icon Picker:** Choose from pre-configured emojis (📺 TV, 🏠 Home, 🎮 Games, 🎵 Music, etc.) to give each link card its own unique visual icon.
- **YouTube Redirect Exploit Support:** Automatically wraps and launches your links using the standard `https://www.youtube.com/redirect?q={TARGET_URL}` exploit, allowing the Tesla browser to run any destination in full screen.
- **Persistent Storage:** Saves all configured links to a simple JSON file mounted via docker volumes, ensuring data survives restarts.

---

## Quick Start (with Docker Compose)

1. **Start the App:**
   From the root of the repository, simply run:
   ```bash
   docker compose up -d --build
   ```
   This will:
   - Build a lightweight `python:3.12-alpine` container.
   - Run the Flask web application on port `5000` inside the container.
   - Automatically expose and map it to port **`5000`** on the host.

2. **Access the Dashboard:**
   Open your browser and navigate to:
   ```text
   http://localhost:5000
   ```

3. **Bookmark on Tesla:**
   Open `http://<YOUR_SERVER_IP>:5000` in your Tesla's browser and bookmark the page for quick, one-click access.

---

## Technical Details

- **Backend:** Flask (Python 3.12)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (no external heavy frontend framework required)
- **Data Store:** `data/links.json` (Local persistent JSON file)
- **Port Mapping:** Host `5000` maps to Container `5000`

---

## Usage Guide

1. **Add Link:** Use the left sidebar to enter a friendly Name, Target URL, and select a fitting visual icon, then click **Add Link**.
2. **Launch Fullscreen:** Simply click anywhere on a card. It will automatically load the YouTube redirect exploit, prompting the Tesla browser to transition into fullscreen mode and load your target link.
3. **Delete Link:** Hover over any card and click the trash can icon in the top right to instantly remove it.
