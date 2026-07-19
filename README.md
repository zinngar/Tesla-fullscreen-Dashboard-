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
   - Automatically expose and map it to port **`8097`** on the host.

2. **Access the Dashboard:**
   Open your browser and navigate to:
   ```text
   http://localhost:8097
   ```

### Run on CasaOS (Custom Install)

We have provided a tailored `casaos-compose.yml` that makes installation on CasaOS straightforward using standard AppData directory mapping.

1. **Import the App Configuration:**
   - Log into your CasaOS Dashboard.
   - Click **App Store** -> **Custom Install** (at the top-right corner).
   - In the import window, click the **Import** button (top-right, showing `Import YAML`).
   - Copy and paste the contents of `casaos-compose.yml` from this repository, then click **Submit**.

2. **Review Settings:**
   - The app's title, description, and branding icons will automatically populate.
   - The default host port is set to **`8097`** (preventing conflict with default Jellyfin installations).
   - The files are mapped to the correct paths on your system:
     - Config: `/DATA/AppData/jellyfin-teslafullscreen/config`
     - Cache: `/DATA/AppData/jellyfin-teslafullscreen/cache`

3. **Install and Run:**
   - Click **Save** to build and launch the container.
   - Once running, open the **TeslaFullscreen Jellyfin** app on your CasaOS dashboard!

### Technical Details (Under the Hood)
- **Automatic Volume Mapping Handling:** When mounting volumes to `/config`, files copied to the volume during the docker build are typically shadowed/hidden. To solve this, our setup copies the compiled plugin from a staging directory into the `/config/plugins/` directory *on startup* via a custom `entrypoint.sh` script.
- **Auto Permission Fixes:** The startup script automatically applies proper file permissions (`chmod 644`) to the plugin assembly DLL so that Jellyfin can load the plugin without crashes or authorization issues.

## Troubleshooting & Common Server Crashes

If your Jellyfin server crashes or fails to start after installing, look at your Jellyfin logs. The most common errors on Docker/CasaOS are:

### 1. Fatals caused by `meta.json` permission denied:
**Error in Log:**
```text
[FTL] Main: Error while starting server
System.UnauthorizedAccessException: Access to the path '/config/data/plugins/TeslaFullscreen/meta.json' is denied.
---> System.IO.IOException: Permission denied
```
* **Why this happens:** Jellyfin tries to write a status file (`meta.json`) inside the folder containing your plugin. If you uploaded the folder as `root` or another user, the Jellyfin container user (UID 1000) does not have permission to write files to that directory, causing a fatal startup crash.
* **The Fix:** Grant read/write permissions to the `plugins/TeslaFullscreen` directory by running this in your server terminal:
  ```bash
  # Change ownership of the folder to Jellyfin (UID 1000 is standard)
  sudo chown -R 1000:1000 /DATA/AppData/jellyfin/plugins/TeslaFullscreen/

  # Ensure the directory itself is writable by Jellyfin
  sudo chmod 755 /DATA/AppData/jellyfin/plugins/TeslaFullscreen/
  ```

### 2. Error loading multiple DLLs (Assembly already loaded):
**Error in Log:**
```text
[ERR] Failed to load assembly "/config/data/plugins/.../TeslaFullscreen.dll". Disabling plugin
System.IO.FileLoadException: Could not load file or assembly 'TeslaFullscreen...'. Assembly with same name is already loaded
```
* **Why this happens:** You copied the **entire source code repository folder** (containing the `obj` and `bin` build folders) directly into your `plugins` directory instead of copying **only** the `TeslaFullscreen.dll` file. Jellyfin scans all subfolders recursively and tries to load the `.dll` multiple times.
* **The Fix:** Delete the entire source repository folder from your `plugins` directory. Make sure you only have a single clean folder named `/plugins/TeslaFullscreen/` containing only the `TeslaFullscreen.dll` (and optionally `TeslaFullscreen.pdb`) file!

---

## Technical Details

- **Backend:** Flask (Python 3.12)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (no external heavy frontend framework required)
- **Data Store:** `data/links.json` (Local persistent JSON file)
- **Port Mapping:** Host `8097` maps to Container `5000`

---

## Usage Guide

1. **Add Link:** Use the left sidebar to enter a friendly Name, Target URL, and select a fitting visual icon, then click **Add Link**.
2. **Launch Fullscreen:** Simply click anywhere on a card. It will automatically load the YouTube redirect exploit, prompting the Tesla browser to transition into fullscreen mode and load your target link.
3. **Delete Link:** Hover over any card and click the trash can icon in the top right to instantly remove it.
