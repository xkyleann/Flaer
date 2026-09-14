# Changelog

All dates use the project workspace timezone (Europe/Warsaw). This log records material product, design, security, and deployment changes.

## 2026-09-14 — Production-readiness, consistency, and product UX

### Brand and website

- Replaced shared in-app Flaer marks with the supplied official logo asset.
- Updated dashboard and login wordmarks to `Flaer`.
- Replaced the legacy purple browser favicon with the Flaer logo and added versioned browser icon links.
- Removed the redundant “Built around your role” landing-page section.
- Added an in-page consultation modal; a Cal.com or Calendly URL can be connected later.
- Fixed the remaining “Use cases” navigation link to target the live Capabilities section.

### Dashboard

- Added a signed-in-user welcome header.
- Reworked the overview into clickable, keyboard-accessible portfolio summary cards.
- Added interactive map filters for all, review-needed, and lower-risk European reference locations.
- Improved responsive behaviour: the sidebar becomes a compact horizontal navigation rail at narrower desktop widths.
- Removed the clipped, duplicate sidebar setup card and duplicate data-connection banner.
- Kept the dashboard’s map presentation while ensuring European location markers render above decorative layers.

### Data integrity and reporting

- Defined the 15 mapped European locations as metro-level reference data, not a live operational directory.
- Added visible notices where verified data is required.
- Changed public metadata to remove unverified claims about real-time global tracking, customer scale, ratings, and enterprise adoption.
- Reframed the landing forecast as an illustrative scenario, not a guaranteed operational outcome.
- Reworked the dashboard PDF export to contain European reference locations and source status instead of unrelated global performance figures.
- Updated footer messaging to match the actual product scope.

### Security and deployment

- Enforced validated authentication before dashboard access.
- Removed production UI exposure of sample credentials and prevented production database seeding.
- Added deployment and environment-variable documentation for Cloudflare Pages and Render.
- Added frontend and backend environment examples.

### Verification

- Frontend production build passes.
- Backend authentication test suite passes (34 tests at the time of verification).
- Production authentication smoke test passes.

## 2026-09-13 — Product refresh and repository cleanup

- Expanded the Flaer product experience and refreshed the website and dashboard.
- Removed unused local artefacts from the active product worktree.

## 2026-04-29 — Quality and backend fixes

- Added backend and frontend quality improvements.
- Fixed API port mismatch, authentication issues, content-security-policy issues, and database-file ignore rules.

## 2026-04-23 — SaaS foundation

- Added database initialisation, testing guidance, pricing navigation, authentication fixes, and SaaS infrastructure foundations.

## 2026-04-19 — Initial Flaer product site

- Added the initial Flaer marketing site and dashboard experience.

## Historical note

Older commits before April 2026 primarily concern the AIrth research prototype. That prototype remains in `AIrth-main/` for historical reference and is not the active production application.
