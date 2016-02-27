# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/n8henrie/eyeflask/issues>.

If you are reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in
    troubleshooting.
-   Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is
open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
"feature" is open to whoever wants to implement it.

### Write Documentation

Eyeflask could always use more documentation, whether as part of the official
EyeFlask docs, in docstrings, or even on the web in blog posts, articles, and
such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/n8henrie/eyeflask/issues>.

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to
    implement.
-   Remember that this is a volunteer-driven project, and that
    contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up EyeFlask
for local development.

1.  Fork the `eyeflask` repo on GitHub.
1.  Clone your fork locally:

        $ git clone git@github.com:your_name_here/eyeflask.git

1.  Install your local copy into a virtualenv. Assuming you have
    python >= 3.4 installed, this is how you set up your fork for
    local development:

        $ cd eyeflask
        $ python3 -m venv venv
        $ source venv/bin/activate
        $ pip install -e .

1.  Create a branch for local development:

        $ git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

1.  When you're done making changes, check that your changes pass flake8
    and the tests, including testing other Python versions with tox:

        $ flake8 eyeflask tests
        $ python3 setup.py test
        $ tox

    To get flake8 and tox, just pip install them into your virtualenv.

1.  Commit your changes and push your branch to GitHub:

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

1.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests if I am using tests in the repo.
1.  If the pull request adds functionality, the docs should be updated.
    Put your new functionality into a function with a docstring, and add
    the feature to the list in README.md
1.  The pull request should work for Python 3.4 and 3.5. If I have included a
    `.travis.yml` file in the repo, check
    <https://travis-ci.org/n8henrie/fauxmo/pull_requests> and make sure that
    the tests pass for all supported Python versions.

## Tips

To run a subset of tests: `py.test tests/test_your_test.py`
