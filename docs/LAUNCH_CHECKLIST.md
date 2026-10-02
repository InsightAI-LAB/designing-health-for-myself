# Publication and CFP launch checklist

Keep an organizer-reviewed copy of this checklist with the release. Automated checks can verify site structure; they cannot approve conference status, personal metadata, or the call for participation.

## Before any public repository or website release

- [ ] Confirm repository owner and maintainer access for `designing-health-for-myself`.
- [ ] Obtain organizer approval for publishing a proposed-workshop page before acceptance, or wait for acceptance before publishing anything.
- [ ] Keep **proposed / acceptance pending** status clear in the page, title, metadata, and downloadable materials while that is the actual status.
- [ ] Check the repository's tracked files and history. Remove private correspondence, working proposals that are not approved for sharing, credentials, participant data, and local QA files.
- [ ] Approve organizer names, order, affiliations, pronouns if used, bios, photographs, homepages, and contact details. Publish only information organizers have approved.
- [ ] Confirm rights to publish all text, downloadable resources, artwork, and images. Decide whether a repository/content license is appropriate.
- [ ] Preserve draft/TBA labels for unconfirmed dates and plans. Do not imply conference endorsement or invent dates, rooms, fees, registration links, or acceptance.
- [ ] Keep the proposal's format factual: two consecutive **85-minute sessions**, with planned attendance of **20–30**. Mark any later revisions as organizer-approved changes.
- [ ] Confirm no live form or submission destination is offered until a real, approved route exists.
- [ ] Run source check, build, and built-site check. Inspect the generated `_site/` contents.
- [ ] Preview desktop and narrow mobile screens; verify no clipped content, readable text, keyboard navigation, visible focus, and reduced-motion behavior where applicable.
- [ ] Check all links and public downloads manually. Confirm no internal source documents are exposed.
- [ ] Review the final destination and the fact that a public repository and ordinary Pages website are public.

## Before opening the call for participation

- [ ] Verify acceptance with the CHI 2027 workshop organizers and record the final approved workshop title/status.
- [ ] Confirm workshop date, conference relationship, location/participation mode, schedule, and any attendance/registration requirements from authoritative sources.
- [ ] Replace draft/TBA dates with approved dates, explicit timezone, and deadline time. Check every repeated date, metadata field, and downloadable CFP.
- [ ] Approve submission format, length, eligibility, selection criteria, review process, notification date, and attendance expectations.
- [ ] Select and test the approved submission destination. Confirm who receives submissions, accessibility, data retention, privacy wording, and who responds to questions.
- [ ] For this health-related topic, explicitly review whether participants could submit sensitive personal information and how organizers will protect it. Do not collect it in GitHub issues or a public repository.
- [ ] Approve the contact route and test it. Do not substitute a guessed email address or an individual's unapproved contact details.
- [ ] Ensure the site, downloadable CFP, submission destination, and organizer announcement agree. Only then change the CTA and status to indicate submissions are open.

## Before enabling GitHub Pages deployment

- [ ] Repository Source is set to **GitHub Actions** under Settings → Pages.
- [ ] `github-pages` environment permits only `main`; any required reviewer is configured.
- [ ] GitHub-owned actions are permitted; default token permissions stay read-only.
- [ ] First CI checks pass. Required `main` checks and review protection are considered/configured.
- [ ] Publication is authorized, then repository variable `PAGES_DEPLOY_ENABLED=true` is added.
- [ ] A manual run on `main` succeeds and the expected commit is deployed.
- [ ] The exact deployed URL is opened and tested, including repository-subpath assets and downloads.
- [ ] Record the deployment run URL and commit for the launch owner. Share the website only after the live content review.

## During and after the workshop cycle

- [ ] On deadline changes, update every occurrence and the submission service together.
- [ ] When submissions close, replace the open-submissions CTA and archive the relevant CFP.
- [ ] Publish accepted submissions, participant names, recordings, photographs, or outcomes only with the necessary rights and consent.
- [ ] Archive the completed workshop with accurate past-tense status and stable approved resources.
