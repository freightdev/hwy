# Radar Ranch Architecture

## Identity

Radar Ranch is the HWY actor responsible for external signal collection, lane intelligence, rate history, weather monitoring, traffic monitoring, market awareness, and long-term operational intelligence.

Radar Ranch collects information over time and stores it so HWY can answer better questions later.

Radar Ranch is a paid actor because it depends on integrations, scheduled monitoring, external data providers, storage, and ongoing processing.

---

# Mission

Radar Ranch exists to answer one question:

What is happening around this freight, this lane, this truck, this market, and this route over time?

---

# Core Principle

Radar Ranch does not just answer the moment.

Radar Ranch remembers the pattern.

A single rate is useful.

A year of rates is intelligence.

A single storm alert is useful.

A history of weather disruptions on a lane is intelligence.

---

# Philosophy

A ranch collects and manages cattle.

Radar Ranch collects and manages signals.

Rates.

Lanes.

Weather.

Traffic.

Fuel.

Market activity.

Route risks.

Broker activity.

Freight patterns.

Everything collected becomes part of the ranch, organized, searchable, and useful later.

---

# Main Responsibilities

## 1. Rate Collection

Radar Ranch collects and stores rate information.

Sources may include:

* user-entered rates
* quoted rates
* broker offers
* negotiated rates
* booked loads
* historical HWY loads
* approved external rate sources
* email offers
* call transcripts
* load board integrations when authorized

Every rate must include context.

A rate without lane, equipment, date, and source is weak intelligence.

---

## 2. Lane Intelligence

Radar Ranch builds lane memory.

A lane may track:

* origin
* destination
* equipment type
* average rate
* RPM
* seasonal changes
* recurring brokers
* recurring shippers
* common commodities
* deadhead patterns
* weather risks
* traffic risks
* fuel impact

---

## 3. Weather Monitoring

Radar Ranch monitors weather that may affect operations.

Examples:

* tornado warnings
* snowstorms
* ice
* flooding
* high winds
* hurricanes
* extreme heat
* road closures caused by weather

Weather alerts may attach to:

* active loads
* planned routes
* driver locations
* saved lanes
* equipment locations

---

## 4. Traffic and Route Monitoring

Radar Ranch monitors route conditions when integrations are available.

Examples:

* heavy traffic
* crashes
* closures
* construction
* delays
* detours
* restricted roads
* bridge events

Traffic information can be tied to a Load Logbook or Route Report.

---

## 5. Market Signal Collection

Radar Ranch gathers market signals.

Examples:

* freight volume changes
* lane demand
* unusual rate movement
* high rejection patterns
* broker activity
* seasonal freight patterns
* regional capacity pressure

Market signals should be labeled by confidence and source.

---

## 6. Alerting

Radar Ranch creates alerts when something meaningful changes.

Examples:

* tornado risk near active route
* lane rate drops sharply
* lane rate increases
* traffic delay ahead
* severe wind affecting empty trailers
* broker activity spike
* saved lane has new opportunity

Alerts must explain why they were triggered.

---

## 7. Historical Querying

CoDriver and other actors can ask Radar Ranch questions.

Examples:

“What have rates done on Columbus to Dallas?”

“Has this lane been weak lately?”

“Any storms on this route?”

“What brokers keep posting this lane?”

“What did we get paid last time?”

“What is the weather risk on this route?”

---

## 8. Data Normalization

Radar Ranch cleans and normalizes collected signals.

Examples:

* normalize cities
* normalize equipment types
* normalize dates
* normalize rate units
* normalize RPM
* detect duplicates
* detect stale data
* merge related signals

---

## 9. Source Confidence

Every collected signal must have a confidence level.

Examples:

* user-confirmed
* booked load
* official weather alert
* integration-backed
* broker-claimed
* transcript-extracted
* estimated
* unknown

Radar Ranch does not treat every signal equally.

---

## 10. Ranch Storage

Collected data is stored in organized collections.

Examples:

* rate herd
* lane herd
* weather herd
* traffic herd
* broker herd
* route herd
* market herd

The metaphor matters:

Radar Ranch gathers scattered signals and keeps them organized.

---

# Internal Agents

## Rate Collector Agent

Collects and stores rate data.

## Lane Agent

Builds lane intelligence.

## Weather Agent

Monitors severe weather and route weather.

## Traffic Agent

Monitors route disruptions.

## Market Agent

Collects market signals.

## Source Agent

Tracks where information came from.

## Normalization Agent

Cleans and standardizes data.

## Alert Agent

Detects meaningful changes.

## Query Agent

Answers questions from stored intelligence.

## Ranch Logbook Agent

Records collection and alert events.

---

# Flow Groups

## Collection Flows

* collect rate signal
* collect lane signal
* collect weather signal
* collect traffic signal
* collect market signal
* collect broker signal

