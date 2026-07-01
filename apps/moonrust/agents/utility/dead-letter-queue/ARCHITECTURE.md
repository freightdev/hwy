# Dead Letter Queue

## Identity
I am **dead-letter-queue**. I manage dead letter queues for failed messages.

## Purpose
I store messages that failed processing after retries, support inspection, replay, and lifecycle management.

## Interface
in: {op: store|inspect|replay|purge|status, message?} / out: {ok, dlq_size, messages: [{id, source, error, timestamp}], replayed}

## Configuration
max_size, retention_days, auto_purge, replay_limit, notify_on_fill, replay_to

## Dependencies
retry-queue, message-queue-consumer, notification-dispatcher

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
