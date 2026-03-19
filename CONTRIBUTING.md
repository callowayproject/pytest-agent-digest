# Contributing to Pytest Agent Digest

First off, thanks for taking the time to contribute!

All types of contributions are encouraged and valued.
See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them.
Please make sure to read the relevant section before making your contribution.
It will make it much easier for us maintainers and smooth out the experience for all involved.
The community looks forward to your contributions.

> If you like the project but don't have time to contribute, that's fine.
> There are other easy ways to support the project and show your appreciation, which we would also be pleased about:
>
> - Star the project
> - Tweet about it
> - Refer to this project in your project's readme.
> - Mention the project at local meetups and tell your friends/colleagues.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating is governed by the [Pytest Agent Digest Code of Conduct](../CODE_OF_CONDUCT.md).

By participating, you are expected to uphold this code. Please report unacceptable behavior to coreyoordt@gmail.com.


## I Have a Question

> If you want to ask a question, we assume you have read the available [documentation][documentation].

Before you ask a question, research existing Issues that might help you. If you find a suitable issue and still need clarification, you can write your question about it. It is also advisable to search the Internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open a [new issue][new_issue].
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## Reporting Bugs

### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you for more information. Therefore, we ask you to investigate carefully, collect information, and describe the issue in detail in your report. Please complete the following steps to help us quickly fix any potential bug.

- Make sure that you are using the latest version.
- Determine if your bug is not an error on your side, e.g., using incompatible environment components/versions (Make sure you have read the [documentation][documentation]. If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker][issues].
- Also, search the internet (including Stack Overflow) to see if users outside the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform, and Version (Windows, Linux, macOS, x86, ARM)
  - The version of Python
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?


### How Do I Submit a Good Bug Report?

> You must never report security-related issues, vulnerabilities, or bugs that include sensitive information to the issue tracker or elsewhere in public. Instead, sensitive bugs must be sent by email to coreyoordt@gmail.com.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [issue][new_issue]. (Since we can't be sure at this point whether it is a bug or not, please don't talk about a bug yet and don't label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* someone else can follow to recreate the issue independently. This usually includes your code. You should isolate the problem and create a reduced test case for good bug reports.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue using the steps you provided. If there are no steps or no obvious way to reproduce the issue, the team will ask you for those steps and will not address them until they are included.
- If the team can reproduce the issue, it will be marked for [implementation](#your-first-code-contribution).


## Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Pytest Agent Digest, including entirely new features and minor improvements to existing functionality. Following these guidelines will help maintainers and the community understand your suggestions and find related suggestions.

### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation][documentation] carefully and discover if the functionality is already covered, maybe by an individual configuration.
- Search the [issues][issues] to see if the enhancement has already been suggested. If it has, comment on the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case of the feature's merits to the project's developers. Remember that we want features that are useful to most users and not just a tiny subset. If you're targeting a minority of users, consider writing an add-on/plugin library.

### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues][issues].

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- **Please describe the problem or use case** this enhancement solves **or the new benefit** it provides.
- **Please explain why this enhancement would be helpful** to most users. You can also point out the other projects that solved it better and which could serve as inspiration.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- If appropriate, you may also tell how current alternatives do not work for you.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

## Your First Code Contribution


> ### Legal Notice
>
> When contributing to this project, you must agree that you have authored 100% of the content, have the necessary rights, and that the content you contribute may be provided under the project license.

### Setup

There are several ways to create an isolated environment. The recommended way is using [uv](https://docs.astral.sh/uv/getting-started/installation/).

Run the following in a terminal:

```console
$ git clone https://github.com/callowayproject/pytest-agent-digest.git

$ cd pytest-agent-digest

$ uv sync
```

### Run tests

Once set up, you should be able to run tests:
```console
$ pytest
```

## Install Pre-commit Hooks


Pre-commit hooks are scripts that run every time you make a commit. If any of the scripts fail, it stops the commit. You can see a listing of the checks in the ``.pre-commit-config.yaml`` file.

```console
$ pre-commit install
```

[documentation]: https://callowayproject.github.io/pytest-agent-digest/
[new_issue]: https://github.com/callowayproject/pytest-agent-digest/issues/new
[issues]: https://github.com/callowayproject/pytest-agent-digest/issues
