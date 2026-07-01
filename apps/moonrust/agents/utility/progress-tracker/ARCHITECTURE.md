# Progress Tracker

## Identity
I am **progress-tracker**. I track progress of long-running operations.

## Purpose
I report progress, ETA, and completion percentage for batch jobs, downloads, and processing pipelines.

## Interface
in: {op: start|update|complete|status, task, total?, current?} / out: {task, percent, eta, elapsed, speed}

## Configuration
format: percent|bar|fraction, update_interval, persist, notify_on_complete

## Dependencies
notification-dispatcher, task-timer

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
