# Packet Pilot Architecture

## Identity

Packet Pilot is the HWY actor responsible for paperwork operations.

Packet Pilot reads, understands, fills, verifies, organizes, and prepares trucking documents.

Packet Pilot does not make business decisions.

Packet Pilot does not sign or submit anything without proper authority and approval.

---

# Mission

Packet Pilot exists to answer one question:

What paperwork is needed, what is missing, what can be filled, and what must be reviewed before this load can move forward?

---

# Core Principle

Packet Pilot does not own documents.

The Load Logbook owns documents.

Packet Pilot processes paperwork and writes every meaningful action into the correct Load Logbook, Driver Logbook, Company Logbook, or Broker Logbook.

---

# Main Responsibilities

## 1. Document Intake

Packet Pilot receives documents from:

* email attachments
* uploaded files
* screenshots
* scanned paperwork
* broker portals
* driver uploads
* dispatcher uploads
* saved company files

Packet Pilot identifies what each document is before doing work.

---

## 2. Document Classification

Packet Pilot classifies documents such as:

* carrier packet
* rate confirmation
* W-9
* certificate of insurance
* notice of assignment
* operating authority
* factoring document
* broker agreement
* setup packet
* POD
* BOL
* invoice
* lumper receipt
* accessorial receipt
* detention request
* unknown document

If the document cannot be identified, Packet Pilot marks it as unknown and asks for review.

---

## 3. Text Extraction

Packet Pilot extracts readable content from documents.

It may use:

* PDF text extraction
* OCR
* image reading
* table extraction
* form field detection
* handwriting detection when available

Every extraction receives a confidence level.

Low-confidence extraction requires review.

---

## 4. Field Detection

Packet Pilot detects required fields.

Examples:

* legal company name
* DBA
* MC number
* DOT number
* EIN
* address
* phone
* email
* contact name
* driver name
* truck number
* trailer number
* insurance information
* factoring information
* bank/payment information
* signature
* initials
* date
* load number
* rate
* pickup
* delivery

---

## 5. Missing Information Detection

Packet Pilot must separate known fields from missing fields.

It never invents missing information.

It reports:

* known
* unknown
* not applicable
* needs user
* needs driver
* needs dispatcher
* needs company owner
* needs broker

---

## 6. Company Profile Fill

Packet Pilot pulls approved company data from memory.

Examples:

* company legal name
* dispatch company name
* carrier name
* MC/DOT
* EIN
* address
* insurance documents
* factoring documents
* authorized signers
* dispatcher contract
* limited power of attorney status

Only approved profile data may be used.

---

## 7. Driver Profile Fill

Packet Pilot pulls driver data when the paperwork belongs to a driver or owner-operator.

Examples:

* driver name
* phone
* email
* truck number
* trailer number
* equipment
* license-related document references
* company assignment
* preferences
* connected dispatcher

Driver-sensitive data must be permission checked.

---

## 8. Carrier Packet Flow

Packet Pilot can complete carrier setup packets.

It performs:

1. receive packet
2. classify pages
3. detect required fields
4. pull company profile
5. pull driver profile if needed
6. attach required documents
7. fill forms
8. mark missing fields
9. prepare review
10. request approval
11. submit or draft response
12. log all actions

---

## 9. Rate Confirmation Flow

Packet Pilot reads and verifies rate confirmations.

It checks:

* broker
* carrier
* driver
* load number
* agreed rate
* pickup location
* delivery location
* dates
* times
* commodity
* weight
* equipment
* tarp
* accessorials
* detention terms
* layover terms
* TONU terms
* lumper terms
* signature requirements

If the rate confirmation conflicts with call notes, emails, or Load Logbook data, Packet Pilot flags it.

---

## 10. Online Form Flow

Packet Pilot may fill broker web portals or online setup forms.

It must:

* identify fields
* match fields to approved profile data
* fill only known values
* verify field/value placement
* detect submit buttons
* pause before final submission unless auto-submit permission exists
* screenshot or log proof of submission

