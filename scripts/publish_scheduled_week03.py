"""Publish the reviewed Week 3 bundle after its fixed release time."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import urllib.request
import zipfile


def read_release(root):
    directory = root / '_scheduled/week-03'
    manifest = json.loads((directory / 'release.json').read_text(encoding='utf-8'))
    release_at = datetime.fromisoformat(manifest['release_at'])
    assert release_at == datetime(2026, 10, 10, 7, tzinfo=timezone.utc)
    return directory, manifest, release_at


def safe_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError(f'Invalid release path: {relative}')
    return path


def unpack_bundle(root, archive_path, expected_sha256):
    archive_path = Path(archive_path)
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError('The downloaded archive differs from the approved bundle.')
    manifest_path = '_scheduled/week-03/release.json'
    prefix = '_scheduled/week-03/files/'
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive paths.')
        manifest = json.loads(archive.read(manifest_path))
        expected = {manifest_path} | {prefix + item['path'] for item in manifest['files']}
        if set(names) != expected:
            raise ValueError('Unexpected archive contents.')
        contents = [(safe_path(root, name), archive.read(name)) for name in names]
    for target, data in contents:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('The approved private bundle was downloaded and unpacked.')


def planned_changes(root, directory, manifest):
    files = []
    for item in manifest['files']:
        relative = item['path']
        if not relative.startswith(('courses/surrogate-models/week-03', 'assets/courses/surrogate-models/')):
            raise ValueError(f'Unexpected release destination: {relative}')
        source = safe_path(directory / 'files', relative)
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Approved file hash changed: {relative}')
        files.append((safe_path(root, relative), data))
    text_files = {}
    allowed = {'index.html', '_data/courses.yml', 'courses/index.html', 'courses/surrogate-models/index.html', 'courses/surrogate-models/syllabus.md'}
    for patch in manifest['patches']:
        if patch['path'] not in allowed:
            raise ValueError(f'Unexpected metadata path: {patch["path"]}')
        target = safe_path(root, patch['path'])
        text = text_files.get(target, target.read_text(encoding='utf-8'))
        if text.count(patch['old']) != 1:
            raise ValueError(f'Course metadata changed; review required: {patch["path"]}')
        text_files[target] = text.replace(patch['old'], patch['new'])
    return files, text_files


def publish(root, now, check=False):
    directory, manifest, release_at = read_release(root)
    marker = directory / 'published.json'
    if marker.exists():
        return 'already_published'
    files, text_files = planned_changes(root, directory, manifest)
    if check:
        return 'checked'
    if now < release_at:
        return 'not_due'
    # Validate the entire bundle and all metadata before writing anything.
    for target, data in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for target, text in text_files.items():
        target.write_text(text, encoding='utf-8')
    marker.write_text(json.dumps({'release_at': manifest['release_at'], 'published_at': now.isoformat(),
                                 'manifest_sha256': hashlib.sha256((directory / 'release.json').read_bytes()).hexdigest()}, indent=2) + '\n', encoding='utf-8')
    return 'published'


def verify_live(root):
    _, manifest, _ = read_release(root)
    base = 'https://sunboogermany.github.io/'
    for item in manifest['files']:
        if not item['path'].endswith('.pdf'):
            continue
        request = urllib.request.Request(base + item['path'] + '?release=week03-20261010', headers={'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Live PDF differs from the approved bundle: {item["path"]}')
    for name, pages in [('week-03', 58), ('week-03-reading', 20)]:
        with urllib.request.urlopen(base + f'courses/surrogate-models/{name}/?release=week03-20261010', timeout=60) as response:
            html = response.read().decode('utf-8')
        if html.count('class="lecture-page"') != pages:
            raise ValueError(f'Unexpected live page count: {name}')
    print('Live lecture, reading materials, and all six PDFs verified.')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--publish', action='store_true')
    group.add_argument('--verify-live', action='store_true')
    group.add_argument('--unpack', metavar='ARCHIVE')
    parser.add_argument('--bundle-sha256')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if args.unpack:
        if not args.bundle_sha256:
            parser.error('--unpack requires --bundle-sha256')
        unpack_bundle(root, args.unpack, args.bundle_sha256)
        return
    if args.verify_live:
        verify_live(root)
        return
    status = publish(root, datetime.now(timezone.utc), check=args.check)
    directory, manifest, _ = read_release(root)
    print(json.dumps({'status': status, 'release_at': manifest['release_at'], 'timezone': manifest['timezone'], 'approved_files': len(manifest['files'])}))
    if output := os.environ.get('GITHUB_OUTPUT'):
        with open(output, 'a', encoding='utf-8') as stream:
            stream.write(f'status={status}\n')


if __name__ == '__main__':
    main()
