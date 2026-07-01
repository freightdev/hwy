# HWY Architecture

## Name

HWY stands for:

**Highway Workflow Yarddog**

HWY is built from trucking culture.

A yarddog keeps the yard moving by moving trailers where they need to go.

HWY does the same thing with trucking work.

It moves information, documents, loads, calls, actors, flows, and decisions to the right place at the right time.

---

# Identity

HWY is an AI-first trucking operations platform.

HWY is not only a TMS.

HWY is not only a dispatch app.

HWY is not only an AI assistant.

HWY is an actor-based operating platform for drivers, dispatchers, owner-operators, and small trucking businesses.

The platform is built around CoDriver, Actors, Agents, Flows, Logbooks, Marks, and trusted execution.

---

# Mission

HWY exists to help trucking people operate with more intelligence, more protection, more organization, and less wasted time.

The mission is simple:

**Give every driver and dispatcher an AI-powered operations team they can actually afford.**

---

# Core Philosophy

HWY is built on a few permanent ideas.

The Load is the center.

Every Load has a Logbook.

CoDriver is the console.

Actors own responsibilities.

Agents perform focused work.

Flows execute repeatable actions.

Logbooks preserve truth.

Humans make business decisions.

AI assists, researches, organizes, verifies, and executes approved work.

---

# The Load-First Principle

The Load is the primary business object in HWY.

Every meaningful business event should either:

Create a Load.

Attach to an existing Load.

Or explain why it does not belong to a Load.

A Load may include:

broker

carrier

driver

dispatcher

truck

trailer

rate

lane

commodity

emails

calls

documents

carrier packet

rate confirmation

POD

invoice

payments

AI activity

human decisions

legal history

Every Load becomes its own workspace.

---

# Every Load Has a Logbook

The Load Logbook is the permanent history of the Load.

It is append-only.

History is not silently rewritten.

Corrections create new entries.

A Load Logbook may contain:

load creation

broker communication

phone calls

transcripts

driver messages

dispatcher changes

rate negotiation

carrier packet status

rate confirmation status

documents

signatures

POD

invoice

payment status

AI actions

alerts

errors

approvals

audit records

Every actor writes meaningful work back to the correct Logbook.

Agents do not own truth.

Actors do not own truth.

The Logbook owns truth.

---

# CoDriver

CoDriver is the main console of HWY.

CoDriver is the AI teammate that drivers and dispatchers talk to.

In trucking, a co-driver is the other driver in a team truck.

HWY gives every user an AI CoDriver, even if they have always worked solo.

CoDriver does not do every job directly.

CoDriver understands the user, decides what needs to happen, and activates the right actor.

CoDriver is the command layer.

---

# Direct Dispatch

Direct Dispatch is CoDriver's most-used actor.

CoDriver decides what needs to happen.

Direct Dispatch decides who should do the work and in what order.

Direct Dispatch routes work to actors, manages dependencies, monitors queues, and keeps the operation moving.

If CoDriver is the brain, Direct Dispatch is the spinal cord.

---

# Actor Model

HWY is built around Actors.

An Actor is not just an AI agent.

An Actor is a named operational role with a responsibility.

Each Actor may have:

identity

mission

rules

agents

flows

permissions

logbooks

memory

models

tools

outputs

review requirements

Actors own domains.

Agents perform tasks inside those domains.

Flows execute reusable actions.

Workers and tools perform low-level work.

The hierarchy is:

User

CoDriver

Direct Dispatch

Actor

Agent

Flow

Worker

Tool or Model

---

# The ABC Actors of HWY

HWY uses 26 core actors.

## A — Auto Assist

Shared automation actor.

Helps other actors with repetitive operational work, queues, cleanup, scheduling, retries, and reusable automation.

Auto Assist does not become another actor.

It assists.

## B — Big Bear

Root-cause investigation actor.

When an actor keeps messing up, Big Bear investigates memory, prompts, flows, routing, and behavior to determine why.

Big Bear does not recover production.

Big Bear investigates after the mess.

## C — Cargo Connect

Freight discovery actor.

Finds loads, searches freight sources, tracks load leads, discovers brokers and shippers, ranks opportunities, and writes freight intelligence to Load Logbooks.

## D — Direct Dispatch

Actor orchestration actor.

Routes work to the right actor, in the right order, with the right permissions.

This is the actor CoDriver uses the most.

## E — Error Echo

Error recovery actor.

When something breaks, Error Echo handles the failure, escalates to powerful models when needed, keeps operations moving, and sends the incident package to Big Bear later.

## F — Fuel Factor

Fuel savings actor.

