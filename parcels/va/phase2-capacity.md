# Virginia Shared Solar Program — Phase II capacity position

> Disclosure: the author has a financial interest in land acquisition in the counties covered by
> this research.

As of 2026-09-22. Every figure below is either read directly from a cited primary source and
tagged `[gov-record]` / `[press]`, or is arithmetic performed on those tagged figures (labeled
"derived" and shown with its inputs). Nothing here is estimated.

## Tagging key

- `[gov-record]` — a statute, a Virginia State Corporation Commission (SCC) docket record, or a
  regulated utility's tariff/program disclosure filed under an SCC-approved program (treated as
  government-record-equivalent, the same way this ledger treats SEC filings elsewhere — it is a
  compliance disclosure under a specific Code of Virginia mandate, not a marketing claim).
- `[press]` — trade press or other non-government source.

## MW authorized

525 MW alternating current authorized for Phase II, of which 450 MW is limited to projects
serving no more than 51% low-income customers and 75 MW may be allocated to projects serving more
than 51% low-income customers. `[gov-record]`

Source (read directly, not paraphrased from a secondary summary): Va. Code § 56-594.3(E) —
*"Upon the earlier of (i) a determination that at least 90 percent of the megawatts of the
aggregate capacity of such program have been subscribed and that project construction is
substantially complete or (ii) July 1, 2026, the Phase II Utility shall release an additional 525
megawatts of capacity as part two of such program, 450 megawatts of which shall serve no more
than 51 percent low-income customers and 75 megawatts of which may serve more than 51 percent
low-income customers."* Enacted 2026 Va. Acts of Assembly cc. 670, 671 (amending § 56-594.3,
originally enacted 2020 cc. 1238, 1264). [law.lis.virginia.gov/vacode/title56/chapter23/section56-594.3](https://law.lis.virginia.gov/vacode/title56/chapter23/section56-594.3/)

## MW awarded

**104,789 kWac (104.789 MWac) across 28 projects.** `[gov-record]`

Source: Dominion Energy's Shared Solar Program page, "Projects Awarded Capacity in Phase II"
table — [dominionenergy.com/virginia/renewable-energy-programs/shared-solar-program](https://www.dominionenergy.com/virginia/renewable-energy-programs/shared-solar-program),
read directly (28 rows, every `Project Capacity Rating (kWac)` cell transcribed into
[phase2-awards.csv](phase2-awards.csv)). Arithmetic:

```
  3,000 + 4,999 + 2,500 + 5,000 + 2,550 + 3,000 + 4,950 + 3,000 + 5,000 + 5,000
+ 4,800 + 3,000 + 3,000 + 3,000 + 3,000 + 2,000 + 5,000 + 3,000 + 3,000 + 3,000
+ 5,000 + 3,000 + 5,000 + 2,000 + 3,000 + 4,990 + 5,000 + 5,000
= 104,789 kWac
```

(28 addends, one per row of `phase2-awards.csv`; re-verified programmatically by summing the
`capacity_kwac` column.)

**Resolving the discrepancy:** you computed 104,789 kWac across 28 projects; a second extraction
returned 117,789. Reading the table directly — all 28 rows, each capacity cell as published on
the live page — reproduces **104,789** exactly. **104,789 is correct.** 117,789 is 13,000 kWac
too high and does not correspond to any combination of values actually printed in the table; I
cannot identify the specific mechanical error behind that second extraction without seeing its
method, but it does not match the source as published, tagged, and re-summed here `[gov-record]`.
One structural feature of the table that a naive parser could plausibly mishandle: the Nexamp
"Harmon West Solar, LLC" row (5,000 kWac total) carries a split low-income annotation —
*"100% 1.799MW - 51% 3.201MW"* — in the column next to capacity, the only row in the table with
two values in that cell. A parser that treated those two sub-values as additional capacity rows,
or that lost column alignment on that row and drifted for subsequent rows, is a plausible
candidate — flagged as a hypothesis, not a confirmed cause.

## Low-income bucket split (per project)

The 525 MW is split by statute into a 450 MW general bucket (projects serving **no more than
51%** low-income customers) and a 75 MW low-income bucket (projects serving **more than 51%**
low-income customers). `[gov-record]` Dominion's award table does not use the words "general" or
"low-income bucket," but every row states an exact "Amount of Capacity Allocated to Low-income
Customers" percentage, and every value observed is either exactly 51% or 100% (one row splits
between the two) — which lines up precisely with the statute's own 51%-threshold dichotomy. I
mapped each row against that threshold directly: `[gov-record]`

- **51%** → not more than 51% → **GENERAL** bucket
- **100%** → more than 51% → **LOW_INCOME** bucket
- One row — Nexamp's "Harmon West Solar, LLC" (5,000 kWac) — carries a split annotation,
  *"100% 1.799MW - 51% 3.201MW"*, meaning 1,799 kWac of that project's capacity falls in the
  LOW_INCOME bucket and 3,201 kWac falls in GENERAL. `phase2-awards.csv` represents this as two
  rows (same project, split capacity) rather than forcing a single bucket value onto a project
  that the source itself splits — the only place the CSV's row count (29) departs from the
  28-project count used elsewhere in this document; the total capacity is unchanged.

No row is `UNSTATED` — the table states a low-income percentage for all 28 projects.

**Bucket totals (summed from `phase2-awards.csv`):**

| Bucket | Awarded | Pool | Remaining |
|---|---|---|---|
| GENERAL (≤51% LI) | 31,191 kWac (31.191 MW) | 450 MW | **418.809 MW** |
| LOW_INCOME (>51% LI) | 73,598 kWac (73.598 MW) | 75 MW | **1.402 MW** |
| **Total** | 104,789 kWac (104.789 MW) | 525 MW | **420.211 MW** |

`[gov-record]`, derived by summing `li_bucket`-grouped rows in `phase2-awards.csv` against the
statutory 450/75 split. The combined remaining figure (420.211 MW) is unchanged from before this
split — but the split itself is the more useful number: **the 75 MW low-income bucket is almost
fully awarded (only 1.402 MW left), while the 450 MW general bucket is 93% unawarded.** A new
low-income-serving project applying today would face a nearly exhausted pool even though the
program overall looks 80% open.

## Awards dated after 7/1/2026

**None.** All 28 Phase II awards carry the identical `Date of Project Acceptance in Program` of
**7/1/2026** — read directly from the table; no row shows a later (or earlier) date. `[gov-record]`

## Allocation rule and waitlist provision

Quoted verbatim from Dominion's Shared Solar Program page: `[gov-record]`

> "Capacity will be awarded on a first-come basis. No action will be taken on any application
> until the application has been deemed complete. If capacity in the program is not available,
> projects with applications that have been deemed complete and that otherwise meet the program's
> qualifications will be placed on a waiting list. The Company will notify the SO within 30 days
> of receipt of a completed application whether the shared solar facility has been awarded
> capacity in the program or placed on a waiting list. To secure awarded capacity, a SO must
> submit the required security deposit within 10 days."

## Pending queue

**Cannot be determined from public record.** What I checked, per the task's four named sources:

- **Dominion's shared solar program page and linked program documents** — the page publishes only
  two tables, "Projects Awarded Capacity in Phase I" and "Projects Awarded Capacity in Phase II."
  No waitlist, queue, or pending-application table or count appears anywhere on the page. The
  linked documents (Subscriber Organization Registration Agreement, Coordination Agreement,
  Schedule SS and Schedule SO-SS tariffs) describe the award/waitlist *process* (quoted above)
  but disclose no current count of pending or waitlisted applications or their aggregate MW.
  `[gov-record]`
- **SCC docket PUR-2020-00125** ("Shared Solar Program") — I reviewed its full document list
  (most-recent-first, through 09/10/2026) and ran a keyword search of "waiting list" OR "queue"
  scoped to this case (30 hits). The 2025–2026 hits are all routine tariff/bill-credit-rate
  filings; they contain no waitlist count. The remainder are 2020–2021 rulemaking-era comments,
  plus one directly relevant historical document: a Coalition for Community Solar Access filing
  (Doc #368920, part of its "Motion to Approve Remaining Shared Solar Program Capacity," filed
  01/11/2024) that reads: *"Accordingly, CCSA requests the SCC enter an order directing Dominion
  to make additional 50 MWs, for a total of 200 MWs, available immediately to wait listed
  projects, with remainder available to shared solar facilities that apply for capacity awards."*
  `[gov-record]` This confirms a formal waitlist mechanism has been invoked and litigated in this
  docket before — but it concerns **Part One's original 200 MW cap in early 2024**, not Part
  Two/Phase II's 525 MW (which didn't exist as a released tranche until 7/1/2026). It does not
  state a current Phase II queue size.
