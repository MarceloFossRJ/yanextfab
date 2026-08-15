## Purpose

Defines the structure, publication, and scope of Yanextfab's user-facing documentation: a published, searchable, navigable documentation site that replaces most of the current README, plus the reduced role the README keeps as the entry point into it.

## ADDED Requirements

### Requirement: Published Documentation Site
The repo SHALL publish a browsable documentation site built from Markdown source, automatically rebuilt and redeployed on every push to `main`, so the site's content always reflects the current state of `main`.

#### Scenario: Site rebuilds on push to main
- **WHEN** a commit is pushed to `main`
- **THEN** the documentation site is rebuilt and redeployed to reflect that commit's content

#### Scenario: Site is publicly browsable
- **WHEN** a user navigates to the published documentation site's URL
- **THEN** they see the current documentation without needing any repo access beyond what's already public

### Requirement: Single Unversioned Documentation Site
The documentation site SHALL present exactly one version of the docs, tracking `main`, without a version switcher or per-release document snapshots.

#### Scenario: No version selector shown
- **WHEN** a user views the documentation site
- **THEN** there is no version switcher and no way to view docs as they existed for a specific past release

### Requirement: Documentation Site Search and Navigation
The documentation site SHALL provide full-text search across its pages and a persistent navigation menu for moving between topics without returning to a single long page.

#### Scenario: Reader searches for a term
- **WHEN** a user enters a search term on the documentation site
- **THEN** matching pages or sections are surfaced for the user to navigate to

### Requirement: Documentation Site Content Scope
The documentation site SHALL cover, at minimum, the following topics as distinct, navigable pages: getting started (prerequisites, template setup, quickstart), tech stack, testing, deployment, API client codegen, configuration, and troubleshooting.

#### Scenario: Reader finds a specific topic
- **WHEN** a user opens the documentation site's navigation
- **THEN** each of the listed topics is reachable as its own page rather than requiring a full-page scroll through unrelated content

### Requirement: Documentation Site Excludes Agent/Process Docs
The documentation site SHALL NOT include content from `AGENTS.md` or `openspec/`, which remain repo-local, contributor/agent-facing process documentation outside the site's intended audience.

#### Scenario: Process docs stay out of the site
- **WHEN** the documentation site's navigation is reviewed
- **THEN** no page reproduces or links into `AGENTS.md` or `openspec/` content as site content

### Requirement: README Scope
The root `README.md` SHALL contain only: a project pitch, prerequisites, "Use this template" steps, and a quickstart, plus a link to the published documentation site. It SHALL NOT duplicate content that lives on the documentation site.

#### Scenario: Reader needs topic detail beyond the quickstart
- **WHEN** a reader looks in `README.md` for deployment, tech stack, testing, configuration, or troubleshooting detail
- **THEN** they find a link to the documentation site rather than the full content inline
