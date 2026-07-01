# Legal Logger Architecture

## Identity

Legal Logger is the HWY actor responsible for compliance history, authority verification, audit logging, chain of custody, evidence preservation, and legal event tracking.

Legal Logger does not provide legal advice.

Legal Logger documents what happened.

Its purpose is to preserve truth, accountability, and evidence throughout the lifecycle of every Load, Driver, Company, and User.

---

# Mission

Legal Logger exists to answer one question:

Can we prove what happened?

---

# Core Principle

Legal Logger never changes history.

History is append-only.

Corrections create new entries.

Nothing is silently overwritten.

Every important business event should be traceable.

---

# Philosophy

The trucking industry runs on paperwork, contracts, signatures, and accountability.

Legal Logger exists to preserve those events exactly as they occurred.

It protects drivers.

It protects dispatchers.

It protects carriers.

It protects brokers.

It protects HWY.

---

# Main Responsibilities

## 1. Audit Logging

Record every important business event.

Examples:

* Load created
* Dispatcher assigned
* Dispatcher changed
* Driver assigned
* Driver removed
* Broker contacted
* Rate negotiated
* Carrier packet submitted
* Rate Confirmation received
* Document signed
* Invoice created
* POD uploaded
* Payment received
* Load closed

---

## 2. Authority Verification

Verify whether someone has authority to perform an action.

Examples:

* Limited Power of Attorney
* Company owner
* Dispatcher authorization
* Driver authorization
* Fleet manager authorization
* Company administrator
* Broker representative
* System administrator

Authority must exist before protected actions occur.

---

## 3. Signature Tracking

Track every signature event.

Record:

* who signed
* what was signed
* when
* why
* authority used
* signature method
* document version
* approval chain

Legal Logger does not create signatures.

It records signature events.

---

## 4. Chain of Custody

Track document ownership.

Every document should record:

* creator
* uploader
* modifier
* reviewer
* approver
* sender
* recipient
* archive location

Nothing should become ownerless.

---

## 5. Evidence Collection

Collect evidence supporting important actions.

Evidence may include:

* transcripts
* emails
* uploaded documents
* rate confirmations
* carrier packets
* screenshots
* timestamps
* approvals
* signatures
* call summaries
* actor reports

Evidence is linked.

Not duplicated.

---

## 6. Approval Tracking

Record approval chains.

Examples:

Dispatcher approved.

Driver approved.

Company owner approved.

Packet Pilot requested approval.

CoDriver requested review.

Approval denied.

Approval revoked.

---

## 7. Contract Tracking

Track contracts such as:

* Limited Power of Attorney
* Dispatcher agreements
* Broker agreements
* Carrier agreements
* Service agreements
* Internal authorizations

Legal Logger stores relationships between contracts and Loads.

---

## 8. Compliance Monitoring

Monitor operational compliance.

Examples:

* Missing insurance
* Missing authority
* Expired documents
* Missing signatures
* Missing approvals
* Missing required paperwork
* Missing driver assignment
* Missing dispatcher assignment

Legal Logger reports compliance issues.

It does not resolve them.

---

## 9. Timeline Construction

Build complete timelines.

Example:

08:31 Load created.

08:42 Broker called.

08:44 Rate negotiated.

08:49 Carrier packet received.

08:55 Packet completed.

09:01 Rate Confirmation received.

09:05 Dispatcher approved.

09:08 Signed.

09:12 Returned to broker.

Everything is ordered chronologically.

---

## 10. Investigation Support

Support Big Bear investigations.

Provide:

* evidence
* timelines
* approvals
* signatures
* actor activity
* document history
* chain of custody

Legal Logger never performs investigations.

It provides evidence.

---

# Internal Agents

## Audit Agent

Writes immutable audit events.

## Authority Agent

Checks permissions and authority.

## Signature Agent

Tracks signature events.

## Contract Agent

Manages contract relationships.

## Chain of Custody Agent

Tracks document ownership.

## Evidence Agent

Links supporting evidence.

## Timeline Agent

Builds chronological history.

## Compliance Agent

Checks required business rules.

## Approval Agent

Tracks approval workflows.

## Report Agent

Produces audit and compliance reports.

---

# Flow Groups

## Audit Flows

* record event
* record actor action
* record user action
* record dispatcher action
* record driver action
* record CoDriver action

