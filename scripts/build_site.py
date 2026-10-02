#!/usr/bin/env python3
"""Stage only explicitly public static files; no third-party dependencies."""
from pathlib import Path
import html
import json
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
ALLOWED_SUFFIXES = {'.html', '.css', '.js', '.svg', '.txt'}
CONFIG = {'site_url': '', 'search_indexing': False}


def main():
    config_path = ROOT / 'site.config.json'
    if config_path.exists():
        CONFIG.update(json.loads(config_path.read_text(encoding='utf-8')))
    site_url = CONFIG['site_url']
    if not isinstance(site_url, str) or not isinstance(CONFIG['search_indexing'], bool):
        raise SystemExit('site_url must be a string; search_indexing must be a boolean.')
    if site_url:
        parsed = urlsplit(site_url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise SystemExit('site_url must be a real, approved HTTPS origin/path without credentials, query, or fragment.')
        if any(marker in site_url.upper() for marker in ('YOUR_', 'EXAMPLE.', '<', '>')):
            raise SystemExit('Replace the example owner/domain before setting site_url.')
        if not site_url.endswith('/'):
            raise SystemExit('site_url must end in / (include the repository path for project Pages).')
    if CONFIG['search_indexing'] and not site_url:
        raise SystemExit('Set the verified public site_url before enabling search_indexing.')
    if OUT.is_symlink():
        raise SystemExit('Refusing to replace a symlinked output directory.')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    copied = []
    for name in ('index.html', '.nojekyll'):
        src = ROOT / name
        if src.is_symlink():
            raise SystemExit(f'Refusing symlink: {src}')
        shutil.copyfile(src, OUT / name)
        copied.append(name)
    for directory in ('assets', 'resources'):
        for src in sorted((ROOT / directory).rglob('*')):
            if src.is_symlink():
                raise SystemExit(f'Refusing symlink: {src}')
            if not src.is_file():
                continue
            rel = src.relative_to(ROOT)
            if any(part.startswith('.') for part in rel.parts) or src.suffix.lower() not in ALLOWED_SUFFIXES:
                raise SystemExit(f'File not approved for public staging: {rel}')
            target = OUT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            copied.append(str(rel))
    for page in OUT.rglob('*.html'):
        content = page.read_text(encoding='utf-8')
        robots = 'index, follow' if CONFIG['search_indexing'] else 'noindex, nofollow'
        content = content.replace('content="noindex, nofollow"', f'content="{robots}"')
        if site_url:
            path = page.relative_to(OUT).as_posix()
            canonical = site_url + ('' if path == 'index.html' else path)
            metadata = f'  <link rel="canonical" href="{html.escape(canonical, quote=True)}">\n  <meta property="og:url" content="{html.escape(canonical, quote=True)}">\n'
            content = content.replace('</head>', metadata + '</head>')
        page.write_text(content, encoding='utf-8')
    print(f'Built {len(copied)} public files in {OUT.name}/')
    print('Search indexing:', 'enabled' if CONFIG['search_indexing'] else 'disabled (not access control)')
    print('Canonical site URL:', site_url or 'omitted until the approved live URL is known')


if __name__ == '__main__':
    main()
