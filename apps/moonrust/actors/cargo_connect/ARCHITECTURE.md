# Cargo Connect Architecture

## Identity

Cargo Connect is the HWY actor responsible for freight discovery, load intelligence, shipper discovery, broker discovery, and opportunity tracking.

Cargo Connect does not make business decisions for the dispatcher or driver.

Cargo Connect finds, organizes, verifies, ranks, and reports freight opportunities.

---

# Mission

Cargo Connect exists to answer one question:

What freight is available, worth looking at, and connected to the right driver, lane, equipment, and business goal?

---

# Core Principle

Cargo Connect does not own the load.

The Load Logbook owns the load.

Cargo Connect creates load leads, enriches them, monitors them, and writes updates into the Load Logbook.

---

# Main Responsibilities

## 1. Load Discovery

Cargo Connect searches for available freight from:

* load boards
* broker websites
* public freight postings
* shipper pages
* emails
* saved broker contacts
* dispatcher notes
* historical lanes
* manual user requests

Cargo Connect may use web search, browser automation, email monitoring, saved sources, and internal memory.

---

## 2. Load Lead Creation

When Cargo Connect finds a possible load, it creates a Load Lead.

A Load Lead is not a booked load.

A Load Lead contains:

* origin
* destination
* pickup date
* delivery date
* equipment type
* commodity
* weight
* rate if available
* broker or shipper
* contact info
* source
* confidence level
* missing information
* discovered time
* current status

---

## 3. Load Enrichment

Cargo Connect improves a Load Lead by finding missing information.

Examples:

* missing broker MC
* missing pickup date
* missing delivery time
* missing commodity
* missing weight
* missing contact phone
* missing email
* missing rate
* missing equipment type

Cargo Connect should never fake missing information.

If it does not know, it marks the field as unknown.

---

## 4. Broker and Shipper Discovery

Cargo Connect builds contact intelligence.

It can search for:

* brokers
* shippers
* warehouses
* manufacturers
* distribution centers
* direct freight contacts
* phone numbers
* emails
* lanes served
* freight types

Discovered companies are stored as contacts, not automatically trusted.

---

## 5. Lane Monitoring

Cargo Connect watches lanes that matter to the user.

Example:

* Ohio to Texas
* Midwest regional
* flatbed tarp freight
* dry van under 40,000 lbs
* weekend pickup
* driver-preferred lanes

Cargo Connect can say:

“I found 4 new loads matching this driver’s lane profile.”

---

## 6. Driver Matching

Cargo Connect compares load leads against driver profiles.

It checks:

* driver location
* equipment
* trailer type
* preferred lanes
* blocked lanes
* home time
* availability
* deadhead distance
* endorsements
* company permissions
* dispatcher assignment

Output:

* good match
* maybe match
* bad match
* missing data

---

## 7. Rate Intelligence

Cargo Connect can estimate whether a load is worth attention.

It checks:

* mileage
* RPM
* commodity
* equipment
* tarp requirements
* deadhead
* fuel impact
* historical lane data
* saved company history
* available external sources

It does not tell the user what to accept.

It says:

* low estimate
* fair estimate
* strong ask
* unknown
* confidence level

---

## 8. Opportunity Ranking

Cargo Connect ranks load leads.

Ranking factors:

* rate strength
* driver fit
* lane preference
* broker risk
* pickup timing
* delivery timing
* deadhead
* missing information
* confidence
* urgency
* user preference

Cargo Connect should show why a load was ranked high or low.

---

## 9. Monitoring and Rechecking

Cargo Connect can keep watching a load lead.

It tracks:

* still available
* removed
* rate changed
* contact changed
* duplicate detected
* better match found
* expired
* booked
* rejected

A lead should not silently disappear.

It should leave a log entry.

---

## 10. Load Logbook Writing

Every meaningful Cargo Connect action writes to a logbook.

Examples:

* Load lead created.
* Source found.
* Broker identified.
* Rate estimated.
* Missing fields detected.
* Driver matched.
* Lead rejected.
* Lead converted to active load.
* Broker contacted.
* Load expired.

---

# Cargo Connect Internal Agents

## Search Agent

Finds load opportunities and freight contacts.

Uses:

* web search
* saved websites
* broker pages
* shipper pages
* email sources

## Browser Agent

