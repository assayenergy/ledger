Mirror of the Substack page, kept here for timestamped history. Last synced: 2026-09-20.

# Corrections

A verification practice that doesn't correct itself is not an honest one. Every correction is
listed here with its date. Both after publishing, and in review before going live.

**September 26, 2026, GridScore table sync.**
- docs/scored_table.csv synced from gridscore main (33529a1), with the
  corrections link made a full URL.
- Fermi's Dec 12, 2025 share drop is 33.8% (closes of $15.25 and $10.09;
  matches the Lupia complaint). This reverses my Aug 5 correction, which
  changed "about 34%" to "about 33%". The original figure was closer; the
  Aug 5 correction was wrong.
- The "parallel filing" was a law-firm press release about the same case.
  There is one securities class action.
- No score changed. Details:
  https://github.com/assayenergy/gridscore/blob/main/corrections.md

**September 23, 2026, parcel reference.**

- Removed a reference to a specific parcel from parcels/va/county-surry.md. The reference remains
  in earlier history; it concerns a parcel no longer under consideration.

**September 23, 2026, utility territory method file.**

- Removed references to private working data from the method file. Sections 3 and 5 of
  parcels/va/utility-territory-method.md are rewritten as general method: evidence tiers for which
  utility serves a location, and a three-state way of recording the determination. Removed text
  that referred to non-public working files. The change is forward-only; the earlier text remains
  in the repository history.

**September 23, 2026, Surry setback wording and citations.**

- Surry: the setback was summarized as "300 feet from all abutting public rights-of-way and main
  buildings on adjoining parcels/property lines." The slash blurred whether the 300 ft runs from
  buildings or from property lines. The adopted text (§ 4-608(A)(7), Ord. No. 2025-01) runs it
  from both: "from all abutting public rights of way and main buildings on adjoining parcels and
  from adjacent property lines," with an exception for adjoining parcels the applicant owns or
  leases. The file now quotes the Municode text verbatim.
- Surry: the discretionary proximity factor was cited as "Sec. 1-501.1(B)(4)." Corrected to
  § 4-608(B)(4).
- Surry: the § 1-501.1 cap quote came from the Feb. 2025 hearing-notice draft ("7 percent"). It is
  now quoted from the codified text ("seven percent"). The substance is unchanged.

**September 23, 2026, Virginia county solar files, precedent check.**

- Surry: Sycamore Cross was listed as "Approved" in Surry with a siting agreement on Feb. 13,
  2025. Corrected: the Surry Board of Supervisors denied the CUP and the siting agreement
  unanimously that night, overturning a 5–4 Planning Commission recommendation.
- Surry: cap headroom was given as a bottom-up sum of 6,737 acres used and 3,958 acres remaining.
  That sum double-counted Spring Grove II's ~1,650 acres, which lie inside CUP 2018-03 and CUP
  2020-02; it counted the denied Sycamore Cross (124 acres); and it used a press figure (2,950)
  where a county letter gives 3,905+ acres. Replaced with the county's own figure from the 2026
  Comprehensive Plan: 8,260 acres used and 2,435 acres remaining (10,695 − 8,260). Spring Grove
  II's approval date was also corrected: it has no CUP of its own and was approved in two parts,
  on May 3, 2018 and July 2, 2020.
- Sussex: Blackwater Solar was described as "500 MWac on ~4,200 acres." 4,200 acres is the
  disturbance area. Corrected: the total project area is 8,355 acres (July 16, 2026 Board packet).
  The Planning Commission's 7–0 recommendation to deny was placed "in an earlier round." Corrected:
  it was made on this application, on March 2, 2026.
- Southampton: an Aug. 2021 staff remark was presented as acknowledging the gap in the current
  ordinance. Corrected: the remark described the Dec. 2018 ordinance. The 20 MW minimum was
  adopted later, in July 2022, and the adoption record shows the Board was told it excludes 1–5 MW
  projects.
- Removed from the Surry and Southampton files: a reference to a specific parcel, a link to an
  unpublished file, a tax-map parcel ID and two street addresses. Parcel-level data does not belong
  in this repository. They remain in the history of commit 2528f36.

**August 5, 2026, pre-publication review (GridScore).**

- Fermi America's IPO date was written as September 2025. Corrected to on or around October 1,
  2025.
- Fermi's one-day stock decline was written as about 34%. Corrected to about 33%, matching
  multiple independent reports of the decline.
- The Announced-only share of disclosed capacity was written as 22%. Corrected to 23.0% (6,601 of
  28,722 MW) after the scoring correction below.
- Fermi's 65-point score was described as "middle of the Progressing tier." Corrected to "upper
  half."
- The scored table's sort order was stale from an earlier scoring pass (Riot at 80 was listed
  above Google Haskell at 87). Re-sorted. No scores changed.

**August 5, 2026, scoring rule change (GridScore).**

Projects whose generators plausibly qualify for permit-by-rule were first scored zero on the
Physical signal, then given a flat five-point credit. Both were wrong. The zero punished them for
evidence that can't be observed, and the credit awarded points for it. I replaced it with the
renormalization rule now on the Method page. Compared with the original zero scoring, five
projects moved up a tier: Google Haskell, Core Scientific Denton, Marathon Garden City, Aligned
Caprock, and the ECP/KKR Bosque County campus. The transparency table in the repo shows every
score under both treatments.

**August 9, 2026, at publication (GridScore).**

The draft title claimed the audit was run "two days before" the Governor's August 3 directive.
Checked against my own file dates, that was not accurate: the evidence digging ran August 4 and
5, straddling the directive. The title and body were corrected before publishing to say the work
started before the order and finished two days after it. The repo README carried the stale
phrasing for a few hours after publication and was fixed the same day.

**July 31, 2026, pre-publication review (FlexValue).**

- The calibration against Cipher Mining's disclosed power cost first compared a 2024 model year
  to a Q1 2025 disclosure and described them as matching "within a dollar." The mismatch in
  periods was flagged and the published text shows both model years against the disclosure, with
  the 2025 model running higher and the reasons stated.
- A summary bullet claiming "resource nodes beat hub benchmarks" was dropped from the FlexValue
  write-up. The difference was $11.18 versus $10.74 per MWh, about 4%, too thin to carry the
  claim.

## 2026-09-22

A working file committed to this repository in error was removed by history
rewrite on 2026-09-22. No other history has been altered. This is the only
instance of history modification in this repository.

If you find an error, reply to any post or write to hello@assay.energy. Corrections are credited.

Source: [assayenergy.substack.com/p/corrections](https://assayenergy.substack.com/p/corrections)
