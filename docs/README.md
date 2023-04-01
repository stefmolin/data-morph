# Docs

1. Install the docs dependencies: `pip install '.[docs]'`.
2. From this directory, run `python3 -m sphinx -b html . _build/html/<version>`.

Note that if you clean out the `_build` directory, you need to run this again:

```shell
cd _build
git worktree add -f html gh-pages
```
