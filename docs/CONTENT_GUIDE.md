# Editing and maintaining the workshop website

## Edit the source

Work in `index.html`, `assets/`, and approved public files in `resources/`. `_site/` is generated and is overwritten by the build. Do not edit it directly or commit it.

The website has no framework, theme installation, remote CMS, database, or submission backend. Small content changes can be made directly in HTML. Preserve semantic headings, descriptive link labels, image alternative text, and keyboard-accessible controls when editing.

## Content that needs organizer confirmation

- Acceptance status and final approved title
- Dates, timezone, workshop schedule, location, mode, and registration requirements
- Submission instructions, criteria, notification timing, and destination
- Organizer names, bios, affiliations, links, photos, and contact details
- Public resources and permission to redistribute them

Keep current unknowns as TBA or clearly marked draft. The planning format in the source proposal is two consecutive 85-minute sessions for 20–30 participants. Do not silently replace those with a different session length or capacity.

The submission call must remain inactive while no route is approved. A static website cannot securely receive files by itself. When organizers choose a service, use its actual approved URL and review the information requested and the privacy/retention process before enabling the CTA. Never put submission credentials or participant health information in HTML, JavaScript, GitHub issues, or the repository.

## Links, assets, and downloads

- Use relative URLs for local files so the site works at the GitHub project subpath.
- Match filename case exactly; GitHub Pages paths are case-sensitive.
- Keep external links descriptive, and review their destinations before publication.
- Put only intended public downloads in `resources/`; use descriptive filenames and visible format/size information where helpful.
- Keep images appropriately sized and retain alternative text. Prefer local assets rather than adding third-party tracking scripts or embeds.
- Do not infer the final public URL. Use the actual deployment URL when adding canonical/share metadata.
- Review `scripts/build_site.py` before adding a new public directory or root file; the build intentionally stages a bounded set of public files.

## Review and publish an update

1. Create a working branch and edit the source.
2. Run:

   ```sh
   python3 scripts/check_site.py
   python3 scripts/build_site.py
   python3 scripts/check_site.py --root _site
   ```

3. Preview `_site/` with `python3 -m http.server 8000 --directory _site --bind 127.0.0.1` and open <http://127.0.0.1:8000/>.
4. Test on a phone-width viewport and desktop. Use Tab/Shift+Tab to check navigation and controls. Check repeated interactions, links, downloads, and any mobile menu.
5. Open a pull request to `main`, record the approved source for factual changes, and use the supplied PR checklist.
6. Obtain review before merging. When publication is enabled, merging to `main` deploys automatically. Follow [DEPLOYMENT.md](../DEPLOYMENT.md) for initial setup, pausing, or rollback.

If you need a holding page after a deadline or cancellation, make an explicit reviewed content update. Turning off the deployment variable alone leaves the previously published content online.

## Canonical URL and search indexing

`site.config.json` is the build configuration. Its defaults are deliberately safe for a draft:

```json
{
  "site_url": "",
  "search_indexing": false
}
```

After an authorized deployment, copy the actual HTTPS URL from GitHub Pages into `site_url`, including the final slash and any repository subpath. `site.config.example.json` illustrates the format but is not a valid production value. Rebuild to add canonical and Open Graph URL metadata to each page. The configuration is not deployed as a public file.

Keep `search_indexing` false for the review edition. Set it true only when the organizers approve public discoverability. `noindex` is a search-engine request, not access control: it cannot make a published page private. The build rejects a missing or obvious placeholder URL when indexing is enabled.

The homepage keeps acceptance and submission status in ordinary HTML, not hidden behind this configuration. Update the visible status, metadata, FAQ, call, and downloads together when those facts change. The review-edition assertions near the end of `scripts/check_site.py` deliberately expect pending status; replace those assertions with the approved new status during the same reviewed change.

## The 250-word call

The HTML call is bracketed by `CFP_START` and `CFP_END` comments. Its download is bracketed by `BEGIN 250-WORD CALL` and `END CALL` markers. The checker confirms both versions agree and have exactly 250 whitespace-delimited words, excluding draft notices and headings. The final three words currently read “Workshop website: forthcoming”; replace “forthcoming” with the approved URL (one word) in both places after the URL is known. The rest of the call reproduces the proposal’s wording.

## What the build can publish

The build copies only `index.html`, `.nojekyll`, and regular, non-hidden files in `assets/` and `resources/`. Allowed extensions are `.html`, `.css`, `.js`, `.svg`, and `.txt`. It rejects symbolic links and unexpected extensions instead of quietly publishing them. If you later add permission-cleared PDFs, extend that explicit allowlist in a reviewed change. The original proposal, author-review companion, private correspondence, and participant submissions are intentionally absent from this repository.

See [VALIDATION.md](VALIDATION.md) for what was checked and what still needs a live-browser and first-deployment check.
