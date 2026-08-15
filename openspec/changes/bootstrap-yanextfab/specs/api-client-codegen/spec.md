## Purpose

Keeps frontend API calls compile-time type-checked against the backend's actual API surface, and makes it impossible for the two to silently drift apart without a build failure.

## ADDED Requirements

### Requirement: Typed Client Reflects Backend API
The generated frontend API client SHALL expose types that match the backend's current API contract (request and response shapes) for every implemented endpoint.

#### Scenario: New backend field appears in generated types
- **WHEN** a backend endpoint's response schema gains a new field
- **THEN** regenerating the client produces a type that includes the new field

#### Scenario: Removed backend field is no longer typed
- **WHEN** a backend endpoint's response schema removes a field
- **THEN** regenerating the client removes that field from the generated type, causing any frontend code still referencing it to fail type-checking

### Requirement: Automatic Regeneration During Development
The frontend's generated API client SHALL be regenerated automatically when the backend's API schema changes while the local development environment is running, without a developer manually invoking a generation command.

#### Scenario: Backend route added during local development
- **WHEN** a developer adds or changes a backend route while the local development environment is running
- **THEN** the frontend's generated client is regenerated automatically, without a manual command

### Requirement: CI Drift Detection
Continuous integration SHALL fail when the committed generated client does not match what regenerating it from the current backend API would produce.

#### Scenario: Client committed out of date
- **WHEN** a pull request changes a backend endpoint but does not include the corresponding regenerated client
- **THEN** the CI drift-check fails and blocks the pull request

#### Scenario: Client committed in sync
- **WHEN** a pull request's committed client matches what regeneration from the current backend API produces
- **THEN** the CI drift-check passes
