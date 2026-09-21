# GridScore v0: Methodology

How I scored readiness for the 20 [21] largest publicly announced ERCOT-bound data center
projects, what evidence it's built on, and where the score is deliberately conservative,
incomplete, or contested.

## The core rule

This scores **projects on public evidence**, not companies on character. Every scored signal has
a linked public source and a capture date (2026-08-05 throughout, unless noted). No evidence found
means the signal scores zero, logged as "no public evidence found (as of 2026-08-05)" — that is
explicitly not a claim the thing doesn't exist, only that I couldn't find it in public record.
When evidence was ambiguous, I scored conservatively and flagged it rather than picking the more
flattering read.

## The five signals

| Signal | Points | What earns full credit |
|---|---|---|
| Site control | 25 | Recorded ownership/lease with a traceable paper trail — a government counterparty (a city, county, or university) is the strongest version; an SEC-disclosed public-company transaction is the second-strongest. Partial credit for a self-disclosed but unconfirmed acquisition, or an affiliate LLC traceable via a filed deed. |
| Physical commitment | 25, or excluded (see below) | A docket-numbered TCEQ air permit tied to the specific site — the single strongest "this is real" signal, because it means someone is actually building generation. Building/TDLR permits count when TCEQ evidence isn't found. For projects where the absence of a permit is itself structurally uninformative, the signal is excluded from scoring entirely rather than defaulted to zero — see "Three meanings of a low Physical signal" below. |
| Financial commitment | 15 | An executed interconnection or power-supply agreement, a PUC filing, or an SEC-disclosed financing figure specific to the project. Corporate-level investment figures (not tied to this specific site) earn partial credit. |
| Incentive filings | 15 | An **executed** Texas JETI Act (Ch. 403) agreement or a county/municipal tax abatement agreement earns up to the full 15. A match on the Texas Comptroller's separate §151.359 "Qualifying Data Center" sales-tax-exemption registry — a real, verified state filing, but a different and lower bar than a negotiated abatement — caps at **7 of 15**. |
| Sponsor track record | 20 | A documented pattern of the sponsor (or, where relevant, its named founder) delivering announced projects before, at claimed scale, on roughly claimed timelines, with specific cited instances — not general reputation alone. |

**Tiers:** 70–100 Evidenced · 40–69 Progressing · 0–39 Announced-only. Neutral names on purpose —
not "real" and "fake."

## Documented reversals are flagged, not scored negative

Two projects (Fermi America's Project Matador, Poolside's Project Horizon) have publicly
documented, dated setbacks since their original announcement — a cancelled tenant-funding pact and
an open lawsuit in Fermi's case, a terminated anchor lease and a collapsed funding round in
Poolside's. I did not subtract points for these beyond what the underlying evidence already
implies (a company with no operating history and a cancelled deal naturally scores low on Sponsor
Track Record on the evidence alone). Instead, both carry a `documented_reversal_flag` with a
citation in every output table. The reasoning: this project scores evidence, not vibes, in both
directions — a reversal is a fact to report, not a hit to double-count.

## Site-control confidence labels

Every site-control score in `scored_table.csv` carries a confidence label:

- **government-record**: the paper trail runs through a government body's own action — a city
  council vote, a county commissioners court document, a university system lease, or an SEC
  filing (a legally binding federal disclosure, treated as government-record-equivalent for this
  purpose).
- **press-reported-only**: the only public evidence is the sponsor's own press release or trade
  coverage, with no independent government or filing-level confirmation found.

7 of 21 projects carry a government-record label; the rest are press-reported-only. That split is
itself worth reading as a finding: most of what the public "knows" about site control for these
projects is what the sponsor chose to say about it.

## The CAD-portal limitation (read this before trusting site-control scores)

**No individual county appraisal district (CAD) parcel record was pulled directly this session.**
I attempted one live lookup (Carson County CAD, for the Fermi America project) via an interactive
browser tool; the tool timed out and wasn't usable for the rest of the session. Generic web search
cannot reach the dynamic, form-based search portals that essentially every Texas CAD uses — this
is a real, structural gap in what's automatable, not a shortcut I took. Every "site control"
finding in this dataset is therefore sourced from a press release, an SEC filing, or a government
body's own minutes/records — never from an appraisal district's raw parcel data. Where that
distinction changes a score's reliability, it's marked in the near-tier-boundary watchlist in
`scored_table.md`. Treat every press-reported-only site-control score as provisional until someone
with working CAD access confirms it.

