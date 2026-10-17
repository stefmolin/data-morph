"""Maintains the stable docs on the latest version; groups others together."""

import json
import re
import shutil
from pathlib import Path

from packaging.version import parse as parse_version

import data_morph

# information on where temporary and permanent files will go
build_html_dir = Path('_build') / 'html'
tmp_build = Path('_build') / '_tmp'

# where the docs are hosted
base_url = 'https://stefaniemolin.com/data-morph'


def get_minor_releases():
    """Find the minor versions that have docs builds (in ascending order)."""
    return sorted(
        parse_version(directory.name)
        for directory in build_html_dir.glob('*')
        if directory.is_dir() and re.fullmatch(r'\d+\.\d+', directory.name)
    )


def determine_versions():
    """Determine stable/dev/etc. and docs version number."""
    last_minor_release = max(get_minor_releases(), default=parse_version('0.0'))
    docs_version = parse_version(data_morph.__version__)
    docs_version_group = parse_version(f'{docs_version.major}.{docs_version.minor}')

    if docs_version.is_devrelease:
        version_match = 'dev'
    elif docs_version_group >= last_minor_release:
        version_match = 'stable'
    else:
        version_match = f'{docs_version.major}.{docs_version.minor}'
    return version_match, docs_version_group


def update_switcher():
    """Regenerate the version switcher entries from the docs builds that exist."""
    minor_releases = get_minor_releases()
    if not (build_html_dir / 'stable').exists() or not minor_releases:
        return

    *older_releases, latest_release = minor_releases
    versions = [(f'{latest_release} (stable)', 'stable')]
    if (build_html_dir / 'dev').exists():
        versions.append(('dev', 'dev'))
    versions.extend((str(release), str(release)) for release in older_releases[::-1])

    # all versions of the docs read the switcher from the stable build
    switcher = build_html_dir / 'stable' / '_static' / 'switcher.json'
    switcher.parent.mkdir(exist_ok=True)
    switcher.write_text(
        json.dumps(
            [
                {'name': name, 'version': version, 'url': f'{base_url}/{version}/'}
                for name, version in versions
            ],
            indent=4,
        )
        + '\n'
    )


if __name__ == '__main__':
    version_match, docs_version_group = determine_versions()

    # clean up the old version
    if (old_build := build_html_dir / version_match).exists():
        shutil.rmtree(old_build)

    # move html files to proper spot
    tmp_html = tmp_build / 'html'
    for file in tmp_html.glob('*'):
        file.rename(tmp_build / file.name)
    tmp_html.rmdir()

    build = build_html_dir / version_match
    shutil.move(tmp_build, build)

    if version_match == 'stable':
        # replace (rather than merge into) the copy for this minor version
        if (versioned_build := build_html_dir / str(docs_version_group)).exists():
            shutil.rmtree(versioned_build)
        shutil.copytree(build, versioned_build)

    update_switcher()
    print(f'Build finished. The HTML pages are in {build}.')
