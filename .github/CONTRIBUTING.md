# Contributing to floss-toolbox

**Thank you for your interest in floss-toolbox. Your contributions are highly welcome.**

We would like to improve documentation, curent scripts and tools and maangement of GitHub / GitLab API in CLI.
We would like also to extract interesting KPI and emtrics from Git histories.
Keep in mind we are in the worst case possible with only Git histories and free GitHub / GitLab organizations, so some features can have been implemented in premium plans but we don't have them today.

----

## Ground Rules

- Be nice. You can apply here the [Crocker's rules](https://old-wiki.lesswrong.com/wiki/Crocker%27s_rules) for better efficiency if you want. Some peoplee here do.
- We have a [CODE_OF_CONDUCT](CODE_OF_CONDUCT) you **must** apply.
- For any improvemens or issues, bring tests data
- When in doubt, open an issue.  For almost any type of contribution, the first step is opening an issue. Even if you think you already know what the solution is, writing down a description of the problem you're trying to solve will help everyone get context when they review your pull request. If it's truly a trivial change (e.g. spelling error), you can skip this step -- but as the subject says, when it doubt.
- Only submit your own work (or work you have sufficient rights to submit). Please make sure that any code or documentation you submit is your work or you have the rights to submit. We respect the intellectual property rights of others, and as part of contributing, we'll ask you to sign your contribution with a "Developer Certificate of Origin" (DCO) that states you have the rights to submit this work and you understand we'll use your contribution. There's more information about this topic in the [DCO section](#developer-certificate-of-origin). Keep also meta field oin your Git commits body with **Co-authored-by:**.

## Bug Reports

Ugh! Bugs!

A bug is when software behaves in a way that you didn't expect and the developer didn't intend. To help us understand what's going on, we first want to make sure you're working from the latest version.

Once you've confirmed that the bug still exists in the latest version, you'll want to check to make sure it's not something we already know about on the [open issues GitHub page](https://github.com/Orange-OpenSource/floss-toolbox/issues).

## Feature Requests & Proposals

If you've thought of a way that floss-tooblox could be better, we want to hear about it. We track `feature requests` ([examples](https://github.com/search?q=org%3Aopensearch-project+%22Is+your+feature+request+related+to+a+problem%3F%22&type=Issues)) using GitHub, so please feel free to open an issue which describes the feature you would like to see, why you need it, and how it should work. If you would like contribute code toward building it, you might consider a `feature-request` ([examples](https://github.com/Orange-OpenSource/floss-toolbox/issues?q=is%3Aissue+is%3Aopen+label%3A%22feature-request%22)) instead. A feature request is the first step to helping the community better understand what you are planning to contribute, why it should be built, and collaborate on ensuring you have all the data points you need for implementation.

## Documentation Changes

There are few documentations, mainly absed on README.md files. There must be kept updated with each fixes or evolutions.two types of documentation in OpenSearch: developer documentation, which describes how OpenSearch is designed internally, and user documentation, which describes how to use OpenSearch. 
Feel free to improve the suitable files.

## Contributing Code

As with other types of contributions, the first step is to [open an issue on GitHub](https://github.com/Orange-OpenSource/floss-toolbox/issues/new). Opening an issue before you make changes makes sure that someone else isn't already working on that particular problem. It also lets us all work together to find the right approach before you spend a bunch of time on a PR. So again, when in doubt, open an issue.

## Developer Certificate of Origin

floss-tooblox is an open source product released under the Apache 2.0 license (see either [the Apache site](https://www.apache.org/licenses/LICENSE-2.0) for example. The Apache 2.0 license allows you to freely use, modify, distribute, and sell your own products that include Apache 2.0 licensed software. See also the file *LICENSE.txt*.

We respect intellectual property rights of others and we want to make sure all incoming contributions are correctly attributed and licensed. A Developer Certificate of Origin (DCO) is a lightweight mechanism to do that.

The DCO is a declaration attached to every contribution made by every developer. In the commit message of the contribution, the developer simply adds a `Signed-off-by` statement and thereby agrees to the DCO, which you can find below or at [DeveloperCertificate.org](http://developercertificate.org/). See also the file *DCO.txt*.

We require that every contribution to floss-toolbox is signed with a Developer Certificate of Origin. Additionally, please use your real name. We do not accept anonymous contributors nor those utilizing pseudonyms.

Each commit must include a DCO which looks like this

```
Signed-off-by: Jane Smith <jane.smith@email.com>
```
You may type this line on your own when writing your commit messages. However, if your user.name and user.email are set in your git configs, you can use `-s` or `--signoff` to add the `Signed-off-by` line to the end of the commit message.

If you worked with other people on the provided contributions, add also the *Co-authored-by* in your commit body if relevant.

## Changelog, versioning and commits

floss-toolbox follows [Keep A Changelog](https://keepachangelog.com/en/1.0.0/) format and *semantic verisoning*.
We try also to apply [commit message conventions](https://www.conventionalcommits.org/en/v1.0.0/#summary)

## How to contribute

- Open an issue descrbing your needs and the evolutions or fixes you will bring
- Submit a pull request
- Ensure your commits are clean (atomic, DCO applied, co-authoring if needed)
- Keep the CHANGELOG updated
- Attach to the PR the tests data
- Do not forget to update the README associate to the folderwhere your evolutions are

Project maintainers will then update the wiki and the CONTRIBUTORS file once your pull request will be merged.

About the source files, ensure you commented and documented the use of the scripts and tools like the others existing files.
Use also the SPDX format headers.

**Thanks for your contributions!**
**Have fun, and happy coding!**
