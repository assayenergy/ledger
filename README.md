# Assay Energy
Claims about large power projects, checked against the public record.

Every data center announcement is a bundle of claims. This many megawatts, on this land, powered
this way, funded by these people, energized by this date. Assay breaks each announcement into
those claims, turns each claim into an objective variable with a number against it, and gathers
the evidence for each from open public sources: county deeds, permit databases, regulatory
filings, court records, SEC disclosures. Five variables, one score, every source linked.

## What's here

* [/ledger](ledger) — the ledger itself: one row per claimed project, scored, tiered, and dated.
  Refreshed monthly; every refresh is a commit.
* [/method](method) — how the scoring works, in plain English.
* [/projects/tx](projects/tx) — the Texas project audit (21 announced data centers).
* [/pricing](pricing) — what grid flexibility is worth by location (FlexValue).
* [track-record.md](track-record.md) — what was published and what the record shows, dated.
* [corrections.md](corrections.md) — every correction, dated. Git history shows when each was
  made.

## The method in one paragraph

Five signals: site control (25), physical commitment (25), financial commitment (15), incentive
filings (15), sponsor track record (20). Tiers: Evidenced (70–100), Progressing (40–69),
Announced-only (0–39). Every point needs a linked source. Signals that can't be observed in the
public record are excluded rather than scored zero. Reversals - a cancelled tenant, a failed
financing, a lawsuit - are flagged with citations but never subtracted. Full detail in
[/method](method).

## Who am I

I am Vish Tella. I am not an energy expert. I am a verification person. I spent a decade in ad
tech building the fraud-detection and inventory-quality products that made RhythmOne's inventory
the #1-ranked in the world for quality by Pixalate, two years running. Ad tech learned that much
of what is offered for sale isn't what it claims to be, and built verification into the pipes.
Same concept, different context here.

## Commissioned work

The ledger is free. If you are exposed to a specific project, company, or parcel, I will run the
same check privately on yours: an evidence file on one project or company, a screen across your
list, or monitoring with dated alerts when the record changes. Email me at hello@assay.energy

## Independence

No money from developers, sponsors, or projects being scored. Public records only. Results are
published whether they pass or fail.

## Read and subscribe

Monthly editions and analysis: [assayenergy.substack.com](https://assayenergy.substack.com/)

Data and charts released under CC BY 4.0.