Helps drivers fight fuel costs with fuel planning, price comparison, route fuel strategy, fuel history, MPG tracking, and savings reports.

Fuel Factor is a free actor.

## G — Ghost Guard

Actor integrity and monitoring actor.

Watches actors and temporary agents to make sure they follow policy, do not leave traces, do not tamper with data, and do not behave maliciously.

Ghost Guard is free forever.

## H — Highway Helper

Free trucking help actor.

Answers trucking questions, teaches drivers and dispatchers, helps with FMCSA/DOT research, finds roadside help, and explains industry knowledge.

Highway Helper is the public free helper of HWY.

## I — Iron Insight

Equipment intelligence actor.

Tracks trucks, trailers, PMs, inspections, insurance, repairs, parts, GPS location, and Equipment Logbooks.

Iron Insight helps drivers know their iron.

## J — Jackknife Jailer

Reinforcement actor.

Jack helps overloaded actors by temporarily operating with that actor's agents, rules, and scoped permissions.

Jack does not assist like Auto Assist.

Jack temporarily becomes extra capacity.

## K — Key Keeper

Authorization actor.

Knows who can talk to whom, what keys everyone has, what actors can access, and what actions are allowed.

Secret Safe checks Key Keeper before protected access.

## L — Legal Logger

Audit and evidence actor.

Records who did what, when, under what authority, and with what proof.

Legal Logger is not a lawyer.

Legal Logger preserves truth and chain of custody.

## M — Memory Mark

Memory support and memory safety actor.

It can hold temporary thoughts.

It also validates memory and protects CoDriver from prompt injection when reading untrusted emails, PDFs, websites, OCR, or documents.

## N — Night Nexus

Night dispatcher actor.

Runs the overnight shift, usually 8 PM to 4 AM, using cached data and instructions left by other actors.

Night Nexus monitors loads while the daytime operation sleeps.

## O — Oversize Overseer

Oversize and overweight compliance actor.

Once Oversize Overseer touches a Load, that domain is non-negotiable.

It tracks dimensions, permits, route concerns, escorts, equipment, and oversize safety.

## P — Packet Pilot

Paperwork actor.

Handles carrier packets, rate confirmations, OCR, forms, placeholders, signatures, online forms, missing fields, review, and submission.

Packet Pilot does not sign or submit without proper authority.

## Q — Quick Quote

Advanced intelligence actor.

When CoDriver or another actor does not know something, Quick Quote finds the best available intelligence source, including stronger AI models, official sources, or expert systems.

Quick Quote is loyal to truth, not one model.

## R — Radar Ranch

Paid intelligence collection actor.

Collects rates, lanes, weather, traffic, fuel signals, market signals, and operational intelligence over time like cattle in a ranch.

Radar Ranch is paid because it requires integrations and long-term monitoring.

## S — Secret Safe

Zero-trust secret protection actor.

Protects credentials, secrets, protected documents, identity proof, tokens, and sensitive access.

Not even the owner gets access until identity and authority are proven.

## T — Trucker Tales

Story preservation actor.

Listens to drivers' stories, preserves road wisdom, captures lived experience, and helps future AI learn from real trucking lives.

Every mile has a story.

## U — Unit Usage

Personal privacy bodyguard actor.

Controls disclosure of personal information.

It asks whether someone actually needs the information and releases only the minimum necessary.

## V — Voice Validator

Voice authenticity actor.

Checks whether a speaking actor or user is really who they claim to be.

Protects against fake voices, spoofed actor speech, cloned audio, and compromised devices.

## W — Whisper Witness

Live call and conversation witness actor.

Listens to calls when authorized, transcribes, extracts load information, creates private whispers, tracks negotiation, and writes call history to Logbooks.

## X — Xeno Xeno

Unknown and foreign interpretation actor.

Handles foreign languages, strange documents, unknown requests, unfamiliar terminology, and information CoDriver or another actor does not understand.

## Y — Yes Yes

Delegated approval actor.

When CoDriver has already approved a workflow, Yes Yes answers repeated confirmation prompts so actors can keep working without bothering CoDriver over and over.

## Z — Zone Zipper

Workspace index actor.

Zips through the whole workspace, indexes what is happening, manages today's board, tracks zones, and gives CoDriver real-time operational visibility.

---

# Actor Departments

The ABC actors can be understood as departments.

## Command Layer

CoDriver

Direct Dispatch

Yes Yes

These control decisions, routing, and delegated continuation.

## Trucking Operations Layer

Cargo Connect

Packet Pilot

Whisper Witness

Fuel Factor

Highway Helper

