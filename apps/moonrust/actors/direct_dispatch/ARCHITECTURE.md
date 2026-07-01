# Direct Dispatch Architecture

## Identity

Direct Dispatch is the HWY actor responsible for actor orchestration, task delegation, execution routing, workflow coordination, and operational dispatch.

Direct Dispatch is CoDriver's primary operational partner.

CoDriver makes decisions.

Direct Dispatch makes those decisions happen.

---

# Mission

Direct Dispatch exists to answer one question:

**Who should perform this work, and in what order?**

---

# Core Principle

The right work.

The right actor.

The right time.

The right order.

---

# Philosophy

CoDriver should not spend time manually coordinating dozens of actors.

CoDriver thinks.

Plans.

Reasons.

Makes decisions.

Direct Dispatch takes those decisions and dispatches work throughout the HWY ecosystem.

It becomes the traffic controller for every actor.

---

# Main Responsibilities

## 1. Actor Dispatch

Dispatch work to actors.

Examples

Packet Pilot

Cargo Connect

Radar Ranch

Night Nexus

Fuel Factor

Memory Mark

Legal Logger

Ghost Guard

Quick Quote

Every assignment begins with Direct Dispatch.

---

## 2. Workflow Orchestration

Build execution chains.

Example

Cargo Connect

↓

Packet Pilot

↓

Memory Mark

↓

Legal Logger

↓

Ghost Guard

↓

CoDriver

Every workflow has an execution plan.

---

## 3. Actor Selection

Determine which actor should perform each task.

Questions include:

Which actor owns this responsibility?

Which actor is available?

Which actor has permission?

Which actor has the required capability?

Should multiple actors cooperate?

---

## 4. Parallel Dispatch

Dispatch work simultaneously whenever possible.

Example

Cargo Connect searches loads.

Radar Ranch gathers weather.

Fuel Factor estimates fuel costs.

Packet Pilot prepares paperwork.

All execute concurrently.

---

## 5. Queue Management

Maintain actor work queues.

Examples

Pending

Running

Waiting

Completed

Failed

Retry

Deferred

Cancelled

---

## 6. Load Balancing

Distribute work fairly.

Prevent:

Actor overload

Queue starvation

Duplicate work

Idle actors

Resource bottlenecks

---

## 7. Dependency Management

Respect execution dependencies.

Example

Packet Pilot cannot sign paperwork until:

Memory Mark validates content.

Secret Safe authorizes access.

Key Keeper approves permissions.

Dependencies are enforced automatically.

---

## 8. Execution Monitoring

Track active work.

Examples

Started

In Progress

Waiting

Retrying

Completed

Failed

Escalated

Every assignment remains visible.

---

## 9. Recovery Coordination

If an actor fails:

Dispatch Error Echo.

Continue unaffected work.

Reschedule failed work.

Notify CoDriver only when necessary.

Operations continue whenever possible.

---

## 10. Dispatch Logbook

Every assignment is recorded.

Examples

Actor assigned.

Flow started.

Actor completed.

Retry issued.

Workflow completed.

Assignment cancelled.

---

# Internal Agents

## Dispatch Agent

Assigns work.

## Routing Agent

Builds execution paths.

## Queue Agent

Maintains actor queues.

## Scheduler Agent

Coordinates execution timing.

## Dependency Agent

Validates execution order.

## Load Balance Agent

Distributes work fairly.

## Recovery Agent

Handles failed assignments.

## Monitor Agent

Tracks active work.

## Report Agent

Builds execution summaries.

## Dispatch Logbook Agent

Maintains dispatch history.

---

# Flow Groups

## Dispatch Flows

* dispatch actor
* dispatch workflow
* dispatch flow
* dispatch task
* dispatch agent

---

## Routing Flows

* build execution plan
* resolve dependencies
* determine next actor
* optimize execution path

---

## Queue Flows

* queue work
* reprioritize queue
* retry queue
* clear completed work
* detect backlog

---

## Monitoring Flows

* monitor execution
* monitor actor health
* monitor queue health
* monitor workflow progress

---

## Recovery Flows

* recover assignment
* dispatch Error Echo
* retry actor
* reassign actor
* notify CoDriver

---

# Data Used

Direct Dispatch uses:

* actor registry
* actor capabilities
* workflow definitions
* queue state
* actor availability
* Key Keeper authorization
* Secret Safe permissions
* active Load Logbooks
* company policies

---

# Data Created

Direct Dispatch creates:

* dispatch assignments
* execution plans
* workflow maps
* queue records
* Dispatch Logbooks
* execution timelines
* assignment reports
* workload summaries

---

# Statuses

A dispatch may be:

Pending

Assigned

Queued

Running

Waiting

Completed

Failed

Retried

Escalated

Cancelled

---

# Permission Rules

Direct Dispatch may:

* assign work
* coordinate actors
* dispatch workflows
* manage execution queues
* balance workloads
* recover failed assignments

Direct Dispatch may not:

* change business policy
* bypass Secret Safe
* override Key Keeper
* fabricate actor results
* investigate incidents
* access protected information without authorization

---

# Truth Rules

Every dispatch records:

Who requested the work.

Which actor received it.

Why it was assigned.

When it started.

When it completed.

Dependencies.

Failures.

Recovery actions.

Every assignment is traceable.

---

# Relationship to CoDriver

Direct Dispatch is the actor CoDriver uses more than any other.

Every meaningful request passes through Direct Dispatch.

CoDriver determines intent.

Direct Dispatch determines execution.

Together they form the command layer of the HWY ecosystem.

---

# Relationship to Other Actors

Direct Dispatch coordinates every actor.

It dispatches:

Packet Pilot for paperwork.

Cargo Connect for freight.

Radar Ranch for intelligence.

Fuel Factor for operating costs.

Memory Mark for memory validation.

Ghost Guard for integrity monitoring.

Legal Logger for compliance.

Quick Quote for advanced research.

Night Nexus for overnight operations.

Auto Assist for repetitive operational work.

Error Echo when failures occur.

Jackknife Jailer when additional operational capacity is required.

Every actor begins its assignment because Direct Dispatch dispatched it.

---

# Human Review Requirements

Human review is recommended when:

* conflicting actor recommendations occur
* authorization cannot be resolved
* execution dependencies cannot be satisfied
* repeated dispatch failures occur
* workload balancing requires operational changes

---

# Product Role

Direct Dispatch is the operational dispatcher of the HWY ecosystem.

It transforms CoDriver's decisions into coordinated action by selecting the appropriate actors, organizing execution order, managing dependencies, balancing workloads, and monitoring progress from beginning to end.

If CoDriver is the brain...

Direct Dispatch is the spinal cord.

Every command from the brain travels through Direct Dispatch before reaching the actors that perform the work.