- **Dominion's shared solar annual or periodic reports to the SCC** — I found no case type or
  filing in PUR-2020-00125's history captioned as a recurring shared-solar-specific annual or
  periodic status report. Dominion's compliance filings in this docket are tariff-sheet and
  bill-credit-rate updates, not queue-status reports. `[gov-record]`
- **Any SCC staff report on the program** — the docket's only Staff Report and Staff Update
  documents date to the original 2020 rulemaking; no staff report addressing current Phase II
  subscription or waitlist status appears in the 2025–2026 filings I reviewed. `[gov-record]`

**Consequences for the numbers above:**

1. **How many applications are pending/waitlisted for Phase II, and their aggregate MW:**
   unverified — not stated anywhere I could find in the public record.
2. **Size of the waitlist immediately before the 7/1/2026 release, and whether 104.789 MW cleared
   it fully or partially:** unverified. I found no pre-7/1/2026 waitlist count for Part Two
   specifically, so I cannot say whether the 28 (29, split) awarded projects represent all of a
   prior waitlist, a subset of it, or new applications with no queue history at all.
3. **Whether Dominion publishes queue or waitlist position anywhere:** **No** — not on the
   program page, not in its linked documents, and not (as a current, standing disclosure) in the
   umbrella SCC docket. The only place a waitlist has been quantified in the public record is the
   one 2024 litigation filing above, about a different (Part One) capacity tranche.

