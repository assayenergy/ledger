# /ledger

The ledger itself: `ledger.csv`, one row per claimed capacity at one site by one sponsor as of
one date, plus `schema.md` documenting every column in plain English.

Rows are scored using the methods in [/method](../method) and cite an `evidence_file` for the
underlying record. Refreshed monthly; every refresh is a commit.

2026-09-21: Fermi Project Matador refreshed, 65 → 80. Eight points are a correction (a missed
county tax abatement); seven are new evidence. See the gridscore evidence file.
