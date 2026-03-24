# ADR 0001: Modular Monolith First

## Status

Accepted

## Decision

Trend Buddy starts as a modular monolith with one backend entrypoint in `apps/api` and explicit domain modules in `packages/core`.

## Rationale

- The current repository is at architecture-definition stage, so one deployable keeps delivery simple.
- Core business boundaries can still be enforced through adapters and package ownership.
- This shape preserves a clean migration path to service extraction once throughput, compliance, or team size requires it.

## Consequences

- Vendor integrations remain isolated under `packages/integrations`.
- Shared contracts remain stable when modules are later split into services.
- Operational complexity stays low during early product development.
