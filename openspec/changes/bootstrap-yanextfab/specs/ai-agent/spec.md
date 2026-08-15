## Purpose

Provides a working example of a conversational, tool-using AI agent with persisted state and streamed responses, so new projects built from this boilerplate have a real integration to extend instead of building one from scratch.

## ADDED Requirements

### Requirement: Streamed Agent Responses
The system SHALL stream an AI agent's response to the frontend incrementally as it is generated, rather than waiting for the full response before sending anything.

#### Scenario: Partial response arrives before completion
- **WHEN** a user sends a message to the agent
- **THEN** the frontend begins receiving and displaying response content before the agent has finished generating the full reply

### Requirement: Tool Use
The example agent SHALL be able to invoke at least one external tool as part of producing a response.

#### Scenario: Agent uses its tool
- **WHEN** a user's message requires information the agent does not already have
- **THEN** the agent invokes its available tool and incorporates the result into its response

### Requirement: Conversation State Persistence
The system SHALL persist an agent conversation's state so that it survives a backend process restart.

#### Scenario: Conversation resumes after restart
- **WHEN** the backend process restarts in the middle of a conversation
- **THEN** a subsequent message in the same conversation continues from the persisted state rather than starting over

### Requirement: Streaming Payload Validation
The frontend SHALL validate the shape of each streamed event before rendering it.

#### Scenario: Malformed stream event
- **WHEN** a streamed event does not match the expected shape
- **THEN** the frontend rejects that event rather than rendering it or crashing

### Requirement: LLM Provider Substitutability
The system SHALL allow the underlying LLM provider to be changed via configuration, without changing the agent's logic.

#### Scenario: Provider swapped via configuration
- **WHEN** the configured LLM provider is changed
- **THEN** the agent continues to function using the newly configured provider without any code changes to the agent's logic
