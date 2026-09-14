# Publish Flaer on Cloudflare

This repository is ready for a split deployment: Cloudflare Pages serves the Svelte site and Render runs the FastAPI API and PostgreSQL database.

## 1. Deploy the API

1. Sign in to [Render](https://render.com) with GitHub and choose **New → Blueprint**.
2. Select `xkyleann/Flaer`. Render reads `render.yaml`, creates `flaer-api` and `flaer-db`, and generates a private JWT secret.
3. After deployment, open the API service and add the custom domain `api.flaer.io`.
4. In Cloudflare DNS, create the CNAME record Render requests for `api`. Leave it **DNS only** until Render has verified the certificate.
5. Confirm `https://api.flaer.io/api/health` returns `{ "status": "ok" }`.

## 2. Deploy the site

1. In Cloudflare, choose **Workers & Pages → Create → Pages → Connect to Git**.
2. Select `xkyleann/Flaer` and use these settings:

   | Setting | Value |
   | --- | --- |
   | Production branch | `main` |
   | Root directory | `flaer/frontend-svelte` |
   | Build command | `npm run build` |
   | Build output directory | `dist` |

3. Add Pages environment variables from `flaer/frontend-svelte/.env.example`:
   - `VITE_API_URL=https://api.flaer.io`
   - `VITE_MAPBOX_TOKEN=<your public Mapbox token>`
   - `VITE_BOOKING_URL=<your Cal.com or Calendly event URL>` (optional)
4. In **Custom domains**, add `flaer.io` and `www.flaer.io`; redirect `www` to the apex domain.

## 3. Final verification

- Open `https://flaer.io` and check the Europe map loads and shows all facility markers.
- Register a new account, sign in, and open `#dashboard`.
- Verify `https://api.flaer.io/docs` and `https://api.flaer.io/api/health`.
- In Mapbox, restrict the public token to `https://flaer.io/*`, `https://www.flaer.io/*`, and the Cloudflare Pages preview domain.

Never commit production secrets or database URLs. Cloudflare Pages needs only values prefixed with `VITE_`; these become public in the built site.
