# Servarr Status

Small Docker web dashboard for monitoring Sonarr and Radarr.

## Environment variables

- `SONARR_URL` - e.g. `http://192.168.10.100:8989`
- `SONARR_API_KEY` - Sonarr API key
- `RADARR_URL` - e.g. `http://192.168.10.100:7878`
- `RADARR_API_KEY` - Radarr API key

Web interface listens on port `8080`.

## Unraid

The included XML template expects image:

`ghcr.io/YOUR_GITHUB_USER/servarr-status:latest`

Change that to your own image if publishing to GHCR.

Container port:
`8080 -> host port 8090`

Then open:

`http://UNRAID-IP:8090`
