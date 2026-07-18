# TeslaFullscreen Jellyfin Plugin

A custom Jellyfin plugin designed to allow users to easily open external web links (like self-hosted services, home automation, or other media sites) in full screen on the Tesla browser by utilizing the YouTube redirect exploit.

Because the Tesla browser does not natively allow bookmarking links that automatically open in full-screen mode, this plugin provides a centralized dashboard in Jellyfin containing all your target links. Bookmarking this custom Jellyfin tab on your Tesla browser lets you easily open any designated link in full screen with a single click.

## Features

- **Centralized Admin Dashboard:** Administrators can dynamically add, view, and delete links (storing them server-side inside the plugin's configuration XML).
- **"Tesla Links" Sidebar Tab:** Available to all logged-in users, providing a clean interface with a "Launch" / "Open Fullscreen" button next to each link.
- **YouTube Redirect Exploit Support:** Generates and launches links using the standard `https://www.youtube.com/redirect?q={TARGET_URL}` exploit to unlock full-screen capabilities on the Tesla browser.
- **Clean C# Backend & HTML5/JS Frontend:** Uses lightweight ASP.NET Core MVC Controllers and native Jellyfin Web Client UI components.

## Technical Details

- **Target Framework:** `.NET 9.0`
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

1. Install the [.NET SDK 9.0](https://dotnet.microsoft.com/download/dotnet).
2. Build the solution:
   ```bash
   dotnet build
   ```
3. The compiled binary (`TeslaFullscreen.dll`) will be available in the `TeslaFullscreen/bin/Debug/net9.0/` folder.

## How to Install

1. Navigate to your self-hosted Jellyfin server data directory.
2. Under the `plugins` folder, create a new subfolder named `TeslaFullscreen`:
   ```bash
   mkdir -p /path/to/jellyfin/plugins/TeslaFullscreen/
   ```
3. Copy the compiled `TeslaFullscreen.dll` file and any accompanying `.pdb` files into the newly created folder.
4. Restart your Jellyfin server.

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