**Therefore: 420.211 MW remaining is an UPPER BOUND on capacity available to a new applicant
today, not a firm figure.** If applications beyond the 28 (29) already awarded are currently
pending or waitlisted for Phase II — which the program's own stated first-come/waitlist process
implies is plausible, especially given the near-exhaustion of the 75 MW low-income bucket — some
or all of the 420.211 MW headroom may already be spoken for by queued applicants ahead of any new
applicant, even though it has not yet been converted into an "awarded" row on Dominion's table.

**Document or contact that would settle it:**

- Dominion's Shared Solar Program team directly — **sharedsolar@dominionenergy.com** — the exact
  contact the program itself designates for subscriber-organization application status.
- A future compliance filing, Staff Report, or Staff Update in **SCC docket PUR-2020-00125**,
  where an equivalent Part One waitlist figure has surfaced before (Doc #368920).
- A Virginia FOIA request to the SCC or to Dominion for the current Phase II subscriber
  organization application/waitlist roster.

## Status of the additional 268 MW (Part III trigger)

Va. Code § 56-594.3(E) directs: *"On or before the substantial completion of 268 megawatts of
capacity under part two of such program, the Phase II Utility shall petition the Commission to
initiate a shared solar expansion proceeding to determine the capacity for part three of the
shared solar program."* `[gov-record]`

**Petition status: unverified as filed — no petition located in the public record as of
2026-09-22.** What I checked:

- SCC Case Information docket search, case name "shared solar" — returns 5 cases, the most
  recent being PUR-2022-00144 (a 2022 subscriber-organization licensing matter). No 2026 filing
  matching "expansion," "Part III," or "268 megawatts." `[gov-record]`
- The umbrella rulemaking docket **PUR-2020-00125** ("Shared Solar Program," Ex Parte, status
  Pending, last amended 09/04/2026) — where every prior Part I/Part II aggregate-capacity order
  and tariff compliance filing has historically landed (e.g., "Order on Aggregate Capacity —
  6/14/2024"). Its document list, most-recent-first through 09/10/2026, shows only routine
  tariff/bill-credit-rate filings in 2025–2026; no Part III expansion petition appears.
  `[gov-record]`
- A keyword search of SCC's full-text PDF index for "shared solar expansion" returned one
  unrelated Appalachian Power Company hearing transcript. `[gov-record]`
- A broader search of Virginia Electric and Power Company's 2026 dockets (participant-name
  search, ~40 most recent cases by filing date, back to 01/2026) found no case captioned around
  shared solar capacity expansion. This search returned more result pages than I reviewed
  exhaustively, so I cannot rule out a differently captioned petition elsewhere in that list.
  `[gov-record]`

Given all 28 Phase II awards were only accepted into the program on 7/1/2026, it is unsurprising
that none has yet reached "substantial completion" — but that is context, not a finding; I did not
find the petition itself in the public record.

**Document that would settle it:** the SCC's Case Information docket search
([scc.virginia.gov/docketsearch](https://scc.virginia.gov/docketsearch)) — specifically, watch
case **PUR-2020-00125** for a new filing captioned around "shared solar expansion proceeding" or
"Part III," or a new standalone PUR-numbered petition docket from Virginia Electric and Power
Company on the same subject.

## Locality frequency (by awarded capacity)

Computed from `phase2-awards.csv`. `[gov-record]`

| Locality | Awarded capacity (kWac) | Projects |
|---|---|---|
| Petersburg, VA | 19,000 | 6 |
| Suffolk, VA | 17,989 | 4 |
| South Boston, VA | 8,000 | 2 |
| Fisherville, VA | 6,000 | 2 |
| South Hill, VA | 4,000 | 2 |
| West Point, VA | 5,000 | 1 |
| Chesapeake, VA | 5,000 | 1 |
| Moseley, VA | 5,000 | 1 |
| King George, VA | 5,000 | 1 |
| Edinburg, VA | 5,000 | 1 |
| Norfolk, VA | 5,000 | 1 |
| Colonial Beach, VA | 4,800 | 1 |
| Smithfield, VA | 3,000 | 1 |
| Charlottesville, VA | 3,000 | 1 |
| Fredericksburg, VA | 3,000 | 1 |
| Waynesboro, VA | 3,000 | 1 |
| Toana, VA | 3,000 | 1 |

**Petersburg has the most awarded capacity** (19,000 kWac across 6 projects), followed by
Suffolk (17,989 kWac across 4 projects).
