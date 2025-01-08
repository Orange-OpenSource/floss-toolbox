<!-- Inspired by https://github.com/Orange-OpenSource/ouds-ios/blob/develop/.github/DEVELOP.md -->

# Developer guide

<!-- TODO: Do not forget to update the menu -->
- [Technical preconditions](#technical-preconditions)
- [Build project](#build-project)
- [Run tests](#run-tests)
- [Developer Certificate of Origin](#developer-certificate-of-origin)
- [Commits, changelog, release note, versioning](#commits-changelog-release-note-versioning)
  * [About commits](#about-commits)
  * [About release note and changelog](#about-release-note-and-changelog)

## Technical preconditions

<!-- TODO: Add details about commnds to install dependencies (with brew, bundler, npm, pod commands, etc. -->

<!-- TODO: Talk about the versions of the environments, like verison of Ruby, which JDK, etc. -->

## Build project

<!-- TODO: Explain how you can build the project, put in production, etc. -->

## Run tests 

<!-- TODO: Explain which tests are done and how they can be run -->

## Developer Certificate of Origin

The *Linux Foundation* *Developer Certificate of Origin* is applied for this project, and very commit must be signed-off.
You can get its full text at [developercertificate.org](https://developercertificate.org/).

## Commits, changelog, release note, versioning

### About commits

#### Convention commits rules

Try as best as possible to apply [conventional commits rules](https://www.conventionalcommits.org/en/v1.0.0/).
Keep in mind to have your commits well prefixed, and with the issue number between parenthesis at the end, and also if needed the pull request issue number.
If your commits embed contributions for other people, do not forget to [add them as co-authors](https://docs.github.com/fr/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors).
All of you should also comply to DCO.

Your commit message should be prefixed by keywords [you can find in the specification](https://www.conventionalcommits.org/en/v1.0.0/#specification):
- `fix:`
- `feat:`
- `build:`
- `chore:`
- `ci:`
- `docs:`
- `style:`
- `refactor:`
- `perf:`
- `test:`

You can add also ! after the keyword to say a breaking change occurs, and also add a scope between parenthesis like:
- `feat!:` breaking change because..
- `feat(API)!:` breaking change in the API because..
- `feat:` add something in the API...

#### Chain of responsability

We can add metafields picked from [this good guideline](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/process/submitting-patches.rst#n525) in the commit messages.

This is not mandatory (yet) but a good practice and quite interesting to know who reviewed and validated what.

For example, given a commit to fix the issue n°42, with Foo FOO and Bar BAR as commit authors, with Wizz WIZZ as source code reviewer, and John DOE as accessibility / PO / design reviewer, the commit should be like:

```text
fix: title of your commit (#42)

Some details about the fix you propose

Co-authored-by: Foo FOO <foo email>
Co-authored-by: Bar BAR <bar email>

Reviewed-by: Wizz WIZZ <wizz email>

Acked-by: John DOE <john email>

Signed-off-by: Foo FOO <foo email>
Signed-off-by: Bar BAR <bar email>
```

### About release note and changelog

We try also to apply [keep a changelog](https://keepachangelog.com/en/1.0.0/), and [semantic versioning](https://semver.org/spec/v2.0.0.html) both with [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

<!-- TODO: You can talk about also:
- linters
- tools like Renovate, GitLeaks
- CI/CD
- etc.
-->