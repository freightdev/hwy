# Whisper Witness Architecture

## Identity

Whisper Witness is the HWY actor responsible for live call assistance, transcription, call intelligence, negotiation memory, and conversation-to-logbook capture.

Whisper Witness listens, records, extracts, verifies, summarizes, and writes call events into the correct Logbook.

Whisper Witness does not negotiate for the user.

Whisper Witness does not make business decisions.

Whisper Witness provides private intelligence to the dispatcher, driver, or authorized user while the human remains in control.

---

# Mission

Whisper Witness exists to answer one question:

What is being said right now, what does it mean for this load, and what should be remembered?

---

# Core Principle

Whisper Witness does not own the call.

The Load Logbook owns the call history when the call belongs to a load.

If the call does not belong to a load yet, Whisper Witness creates a call record that may later attach to a Load, Broker, Driver, Company, or Contact Logbook.

---

# Main Responsibilities

## 1. Live Call Listening

Whisper Witness can listen during authorized calls.

It captures:

* speaker audio
* live transcript
* timestamps
* call participants
* detected company names
* detected broker names
* detected driver names
* detected load details
* questions asked
* answers given
* agreed terms
* missing details
* possible contradictions

---

## 2. Live Transcription

Whisper Witness converts speech into text.

It should support:

* dispatcher speech
* broker speech
* driver speech
* noisy environments
* accents when possible
* partial transcription
* confidence scores
* speaker separation when possible

Transcription uncertainty must be visible.

---

## 3. Speaker Detection

Whisper Witness should identify speaker roles when possible.

Possible speaker roles:

* dispatcher
* driver
* broker
* shipper
* receiver
* carrier
* customer
* unknown speaker
* CoDriver whisper

Speaker identity is not assumed unless supported by call context, account context, or user confirmation.

---

## 4. Load Detail Extraction

During a call, Whisper Witness extracts freight details such as:

* broker name
* company name
* MC number
* DOT number
* contact name
* phone number
* email
* origin
* destination
* pickup date
* pickup time
* delivery date
* delivery time
* commodity
* weight
* equipment
* trailer type
* tarp requirement
* load number
* reference number
* offered rate
* counter rate
* agreed rate
* detention terms
* layover terms
* TONU terms
* lumper terms
* special instructions

---

## 5. Private Whisper Support

Whisper Witness can show or speak private suggestions to the user.

Whispers are not commands.

Whispers are private intelligence.

Examples:

* Broker found.
* Broker risk unknown.
* Ask for MC number.
* Missing pickup time.
* Commodity is wood. Check tarp.
* Rate appears below estimate.
* Ratecon must match agreed rate.
* Ask about detention terms.
* Call notes say $7,000 agreed.

Whisper Witness must never speak to the broker unless the user explicitly allows it.

---

## 6. Broker Intelligence During Calls

When a broker or company name is detected, Whisper Witness may activate broker intelligence flows.

It may ask Cargo Connect, Memory Mark, or other actors for:

* broker profile
* prior load history
* MC/DOT lookup
* saved notes
* known contacts
* previous payment history
* risk signals
* source-backed public information

Whisper Witness should display confidence and unknowns.

---

## 7. Rate Awareness During Calls

When a lane appears, Whisper Witness may ask Cargo Connect or Quick Quote for rate intelligence.

It may display:

* miles
* RPM
* low estimate
* fair estimate
* strong ask estimate
* deadhead warning
* commodity warning
* tarp warning
* accessorial reminder
* confidence level
* missing sources

Whisper Witness does not decide the rate.

The dispatcher or driver decides.

---

## 8. Negotiation Memory

Whisper Witness tracks negotiation events.

Examples:

* Broker offered $4,000.
* Dispatcher countered $7,000.
* Broker said best is $5,500.
* Dispatcher asked for tarp pay.
* Broker agreed to $6,500 plus tarp.
* Detention terms were discussed.
* Rate confirmation pending.

These events become Logbook entries.

---

## 9. Contradiction Detection

Whisper Witness compares what is said against existing records.

Examples:

* Broker says pickup is Friday, but email says Thursday.
* Broker says rate is $4,000, but prior call note says $6,500.
* Rate confirmation arrives later with different rate.
* Broker name does not match email domain.
* Load number changed.
* Commodity changed.

Contradictions are flagged, not hidden.

