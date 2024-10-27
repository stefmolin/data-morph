"""Maintains the stable docs on the latest version; groups others together."""

import shutil
from pathlib import Path

from packaging.version import parse as parse_version

import data_morph

# information on where temporary and permanent files will go
build_html_dir = Path('_build') / 'html'
tmp_build = Path('_build') / '_tmp'


def determine_versions():
    """Determine stable/dev/etc. and docs version number."""
    last_minor_release = sorted(
        [
            parse_version(directory.name)
            for directory in Path().glob(f'{build_html_dir}/[0-9].[0-9]/')
        ]
        or [parse_version('0.0')]
    )[-1]
    docs_version = parse_version(data_morph.__version__)
    docs_version_group = parse_version(f'{docs_version.major}.{docs_version.minor}')

    if docs_version.is_devrelease:
        version_match = 'dev'
    elif docs_version_group >= last_minor_release:
        version_match = 'stable'
    else:
        version_match = f'{docs_version.major}.{docs_version.minor}'
    return version_match, docs_version_group


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
        shutil.copytree(
            build,
            build_html_dir / str(docs_version_group),
            dirs_exist_ok=True,
        )
    print(f'Build finished. The HTML pages are in {build}.')