Iron Insight

Oversize Overseer

Night Nexus

These perform trucking work.

## Intelligence Layer

Quick Quote

Radar Ranch

Xeno Xeno

Trucker Tales

These research, collect, translate, interpret, and preserve knowledge.

## Security Layer

Secret Safe

Key Keeper

Ghost Guard

Voice Validator

Unit Usage

Memory Mark

These protect identity, memory, data, permissions, actors, and trust.

## Reliability Layer

Error Echo

Big Bear

Jackknife Jailer

Auto Assist

These keep the system stable, recover from failure, investigate mistakes, and provide extra help.

## Compliance and Evidence Layer

Legal Logger

Whisper Witness

Ghost Guard

These preserve proof, records, transcripts, and accountability.

---

# Flows

A Flow is a callable capability.

Flows are the functions of HWY.

A workflow is only a larger flow made of smaller flows.

Examples of flows:

read email

read PDF

run OCR

extract fields

verify document

check broker

estimate rate

transcribe call

write logbook entry

request approval

sign document

submit packet

find fuel

monitor weather

query lane history

validate memory

check permission

A Flow receives context and returns context.

Every Flow should define:

purpose

required inputs

outputs

allowed actors

allowed tools

permissions

risk level

logbook behavior

human review requirements

failure behavior

---

# Marks and Markers

HWY may use `.mrk` and `.mrkr` files during development and future runtime design.

A Mark describes work, knowledge, or intent.

A Marker routes and executes Marks through the right path.

A Mark is like the passenger with a destination.

A Marker is like the bus driver that moves the Mark.

The same Mark can be routed by different Markers for different outcomes.

One Marker may return Markdown.

Another may return JSON.

Another may translate.

Another may add verification.

Marks are reusable.

Markers define execution style.

---

# Spots

Spots are destination services or capability zones.

The platform may later use `.spot` domains.

Examples:

aflow.spot

keepa.spot

marka.spot

infra.spot

viewa.spot

dropa.spot

jesta.spot

The local Python system should be built first.

Spots are a deployment and network evolution, not a requirement for the first working system.

The architecture should work locally before becoming distributed.

---

# Data Ownership

Agents do not own data.

Actors do not own final truth.

Logbooks own truth.

The system should contain multiple Logbook types:

Load Logbook

Driver Logbook

Company Logbook

Broker Logbook

Equipment Logbook

Fuel Logbook

Privacy Logbook

Key Logbook

Legal Logbook

Error Logbook

Actor Logbook

Shift Logbook

Automation Logbook

Every meaningful action is written somewhere.

Nothing important disappears.

---

# Trust Model

HWY is zero-trust by design.

Important rules:

No actor is trusted automatically.

No user is trusted automatically.

No device is trusted automatically.

No external content is trusted automatically.

No memory is trusted automatically.

No voice is trusted automatically.

No permission is permanent unless policy says so.

Important security actors:

Key Keeper checks authority.

Secret Safe protects secrets.

Unit Usage controls disclosure.

Memory Mark validates untrusted content.

Ghost Guard watches actor behavior.

Voice Validator checks authenticity.

Legal Logger records proof.

Big Bear investigates failures.

---

# Truth Model

HWY should never lie.

Every important answer should identify the kind of truth being used.

Truth labels may include:

official source

source-backed

profile-backed

logbook-backed

user-provided

speaker-claimed

transcribed

calculated

estimated

inferred

uncertain

unknown

A broker claiming something is not the same as verified truth.

An AI estimating something is not the same as official data.

A document extraction is not the same as human approval.

The system must preserve these differences.

---

# Human Authority

HWY assists humans.

HWY does not replace human judgment.

Humans remain responsible for:

accepting rates

booking freight

signing contracts

approving submissions

changing legal authority

releasing sensitive data

making business decisions

CoDriver and the actors may recommend, prepare, research, organize, and execute approved work.

They do not silently decide high-risk business actions.

---

# Driver Product

HWY Driver is the driver-facing product.

The core idea:

**Every driver deserves a CoDriver.**

A solo driver may not have a team driver.

A solo driver may not afford a dispatcher taking 15–30 percent.

HWY gives the driver an AI teammate.

Driver-side features include:

CoDriver

Load Logbooks

Highway Helper

Iron Insight

Fuel Factor

Packet Pilot

Whisper Witness

Cargo Connect

Trucker Tales

Equipment Logbooks

roadside help

document help

call support

rate awareness

The driver stays in control.

---

# Dispatcher and TMS Product

HWY TMS is the dispatcher and company-facing product.

It is a mini TMS powered by actors.

