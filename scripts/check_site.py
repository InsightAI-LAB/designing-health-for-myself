#!/usr/bin/env python3
"""Dependency-free static regression checks; not a complete accessibility audit."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.errors = []
        self.h1 = 0
        self.lang = False
        self.title = False
        self.viewport = False
        self.robots = False
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'html': self.lang = bool(a.get('lang'))
        if tag == 'title': self.title = True
        if tag == 'main': self.has_main = True
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and a.get('name') == 'viewport': self.viewport = True
        if tag == 'meta' and a.get('name') == 'robots': self.robots = True
        if tag in ('form', 'iframe'): self.errors.append(f'Unexpected data-collection/embed element: {tag}')
        if tag == 'img' and 'alt' not in a: self.errors.append('Image missing alt attribute')
        if tag == 'a' and a.get('target') == '_blank' and 'noopener' not in a.get('rel', ''):
            self.errors.append('New-window link missing noopener')
        for attr in ('href', 'src'):
            if a.get(attr): self.links.append((tag, attr, a[attr]))
        if tag == 'script' and not a.get('src'): self.errors.append('Unexpected inline script')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.', help='Source or built public-site directory')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = []
    pages = {}
    for file in [root / 'index.html', *sorted((root / 'resources').glob('*.html'))]:
        if not file.exists():
            errors.append(f'Missing {file}')
            continue
        doc = Document()
        doc.feed(file.read_text(encoding='utf-8'))
        pages[file] = doc
        for flag in ('lang', 'title', 'viewport', 'robots', 'has_main'):
            if not getattr(doc, flag): errors.append(f'{file.name}: missing {flag}')
        if doc.h1 != 1: errors.append(f'{file.name}: expected one h1, found {doc.h1}')
        errors.extend(f'{file.name}: {e}' for e in doc.errors)
        errors.extend(f'{file.name}: duplicate id {key}' for key, count in Counter(doc.ids).items() if count > 1)
    for file, doc in pages.items():
        for tag, attr, link in doc.links:
            u = urlsplit(link)
            if u.scheme in ('https', 'mailto'):
                if tag in ('script', 'img') or (tag == 'link' and attr == 'src'):
                    errors.append(f'{file.name}: unexpected external runtime asset {link}')
                continue
            if u.scheme or link.startswith('//'):
                errors.append(f'{file.name}: unsupported link scheme {link}')
                continue
            if u.path.startswith('/'):
                errors.append(f'{file.name}: root-relative path breaks project Pages: {link}')
                continue
            target = (file.parent / unquote(u.path)).resolve() if u.path else file
            if target.is_dir(): target = target / 'index.html'
            if not target.is_relative_to(root):
                errors.append(f'{file.name}: asset escapes root: {link}')
            elif not target.is_file():
                errors.append(f'{file.name}: missing local target {link}')
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(f'{file.name}: missing anchor {link}')
    for file in (root / 'assets').glob('*.css'):
        text = file.read_text(encoding='utf-8')
        if '@import' in text: errors.append(f'{file.name}: external/imported CSS is not expected')
        for path in re.findall(r'url\([\"\']?([^\)\"\']+)', text):
            if urlsplit(path).scheme or not (file.parent / path).is_file():
                errors.append(f'{file.name}: invalid or external CSS asset {path}')
    index = (root / 'index.html').read_text(encoding='utf-8') if (root / 'index.html').exists() else ''
    for text in ('Acceptance pending', 'Submissions are not open', '85 minutes', 'Wordh Ul Hasan', 'Kimia Zaman', 'Baiyun Chen', 'Fan Wu'):
        if text not in index: errors.append(f'Expected current review-edition text missing: {text}')
    if 'WORKSHOP_WEBSITE_URL' in index or 'YOUR_GITHUB_OWNER' in index:
        errors.append('Placeholder leaked into the visitor-facing homepage')
    cfp = re.search(r'<!-- CFP_START -->(.*?)<!-- CFP_END -->', index, re.S)
    if not cfp:
        errors.append('Missing identifiable CFP block')
    else:
        text = re.sub('<[^>]+>', ' ', cfp.group(1))
        count = len(text.split())
        if count != 250: errors.append(f'CFP must have 250 whitespace-delimited words, found {count}')
        txt = (root / 'resources/call-for-participation.txt').read_text(encoding='utf-8')
        call = txt.split('--- BEGIN 250-WORD CALL ---')[1].split('--- END CALL ---')[0]
        if ' '.join(call.split()) != ' '.join(text.split()): errors.append('HTML and TXT calls differ')
    if not (root / '.nojekyll').is_file(): errors.append('Missing .nojekyll')
    if root.name == '_site':
        allowed = {'index.html', '.nojekyll', 'assets', 'resources'}
        extras = {p.name for p in root.iterdir()} - allowed
        if extras: errors.append(f'Unexpected files in public output: {sorted(extras)}')
    if errors:
        print('\n'.join('FAIL ' + e for e in errors))
        raise SystemExit(1)
    print(f'PASS: {len(pages)} HTML pages; all local links/fragments, metadata, duplicate IDs, public-only output, and 250-word CFP checks')
    print('Manual review still required: real-browser layout, keyboard use, assistive technology, publication approvals, external links.')


if __name__ == '__main__':
    main()
