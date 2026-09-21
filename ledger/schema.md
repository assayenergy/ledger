# Ledger schema

One row in `ledger.csv` = one claimed capacity, at one site, by one sponsor, as of one date. A
project that is re-scored later gets a new row with a new `last_verified` date rather than an
overwrite, so the history of what was claimed and known when stays intact.

## Columns

| Column | Meaning |
|---|---|
| `row_id` | A stable identifier for this row, unique within the ledger. |
| `row_type` | What kind of thing this row claims: `project` (a data center or campus), `company` (a sponsor-level claim), or `parcel` (a specific piece of land). |
| `grid` | The electric grid the site sits on or interconnects to (e.g. `ERCOT`). |
| `state` | The US state the site is in. |
| `county` | The county the site is in. |
| `sponsor` | The company or companies claiming to build, own, or operate the capacity. |
| `project_name` | The name the project is publicly known by. |
| `claimed_mw` | The megawatt capacity the sponsor has publicly claimed for this site, as reported. |
| `claim_date` | The date the `claimed_mw` figure was publicly stated (announcement date), where known. |
| `site_control` | Score (0–25) for how solid the public evidence is that the sponsor actually controls the land — a recorded deed or lease, an SEC filing, or a government body's own record scores highest; a press release alone scores lowest. |
| `physical` | Score (0–25) for physical build evidence — a docket-numbered generation permit is the strongest signal that construction is real. Shown as `n/o` (not observable) when the project's power strategy falls under Texas's permit-by-rule exemption (30 TAC §106.511), meaning the absence of a permit is genuinely uninformative rather than a sign nothing exists — see `scoring_basis`. |
| `financial` | Score (0–15) for financial commitment evidence specific to this site — an executed interconnection or power-supply agreement, a PUC filing, or a disclosed financing figure. |
| `incentive` | Score (0–15) for public incentive-filing evidence — an executed tax abatement or JETI agreement scores highest; a match on the state's separate sales-tax-exemption registry is real but caps lower. |
| `track_record` | Score (0–20) for the sponsor's documented history of delivering similarly-scaled projects on roughly the timelines it has claimed, evidenced by specific cited instances rather than general reputation. |
| `score` | The total score (0–100): the sum of the five signal columns above, or a renormalized total — see `scoring_basis`. |
| `scoring_basis` | `standard_100`: the total is a straight sum of all five signals out of 100. `renormalized_75`: `physical` was excluded from scoring (see above), so the total is the sum of the remaining four signals divided by their combined maximum of 75, scaled back to a 0–100 total. The two bases are not directly comparable signal-for-signal. |
| `tier` | The score band: `Evidenced` (70–100), `Progressing` (40–69), or `Announced-only` (0–39). Neutral labels — not "real" and "fake." |
| `site_control_provenance` | `government_record`: the site-control claim traces to a government body's own action (a council vote, a court filing, an SEC disclosure) or an equivalent recorded instrument. `press_reported_only`: the only public evidence is the sponsor's own statement or trade press, with no independent confirmation found. |
| `reversal_flag` | `YES` if a publicly documented, dated setback (a cancelled tenant, a failed financing round, a terminated lease, a lawsuit) has occurred since the original claim; blank otherwise. A reversal is never subtracted from the score — it is flagged with a citation instead. |
| `reversal_citation` | The source and brief description of the documented reversal, when `reversal_flag` is `YES`. |
| `last_verified` | The date this row's information was last checked against public sources. |
| `evidence_file` | A link to the file containing the sourced evidence for every claim in this row. |

## Notes

- A blank cell means the signal wasn't scored a nonzero value and no special basis applies (e.g. a
  `financial` score of 0 with no further note).
- `n/o (§106.511)` in `physical` is not a zero — it means the signal was excluded from scoring
  entirely because a missing permit is structurally uninformative for that project's power
  strategy. See [gridscore-method.md](../method/gridscore-method.md) for the full explanation.