It focuses on:

drivers

loads

dispatchers

connections

paperwork

load logbooks

broker communication

carrier packets

rate confirmations

team handoffs

contracts

authority

audit

AI-assisted operations

It is not trying to be every giant TMS at once.

It is an AI operations desk for dispatchers and small trucking companies.

---

# Website Product

HWY Trucking is the ecosystem front door.

It explains:

HWY

CoDriver

HWY Driver

HWY TMS

actors

pricing

support

training

resources

blog

mission

It introduces people to the platform.

---

# App Navigation

The driver and dispatcher apps should share a simple navigation pattern.

Me

Connect

AI

Loads

More

## Me

Personal dashboard.

Current responsibilities.

Today’s work.

Profile.

Status.

## Connect

Connections with drivers, dispatchers, companies, brokers, and teams.

## AI

Direct access to CoDriver.

Voice, chat, and actor activation.

## Loads

All loads, load leads, active loads, completed loads, and Load Logbooks.

## More

Settings, actors, documents, equipment, training, billing, support, and advanced tools.

---

# Load Lifecycle

A Load may move through stages such as:

lead discovered

lead enriched

driver matched

broker contacted

negotiating

rate agreed

carrier packet requested

carrier packet submitted

rate confirmation received

rate confirmation verified

signed

dispatched

pickup

in transit

delivered

POD uploaded

invoiced

paid

closed

Every stage writes to the Load Logbook.

---

# Example End-to-End Operation

A broker calls.

Whisper Witness listens and transcribes.

Cargo Connect identifies broker and lane.

Radar Ranch checks lane history and weather.

Fuel Factor estimates fuel impact.

Quick Quote answers anything CoDriver does not know.

CoDriver whispers private intelligence to the dispatcher.

Legal Logger records meaningful authority and negotiation events.

The call ends.

Whisper Witness writes the summary.

Packet Pilot waits for carrier packet or rate confirmation.

When email arrives, Packet Pilot reads it.

Memory Mark sanitizes it.

Key Keeper checks authority.

Secret Safe protects sensitive data.

Unit Usage controls disclosure.

Packet Pilot fills documents.

Human approves.

Legal Logger records approval and signature.

The Load Logbook preserves everything.

---

# Failure Handling

When something breaks:

Error Echo responds first.

It captures the error, attempts recovery, escalates to stronger models if needed, and keeps operations moving.

Ghost Guard watches for suspicious actor behavior.

Legal Logger records what happened.

After operations stabilize, Big Bear investigates root cause.

Big Bear recommends prompt, memory, flow, routing, or actor changes.

Nothing is hidden.

Nothing is silently forgotten.

---

# Free Actors

HWY should have useful free actors forever.

Core free actors include:

Highway Helper

Iron Insight

Fuel Factor

Ghost Guard

These build trust, help drivers, and prove the mission before users pay.

---

# Paid Actors

Paid actors require heavier cost, integrations, monitoring, or business value.

Examples:

Radar Ranch

Cargo Connect advanced monitoring

Packet Pilot automation

Whisper Witness live call intelligence

Night Nexus

Premium Quick Quote

Paid actors should provide clear operational value.

---

# Development Strategy

Build local first.

Python first.

No fake hardcoded intelligence.

No fake rate answers.

No pretending to know.

The first system should include:

CoDriver console

Direct Dispatch

actor registry

flow registry

worker registry

local memory

logbooks

Packet Pilot basics

Cargo Connect basics

Whisper Witness basics

Legal Logger basics

Memory Mark basics

Error Echo basics

The system should prove the architecture locally before moving into `.spot` services.

---

# Non-Negotiable Rules

Every Load has a Logbook.

Actors own domains.

Agents perform focused tasks.

Flows execute reusable actions.

Logbooks preserve truth.

Secret Safe protects secrets.

Key Keeper controls authority.

Memory Mark validates untrusted content.

Legal Logger records proof.

Error Echo handles the mess.

Big Bear investigates after.

Ghost Guard watches everyone.

Humans decide high-risk business actions.

CoDriver never lies.

If HWY does not know, it says it does not know.

---

# Final Vision

HWY is an AI-powered operating platform for trucking.

It gives drivers and dispatchers a workforce of specialized actors that can help find freight, handle paperwork, listen to calls, protect data, track equipment, save fuel, preserve stories, monitor operations, and keep every Load organized inside a permanent Logbook.

HWY is not built to replace trucking people.

HWY is built to give trucking people leverage.

Every driver deserves a CoDriver.

Every Load deserves a Logbook.

Every operation deserves truth.

That is HWY.
