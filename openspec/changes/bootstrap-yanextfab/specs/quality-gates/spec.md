## Purpose

Ensures code quality, type safety, and API-contract consistency are checked both before code is committed locally and before it is merged, so regressions are caught as early as possible rather than only after landing on the main branch.

## ADDED Requirements

### Requirement: Pre-Commit Enforcement
The system SHALL check code quality (lint and format) on both the frontend and backend before a commit completes, when pre-commit hooks are installed.

#### Scenario: Formatting violation blocks commit
- **WHEN** a developer with hooks installed attempts to commit code that fails a lint or format check
- **THEN** the commit is blocked until the violation is fixed or auto-fixed

### Requirement: CI Test Enforcement
Continuous integration SHALL run the backend and frontend automated test suites on every pull request and report failures.

#### Scenario: Failing test blocks merge readiness
- **WHEN** a pull request introduces a change that breaks an existing automated test
- **THEN** CI reports a failure on that pull request

### Requirement: CI Type-Check Enforcement
Continuous integration SHALL run static type checking on the backend on every pull request.

#### Scenario: Type error blocks merge readiness
- **WHEN** a pull request introduces a backend type error
- **THEN** CI reports a failure on that pull request

### Requirement: CI Drift-Check Enforcement
Continuous integration SHALL run the API client drift-check on every pull request as part of the standard quality gate suite.

#### Scenario: Drift check runs alongside other checks
- **WHEN** a pull request is opened
- **THEN** the API client drift-check runs alongside lint, format, type-check, and test checks, and its failure is reported the same way as any other check failure

### Requirement: Consistent Local/CI Enforcement Surface
The categories of checks enforced in CI SHALL also be runnable locally via pre-commit hooks, so failures can be caught before push rather than only after.

#### Scenario: Local check matches CI check
- **WHEN** a developer runs pre-commit hooks locally
- **THEN** the same lint and format checks that would fail in CI are caught locally before the commit is made
