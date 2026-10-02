# Servarr Status

Lightweight Docker web dashboard for monitoring homelab media services.

Supported services:
- Sonarr
- Radarr
- Bazarr
- Fetcharr
- FlareSolverr
- Jackett
- Plungarr

## Environment variables

- `SONARR_URL`
- `SONARR_API_KEY`
- `RADARR_URL`
- `RADARR_API_KEY`
- `BAZARR_URL`
- `BAZARR_API_KEY`
- `FETCHARR_URL`
- `FLARESOLVERR_URL`
- `JACKETT_URL`
- `JACKETT_API_KEY`
- `PLUNGARR_URL`

The web interface listens on port `8080`.

## Health checks

- Sonarr/Radarr: `/api/v3/system/status`
- Bazarr: `/api/system/ping`
- FlareSolverr: `/health`
- Jackett: server config API
- Fetcharr/Plungarr: generic HTTP reachability when a URL is configured

If Fetcharr or Plungarr do not expose an HTTP endpoint in your deployment, leave their URL blank and the dashboard will show `NOT CONFIGURED` rather than incorrectly reporting them offline.

## Unraid

Image:

`ghcr.io/utgard21/servarr-status:latest`

Container port:

`8080 -> host port 8090`

Then open:

`http://UNRAID-IP:8090`

Use the included `servarr-status.xml` template to configure service URLs and API keys in the Unraid GUI.
