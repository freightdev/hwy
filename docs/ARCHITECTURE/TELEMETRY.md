# Telemetry Architecture

Events coordinate.

Telemetry measures.

Timeline reconstructs what happened.

## Events

Examples:

- ExecutionStarted.
- ExecutionCancelled.
- ExecutionTimedOut.
- FlowStarted.
- ActorStarted.
- WorkerStarted.
- ApprovalRequested.
- ApprovalGranted.
- FlowCompleted.
- FlowFailed.
- ReportPublished.
- ProfileUpdated.

## Telemetry

Examples:

- Runtime.
- Action count.
- Worker latency.
- Token count.
- Cache hits.
- Cache misses.
- Retry count.
- Error count.
- Model used.

## Rule

Do not confuse coordination events with measurement telemetry.

Both are needed.
