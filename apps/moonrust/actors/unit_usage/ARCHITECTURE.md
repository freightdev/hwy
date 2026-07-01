# Unit Usage Architecture

## Identity

Unit Usage is the HWY actor responsible for identity protection, privacy mediation, controlled disclosure, permission leasing, and secure access to personal information.

Unit Usage stands between every person and their private information.

No actor, user, company, dispatcher, broker, or third-party integration receives personal information directly.

Every request must pass through Unit Usage.

---

# Mission

Unit Usage exists to answer one question:

**Should this person, actor, or service receive this information?**

---

# Core Principle

Ownership does not equal unrestricted access.

Every request deserves verification.

Every disclosure deserves a purpose.

---

# Philosophy

Drivers trust HWY with some of the most important information they own.

Dispatchers trust HWY with their business.

Companies trust HWY with contracts.

Personal information should never be handed out simply because it exists.

Unit Usage protects people before it protects data.

It acts as the personal bodyguard for every identity inside the HWY ecosystem.

---

# Main Responsibilities

## 1. Identity Protection

Protect:

* Driver Profiles
* Dispatcher Profiles
* Company Profiles
* Owner Operator Profiles
* User Accounts

Every identity receives the same level of protection.

---

## 2. Personal Information Mediation

Protect information such as:

* phone numbers
* email addresses
* home addresses
* CDL numbers
* driver's licenses
* insurance policies
* signatures
* banking information
* tax documents
* emergency contacts
* personal documents

Nothing leaves without review.

---

## 3. Access Verification

Before information is released Unit Usage asks:

Who is requesting it?

Why do they need it?

What Load is involved?

What Flow requested it?

Which Actor requested it?

Is permission currently valid?

Is disclosure necessary?

---

## 4. Minimum Necessary Disclosure

Release only what is required.

Examples

Packet Pilot requests:

Insurance Certificate

Unit Usage releases:

Insurance Certificate

Unit Usage does NOT release:

Driver Address

Phone Number

CDL

Bank Information

Medical Information

Everything unnecessary remains protected.

---

## 5. Permission Leasing

Access is temporary.

Examples

Broker receives access for:

30 minutes

Packet Pilot receives access until packet completion.

Cargo Connect receives access until load search ends.

After expiration:

Access disappears automatically.

---

## 6. Privacy Shield

Unit Usage masks information whenever possible.

Examples

Display:

***-***-4521

instead of

555-555-4521

Display Company Contact instead of Personal Cell.

Display Reference IDs instead of internal identifiers.

---

## 7. Consent Management

Users decide what may be shared.

Examples

Share GPS

Share Insurance

Share Permits

Share Carrier Packet

Share Contact Information

Share Equipment Data

Consent may be:

granted

denied

temporary

revoked

expired

---

## 8. Disclosure Auditing

Every disclosure is recorded.

Information includes:

Who requested it

Why

When

What was shared

How long access lasted

Whether consent existed

Nothing leaves silently.

---

## 9. Exposure Monitoring

Unit Usage watches for unusual behavior.

Examples

Repeated document requests

Repeated identity requests

Unexpected profile access

Mass downloads

Unusual actor behavior

If suspicious activity is detected:

Ghost Guard is notified.

---

## 10. Privacy Logbook

Every protected identity has a Privacy Logbook.

Examples

Insurance released.

Carrier packet shared.

Temporary access granted.

Consent revoked.

Identity verified.

Broker denied.

Nothing is forgotten.

---

# Internal Agents

## Identity Agent

Verifies identities.

## Permission Agent

Validates permission requests.

## Disclosure Agent

Controls information releases.

## Privacy Agent

Protects personal information.

## Consent Agent

Tracks user consent.

## Masking Agent

Redacts sensitive information.

## Session Agent

Issues temporary permissions.

## Exposure Agent

Monitors unusual access.

## Audit Agent

Records disclosures.

## Privacy Logbook Agent

Maintains permanent disclosure history.

---

# Flow Groups

## Identity Flows

* verify identity
* validate requester
* verify ownership
* verify organization

---

## Permission Flows

* request permission
* approve permission
* deny permission
* lease permission
* revoke permission
* expire permission

---

## Privacy Flows

* redact information
* mask information
* protect document
* sanitize output

---

## Disclosure Flows

* release insurance
* release carrier packet
* release permit
* release contact
* release signature
* release company profile

---

## Monitoring Flows

* detect unusual requests
* detect excessive disclosures
* detect identity abuse
* notify Ghost Guard

---

## Audit Flows

* write Privacy Logbook
* record disclosure
* record denial
* record consent
* record expiration

---

# Data Used

Unit Usage uses:

* Driver Profiles
* Dispatcher Profiles
* Company Profiles
* Permission Policies
* Secret Safe authorizations
* Consent Records
* Privacy Rules
* Active Load assignments
* Actor permissions

---

# Data Created

Unit Usage creates:

* Privacy Logbooks
* Permission Leases
* Disclosure Records
* Consent History
* Exposure Reports
* Privacy Audits
* Access History

---

# Statuses

Permission may be:

Pending

Granted

Denied

Leased

Expired

Revoked

Suspended

A disclosure may be:

Requested

Approved

Released

Masked

Redacted

Denied

Archived

---

# Permission Rules

Unit Usage may:

* verify identity
* lease temporary permissions
* release approved information
* redact sensitive information
* deny unauthorized requests
* create Privacy Logbooks
* monitor exposure

Unit Usage may not:

* bypass Secret Safe
* permanently expose private data
* ignore consent
* fabricate permissions
* leak protected information
* override company privacy policy

---

# Truth Rules

Every disclosure records:

Who requested it

Who approved it

Why it was needed

What information was released

What information remained protected

When access expires

Confidence in requester identity

Unit Usage never releases information without a documented reason.

---

# Relationship to CoDriver

CoDriver never hands out protected information directly.

Instead it asks:

"Unit Usage, can Packet Pilot have the driver's insurance certificate?"

Unit Usage verifies:

Identity

Purpose

Permissions

Consent

Load Assignment

Company Policy

Only then does the information move forward.

---

# Relationship to Other Actors

Unit Usage protects every actor.

Packet Pilot requests paperwork.

Cargo Connect requests carrier contacts.

Legal Logger requests evidence.

Radar Ranch requests operational information.

Fuel Factor requests fuel card access.

Memory Mark requests temporary protected storage.

Ghost Guard audits disclosure history.

Secret Safe confirms identity before Unit Usage evaluates the request.

---

# Relationship to Secret Safe

Secret Safe proves **who** someone is.

Unit Usage decides **what** they may receive.

Together they create Zero Trust inside HWY.

Neither actor can replace the other.

---

# Human Review Requirements

Human review is required when:

* banking information is requested
* tax documents are requested
* ownership is disputed
* legal authority is uncertain
* mass data exports are requested
* consent conflicts exist
* privacy policy violations are detected

---

# Product Role

Unit Usage is the personal privacy bodyguard of the HWY ecosystem.

It exists to protect drivers, dispatchers, companies, and every identity inside HWY from unnecessary exposure.

While Secret Safe secures access and Ghost Guard monitors behavior, Unit Usage ensures that only the minimum necessary information is ever disclosed—and only for a legitimate, authorized purpose.

In the HWY ecosystem, personal information is never simply handed over.

It is entrusted to Unit Usage, which stands between every user and the outside world as their permanent privacy advocate.
