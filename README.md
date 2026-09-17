# LENO · DE / FR Rota

Single-page rota workspace for the DE / FR Customer Service team.

## Project

- Frontend: `index (7).html`
- Backend: Supabase
- Hosting: Netlify
- Primary production site: `https://leno-workespace.netlify.app`

## Safety / QA

Run the lightweight static validation before publishing:

```bash
python scripts/validate_leno.py
```

The check validates the HTML entry file for a doctype, title, viewport configuration, duplicate IDs, and obvious hard-coded credential patterns.

## Deployment

The production deployment is currently managed through Netlify. GitHub is the source-of-truth repository for the frontend file; deployment should be verified after publishing rather than assuming a GitHub commit is already live.

<!-- mobile rota v6 trigger 2 -->
