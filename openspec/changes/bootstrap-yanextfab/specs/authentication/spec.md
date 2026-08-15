## Purpose

Provides account registration, login, session management, and password recovery so that users can securely access protected areas of the application without their credentials or session tokens being exposed to client-side code.

## ADDED Requirements

### Requirement: User Registration
The system SHALL allow a new visitor to register an account using an email address and a password.

#### Scenario: Successful registration
- **WHEN** a visitor submits a valid, previously unused email and a password meeting the complexity requirements
- **THEN** the system creates a new user account and establishes an authenticated session for them

#### Scenario: Duplicate email rejected
- **WHEN** a visitor submits an email that is already registered
- **THEN** the system rejects the registration with a clear error and creates no new account

### Requirement: Password Storage
The system SHALL NOT store user passwords in plaintext.

#### Scenario: Password is hashed at rest
- **WHEN** a user registers or changes their password
- **THEN** the system stores only a securely hashed representation of the password, never the plaintext value

### Requirement: User Login
The system SHALL allow a registered user to authenticate using their email and password.

#### Scenario: Successful login
- **WHEN** a registered user submits their correct email and password
- **THEN** the system establishes an authenticated session for that user

#### Scenario: Invalid credentials rejected
- **WHEN** a user submits an incorrect password or an unregistered email
- **THEN** the system rejects the login attempt without revealing which field was incorrect

### Requirement: Session Persistence
The system SHALL keep a user authenticated across page reloads and browser restarts, using a session token that is inaccessible to client-side JavaScript, until the session expires or the user logs out.

#### Scenario: Session survives reload
- **WHEN** an authenticated user reloads the application
- **THEN** they remain authenticated without re-entering their credentials

#### Scenario: Logout ends the session
- **WHEN** an authenticated user logs out
- **THEN** their session is invalidated and subsequent requests to protected resources are rejected

### Requirement: Protected Resource Access
The system SHALL reject unauthenticated requests to protected resources.

#### Scenario: Unauthenticated access denied
- **WHEN** an unauthenticated visitor requests a protected resource
- **THEN** the system denies access and directs them to the login flow

### Requirement: Password Recovery
The system SHALL allow a user who has forgotten their password to reset it via an emailed, time-limited link.

#### Scenario: Recovery email sent
- **WHEN** a user requests a password reset for a registered email address
- **THEN** the system sends an email containing a time-limited reset link to that address

#### Scenario: Reset completes the flow
- **WHEN** a user follows a valid, unexpired reset link and submits a new password
- **THEN** the system updates the stored password hash, and the old password no longer authenticates the account

#### Scenario: Expired or reused link rejected
- **WHEN** a user attempts to use an expired or already-used reset link
- **THEN** the system rejects the reset attempt

### Requirement: Recovery Request Confidentiality
The system SHALL NOT reveal whether a given email address is registered when a password reset is requested for it.

#### Scenario: Reset requested for unknown email
- **WHEN** a password reset is requested for an email address with no matching account
- **THEN** the system responds identically to a successful request, without sending an email or revealing that no account exists