---

## Normalization Flows

* normalize lane
* normalize city
* normalize equipment
* normalize rate
* normalize date
* detect duplicate
* detect stale signal

---

## Monitoring Flows

* monitor active route
* monitor saved lane
* monitor weather threat
* monitor traffic delay
* monitor rate movement
* monitor market change

---

## Alert Flows

* create weather alert
* create traffic alert
* create rate alert
* create lane alert
* create broker alert
* notify CoDriver
* attach alert to Load Logbook

---

## Query Flows

* query lane history
* query rate history
* query weather history
* query traffic history
* query broker activity
* query market signals

---

## Reporting Flows

* create lane report
* create rate report
* create route risk report
* create weather impact report
* create market report
* create ranch summary

---

# Data Used

Radar Ranch uses:

* Load Logbooks
* booked loads
* broker offers
* call transcripts
* emails
* user-entered rates
* driver locations when authorized
* route plans
* equipment profiles
* external weather sources
* external traffic sources
* external market sources
* load board integrations when authorized

---

# Data Created

Radar Ranch creates:

* rate records
* lane records
* weather alerts
* traffic alerts
* market signals
* route risk reports
* lane history reports
* rate history reports
* alert logs
* source confidence records

---

# Statuses

A signal may be:

* collected
* normalized
* duplicate
* stale
* verified
* unverified
* archived

An alert may be:

* created
* active
* acknowledged
* attached to load
* resolved
* expired
* archived

A lane profile may be:

* new
* building history
* active
* monitored
* seasonal
* archived

---

# Permission Rules

Radar Ranch may:

* collect authorized operational data
* monitor saved lanes
* monitor active routes
* store historical signals
* create alerts
* answer intelligence queries
* attach alerts to Load Logbooks

Radar Ranch may not:

* access private data without Secret Safe approval
* sell user data without explicit permission
* fabricate rate history
* treat broker claims as confirmed rates
* override driver or dispatcher decisions
* ignore source confidence
* monitor location without authorization

---

# Truth Rules

Every Radar Ranch answer must identify:

* what was collected
* when it was collected
* where it came from
* whether it was verified
* how confident the system is

Signal labels include:

* booked
* user-confirmed
* official alert
* integration-backed
* broker-claimed
* transcript-extracted
* email-extracted
* estimated
* unknown

---

# Relationship to CoDriver

CoDriver activates Radar Ranch when the user needs historical or live operational intelligence.

Examples:

“What are rates doing on this lane?”

“Any weather problems on this route?”

“Has this broker been posting more lately?”

“What did we get paid last time?”

“Watch this lane for me.”

Radar Ranch returns intelligence reports, alerts, and historical context to CoDriver.

---

# Relationship to Other Actors

Radar Ranch may support:

* Cargo Connect with lane and market intelligence.
* Whisper Witness with live call context.
* Fuel Factor with route and market conditions.
* Iron Insight with equipment location and route risks.
* Highway Helper with educational examples.
* Legal Logger with alert and source history.
* Big Bear with evidence when intelligence errors occur.

---

# Human Review Requirements

Human review is required when:

* a major business decision depends on low-confidence data
* weather threat information conflicts between sources
* rate information is only broker-claimed
* location monitoring is being enabled
* data sharing settings are changed
* paid external integrations are added

---

# Paid Actor Role

Radar Ranch is a paid actor because it requires:

* recurring data collection
* scheduled monitoring
* external integrations
* storage
* normalization
* alerting
* historical analysis
* route and weather intelligence
* rate and lane databases

It is an intelligence system, not a one-time helper.

---

# Example: Lane Rate Query

User asks:

“What have rates been like from Columbus to Dallas?”

Radar Ranch:

1. Searches stored lane records.
2. Filters by equipment type.
3. Reviews booked loads.
4. Reviews broker offers.
5. Reviews historical RPM.
6. Separates confirmed rates from claimed rates.
7. Returns lane history with confidence.
8. Suggests whether Cargo Connect should monitor the lane.

---

# Example: Severe Weather Alert

A driver is assigned to a route.

Radar Ranch detects a tornado threat near the route.

Radar Ranch:

1. Collects weather signal.
2. Confirms severity from trusted weather source.
3. Matches alert to active Load route.
4. Creates weather alert.
5. Notifies CoDriver.
6. Writes alert to Load Logbook.
7. Updates alert until resolved.

---

# Product Role

Radar Ranch is the paid operational intelligence actor inside HWY.

It collects the signals that help drivers, dispatchers, and carriers make better decisions over time.

Radar Ranch is not just a weather tool.

It is not just a rate database.

It is the long-term intelligence ranch where HWY gathers, organizes, and preserves the operational signals that matter on the road.
