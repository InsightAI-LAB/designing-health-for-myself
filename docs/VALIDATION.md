# Validation record

Prepared 2026-10-02. This is an organizer-review website package, not a claim of workshop acceptance or a live deployment.

## Passed

- The delivered proposal and companion were used as the content sources; local source-file checksums matched the delivered package
- Independent content review found no substantive mismatch in pending status, proposed dates, closed submissions, organizers, session timings, fictional-information boundaries, or permission-based publication
- Dependency-free source and built-output checks: three HTML pages; local files and anchor targets resolve; metadata, language, one main heading per page, no duplicate IDs, and basic image alternatives
- HTML/TXT calls agree and contain exactly 250 whitespace-delimited words, excluding their draft notices and headings
- JavaScript syntax check
- Static Pages workflow YAML and policy review; SHA-pinned actions checked against their official release pages
- All 45 tested combinations of event, branch, and deployment opt-in matched the intended deployment guard
- Build output contains only the ten intended public files; no proposal working documents, deployment docs, QA files, configuration, workflow files, or credentials are staged
- ZIP extracted into a clean directory, with dotfiles retained, and the source/build/output checks repeated successfully

## Not verified here

Local headless Chromium could not start in the build environment because its required socket operation was unavailable, including after the supported execution retry. The separate cloud browser could not open the localhost preview. As a result, **real-browser desktop/mobile rendering, menu interactions, keyboard focus behavior, reduced-motion behavior, and print output were not visually or interactively verified**. Responsive CSS and the corresponding navigation code are implemented, but implementation is not a substitute for those tests.

No GitHub repository was created, source pushed, Pages enabled, or hosted Actions run performed. Live deployment, the final public URL, repository/organization policies, and external-link availability remain unverified. Static checks do not establish full WCAG conformance or an assistive-technology audit.

## Required preview checks before release

1. Run the local commands in README.md; open the built site in Chrome, Firefox, or Safari
2. Check 320, 375, 390, 768, 1024, and 1440-pixel widths for horizontal overflow, overlapping text, and clipped content
3. With the keyboard, confirm the first Tab reveals the skip link and activating it moves focus to the main content
4. At a mobile width, open and close the menu repeatedly; confirm Escape closes it and restores focus, and selecting an anchor closes it
5. Expand the full draft call and every FAQ; verify content remains readable and focus visible
6. Test with JavaScript disabled; the navigation, all sections, and downloads must remain available
7. Enable reduced motion; anchor navigation should not animate
8. Open the activity pack and privacy page; download all text resources; use the activity pack’s print button and inspect the print preview
9. On the real project URL, confirm assets and downloads work under the repository subpath
10. Confirm publication approvals, dates, names, and submission status against the launch checklist