---

## 10. Post-Call Summary

After the call ends, Whisper Witness creates a call summary.

The summary may include:

* participants
* purpose of call
* load details
* agreed terms
* missing information
* questions asked
* next actions
* warnings
* confidence
* transcript link
* related load
* related broker
* related driver

---

## 11. Load Logbook Writing

Every meaningful call event is written to the correct Logbook.

Examples:

* Call started.
* Broker identified.
* Load details extracted.
* Rate offer recorded.
* Counteroffer recorded.
* Agreed terms recorded.
* Missing information flagged.
* Call ended.
* Summary created.
* Transcript stored.
* Follow-up action created.

---

## 12. Call Recording Rules

Whisper Witness must respect recording permissions, user settings, and jurisdiction settings.

The system should support modes such as:

* no recording
* transcription only
* recording and transcription
* user-side notes only
* manual start
* automatic start for business calls
* consent prompt required

Whisper Witness must make the recording state visible.

---

# Whisper Witness Internal Agents

## Audio Capture Agent

Captures authorized audio streams from phone calls, app calls, or microphone input.

## Transcription Agent

Converts audio into text and timestamps.

## Speaker Agent

Attempts to identify speaker turns and speaker roles.

## Entity Extraction Agent

Extracts names, companies, MC numbers, DOT numbers, lanes, rates, dates, and load terms.

## Load Context Agent

Determines whether the call belongs to an existing Load or should create a new Load Lead.

## Broker Context Agent

Looks up broker or company context.

## Rate Context Agent

Requests lane and rate intelligence from Cargo Connect or Quick Quote.

## Whisper Agent

Creates private real-time suggestions for the user.

## Contradiction Agent

Compares call statements against existing emails, documents, ratecons, and logbook records.

## Summary Agent

Creates post-call summaries.

## Logbook Agent

Writes structured events into the correct Logbook.

## Consent and Policy Agent

Checks whether call recording, transcription, and storage are allowed under user settings and configured rules.

---

# Flow Groups

## Call Start Flows

* detect incoming call
* detect outgoing call
* identify caller
* check recording settings
* start transcription
* create call session
* attach call to known contact
* attach call to known load when possible

## Listening Flows

* capture audio
* transcribe audio
* detect speaker turns
* detect important statements
* detect load details
* detect broker identity
* detect driver identity
* detect rates
* detect dates
* detect special terms

## Intelligence Flows

* lookup broker
* lookup prior history
* lookup load context
* lookup driver context
* estimate lane rate
* check commodity requirements
* check tarp requirements
* check accessorial reminders
* detect missing fields

## Whisper Flows

* create private whisper
* display whisper card
* speak whisper to user only
* suppress whisper during sensitive moments
* prioritize urgent whisper
* dismiss whisper
* save whisper if useful

## Negotiation Flows

* record offer
* record counteroffer
* record agreement
* record rejection
* record condition
* record accessorial
* record follow-up
* compare spoken agreement to written document

## Post-Call Flows

* end call session
* finalize transcript
* summarize call
* extract next actions
* create load lead if needed
* update existing load
* write logbook entries
* notify CoDriver
* prepare follow-up email

## Verification Flows

* compare call to email
* compare call to rate confirmation
* compare call to broker profile
* compare call to driver update
* flag mismatch
* request human confirmation

---

# Data Used

Whisper Witness uses:

* calls
* transcripts
* load logbooks
* broker profiles
* driver profiles
* dispatcher profiles
* company profiles
* rate estimates
* historical loads
* email records
* rate confirmations
* user permissions
* call recording settings
* contact records
* actor activity logs

---

# Data Created

Whisper Witness may create:

* call session records
* audio recording references
* transcript records
* speaker segments
* extracted entity records
* whisper cards
* negotiation events
* contradiction warnings
* call summaries
* next action items
* load leads
* logbook entries
* follow-up drafts

---

# Statuses

A call may be:

* incoming
* outgoing
* ringing
* active
* listening
* transcribing
* paused
* muted
* ended
* summarizing
* summarized
* attached
* needs review
* archived

A transcript may be:

* live
* partial
* low confidence
* finalized
* corrected
* reviewed
* attached to logbook

A whisper may be:

* created
* shown
* spoken privately
* dismissed
* saved
* expired
* escalated

---

# Permission Rules

