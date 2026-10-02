# Designing Health for Myself

A dependency-free static website for a **proposed CHI 2027 workshop**. Workshop acceptance is pending; public dates and the submission route must be confirmed before opening the call for participation.

Repository name: `designing-health-for-myself`. The GitHub owner is intentionally unspecified. Nothing in this package creates a repository, pushes code, enables Pages, or publishes a live website.

## Start here

1. Preview the site locally and review the content.
2. Complete the relevant [launch checklist](docs/LAUNCH_CHECKLIST.md).
3. Follow [DEPLOYMENT.md](DEPLOYMENT.md) to put the files on GitHub and, when approved, publish with GitHub Pages.

The supplied pipeline checks pull requests and `main`. **Deployment stays off until a maintainer configures Pages and sets the repository variable `PAGES_DEPLOY_ENABLED` to `true`.** After that, a successful push to `main`, or a manual run selected on `main`, publishes the checked site.

## Local preview and checks

Python 3.12 is used in CI. There are no npm packages, Python package installs, theme dependencies, or API keys required for this site.

From the repository root:

```sh
python3 scripts/check_site.py
python3 scripts/build_site.py
python3 scripts/check_site.py --root _site
python3 -m http.server 8000 --directory _site --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/> in your browser. Stop the server with Ctrl+C. This serves only the built public files. A successful automated check does not verify workshop acceptance, organizer approval, or every external website; those need human review.

## What lives where

- `index.html`: visitor-facing workshop content and metadata
- `assets/`: local styles, scripts, and artwork
- `resources/`: intended public downloads
- `scripts/check_site.py`: source and built-site checks
- `scripts/build_site.py`: stages the public site into `_site/`
- `site.config.json`: optional verified public URL and search-indexing setting
- `site.config.example.json`: illustrative owner/repository URL format
- `.github/workflows/pages.yml`: checks, build, and opt-in GitHub Pages deployment
- `.github/dependabot.yml`: monthly GitHub Actions update proposals
- `DEPLOYMENT.md`: one-time GitHub setup, publishing, rollback, and troubleshooting
- `docs/LAUNCH_CHECKLIST.md`: publication and call-for-participation review
- `docs/CONTENT_GUIDE.md`: editing and maintenance instructions
- `_site/`: generated output, ignored by Git; do not edit it directly

Only the output of `scripts/build_site.py` is uploaded to Pages. Keep internal correspondence, proposal working documents, participant information, and secrets out of the repository and the public output. A public GitHub repository exposes source files and history even when those files are excluded from Pages.

## Verification status

Source/build/link checks and workflow policy checks passed. Real-browser visual/interaction checks could not run in the build environment, and hosted GitHub Actions has not run. See [the validation record](docs/VALIDATION.md) for exact coverage and the short pre-release test list.

## Editorial status

The site is a proposed/pending workshop presentation, with draft or TBA scheduling and no live submission collection. The proposal's intended format is **two consecutive 85-minute sessions** with **20–30 participants**; these are planning assumptions until confirmed. Review all organizer names, affiliations, bios, links, and contact details before public release.

Use [the content guide](docs/CONTENT_GUIDE.md) when updating these details. Keep the pending status visible until acceptance is confirmed. Do not replace TBA dates or enable submission links with guesses.

## Technology and privacy

This is a static HTML/CSS/JavaScript site. GitHub Pages hosts static files; it does not provide a submission backend. Any future submission service needs its own approved destination and participant-facing privacy information. Do not add credentials, health narratives, or participant records to the site or repository.

## License and ownership

No open-source license is asserted by this package. Before public release, the organizers should confirm rights to the workshop text, downloadable material, names, photos, and artwork, and choose an appropriate license if desired.