Uses browser automation when normal search is not enough.

Can inspect pages, click, extract visible information, and return structured findings.

## Load Parser Agent

Turns messy text into load fields.

Example input:

“Dallas TX pickup Friday going to Columbus OH dry van 42k call Mike.”

Example output:

origin, destination, equipment, weight, pickup date, contact.

## Source Verification Agent

Checks whether a found load has enough proof to trust.

It marks findings as:

* source-backed
* partial
* duplicate
* stale
* unknown

## Broker Finder Agent

Looks up broker information from the lead.

Finds names, MC/DOT if available, phone, email, domain, address, and prior history.

## Driver Match Agent

Compares load lead against driver profiles.

## Rate Estimate Agent

Calculates rough lane value and RPM.

## Duplicate Agent

Checks if this load was already found from another source.

## Monitor Agent

Rechecks leads over time.

## Report Agent

Creates clean output for CoDriver and the user.

---

# Cargo Connect Flow Groups

## Discovery Flows

* search load sources
* search broker websites
* search shipper websites
* search email for load offers
* detect freight opportunity
* create load lead

## Enrichment Flows

* extract load details
* find missing fields
* lookup broker
* lookup shipper
* normalize city/state
* calculate miles
* detect commodity requirements

## Matching Flows

* match driver
* check equipment
* check deadhead
* check availability
* check lane preference

## Rate Flows

* calculate RPM
* estimate lane rate
* compare historical rates
* flag low rate
* flag strong opportunity

## Monitoring Flows

* recheck lead
* detect stale lead
* detect duplicate lead
* detect changed rate
* update lead status

## Reporting Flows

* summarize load lead
* create opportunity card
* write load logbook entry
* notify CoDriver
* prepare call script

---

# Data Owned or Used

Cargo Connect uses:

* drivers
* equipment
* trucks
* trailers
* lanes
* brokers
* shippers
* load leads
* active loads
* historical loads
* rate history
* user preferences
* source history

Cargo Connect does not own final load truth.

Final truth belongs to the Load Logbook.

---

# Statuses

A Cargo Connect lead may be:

* discovered
* enriched
* missing info
* matched
* rejected
* watching
* contacted
* negotiating
* converted to load
* expired
* duplicate
* archived

---

# Permission Rules

Cargo Connect may:

* search public sources
* read connected email if authorized
* create load leads
* rank opportunities
* write logbook entries
* suggest questions
* notify CoDriver

Cargo Connect may not:

* book a load without approval
* agree to a rate
* sign a rate confirmation
* submit documents
* contact a broker automatically unless permission is granted
* pretend unknown data is known

---

# Output Types

Cargo Connect can return:

* load cards
* ranked load list
* lane report
* broker report
* shipper contact list
* missing info report
* driver match report
* opportunity summary
* logbook timeline entry

---

# Example Flow

User asks:

“Find loads for my flatbed driver near Columbus.”

Cargo Connect:

1. Reads driver profile.
2. Reads equipment.
3. Checks driver location.
4. Searches known freight sources.
5. Searches web sources.
6. Extracts load details.
7. Removes duplicates.
8. Estimates rates.
9. Matches loads to driver.
10. Ranks results.
11. Creates load leads.
12. Writes entries to the load logbook.
13. Returns opportunity cards to CoDriver.

---

# Relationship to CoDriver

CoDriver is the console.

Cargo Connect is an actor.

CoDriver activates Cargo Connect when the user needs freight discovery, lane intelligence, or load opportunity tracking.

Cargo Connect reports back to CoDriver.

CoDriver presents the result to the user.

---

# Relationship to Other Actors

Cargo Connect may call:

* Whisper Witness when a broker call starts.
* Packet Pilot when documents arrive.
* Legal Logger when contracts, approvals, or authority matters appear.
* Fuel Factor when fuel cost matters.
* Quick Quote when the user wants fast rate guidance.
* Memory Mark when prior knowledge is needed.

---

# Product Role

Cargo Connect is the load board intelligence actor inside HWY.

It can power:

* driver load discovery
* dispatcher freight search
* company opportunity boards
* lead monitoring
* broker discovery
* shipper discovery
* AI-assisted load board features

Cargo Connect is not just a search bot.

Cargo Connect is the freight opportunity engine for HWY.
