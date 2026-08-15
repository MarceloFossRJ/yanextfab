## Purpose

Defines how the full application — frontend, backend, database, and supporting services — can be brought up as a working system, both for local development and for shipping to production, without depending on a single proprietary hosting platform.

## ADDED Requirements

### Requirement: Single-Command Local Environment
The system SHALL bring up a fully working local environment — frontend, backend, database, and dev email catcher — with a single command.

#### Scenario: Fresh checkout boots successfully
- **WHEN** a developer runs the documented single command against a fresh checkout with no prior local setup
- **THEN** the frontend, backend, database, and dev email catcher are all running and able to communicate with each other

### Requirement: Environment Portability
The primary deployment path SHALL run without modification on any host capable of running the specified container orchestration, not a single proprietary platform.

#### Scenario: Deploys to a different host
- **WHEN** the primary deployment artifact is run on a different compatible host than it was developed on
- **THEN** the application starts and functions without requiring host-specific code changes

### Requirement: Documented Frontend-Only Deployment Path
A documented deployment path SHALL exist allowing the frontend to be deployed independently to a platform-native hosting target, alongside the primary path.

#### Scenario: Frontend deployed independently
- **WHEN** a developer follows the documented frontend-only deployment path
- **THEN** the frontend deploys and functions correctly while still communicating with a separately hosted backend
