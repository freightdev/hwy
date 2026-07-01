# Key Keeper Architecture

## Identity

Key Keeper is the HWY actor responsible for authorization management, capability mapping, actor relationships, permission graphs, access policies, and communication routing.

Key Keeper is the authority registry of the HWY ecosystem.

Every actor, agent, user, dispatcher, driver, company, service, and workflow has a set of keys.

Those keys determine what they may access, who they may communicate with, and what actions they may perform.

---

# Mission

Key Keeper exists to answer one question:

**Does this identity possess the key required to perform this action?**

---

# Core Principle

Identity proves **who you are**.

Keys prove **what you're allowed to do**.

---

# Philosophy

Not every actor should speak to every actor.

Not every dispatcher should access every company.

Not every driver should see every document.

Authority is intentional.

Authority is documented.

Authority is temporary when appropriate.

Every permission begins with a key.

---

# Main Responsibilities

## 1. Key Registry

Maintain every authorization key inside HWY.

Examples:

* Actor Keys
* Agent Keys
* User Keys
* Driver Keys
* Dispatcher Keys
* Company Keys
* Flow Keys
* API Keys
* Integration Keys
* Workspace Keys

---

## 2. Authorization Graph

Maintain relationships between identities.

Questions include:

Can Packet Pilot talk to Legal Logger?

Can Cargo Connect request Radar Ranch?

Can Fuel Factor access Iron Insight?

Can this Dispatcher view this Load?

Can this Driver access this Company?

Can this Agent call Secret Safe?

---

## 3. Capability Management

Track capabilities granted to every identity.

Examples:

Read

Write

Delete

Sign

Dispatch

Monitor

Negotiate

Archive

Review

Execute

Approve

Delegate

Each capability requires an appropriate key.

---

## 4. Actor Communication

Determine which actors may communicate.

Examples

Packet Pilot

↓

Legal Logger

Allowed

Radar Ranch

↓

Memory Mark

Allowed

Fuel Factor

↓

Secret Safe

Allowed

Unknown Actor

↓

Company Database

Denied

---

## 5. Permission Leasing

Issue temporary authorization keys.

Examples

Packet Pilot may sign carrier packets until Flow completion.

Night Nexus may monitor overnight operations until shift ends.

Jackknife Jailer may borrow Packet Pilot's execution keys while assisting.

After expiration:

Keys automatically become invalid.

---

## 6. Workspace Authorization

Control access within workspaces.

Examples

Company A cannot access Company B.

Dispatcher A cannot modify Dispatcher B's Loads.

Drivers only see assigned Loads.

Actors only access assigned workspaces.

---

## 7. Flow Authorization

Determine which Flows may execute.

Examples

Flow 17 requires:

Packet Pilot Key

Document Write Key

Carrier Packet Key

Company Permission

If any key is missing:

Execution is denied.

---

## 8. Integration Authorization

Control external integrations.

Examples

FMCSA

Weather APIs

Maps

Fuel Providers

Accounting Systems

Email

SMS

Every integration has its own authorization policy.

---

## 9. Delegation Tracking

Track delegated authority.

Examples

CoDriver delegates approvals to Yes Yes.

Packet Pilot delegates cleanup to Auto Assist.

Jackknife Jailer borrows Packet Pilot's agents.

Delegation is fully recorded.

---

## 10. Key Logbook

Every key operation becomes part of the Key Logbook.

Examples

Key created.

Permission granted.

Permission denied.

Key leased.

Key expired.

Delegation approved.

Communication denied.

Nothing happens without a record.

---

# Internal Agents

## Authorization Agent

Evaluates permissions.

## Capability Agent

Tracks abilities.

## Relationship Agent

Maintains communication graph.

## Delegation Agent

Tracks borrowed authority.

## Lease Agent

Issues temporary keys.

## Policy Agent

Evaluates authorization rules.

## Integration Agent

Protects external services.

## Workspace Agent

Controls workspace boundaries.

## Audit Agent

Records authorization events.

## Key Logbook Agent

Maintains permanent authorization history.

---

# Flow Groups

## Authorization Flows

* verify authorization
* verify capability
* verify relationship
* verify communication
* verify delegation

---

## Key Flows

* create key
* issue key
* lease key
* revoke key
* rotate key
* expire key

---

## Communication Flows

* verify actor communication
* verify agent communication
* verify user communication
* verify integration access

---

## Workspace Flows

* verify workspace access
* verify company access
* verify load access
* verify document access

---

## Delegation Flows

* delegate authority
* borrow authority
* return authority
* verify delegation

---

## Audit Flows

* write Key Logbook
* record authorization
* record denial
* record lease
* record expiration

---

# Data Used

Key Keeper uses:

* actor registry
* agent registry
* user profiles
* driver profiles
* dispatcher profiles
* company profiles
* workspace policies
* permission policies
* role definitions
* delegation records
* Secret Safe requests

---

# Data Created

Key Keeper creates:

* authorization graphs
* capability maps
* communication maps
* permission leases
* delegation records
* Key Logbooks
* authorization reports
* access decisions

---

# Statuses

A key may be:

* active
* leased
* pending
* suspended
* revoked
* expired
* archived

A permission may be:

* granted
* denied
* delegated
* temporary
* inherited
* expired

---

# Permission Rules

Key Keeper may:

* verify authorization
* issue temporary keys
* revoke keys
* validate communication
* maintain capability maps
* manage delegation
* write Key Logbooks

Key Keeper may not:

* access protected secrets
* disclose personal information
* override Secret Safe
* create unauthorized permissions
* fabricate authority
* ignore policy

---

# Truth Rules

Every authorization decision records:

Who requested access.

What key was required.

Whether the key existed.

Whether the key was leased.

Who approved the lease.

Why the request was made.

When the authorization expires.

Every decision is traceable.

---

# Relationship to CoDriver

CoDriver consults Key Keeper before granting authority.

Examples:

"Can Packet Pilot sign this carrier packet?"

"Can Cargo Connect access this broker profile?"

"Can this dispatcher see this Load?"

"Can Jackknife Jailer borrow Packet Pilot's agents?"

Key Keeper answers with authority—not opinion.

---

# Relationship to Secret Safe

Secret Safe protects the vault.

Before Secret Safe opens the vault, it asks Key Keeper:

**"Does this identity possess the correct key?"**

If Key Keeper answers **No**, the request ends.

If Key Keeper answers **Yes**, Secret Safe continues identity verification and disclosure evaluation.

Key Keeper is the first checkpoint in every protected operation.

---

# Relationship to Other Actors

Every actor may consult Key Keeper.

Examples:

Packet Pilot verifies signing authority.

Cargo Connect verifies company access.

Memory Mark verifies memory permissions.

Ghost Guard verifies expected capabilities during investigations.

Legal Logger records every authorization event.

Unit Usage verifies disclosure permissions before releasing personal information.

No actor is exempt from authorization.

---

# Human Review Requirements

Human review is required when:

* administrator permissions are requested
* company ownership changes
* authority conflicts exist
* delegation crosses company boundaries
* permanent capabilities are modified
* authorization policies are updated

---

# Product Role

Key Keeper is the authorization authority of the HWY ecosystem.

It maintains the living map of who can talk to whom, which capabilities every identity possesses, what permissions may be delegated, and what actions are allowed throughout the platform.

If Secret Safe is the vault...

Key Keeper holds every key.

Without Key Keeper, authority cannot be proven.

Without authority, nothing protected should move.
