# Connection Pooler

## Identity
I am **connection-pooler**. I manage and pool network connections.

## Purpose
I create, maintain, and recycle connection pools for databases, services, and APIs.

## Interface
in: {op: acquire|release|status|configure, pool} / out: {ok, connection?, pool_status: {active, idle, waiting}}

## Configuration
max_pool_size, idle_timeout, max_lifetime, health_check_interval, queue_timeout

## Dependencies
database-query, http-client, health-prober

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
