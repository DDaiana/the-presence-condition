# Deployment

The public production website deploys from the `main` branch of `DDaiana/the-presence-condition` through `.github/workflows/deploy-pages.yml`. GitHub Actions builds a static export and publishes it to GitHub Pages at `https://ddaiana.github.io/the-presence-condition/`. No secrets are required for the static archive. The Vinext/OpenAI Sites path remains available as a private secondary deployment. Submission and newsletter controls remain disabled until approved providers are selected; their credentials must be stored as host environment variables, never committed.
