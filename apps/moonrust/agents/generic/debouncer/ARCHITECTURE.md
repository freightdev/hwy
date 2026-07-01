# Debouncer

## Identity
I am **debouncer**. A generic agent that debounces and throttles event streams.

## Purpose
I debounce rapid events, throttle high-frequency calls, and coalesce redundant operations. I support leading, trailing, and both-edge debounce with configurable windows.

## Interface
- **in**: `{key: string, event: any, window_ms?: int, mode?: debounce|throttle|coalesce, leading?: bool, trailing?: bool}`
- **out**: `{ok: bool, state: string, timer: string}`

## Configuration
- `default_window`: default debounce window (ms)
- `default_mode`: default operation mode
- `max_keys`: maximum tracked keys
- `gc_interval`: cleanup interval for stale keys

## Dependencies
- `timer` for timer management
- `cache-operator` for debounce state

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
