# Execution Architecture

Execution Runtime owns the lifecycle of work.

Every meaningful runtime operation gets an Execution ID.

Execution Runtime does not perform business work.

Execution Runtime does not write official reports.

Execution Runtime coordinates lifecycle so Direct Dispatch, Actor Runtime, Legal Logger, and Telemetry can stay in their own lanes.

---

## Why Execution Runtime exists

Before Execution Runtime, Direct Dispatch could route directly to actor handlers.

That worked for early proof-of-concept code, but it placed lifecycle responsibility too close to routing.

Execution Runtime exists so every future flow inherits the same lifecycle behavior:

- Start.
- Finish.
- Fail.
- Cancel.
- Timeout.
- Event publication.
- Timeline reconstruction.
- Runtime health visibility.

Future actors should not invent their own lifecycle machinery.

---

## Execution status

Every execution has one lifecycle status:

- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`
- `timed_out`

The current Python reference implementation is in:

```text
codriver/runtime/execution.py
```

---

## Execution owns

Execution Runtime owns:

- Execution ID generation.
- Start state.
- Finish state.
- Failure state.
- Cancellation state.
- Timeout state.
- Runtime status.
- Execution-level runtime events.
- Timeline linkage.

Execution Runtime is the lifecycle authority.

---

## Execution does not own

Execution Runtime does not own:

- Actor business decisions.
- Actor domain ownership.
- Flow business meaning.
- Official report authorship.
- Telemetry measurement.
- Frontend presentation.
- Database truth outside its runtime boundary.

Legal Logger still owns official reports.

Telemetry still measures.

Events coordinate.

---

## Runtime event boundary

Runtime events coordinate lifecycle.

Telemetry measures runtime and worker behavior.

Do not merge them.

Current runtime events are defined in:

```text
codriver/runtime/events.py
```

Supported first events:

- `ExecutionStarted`
- `ExecutionCompleted`
- `ExecutionFailed`
- `ExecutionCancelled`
- `ExecutionTimedOut`
- `FlowStarted`
- `FlowCompleted`
- `FlowFailed`
- `ActorStarted`
- `ActorCompleted`
- `ActorFailed`
- `ReportPublished`
- `ProfileUpdated`

The Event Bus lives at:

```text
codriver/runtime/event_bus.py
```

---

## Timeline

Timeline is built from runtime events.

The current Python reference timeline is in:

```text
codriver/runtime/timeline.py
```

Timeline answers:

- What lifecycle events happened?
- In what order?
- Which execution did they belong to?
- Which actor or flow did they reference?

Timeline is not the same as telemetry.

Timeline reconstructs order.

Telemetry measures work.

---

## Actor Runtime boundary

Direct Dispatch should not call actor handlers directly.

Direct Dispatch routes to Actor Runtime.

Actor Runtime invokes the actor through one standard boundary.

Current Python reference implementation:

```text
codriver/runtime/actor_runtime.py
```

Actor Runtime owns:

- Actor invocation boundary.
- ActorStarted events.
- ActorCompleted events.
- ActorFailed events.
- Handler exception capture.
- Normalized ActorResponse failure when a handler raises.

Actor Runtime does not own actor business logic.

---

## Standard path

```text
User
↓
CoDriver
↓
Direct Dispatch
↓
Execution Runtime
↓
FlowStarted event
↓
Actor Runtime
↓
Actor
↓
Telemetry
↓
FlowCompleted or FlowFailed event
↓
Legal Logger
↓
Execution Report
↓
Flow Report
↓
Flow Profile
↓
Logbook
↓
FlowResult
↓
ExecutionCompleted or ExecutionFailed event
↓
CoDriver
```

---

## Direct Dispatch responsibility

Direct Dispatch remains the router.

It selects the flow and actor.

It creates ActorContext.

It calls Actor Runtime.

It passes the actor response to Legal Logger.

It does not invoke actor handlers directly.

It does not write reports.

It does not merge telemetry and events.

---

## Legal Logger relationship

Legal Logger still owns official history.

Execution Runtime and Event Bus can say:

- an execution started
- an actor started
- a flow completed
- a report was published

But Legal Logger owns the actual report content:

- Execution Report
- Flow Report
- Flow Profile
- Logbook entries

---

## Current verification

The Execution Runtime phase is covered by tests in:

```text
tests/test_execution_runtime.py
```

The tests prove:

1. Execution IDs are created.
2. Events publish.
3. Timeline records ordered events.
4. Actor Runtime can invoke Packet Pilot through the registry.
5. Direct Dispatch routes through Actor Runtime.
6. Legal Logger still produces FlowResult.

---

## Moonrust migration notes

Rust Crate:

```text
moonrust/crates/runtime
```

Ownership:

Execution Runtime.

Dependencies:

- Event Bus.
- Actor Runtime.
- Legal Logger boundary.
- Telemetry boundary.

Stable:

No.

Port Status:

Prototype.

Migration Requirements:

Prove lifecycle correctness, cancellation, retry, timeout, and recovery behavior in Python before porting.
