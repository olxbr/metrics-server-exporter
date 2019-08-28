# How to Contribute

This repository accepts contributions via Github pull requests.
This document outlines some of the conventions on commit message formatting,
contact points for developers and other resources to make getting your
contribution accepted.

# Before opening a issue

Before opening a new issue, it's helpful to search the issues - it's likely that another user
has already reported the issue you're facing, or it's a known issue that we're already aware of.

When opening an issue, please provide as much information as possible.

## Contribution Flow

This is a rough outline of what a contributor's workflow looks like:

- Clone the repo.
- Create a topic branch from where you want to base your work. This is usually master.
- Make commits of logical units.
- Make sure your commit messages are in the proper format, see below
- Push your changes to a topic branch in your fork of the repository.
- Submit a PR, make sure to provide as much information as possible.

### Commit Style Guideline

We follow a rough convention for commit messages borrowed from CoreOS, who borrowed theirs
from AngularJS. This is an example of a commit:

    feat(scripts/test-cluster): add a cluster test command

    this uses tmux to setup a test cluster that you can easily kill and
    start for debugging.

To make it more formal, it looks something like this:


    {type}({scope}): {subject}
    <BLANK LINE>
    {body}
    <BLANK LINE>
    {footer}

The {scope} can be anything specifying place of the commit change.

The {subject} needs to use imperative, present tense: “change”, not “changed” nor
“changes”. The first letter should not be capitalized, and there is no dot (.) at the end.

Just like the {subject}, the message {body} needs to be in the present tense, and includes
the motivation for the change, as well as a contrast with the previous behavior. The first
letter in a paragraph must be capitalized.

All breaking changes need to be mentioned in the {footer} with the description of the
change, the justification behind the change and any migration notes required.

Any line of the commit message cannot be longer than 72 characters, with the subject line
limited to 50 characters. This allows the message to be easier to read on github as well
as in various git tools.

The allowed {types} are as follows:

    chore -> maintenance
    docs -> documentation
    feat -> feature
    fix -> bug fix
    ref -> refactoring code
    style -> formatting
    test -> adding missing tests