## The Comptroller §151.359 registry vs. JETI — two different programs, not interchangeable

I manually fetched and read the Texas Comptroller's "Qualifying Data Centers" registry
(comptroller.texas.gov/taxes/data-centers/data-center-lists.php) as raw HTML, not through an
AI-summarized tool — the earlier automated pass missed real matches (Hut 8's "Beacon Point 1,"
Google's "Project Goodnight," Fermi's own "Fermi Data Center 1") and wrongly called others
inconclusive. §151.359 is a state sales-tax exemption program with its own registration process; it
is **not** the JETI Act (Chapter 403) that the original rubric names, and it is not a negotiated,
project-specific incentive the way a county abatement is. I scored it as a real but lesser signal
(caps at 7/15) rather than either ignoring it or treating it as equivalent to an executed
abatement.

## Three meanings of a low Physical Commitment signal — and why one of them isn't "low" at all

A missing TCEQ docket can mean three different things, and treating them identically would have
been the single biggest distortion in this dataset. I sort every project into one of three states:

1. **Confirmed, permitted (score 5–25 on the standard 25-point scale).** A docket-numbered TCEQ air
   permit, a TDLR building permit, or equivalent was found and tied to the specific site. This is
   real, positive evidence — the strongest signal in the entire rubric, because building a
   dedicated generation plant at scale is expensive and hard to fake.
