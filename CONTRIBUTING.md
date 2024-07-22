# Contributing Guidelines

Contributions are welcome. Please adhere to the following process.

## 1. Open an issue
Open up an issue describing in detail the bug or feature request you are proposing. Be sure to fill out all the information requested in the template. Please wait for confirmation from a maintainer that this unit of work is in line with the project's roadmap *before* submitting a pull request.

## 2. Work on your changes
Once you have been given the go ahead, you can start working on the code. Start by forking the project, cloning locally, and then creating a branch to work on. You will need to then install the main dependencies as well as the `dev` and `docs` dependencies, which can be done by running the following command:

```shell
$ pip install -e '.[dev,docs]'
```

Set up the pre-commit hooks to make sure you can pass the CI checks:

```shell
$ pre-commit install
```

All commits will be squashed, so just make sure that the final commit passes all linting, documentation, and testing checks. These will run in GitHub Actions when you open a pull request, but you should also run them locally:

```shell
$ pre-commit run --all-files  # linting and documentation format checks
$ pytest                      # run the test suite
$ cd docs && make html        # build the documentation locally
```

Some things to remember:

- All code must be documented using docstrings in the [numpydoc style](https://numpydoc.readthedocs.io/en/latest/format.html) &ndash; the pre-commit hooks will check for this.
- Any changes to the API must be accompanied by either an additional test case or a new test. Run `pytest` to make sure your changes are covered.
- Documentation for the project is built with Sphinx. Your changes must render correct in the output. Run `make html` from the `docs` directory and inspect the result.

## 3. Open a pull request

Once you have finished with the task you are working on and all the checks and tests pass, you can create a pull request. Please consult [GitHub's guide on how to do this](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork), if you need some guidance.

In your description, please do the following:
1. Link to the corresponding issue for this unit of work.
2. Describe what you changed and why.
3. Include, if applicable, any testing instructions.

When you create your pull request, first-time contributors will need to wait for a maintainer to approve running the GitHub Actions workflows. Please be patient until this happens.

Once it does, the same checks described above (testing, documentation, linting) that you ran on your machine will run on Linux, macOS, and Windows with multiple versions of Python. Please note that it is possible that differences in operating systems and/or Python versions results in a failure, despite it working on your machine.

If anything fails, please attempt to fix it as we're unlikely to review your code until everything passes. If stuck, please feel free to leave a note in the pull request enumerating what you have already tried and someone may be able to offer assistance.

## 4. Code review

After all checks in your pull request pass, a maintainer will review your code. In many cases, there will be some feedback to address, and this may require a few iterations to get to the best implementation. Remember to be patient and polite during this process.

## 5. Congratulations!

When the pull request is approved, it will be merged into the `main` branch. Users of this project won't have your changes until the next release is made.