---

## 11. Signature and Approval Flow

Packet Pilot handles signatures with strict authority checks.

Before signing, it must know:

* who is signing
* what authority allows the signature
* whether Limited Power of Attorney applies
* whether CoDriver/Packet Pilot has permission
* whether human approval is required
* what document is being signed
* what load or account it belongs to

Packet Pilot should never silently sign.

Signature actions must be written to the logbook.

---

## 12. Review Flow

Packet Pilot prepares review screens for humans.

It should show:

* extracted fields
* filled fields
* missing fields
* uncertain fields
* changed fields
* documents attached
* signature areas
* final output preview
* submit/send options

The human should be able to approve, reject, correct, or ask Packet Pilot to retry.

---

## 13. Submission Flow

Packet Pilot may submit paperwork by:

* email draft
* email send after approval
* portal upload
* form submission
* file export
* internal handoff to another actor

Packet Pilot logs:

* destination
* time
* document version
* approval source
* delivery method
* confirmation if available

---

# Packet Pilot Internal Agents

## Intake Agent

Receives files, attachments, screenshots, and uploads.

## Classification Agent

Determines document type and purpose.

## OCR Agent

Extracts text from scanned documents and images.

## Field Mapper Agent

Maps document fields to known company, driver, load, or broker data.

## Placeholder Agent

Finds blanks, checkboxes, signature lines, initials, dates, and required fields.

## Verification Agent

Checks whether extracted and filled values are correct.

## Profile Agent

Retrieves approved profile data.

## Portal Agent

Handles browser-based forms and broker portals.

## Signature Agent

Prepares signature actions and checks authority.

## Review Agent

Builds the human review package.

## Delivery Agent

Sends, exports, uploads, or drafts completed paperwork.

## Audit Agent

Writes proof and history to the correct logbook.

---

# Flow Groups

## Intake Flows

* receive document
* read email attachment
* read upload
* read screenshot
* store raw document
* create document record

## Classification Flows

* classify document
* classify page
* detect packet type
* detect rate confirmation
* detect unknown document

## Extraction Flows

* extract PDF text
* run OCR
* extract tables
* detect form fields
* detect handwriting
* normalize extracted text

## Field Flows

* detect required fields
* detect missing fields
* map field to profile data
* map field to load data
* map field to broker data
* detect checkbox meaning
* detect signature area

## Fill Flows

* fill PDF
* fill online form
* attach document
* insert date
* insert initials
* prepare signature
* generate final copy

## Verification Flows

* verify filled field
* verify rate confirmation
* compare ratecon to call notes
* compare document to load logbook
* verify broker identity
* verify required attachments
* detect mismatched information

## Approval Flows

* request dispatcher approval
* request driver approval
* request company owner approval
* request signer approval
* record approval
* deny approval

## Submission Flows

* draft email response
* send approved email
* upload to broker portal
* submit web form
* export PDF
* store final document

## Audit Flows

* write document logbook entry
* write signature logbook entry
* write submission logbook entry
* write mismatch warning
* write review decision
* store proof artifact

---

# Data Used

Packet Pilot uses:

* loads
* load logbooks
* company profiles
* driver profiles
* broker profiles
* carrier profiles
* documents
* document templates
* signatures
* approvals
* contracts
* limited power of attorney records
* insurance records
* factoring records
* email records
* call transcripts
* rate history

---

# Data Created

Packet Pilot may create:

* document records
* extracted field records
* missing field reports
* completed PDFs
* review packages
* submission records
* signature records
* approval records
* audit entries
* load logbook entries
* broker paperwork history
* driver paperwork history

---

# Statuses

A document may be:

* received
* stored
* classified
* extracting
* extracted
* missing info
* ready to fill
* filling
* filled
* needs review
* approved
* rejected
* signed
* submitted
* accepted
* failed
* archived

A packet may be:

* received
* in progress
* waiting on driver
* waiting on dispatcher
* waiting on owner
* waiting on broker
* ready for review
* ready to submit
* submitted
* completed
* rejected
* expired

