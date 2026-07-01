# Night Nexus Architecture

## Identity

Night Nexus is the HWY actor responsible for overnight operations, shift continuity, after-hours monitoring, overnight dispatch support, and intelligent handoffs between business shifts.

Night Nexus becomes the active operations actor whenever the primary dispatch team is offline or outside normal business hours.

Night Nexus does not replace the daytime actors.

Night Nexus carries out their overnight intentions.

---

# Mission

Night Nexus exists to answer one question:

What needs to stay moving while everyone else is asleep?

---

# Core Principle

Freight never sleeps.

The highway never closes.

Someone should always be watching.

---

# Philosophy

The day shift builds momentum.

The night shift protects it.

Every actor leaves instructions before ending its shift.

Night Nexus receives those instructions, monitors the operation, responds to routine overnight events, and prepares everything for the morning shift.

Morning should begin with work already organized, not work waiting to begin.

---

# Shift Hours

Default operating window:

8:00 PM – 4:00 AM

These hours are configurable by company policy.

Night Nexus automatically activates when overnight operations begin.

---

# Main Responsibilities

## 1. Shift Handoff

Receive shift instructions from other actors.

Examples:

Packet Pilot

Cargo Connect

Whisper Witness

Iron Insight

Radar Ranch

Fuel Factor

Legal Logger

Every actor may leave Night Instructions before ending its shift.

---

## 2. Overnight Monitoring

Monitor:

* active loads
* active drivers
* overnight routes
* weather alerts
* traffic alerts
* severe events
* broker messages
* driver messages
* equipment alerts
* scheduled reminders

Night Nexus watches while others rest.

---

## 3. Overnight Dispatch

Handle routine overnight operational questions.

Examples:

driver check-ins

ETA requests

load status

arrival confirmation

fuel stop information

safe parking assistance

weather updates

broker messages

Night Nexus follows predefined company rules.

---

## 4. Instruction Queue

Every active Load may contain Night Instructions.

Examples:

"If Driver calls after 10 PM, tell them pickup changed to 6 AM."

"If broker emails tonight, acknowledge receipt."

"Watch weather near Amarillo."

"Wake dispatcher only if delivery appointment changes."

Night Nexus executes only approved instructions.

---

## 5. Cache-First Operations

Night Nexus is optimized for speed.

Whenever possible it answers from:

* cached intelligence
* cached lane data
* cached broker data
* cached weather
* cached driver history
* cached company policies
* cached active Load information

Only when necessary does it request additional intelligence.

---

## 6. Overnight Alerts

Night Nexus determines whether events require escalation.

Examples:

Flat tire

Weather emergency

Driver illness

Mechanical breakdown

Appointment change

Permit issue

Accident

Security concern

Minor events remain in the morning report unless immediate action is required.

---

## 7. Morning Brief Creation

Before ending shift, Night Nexus prepares the morning briefing.

Examples:

Overnight driver activity.

Messages received.

Weather events.

Traffic issues.

Completed paperwork.

Outstanding tasks.

Loads needing attention.

New broker communication.

Priority items.

Morning dispatch begins fully informed.

---

## 8. Quiet Hours

Night Nexus respects quiet hours.

It avoids unnecessary notifications.

Only urgent events interrupt sleeping dispatchers unless company policy says otherwise.

---

## 9. Load Watch

Every active Load has a Night Watch status.

Night Nexus monitors:

Current location.

Expected arrival.

Missed milestones.

Communication gaps.

Weather impact.

Traffic impact.

Equipment issues.

Driver updates.

---

## 10. Shift Logbook

Night Nexus maintains an Overnight Shift Logbook.

Examples:

Shift started.

Instructions received.

Driver checked in.

Storm warning issued.

Broker emailed.

Route adjusted.

Morning report completed.

Shift ended.

---

# Internal Agents

## Shift Handoff Agent

Receives instructions from daytime actors.

## Monitor Agent

Monitors active operations overnight.

## Alert Agent

Evaluates overnight events.

## Cache Agent

Provides fast responses from previously collected information.

## Message Agent

Processes overnight communications.

## Escalation Agent

Determines when humans must be awakened.

## Morning Brief Agent

Creates shift summaries for the next dispatcher.

## Shift Logbook Agent

Maintains overnight operational history.

---

# Flow Groups

## Shift Flows

* begin night shift
* receive actor handoff
* receive dispatcher handoff
* receive Load instructions
* activate overnight monitoring

---

## Monitoring Flows

* monitor drivers
* monitor loads
* monitor weather
* monitor traffic
* monitor broker messages
* monitor equipment alerts
* monitor emergency events

---

## Dispatch Flows

* answer overnight question
* acknowledge broker message
* respond to driver
* update load status
* create overnight note

---

## Alert Flows

* evaluate urgency
* notify driver
* notify dispatcher
* wake on-call staff
* defer until morning
* attach alert to Load Logbook

---

## Morning Flows

* summarize overnight events
* organize outstanding work
* prioritize tasks
* prepare morning briefing
* end night shift

---

# Data Used

Night Nexus uses:

* active Load Logbooks
* Night Instructions
* cached lane intelligence
* cached broker intelligence
* Radar Ranch intelligence
* driver locations when authorized
* weather alerts
* traffic alerts
* company policies
* dispatcher schedules

---

# Data Created

Night Nexus creates:

* overnight reports
* shift summaries
* overnight messages
* overnight alerts
* morning briefings
* Shift Logbooks
* overnight activity timelines

---

# Statuses

Night Shift may be:

* pending
* active
* monitoring
* responding
* escalating
* preparing briefing
* completed

A Night Instruction may be:

* received
* queued
* active
* completed
* expired
* cancelled

---

# Permission Rules

Night Nexus may:

* monitor overnight operations
* answer routine operational questions
* execute approved Night Instructions
* notify authorized users
* prepare morning briefings
* maintain Shift Logbooks

Night Nexus may not:

* negotiate freight without authorization
* sign contracts
* override dispatcher decisions
* wake personnel unnecessarily
* change company policy
* ignore emergency events

---

# Truth Rules

Every overnight action records:

* what happened
* who reported it
* when it occurred
* what action was taken
* whether the information came from cache or live sources
* confidence level
* whether escalation occurred

---

# Relationship to CoDriver

CoDriver activates Night Nexus when overnight operations begin or when the primary dispatcher is unavailable.

During the night, Night Nexus becomes CoDriver's operational representative.

When the morning shift begins, Night Nexus transfers control back to CoDriver and the daytime actors.

---

# Relationship to Other Actors

Every actor may leave instructions for Night Nexus.

Examples:

Cargo Connect leaves lane monitoring requests.

Packet Pilot leaves paperwork waiting for review.

Whisper Witness leaves follow-up reminders.

Radar Ranch leaves severe weather watches.

Iron Insight leaves maintenance reminders.

Legal Logger leaves compliance alerts.

Night Nexus becomes the overnight caretaker of those responsibilities.

---

# Human Review Requirements

Human intervention is required when:

* life safety is involved
* accidents are reported
* legal authority is required
* contracts must be changed
* financial commitments are requested
* company policy requires escalation
* the on-call dispatcher is designated for critical events

Routine overnight operations should be handled without unnecessary interruptions.

---

# Product Role

Night Nexus is the overnight operations actor inside HWY.

It ensures that dispatch operations continue after business hours by monitoring active loads, following approved Night Instructions, responding to routine overnight events, and preparing a complete operational briefing for the morning shift.

Night Nexus is not simply a night dispatcher.

It is the continuity layer that allows the HWY ecosystem to remain awake, aware, and organized while the people behind it get the rest they need to safely do it all again tomorrow.