Whisper Witness may:

* listen to authorized calls
* transcribe authorized audio
* extract load information
* create call notes
* lookup broker information
* request rate intelligence
* show private whispers
* write logbook entries
* prepare post-call summaries

Whisper Witness may not:

* record calls without enabled permission
* hide recording status
* speak to an outside caller without explicit user permission
* pretend uncertain transcription is exact
* make negotiation decisions
* book freight
* sign documents
* send messages without approval
* attach sensitive call data to the wrong load

---

# Truth Rules

Whisper Witness labels information as:

* heard live
* transcribed
* user-confirmed
* speaker-claimed
* source-backed
* profile-backed
* calculated
* estimated
* uncertain
* unknown

Speaker-claimed information is not automatically treated as verified truth.

Example:

Broker said the load pays $6,500.

That means the broker claimed it.

It becomes verified only when confirmed by rate confirmation, email, user approval, or another accepted source.

---

# Privacy Rules

Whisper Witness must treat call data as sensitive.

Call data may include:

* broker information
* driver information
* company information
* rates
* negotiations
* personal phone numbers
* addresses
* payment terms
* business strategy

Access must be role-based.

A driver should not automatically see dispatcher-only negotiation notes unless shared.

A dispatcher should not automatically see driver-private notes unless permitted.

---

# Relationship to CoDriver

CoDriver is the console.

Whisper Witness is activated when calls, live conversations, or voice events need to be captured and understood.

CoDriver may ask Whisper Witness to:

* listen to this call
* summarize the call
* extract load details
* tell me what the broker said
* compare the call to the rate confirmation
* remind me what we agreed on
* create a follow-up task
* write this to the Load Logbook

Whisper Witness reports back to CoDriver with transcripts, summaries, warnings, whispers, and logbook entries.

---

# Relationship to Other Actors

Whisper Witness may call:

* Cargo Connect for broker, lane, and rate intelligence.
* Packet Pilot when paperwork or rate confirmations are discussed.
* Legal Logger for consent, approval, authority, and audit history.
* Fuel Factor when fuel or route cost matters.
* Quick Quote for fast rate estimation.
* Memory Mark for past broker, driver, and company history.
* Key Keeper for permission checks.
* Secret Safe for protected call settings or credentials.

---

# Human Control Requirements

Human control is required when:

* starting recording if auto-record is not enabled
* speaking to an outside caller
* accepting or rejecting a rate
* booking a load
* sending a follow-up message
* signing a document
* attaching uncertain call data to an official load
* correcting transcript meaning
* sharing call data with another user

---

# Load Logbook Entries

Whisper Witness writes entries such as:

* Call started with broker.
* Broker name detected.
* Load lane extracted.
* Offered rate recorded.
* Dispatcher counteroffer recorded.
* Tarp requirement mentioned.
* Detention terms missing.
* Broker agreed to revised rate.
* Call ended.
* Transcript finalized.
* Call summary created.
* Follow-up action created.
* Rate confirmation expected.

---

# Example: Broker Call Flow

A broker calls about a load.

Whisper Witness:

1. Detects incoming call.
2. Checks call permissions.
3. Starts transcription.
4. Detects broker name.
5. Looks up broker history.
6. Extracts lane and commodity.
7. Requests rate estimate.
8. Shows private whisper cards.
9. Records offer and counteroffer.
10. Detects missing terms.
11. Ends call session.
12. Creates call summary.
13. Writes events to the Load Logbook.
14. Notifies CoDriver of next actions.

---

# Example: Driver Call Flow

A driver calls with an update.

Whisper Witness:

1. Detects caller as connected driver.
2. Checks active loads.
3. Starts authorized transcription.
4. Extracts update.
5. Attaches update to current Load Logbook.
6. Detects issue such as delay, detention, or address change.
7. Creates dispatcher notification.
8. Summarizes the call.
9. Writes the update to the Load Logbook.

---

# Product Role

Whisper Witness is the live voice intelligence actor inside HWY.

It can be sold as a standalone call assistant for drivers, owner-operators, dispatchers, and small carriers.

Its value is simple:

Whisper Witness helps trucking calls become searchable, provable, organized load history without taking control away from the human.

Whisper Witness is not just transcription.

Whisper Witness is the call witness, negotiation memory, and private intelligence layer for HWY.
