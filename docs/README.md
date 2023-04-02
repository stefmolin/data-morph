# Docs

1. Install the docs dependencies: `pip install '.[docs]'`.
2. From this directory, run `python3 -m sphinx -b html . _build/html/<version>`.

*Group builds by `major.minor` versions.*

## Managing versions

The versions that will show up in the switcher must be kept up-to-date in `_static/switcher.json`.

## Note on cleaning
Note that if you clean out the `_build` directory, you need to run this again:

```shell
cd _build
git worktree add -f html gh-pages
```
