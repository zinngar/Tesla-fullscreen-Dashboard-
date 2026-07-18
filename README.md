# TeslaFullscreen Jellyfin Plugin

A custom Jellyfin plugin designed to allow users to easily open external web links (like self-hosted services, home automation, or other media sites) in full screen on the Tesla browser by utilizing the YouTube redirect exploit.

Because the Tesla browser does not natively allow bookmarking links that automatically open in full-screen mode, this plugin provides a centralized dashboard in Jellyfin containing all your target links. Bookmarking this custom Jellyfin tab on your Tesla browser lets you easily open any designated link in full screen with a single click.

## Features

- **Centralized Admin Dashboard:** Administrators can dynamically add, view, and delete links (storing them server-side inside the plugin's configuration XML).
- **"Tesla Links" Sidebar Tab:** Available to all logged-in users, providing a clean interface with a "Launch" / "Open Fullscreen" button next to each link.
- **YouTube Redirect Exploit Support:** Generates and launches links using the standard `https://www.youtube.com/redirect?q={TARGET_URL}` exploit to unlock full-screen capabilities on the Tesla browser.
- **Clean C# Backend & HTML5/JS Frontend:** Uses lightweight ASP.NET Core MVC Controllers and native Jellyfin Web Client UI components.

## Technical Details

- **Target Framework:** `.NET 8.0` (compatible with Jellyfin 10.9.x)
- **Plugin Name:** `TeslaFullscreen`
- **Plugin ID:** `eb5d7894-8eef-4b36-aa6f-5d124e828ce1`

## Project Structure

- `TeslaFullscreen/Plugin.cs` - Main plugin registration and lifecycle management. Exposes user-level and admin-level custom web pages.
- `TeslaFullscreen/Configuration/PluginConfiguration.cs` - Handles serialization and persistence of the dynamic link list.
- `TeslaFullscreen/Configuration/TeslaLink.cs` - Data model representing a saved link (`Name` and `Url`).
- `TeslaFullscreen/Configuration/configPage.html` - HTML and JavaScript configuration page for Administrators to manage links.
- `TeslaFullscreen/Configuration/teslaLinksPage.html` - HTML and JavaScript page rendered under the main sidebar ("Tesla Links") for all users to launch links in fullscreen.
- `TeslaFullscreen/Controller/TeslaFullscreenController.cs` - REST API endpoints handling link operations with appropriate user and administrator authorization levels.

## How to Build

To build the plugin from source:

1. Install the [.NET SDK 8.0](https://dotnet.microsoft.com/download/dotnet) (or matching version for your Jellyfin release).
2. Build the solution in Release mode:
   ```bash
   dotnet build -c Release
   ```
3. The compiled binary (`TeslaFullscreen.dll`) and debug symbols (`TeslaFullscreen.pdb`) will be available in the `TeslaFullscreen/bin/Release/net8.0/` folder.

---

## How to Install (Foolproof Guide)

To install the plugin on your Jellyfin server, you **must** follow the steps below carefully to prevent Jellyfin from crashing or failing to start.

### Step 1: Identify the Correct Files
After compiling (or downloading a release), navigate to your build output folder (e.g., `TeslaFullscreen/bin/Release/net8.0/`).
- **Files to COPY:**
  - `TeslaFullscreen.dll` (Required)
  - `TeslaFullscreen.pdb` (Optional, provides detailed logs if errors occur)
- **Files to IGNORE (Do NOT copy these!):**
  - Do **NOT** copy any core Jellyfin assemblies (e.g., `Jellyfin.Controller.dll`, `Jellyfin.Model.dll`, `MediaBrowser.Common.dll`).
  - Do **NOT** copy any StyleCop or Code Analyzer files (e.g., `StyleCop.Analyzers.dll`, `SerilogAnalyzer.dll`).
  - *Why?* Copying core Jellyfin or analyzer libraries into the plugin directory will cause Jellyfin to fail to load the plugin or crash on startup due to duplicate assembly errors.

### Step 2: Create the Plugin Folder
Jellyfin **requires** every plugin to have its own dedicated subfolder under the main `plugins` folder.
1. Locate your Jellyfin server's `plugins` folder (see [Common Paths](#common-paths) below).
2. Inside `plugins/`, create a new subfolder named **exactly** `TeslaFullscreen`.
   - **Correct structure:** `/path/to/jellyfin/plugins/TeslaFullscreen/`
   - **Incorrect structure:** `/path/to/jellyfin/plugins/TeslaFullscreen.dll` (Putting the DLL directly in the `plugins` root will not work!)

### Step 3: Copy Files and Set File Permissions
Copy only `TeslaFullscreen.dll` (and optionally `TeslaFullscreen.pdb`) into the new `TeslaFullscreen` folder.

#### ⚠️ Critical for Docker and CasaOS Users:
When you upload files via SFTP or the CasaOS Files app, they are often owned by `root` or `casaos` with restrictive permissions. Since Jellyfin inside Docker runs under a non-root user (typically UID 1000), it will not have permission to read the uploaded `.dll` file, causing Jellyfin to crash, freeze, or ignore the plugin on startup.

To fix this, you must set the correct permissions:
1. SSH into your server or open a terminal.
2. Navigate to your Jellyfin plugins directory, for example:
   ```bash
   cd /DATA/AppData/jellyfin/plugins/TeslaFullscreen/
   ```
3. Run the following commands to ensure the file is readable by the Jellyfin container:
   ```bash
   # Make sure the DLL is readable by everyone
   chmod 644 TeslaFullscreen.dll

   # Optional: Set the correct ownership (UID 1000 is standard for CasaOS/Docker apps)
   chown -R 1000:1000 /DATA/AppData/jellyfin/plugins/TeslaFullscreen/
   ```

### Step 4: Restart Jellyfin
- **CasaOS:** Go to your CasaOS dashboard, find the Jellyfin card, click the three dots (`...`), and select **Restart**.
- **Docker Compose:** Run `docker compose restart jellyfin` in your terminal.
- **Systemd (Linux):** Run `sudo systemctl restart jellyfin`.

---

## Common Paths

Depending on your installation type, the standard paths to the `plugins` directory are:

| Platform / Method | Typical `plugins` Folder Path |
| :--- | :--- |
| **CasaOS (Docker)** | `/DATA/AppData/jellyfin/plugins/` or `/DATA/AppData/jellyfin/config/plugins/` |
| **Docker (Standard)** | Look for the path mapped to `/config` in your volume bindings (e.g. `source_path/plugins/`) |
| **Linux (Native)** | `/var/lib/jellyfin/plugins/` |
| **Windows** | `%ProgramData%\Jellyfin\Server\plugins\` |
| **macOS** | `~/.config/jellyfin/plugins/` |

---

## Usage

1. **Adding Links (Admin):**
   - Log into your Jellyfin server as an administrator.
   - Go to the **Admin Dashboard** -> **Plugins** -> **TeslaFullscreen**.
   - Enter a descriptive Name (e.g. `Jellyfin` or `Home Assistant`) and the Target URL (e.g. `157.211.157.120:8096`).
   - Click **Add Link**. The link will be saved server-side.

2. **Accessing and Launching Links (All Users):**
   - On the Tesla browser, log into your Jellyfin server.
   - Click the **Tesla Links** tab in the sidebar/navigation menu.
   - Bookmark this tab in your Tesla browser for quick access.
   - Click **Open Fullscreen** next to any link. It will launch YouTube, which immediately redirects and opens your target link in full screen!
