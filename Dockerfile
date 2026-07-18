# Stage 1: Build the plugin
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy solution and project files
COPY TeslaFullscreen.sln Directory.Build.props jellyfin.ruleset ./
COPY TeslaFullscreen/TeslaFullscreen.csproj TeslaFullscreen/

# Restore dependencies
RUN dotnet restore

# Copy all sources and build
COPY TeslaFullscreen/ TeslaFullscreen/
RUN dotnet build -c Release -o /app/build

# Stage 2: Create runtime image
FROM jellyfin/jellyfin:10.9.11 AS runtime

# Create plugins staging directory
WORKDIR /app/plugins/TeslaFullscreen
COPY --from=build /app/build/TeslaFullscreen.dll .
COPY --from=build /app/build/TeslaFullscreen.pdb .

# Setup custom entrypoint to copy plugin to /config/plugins at startup
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