2. **True zero (score 0, on the standard scale).** The project's *own stated power strategy* would
   require an individually-permitted facility — dedicated primary generation at meaningful
   scale, the same class of build as the confirmed-permitted projects above — and no such permit
   was found despite that being the reasonable expectation. This happened for exactly 3 of 21
   projects: **Poolside** (aero-derivative turbines, primary generation), **SB Energy** (explicitly
   plans "new energy generation... to supply the majority of the campus's power"), and **Tract**
   (no operator/tenant named yet, so there is nothing to have even applied for a permit — a
   different flavor of zero, but still a real one: "not yet applicable" rather than "missing
   despite expectation"). A true zero here is a meaningful, informative absence.
3. **Not observable by category (excluded from scoring, not scored as zero).** The project's power
   strategy — a grid interconnection agreement plus standard-size backup/emergency generators, or
   reliance on an already-permitted third-party plant — is exactly the profile Texas's "permit by
   rule" regime (30 TAC §106.511, "Portable and Emergency Engines and Turbines") was built to wave
   through without individual public notice or a hearing. Multiple independent sources (Texas
   Tribune, University of Houston Law Center, floodlightnews.org) confirm data-center emergency
   diesel/gas arrays routinely qualify this way, sometimes totaling 150+ MW at a single site with
   zero public docket. **A missing permit here tells you nothing** — not that the generation exists,
   not that it doesn't. Scoring it as a zero would be treating a coin that hasn't been flipped as
   though it landed on tails.

## Physical Commitment renormalization for "not observable by category" projects

For the 9 projects in category 3, I do not assign Physical Commitment a number on the 0–25 scale
at all — not 25, not a partial credit, not a symbolic small number. **The signal is excluded from
both the numerator and the denominator**, and the total is renormalized over the remaining four
signals:

```
total = (Site Control + Financial Commitment + Incentive Filings + Sponsor Track Record)
        ÷ 75 × 100
```

75 is the combined maximum of the four remaining signals (25 + 15 + 15 + 20). The result still
lands on a 0–100 scale and uses the same 70/40 tier cutoffs, but it is **not directly comparable,
signal-for-signal, to a standard /100 score** — it answers "how strong is the evidence across the
four signals we can actually observe for this project," not "how strong is the evidence across all
five." I display Physical Commitment as **"n/o (§106.511)"** for these 9 rather than leaving a
blank or a zero, so the exclusion is visible everywhere the table appears, not just in a footnote.

**Why renormalize instead of the simpler options I tried first:** I initially scored these 9 as a
true zero (Session 3, first pass), then as a flat +5 partial credit out of 100 (a correction pass),
before landing here. The zero was wrong because it punished projects for a regulatory category, not
for a lack of evidence. The flat +5 was an improvement but arbitrary — there's no principled reason
the "can't tell" credit should be worth exactly 5 points rather than 3 or 8, and a flat credit still
quietly dilutes a project's score on a signal that was never really being measured for it.
Renormalization removes the arbitrary constant and the dilution at the same time, at the cost of
making these 9 scores sit on a different footing than the other 12 — a tradeoff I judged better
than either alternative, but one you should weigh differently if you disagree.

### Transparency table — every score and tier that differs, flat-+5-credit vs. renormalized

| Project | Flat-+5 total (/100) | Renormalized total | Flat tier | Renormalized tier |
|---|---|---|---|---|
| Grand Prairie Campus (PowerHouse/Provident) | 29 | 32 | Announced-only | Announced-only |
| Beacon Point (Hut 8) | 51 | 61 | Progressing | Progressing |
| Childress Campus (Crusoe/Lancium) | 53 | 64 | Progressing | Progressing |
| Panhandle — Haskell Co. ("Journey") | 70 | 87 | Evidenced | Evidenced (no longer boundary-fragile) |
| **Project Caprock (Aligned)** | 38 | **44** | Announced-only | **Progressing** |
| **Denton Campus (Core Scientific)** | 62 | **76** | Progressing | **Evidenced** |
| Garden City Facility (Marathon) | 41 | 48 | Progressing | Progressing |
| Kaufman County Campus (Prometheus) | 24 | 25 | Announced-only | Announced-only |
| **Bosque County Campus (ECP+KKR/CyrusOne)** | 35 | **40** | Announced-only | **Progressing** |

Three tier changes emerged from renormalization beyond what the flat-credit version produced —
Aligned and ECP+KKR both cross Announced-only→Progressing, and Core Scientific crosses
Progressing→Evidenced. All three moves point the same direction (upward), because renormalization
is systematically more generous whenever a project's other four signals are strong relative to 75
— exactly the projects where a flat +5-out-of-100 credit was underselling them the most.

## Known limitations (v0)

- **No CAD/deed record was independently pulled.** See above — this is the single biggest
  reliability caveat on the Site Control signal across the dataset.
- **The Google Haskell County site identity is unresolved.** "Journey," "Thelma," and a registry
  entry for "Fort Haskell Data Center" may or may not describe the same facility; a third,
  separate Crusoe Energy proposal in the same county had its abatement request rejected by the
  same commissioners court. Project #14 is scored using only the "Journey" evidence, the most
  documented candidate, and is marked ambiguous rather than resolved.
- **Two MW figures are genuinely undisclosed** (Google's Armstrong and Haskell County campuses,
  bundled into one statewide $40B/6,200MW+ PPA announcement) and excluded from MW arithmetic in
  `key-stats.md`.
- **There is no public registry to check any project's ERCOT interconnection status against.**
  Every ERCOT-approval claim in this dataset is the sponsor's own word, taken at face value where
  no counter-evidence exists. See `candidate_universe.md`'s market-opacity finding.
- **Sponsor Track Record is unevenly researched.** Several sponsors (Provident, CloudBurst/Evolve,
  Vantage, Aligned, CyrusOne) got a general-reputation assessment rather than cited-instance
  evidence, simply because this session's search budget ran out before a deeper pass on each. That
  shows up as a mid-range rather than a definitive score, and is marked as such in the evidence
  appendix.
- **Scoring judgment calls were made explicit, not hidden.** Two examples: Tract's founder-level
  track record (real, cited, but not the same as the company itself having delivered a site under
  this specific land-developer model) was scored as partial credit rather than zero or full marks;
  a project "topped out" reaching a construction milestone (PowerHouse/Irving) was treated as real,
  standard-scale physical-commitment evidence, distinct from an unverified inference that a
  facility "probably" holds permits because it's operating (Core Scientific and Marathon both fall
  into that latter case — no docket was found for either, and rather than guess, both were sorted
  into the "not observable by category" bucket and renormalized, on the judgment that their
  established, long-operating sites plausibly run on permit-by-rule-covered backup generation
  rather than nothing at all).
- **Renormalization makes 9 of 21 scores non-comparable, signal-for-signal, to the other 12.** This
  is a deliberate tradeoff, documented above, not an oversight. If you'd rather see all 21 on a
  strictly identical basis, the flat-+5-credit and true-zero versions of these same 9 scores are
  preserved in the transparency table above and in `scored_table.md`.
