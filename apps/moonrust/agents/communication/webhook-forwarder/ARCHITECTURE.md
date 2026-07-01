# Webhook Forwarder

## Identity
I am **webhook-forwarder**. I forward webhooks to multiple destinations.

## Purpose
I receive webhooks and forward them to multiple registered endpoints with transformation and retry.

## Interface
in: {op: register|forward|transform, source, destinations} / out: {ok, forwarded, failed, results}

## Configuration
max_destinations, retry_count, retry_delay, batch_interval, delivery_guarantee

## Dependencies
webhook-handler, http-client, queue-manager

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
