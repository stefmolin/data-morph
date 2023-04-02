# Docs

1. Install the docs dependencies: `pip install '.[docs]'`.
2. From this directory, run `make html`.

## Managing versions

The versions that will show up in the switcher must be kept up-to-date in `_static/switcher.json`.

## Note on cleaning
Use `make clean` to clean out the `_build` directory properly, if you use `rm` instead, you will need to run this again:

```shell
cd _build
git worktree add -f html gh-pages
```
