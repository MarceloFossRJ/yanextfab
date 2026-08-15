## Purpose

Provides an authenticated area of the application where a logged-in user navigates between example features, proving out the full typed data path end-to-end independent of the AI capability, alongside the AI chat example.

## ADDED Requirements

### Requirement: Dashboard Requires Authentication
The dashboard SHALL be inaccessible to unauthenticated visitors.

#### Scenario: Unauthenticated visitor redirected
- **WHEN** an unauthenticated visitor requests the dashboard
- **THEN** they are redirected to the login flow instead of seeing dashboard content

### Requirement: Navigation Shell
Authenticated users SHALL see consistent navigation, including a way to log out, across all dashboard pages.

#### Scenario: Logout available from any dashboard page
- **WHEN** an authenticated user is on any dashboard page
- **THEN** a logout control is visible and, when used, ends their session

### Requirement: Example Resource CRUD
The dashboard SHALL let an authenticated user create, view, update, and delete instances of one example resource that they own.

#### Scenario: Create example resource
- **WHEN** an authenticated user submits a valid new item through the dashboard form
- **THEN** the item is persisted and appears in that user's list of items

#### Scenario: Invalid submission rejected before request
- **WHEN** an authenticated user submits a form with invalid data
- **THEN** the form is rejected before any request is sent to the backend, with a validation error shown

#### Scenario: Update example resource
- **WHEN** an authenticated user edits an existing item they own and submits the change
- **THEN** the persisted item reflects the update

#### Scenario: Delete example resource
- **WHEN** an authenticated user deletes an item they own
- **THEN** the item no longer appears in their list

### Requirement: AI Chat Access
The dashboard SHALL provide a page where an authenticated user can converse with the example AI agent.

#### Scenario: Chat page reachable from dashboard navigation
- **WHEN** an authenticated user navigates to the chat page from the dashboard
- **THEN** they can send a message and see the agent's streamed response
