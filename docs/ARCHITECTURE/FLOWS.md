# Flow Architecture

Flows perform repeatable business work.

Every Flow should produce a FlowResult.

Every Flow should produce a Flow Report through Legal Logger.

## Flow owns

- Business work sequence.
- Worker selection within actor boundaries.
- Inputs and outputs for a business operation.
- FlowResult construction.

## Flow does not own

- Official history publication.
- Secret access policy.
- Authorization policy.
- Global runtime lifecycle.

## Flow evolution

Flow execution creates telemetry.

Telemetry feeds Legal Logger.

Legal Logger writes Flow Reports.

Flow Reports update Flow Profiles.

Flow Profiles reveal patterns.

Humans approve structural changes.

Flows do not rewrite themselves silently.
