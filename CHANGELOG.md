# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.16.0..dev)

## [2.16.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.16.0..2.15.0) - 2024-03-16

### Added

- [Utils] Add metrics and improve outputs for third-party generator scripts

### Changed

- [Licenses Inventory] Update dependency pytests to v7.4.4
- [Licenses Inventory] Update dependency beautifulsoup4 to v4.12.3
- [Licenses Inventory] Improve requirements for Python modules in use ([#108](https://github.com/Orange-OpenSource/floss-toolbox/issues/108))
- [Project] Plug Renovate, Gitleaks ([#112](https://github.com/Orange-OpenSource/floss-toolbox/issues/112))
- [Project] Apply REUSE standards ([#114](https://github.com/Orange-OpenSource/floss-toolbox/issues/114))
- [Project] Improve a bit CHANGELOG by leading scope keyword for each line

### Security

- [Licenses Inventory] Bump requests from v2.28.1 to v2.31.0 ([#3](https://github.com/Orange-OpenSource/floss-toolbox/security/dependabot/3))

## [2.15.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.15.0..2.14.0) - 2024-03-12

### Added

- [Project] Generate THIRD-PARTY.md based on user inputs ([#119](https://github.com/Orange-OpenSource/floss-toolbox/issues/119))

## [2.14.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.14.0..2.13.0) - 2024-03-01

### Added

- [Utils] Generate template-based text using variables ([#84](https://github.com/Orange-OpenSource/floss-toolbox/issues/84))

### Changed

- [Project] Make CHANGELOG more compliant ([#103](https://github.com/Orange-OpenSource/floss-toolbox/issues/103))

## [2.13.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.13.0..2.12.0) - 2023-07-19

### Added

- [Diver] Compute metrics with in parameter URL to clone repo ([#98](https://github.com/Orange-OpenSource/floss-toolbox/issues/98))

### Fixed

- [Project] Broken links in README ([#96](https://github.com/Orange-OpenSource/floss-toolbox/issues/96))

## [2.12.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.12.0..2.11.0) - 2023-07-18

### Added

- [Diver] Lines of codes and useful metrics ([#28](https://github.com/Orange-OpenSource/floss-toolbox/issues/28))

### Changed

- [Project] Add DCO ([#87](https://github.com/Orange-OpenSource/floss-toolbox/issues/87))
- [Project] Add security policy file ([#90](https://github.com/Orange-OpenSource/floss-toolbox/issues/90))
- [Project] Split README files  ([#85](https://github.com/Orange-OpenSource/floss-toolbox/issues/85))
- [Licenses Inventory] Move HTML test files to archives of release ([#86](https://github.com/Orange-OpenSource/floss-toolbox/issues/86))
- [GitHub] Add in dry-run Gemfiles ([#93](https://github.com/Orange-OpenSource/floss-toolbox/issues/93))

## [2.11.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.11.0..2.10.1) - 2023-06-28

### Added

- [GitHub] Set teams permissions to read ([#82](https://github.com/Orange-OpenSource/floss-toolbox/issues/82))

## [2.10.1](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.10.1..2.10.0) - 2023-05-31

### Fixed

- [Diver] Path variables not protected ([#80](https://github.com/Orange-OpenSource/floss-toolbox/issues/80))

## [2.10.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.10.0..2.9.0) - 2023-05-30

### Added

- [Licenses Inventory] New release ([#77](https://github.com/Orange-OpenSource/floss-toolbox/issues/77))

## [2.9.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.9.0..2.8.0) - 2023-03-31

### Added

- [Licenses Inventory] New release ([#64](https://github.com/Orange-OpenSource/floss-toolbox/issues/64))

## [2.8.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.8.0..2.7.1) - 2023-03-10

### Added

- [Project] Split dry run ([#68](https://github.com/Orange-OpenSource/floss-toolbox/issues/68))

### Changed

- [Project] Update copyright ([#70](https://github.com/Orange-OpenSource/floss-toolbox/issues/70))
- [Project] Improve README ([#69](https://github.com/Orange-OpenSource/floss-toolbox/issues/69))

## [2.7.1](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.7.1..2.7.0)

### Changed

- Add missing files ([#63](https://github.com/Orange-OpenSource/floss-toolbox/issues/63))

## [2.7.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.7.0..2.6.0) - 2023-01-18

### Added

- Package manager - Extract from files downloaded dependencies ([#2](https://github.com/Orange-OpenSource/floss-toolbox/issues/2))

## [2.6.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.6.0..2.5.0) - 2022-05-05

### Added

- Look for leaks and vulnerabilities with exclusion of projects ([#57](https://github.com/Orange-OpenSource/floss-toolbox/issues/57))

## [2.5.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.5.0..2.4.0) - 2022-03-09

### Added

- GitLab Auto Backup ([#32](https://github.com/Orange-OpenSource/floss-toolbox/issues/32))
- Look for leaks (GitLab) ([#49](https://github.com/Orange-OpenSource/floss-toolbox/issues/49))

### Fixed

- Failure of git log if no commits ([#52](https://github.com/Orange-OpenSource/floss-toolbox/issues/52))

## [2.4.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.4.0..2.3.0) - 2022-03-08

### Added

- [GitHub] Look for leaks ([#44](https://github.com/Orange-OpenSource/floss-toolbox/issues/44))
- Dry run ([#29](https://github.com/Orange-OpenSource/floss-toolbox/issues/29))

### Changed

- Check of vulnerabilities ([#37](https://github.com/Orange-OpenSource/floss-toolbox/issues/37))
- Fix typo in doc and files ([#40](https://github.com/Orange-OpenSource/floss-toolbox/issues/40))

## [2.3.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.3.0..2.2.0) - 2022-02-25

### Added

- Find repositories with vulnerabilities (Dependabot) ([#20](https://github.com/Orange-OpenSource/floss-toolbox/issues/20))

## [2.2.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.2.0..2.1.0) 2022-02-24

### Added

- Backup of repositories ([#19](https://github.com/Orange-OpenSource/floss-toolbox/issues/19))
- Extract email addresses ([#27](https://github.com/Orange-OpenSource/floss-toolbox/issues/27))

## [2.1.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.1.0..2.0.0) - 2021-10-06

### Added

- List all contributors of a Git repository using Git history ([#13](https://github.com/Orange-OpenSource/floss-toolbox/issues/13))

## [2.0.0](https://github.com/Orange-OpenSource/floss-toolbox/compare/2.0.0..1.0.0) - 2021-06-05

## Added

- Get all members of GitHub organization ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get members who don't have 2FA enabled ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get members of organization with "company" field undefined ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get projects which don't have any assigned GitHub team ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get users which have undefined or hidden email ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get users which may have not suitable fullname ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get repositories with undefined licenses ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get repositories which seems to be unconform (i.e. missing files) ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Get repositories which seems to be empty or have not enough files ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Define permissions (push / write) for all contributors of all projects (except teams and organization owners) ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))
- Define permissions (push / write) for all teams of all projects ([#4](https://github.com/Orange-OpenSource/floss-toolbox/issues/4))

## [1.0.0]

### Added

- Find contributors in files using a base of words and producing logs
- Find contributors in git logs
- Find credentials in files
- Find missing signed-off in commits
- Find notices