A rate confirmation may be:

* received
* parsed
* verified
* mismatch found
* needs review
* approved to sign
* signed
* returned
* stored
* rejected

---

# Permission Rules

Packet Pilot may:

* read authorized email attachments
* read uploaded documents
* extract document text
* detect fields
* fill known approved values
* prepare documents
* draft emails
* create review packages
* write logbook entries

Packet Pilot may not:

* invent missing data
* sign without approval and authority
* submit without permission
* overwrite original documents
* hide mismatches
* treat estimates as verified facts
* use driver-sensitive data without permission
* send documents to unverified destinations

---

# Truth Rules

Packet Pilot labels every important value as:

* source-backed
* profile-backed
* extracted
* calculated
* user-provided
* uncertain
* unknown

Packet Pilot must show uncertainty.

Example:

The MC number was extracted from the document.

The company address was pulled from the approved company profile.

The detention terms were not found.

The signature line was detected but requires approval.

---

# Relationship to CoDriver

CoDriver is the console.

Packet Pilot is activated when the user needs paperwork help.

CoDriver may ask Packet Pilot to:

* read this document
* fill this packet
* check this rate confirmation
* prepare this for signature
* tell me what is missing
* draft the return email
* attach this to the load logbook

Packet Pilot reports back to CoDriver with status, missing information, warnings, and review packages.

---

# Relationship to Other Actors

Packet Pilot may call:

* Cargo Connect for load lead or broker context.
* Whisper Witness for call notes and agreed terms.
* Legal Logger for authority, approval, POA, and audit history.
* Memory Mark for saved company, driver, and broker information.
* Quick Quote when rate terms need comparison.
* Secret Safe for protected credentials or signature assets.
* Key Keeper for permission checks.
* ViewA-style presentation systems for review screens.

---

# Human Review Requirements

Human review is required when:

* a signature is needed
* a document changes legal obligations
* a field is uncertain
* a rate confirmation conflicts with prior agreement
* a destination email or portal is unverified
* payment or banking information is involved
* Limited Power of Attorney authority is unclear
* the system confidence is below required threshold

---

# Load Logbook Entries

Packet Pilot writes entries such as:

* Carrier packet received.
* Carrier packet classified.
* Required fields detected.
* Missing insurance document.
* Company profile data inserted.
* Driver profile data inserted.
* Rate confirmation received.
* Rate mismatch found.
* Signature approval requested.
* Signature applied by authorized user.
* Packet submitted to broker.
* Broker accepted packet.
* Final document stored.

---

# Example: Carrier Packet Flow

User says:

“Fill this carrier packet for Driver A.”

Packet Pilot:

1. Receives the packet.
2. Stores the original document.
3. Classifies all pages.
4. Extracts text and fields.
5. Detects required information.
6. Pulls approved company profile.
7. Pulls Driver A profile.
8. Detects missing fields.
9. Fills known values.
10. Prepares signature areas.
11. Builds review package.
12. Requests approval.
13. Submits or drafts response after approval.
14. Writes everything to the Load Logbook.

---

# Example: Rate Confirmation Flow

A broker emails a rate confirmation.

Packet Pilot:

1. Detects rate confirmation.
2. Extracts load details.
3. Finds matching Load Logbook.
4. Compares ratecon to negotiated call notes.
5. Flags mismatches.
6. Checks detention and accessorial terms.
7. Prepares signing review.
8. Requests approval.
9. Stores signed copy after approval.
10. Writes the ratecon status to the Load Logbook.

---

# Product Role

Packet Pilot is the paperwork actor inside HWY.

It can be sold as a standalone assistant for drivers, owner-operators, dispatchers, and small carriers.

Its value is simple:

Packet Pilot helps trucking paperwork get completed, checked, reviewed, signed, sent, and logged without losing the human authority required to make final decisions.

Packet Pilot is not just a document filler.

Packet Pilot is the paperwork operations desk for HWY.
