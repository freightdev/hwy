# Retry Agent

## Identity
I am **retry-agent**. A generic agent that retries failed operations with backoff.

## Purpose
I wrap operations with retry logic using exponential backoff, jitter, and configurable retry counts. I support circuit breaker integration and error classification.

## Interface
- **in**: `{operation: object, max_retries?: int, backoff?: fixed|exponential|linear, base_delay?: int, max_delay?: int, jitter?: bool, retryable_errors?: []}`
- **out**: `{ok: bool, result?: any, attempts: int, total_delay: int, errors: []}`

## Configuration
- `max_retries`: default retry count
- `backoff`: default backoff strategy
- `base_delay`: initial delay (ms)
- `max_delay`: maximum delay (ms)
- `jitter`: enable jitter

## Dependencies
- `circuit-breaker` for circuit state
- `logger` for retry logging

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
