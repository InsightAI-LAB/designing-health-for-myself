# GitHub Pages deployment

This guide targets **GitHub.com**, the repository `designing-health-for-myself`, and the branch `main`. Replace `YOUR_GITHUB_OWNER` with the actual GitHub username or organization; it is a placeholder, not an account selected for you.

## Before publishing

- Confirm who should own the repository and who may approve changes.
- Review [docs/LAUNCH_CHECKLIST.md](docs/LAUNCH_CHECKLIST.md). The workshop is proposed, acceptance is pending, and the call for participation is not open.
- Decide whether a clearly labeled pending-workshop page is approved for publication now, or whether the entire website should wait for acceptance.
- Review every tracked file and its history for unapproved information. A public repository exposes source and history, not just the website.
- Treat the Pages website as public. A private source repository does not by itself make the hosted website private. GitHub plan and organization policies affect availability; confirm them before relying on private repository hosting. See [GitHub's publishing-source guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

**This package is not yet deployed.** Repository creation, upload/push, settings changes, and publication are intentional steps for an authorized maintainer. No personal access token or deployment secret is needed by the workflow.

## 1. Validate the local package

Run these from the directory containing `index.html`:

```sh
python3 scripts/check_site.py
python3 scripts/build_site.py
python3 scripts/check_site.py --root _site
python3 -m http.server 8000 --directory _site --bind 127.0.0.1
```

Preview <http://127.0.0.1:8000/>. Inspect the main page, navigation, resources, desktop/mobile layout, and keyboard operation. Stop the server with Ctrl+C.

GitHub project sites live under a repository path. Keep local references relative, such as `assets/styles.css`, rather than root-absolute references such as `/assets/styles.css`. The [default project-site URL](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) will be:

```text
https://YOUR_GITHUB_OWNER.github.io/designing-health-for-myself/
```

That is a URL pattern, not a verified live address. If the owner already uses a custom domain or Pages gives a different address, use the actual URL reported by the deployment and Settings → Pages. Do not add a guessed canonical URL or custom domain.

## 2. Create the repository and upload the source

On GitHub, create a repository named `designing-health-for-myself` under the approved owner. Choose visibility intentionally. For the simplest free Pages setup, use a public repository after the publication review. For the command-line path below, create an empty repository without a generated README, license, or `.gitignore`.

### Recommended: Git from the terminal

For a new, unversioned copy of this package:

```sh
cd /path/to/designing-health-for-myself
git init -b main
git add .
git status --short
git diff --cached --stat
git diff --cached
```

Review the staged content. Confirm that `.github/workflows/pages.yml`, `.github/dependabot.yml`, `.gitignore`, and `.nojekyll` are included; dotfiles must not be omitted. `_site/`, local QA output, and secrets should not be staged. Then, when upload is authorized:

```sh
git commit -m "Add workshop website and GitHub Pages pipeline"
git remote add origin https://github.com/YOUR_GITHUB_OWNER/designing-health-for-myself.git
git push -u origin main
```

Use your normal GitHub authentication. Never paste tokens into website files, workflow YAML, or a remote URL. If this is already a Git checkout, inspect `git status`, `git branch --show-current`, and `git remote -v`; do not run initialization or replace an existing remote blindly. If a remote repository already contains commits, clone it first and copy the package contents into it, including dotfiles.

### Alternative: GitHub's browser editor/upload

Upload the **contents** of the package directory to the repository root, rather than uploading its enclosing folder or the ZIP itself. `index.html` and `scripts/` must be at the root. Commit to `main`.

Some file pickers hide dotfiles. Show hidden files in your file manager, and verify the repository contains `.github/workflows/pages.yml`, `.github/dependabot.yml`, `.github/pull_request_template.md`, `.gitignore`, and `.nojekyll`. If the upload omitted them, use **Add file → Create new file** and paste each file using its exact path. An empty `.nojekyll` file can contain a newline. Do not upload `_site/` or `qa/`.

With deployment disabled, the first push runs **Check and build** while **Deploy to GitHub Pages** is skipped. This is expected and lets you verify CI before going live.

## 3. Review GitHub settings

An authorized maintainer should review these settings. Organization policy can override repository settings.

1. **Settings → Actions → General:** allow the GitHub-owned actions used by this workflow. The workflow invokes `actions/checkout`, `actions/setup-python`, `actions/upload-pages-artifact`, `actions/configure-pages`, and `actions/deploy-pages`. The upload action also invokes GitHub's `actions/upload-artifact`. If an allowlist is enforced, it must permit these pinned actions and their required dependency. Use a GitHub-hosted `ubuntu-latest` runner with Node 24 support.
2. Keep the repository's default workflow token permissions read-only. The workflow requests `pages: write` and `id-token: write` only for its deployment job. Do not make all workflows broadly writable or add a PAT to fix a policy error; ask the repository/organization administrator to review the specific restriction.
3. **Settings → Pages → Build and deployment → Source:** select **GitHub Actions**. The workflow is already supplied; do not add a second starter workflow or select a `/docs` branch source. `configure-pages` explicitly has `enablement: false` and will not create the Pages site for you. See [GitHub's setup steps](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
4. **Settings → Environments → github-pages:** create or review this environment. Restrict deployment branches to the selected branch `main`. Add required reviewers if your plan and governance need release approval. If no environment exists, the first eligible workflow deployment can create it, but review its branch restriction before opening deployment.
5. Consider protecting `main`: require a reviewed pull request and the **Check and build** status check after it first appears. Branch protection and environment protection complement the workflow's branch guard.

The workflow never deploys pull requests or branches other than `main`. It does not use `pull_request_target`, checkout credentials are not persisted, and the deploy job does not execute repository scripts.

## 4. Explicitly enable publication and make the first deployment

**After this step, successful pushes to `main` automatically publish the website.** Resolve the launch checklist and approval first.

1. Open **Settings → Secrets and variables → Actions → Variables**.
2. Create a **repository variable**, not a secret or environment variable: name `PAGES_DEPLOY_ENABLED`, value `true` (lowercase).
3. Open **Actions → Website checks and Pages → Run workflow**.
4. Select branch **main**, then run. Setting the variable alone does not trigger a run.
5. If the `github-pages` environment requires review, an authorized reviewer approves the waiting deployment.
6. Confirm both **Check and build** and **Deploy to GitHub Pages** finish successfully. Verify the expected commit SHA in the run. Open the deployment's environment URL, also shown in **Settings → Pages**.
7. Check the published site in a fresh browser tab, including local assets and downloads under `/designing-health-for-myself/`. Verify that pending status and submission availability match the approved content before sharing the URL.

`GITHUB_TOKEN` is generated by GitHub for each run. The deployment uses GitHub Pages' OpenID Connect token (`id-token: write`); no stored deployment key or manually created token is needed. The [official Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) describes the build artifact, deployment permissions, environment, and deployment URL.

## How the pipeline behaves

- Pull requests targeting `main`: source check → build → built-site check; no Pages upload or deployment.
- Pushes to `main`: the same checks; upload and deploy only when the repository variable is exactly `true`.
- Manual workflow run on `main`: the same checks and opt-in deployment.
- Manual run on another branch: checks only; no upload or deployment.
- A failed check blocks later steps and deployment through `needs: build`.
- Only `_site/` is uploaded. The upload retains `.nojekyll` from the public-only output. Workflow files, documentation, and local QA output are not intended website content.
- Concurrency serializes runs for the same branch/PR and deployment uses a shared `github-pages` group. `cancel-in-progress: false` avoids interrupting an active deployment. GitHub may replace older pending runs; a canceled pending run is not a deployment failure. See [concurrency guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

## Update and rollback

For normal updates, create a branch, edit source files, run the three checks, and open a pull request against `main`. Review the content and green CI before merging. When publication is enabled, merge/push to `main` triggers a new deployment.

For rollback, revert the unwanted commit in a new change and merge that revert to `main`; this creates an auditable, freshly checked deployment. For a simple non-merge commit, a local example is:

```sh
git switch -c revert-website-change
git revert BAD_COMMIT_SHA
# Resolve any conflicts, run the three checks, then push this branch and open a PR.
```

Merge commits need special handling; use GitHub's revert-PR flow or have a maintainer select the appropriate parent. Do not force-push or rewrite shared history as a rollback shortcut. Old uploaded artifacts expire after seven days, so rebuilding a reviewed revert is more reliable than re-running only an old deployment job.

To stop **future** automatic publication, set `PAGES_DEPLOY_ENABLED` to `false` or remove it. This does not stop a deployment already running and does not remove the live site. If you need to take the website offline, an authorized maintainer must unpublish it in Pages settings and check that it is no longer accessible. Public caches and already downloaded copies may remain.

## Troubleshooting

- **Deploy job is skipped:** check the repository variable spelling/value, event type, and selected branch. Skipping is correct on pull requests or before opt-in.
- **No workflow appears:** verify `.github/workflows/pages.yml` was uploaded to the repository root, is committed on the default branch, and Actions is enabled. Do not upload only the visible website files.
- **Cannot find Pages / configuration returns 404:** select Source → GitHub Actions; confirm repository access, plan eligibility, and organization policy. Do not turn on automatic enablement or introduce a broad PAT as a workaround.
- **Permission or OIDC error:** confirm deployment job permissions, environment branch rules, required reviews, and organization Actions policy. Keep permission changes narrow.
- **Missing artifact:** inspect the source/build checks and artifact-upload step in the same run. Re-run the full workflow on `main` if the seven-day artifact retention has elapsed.
- **404 or broken styles/downloads after a successful deployment:** use the exact environment URL; verify `_site/index.html`, relative paths, filename case, and the repository subpath. Allow the publish to finish and refresh. Do not change the URL to the owner's root site unless Pages actually reports that URL.
- **Waiting or superseded run:** inspect environment approval and concurrency. Let an active deployment finish; a newer run may replace an older pending one.
- **GitHub Enterprise Server:** this package targets GitHub.com. Review the official actions' compatibility notes and your server's supported action/artifact versions before adapting it.

## Action-version maintenance

Workflow actions are pinned to full upstream commit SHAs, with release comments for review. On **2026-10-02**, the official release pages resolved to:

- [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)
- [setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0)
- [configure-pages v6.0.0](https://github.com/actions/configure-pages/releases/tag/v6.0.0)
- [upload-pages-artifact v5.0.0](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0)
- [deploy-pages v5.0.1](https://github.com/actions/deploy-pages/releases/tag/v5.0.1)

`.github/dependabot.yml` proposes monthly GitHub Actions updates when the repository enables Dependabot version updates. Review release notes and CI before merging. Do not automatically merge workflow changes. The site's static build has no application packages to update. GitHub recommends [full-length commit pinning and minimal permissions](https://docs.github.com/en/actions/reference/security/secure-use).