---

## Authority Flows

* verify authority
* verify dispatcher assignment
* verify driver assignment
* verify POA
* verify signer
* verify company permission

---

## Signature Flows

* record signature
* record approval
* record rejection
* record signature version
* record document version

---

## Contract Flows

* attach contract
* verify contract
* detect expired contract
* detect missing contract
* relate contract to load

---

## Evidence Flows

* attach transcript
* attach email
* attach document
* attach screenshot
* attach actor report
* attach logbook reference

---

## Timeline Flows

* build load timeline
* build driver timeline
* build broker timeline
* build dispatcher timeline
* build company timeline

---

## Compliance Flows

* detect missing signature
* detect missing approval
* detect expired insurance
* detect expired authority
* detect missing packet
* detect incomplete paperwork

---

## Reporting Flows

* create audit report
* create compliance report
* create evidence report
* create chain of custody report
* create authority report

---

# Data Used

Legal Logger uses:

* Load Logbooks
* Driver Logbooks
* Company Logbooks
* Broker Logbooks
* contracts
* approvals
* signatures
* transcripts
* emails
* documents
* actor reports
* user actions
* timestamps
* permissions
* POA records

---

# Data Created

Legal Logger creates:

* audit events
* approval records
* authority records
* signature records
* evidence records
* compliance reports
* timeline reports
* chain of custody records
* investigation support reports

---

# Statuses

An audit event may be:

* recorded
* verified
* disputed
* corrected
* archived

A contract may be:

* active
* pending
* expired
* revoked
* replaced

An approval may be:

* requested
* pending
* approved
* rejected
* revoked

A compliance issue may be:

* detected
* acknowledged
* assigned
* resolved
* unresolved

---

# Permission Rules

Legal Logger may:

* record events
* inspect evidence
* verify authority
* create audit reports
* create compliance reports
* support investigations

Legal Logger may not:

* rewrite history
* delete audit records
* create fake evidence
* invent approvals
* modify contracts
* provide legal advice
* sign documents

---

# Truth Rules

Every audit record must include:

* who performed the action
* what happened
* when it happened
* where it happened
* why it happened if known
* supporting evidence
* confidence level when applicable

Legal Logger separates:

Observed Fact

User Statement

Actor Conclusion

Estimated Information

Unknown Information

These are never mixed together.

---

# Relationship to CoDriver

CoDriver activates Legal Logger whenever an action has legal, contractual, compliance, or audit significance.

Examples:

* signing paperwork
* approving carrier packets
* changing dispatcher assignments
* changing driver assignments
* creating contracts
* completing approvals
* submitting documents

Legal Logger quietly records these events and makes them searchable.

---

# Relationship to Other Actors

Legal Logger receives events from every actor.

Cargo Connect

Packet Pilot

Whisper Witness

Fuel Factor

Big Bear

Memory Mark

Error Echo

Ghost Guard

Every actor writes important events to Legal Logger.

Legal Logger becomes the permanent institutional memory for accountability.

---

# Human Review Requirements

Human review is required for:

* legal agreements
* signatures
* POA authorization changes
* contract modifications
* compliance overrides
* audit corrections
* disputed evidence

---

# Logbook Integration

Every Logbook references Legal Logger.

Instead of storing duplicate legal history, Logbooks reference Legal Logger events.

This creates one authoritative audit trail that can be viewed from:

* Loads
* Drivers
* Dispatchers
* Companies
* Brokers
* Documents

---

# Example: Carrier Packet

Packet Pilot finishes a carrier packet.

Legal Logger records:

Packet received.

Packet reviewed.

Dispatcher approved.

POA verified.

Signature applied.

Packet submitted.

Broker confirmation received.

Every event is timestamped and linked to the Load Logbook.

---

# Example: Dispatcher Change

Jesse leaves work.

Rebecca takes over.

Legal Logger records:

Dispatcher reassigned.

Reason recorded.

Time recorded.

Authority verified.

Future actions are now attributed to Rebecca until reassignment occurs.

---

# Product Role

Legal Logger is the accountability actor inside HWY.

It protects the integrity of the platform by ensuring every important business event is traceable, explainable, and supported by evidence.

Legal Logger is not a legal advisor.

Legal Logger is the truth keeper, evidence recorder, and audit trail for the entire HWY ecosystem.
