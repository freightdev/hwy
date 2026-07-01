# Worker Architecture

Workers perform mechanical operations.

Workers should be small, observable, and replaceable.

## Worker Runtime owns

- Worker invocation.
- Retry behavior.
- Timeout behavior.
- Cancellation behavior.
- Worker telemetry.
- Worker result normalization.

## Workers own

- One mechanical capability.
- Clear inputs.
- Clear outputs.
- Clear failure modes.

## Workers do not own

- Actor business ownership.
- Official reports.
- Runtime lifecycle.
- Global truth.

## Design goal

Workers should be easy to monitor, replay, replace, and port to Moonrust when proven.
