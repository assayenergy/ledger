#!/usr/bin/env python3
"""Build docs/ledger-watch.ics from docs/dates.csv.

Each row becomes an all-day VEVENT. UIDs are a SHA-1 of "date|event", so a
row keeps its UID across rebuilds unless its date or event text changes.
DTSTAMP is taken from source_captured, so the output is deterministic.

Standard library only. Usage: python3 scripts/build_ics.py
"""
import csv
import datetime as dt
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "dates.csv"
OUT = ROOT / "docs" / "ledger-watch.ics"
COLUMNS = ["date", "event", "projects_affected", "source_url", "source_captured"]


def escape(text):
    """Escape a TEXT value per RFC 5545 section 3.3.11."""
    return (text.replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    """Fold a content line to at most 75 octets per RFC 5545 section 3.1."""
    raw = line.encode("utf-8")
    parts = []
    limit = 75
    while len(raw) > limit:
        cut = limit
        while (raw[cut] & 0xC0) == 0x80:  # don't split a UTF-8 sequence
            cut -= 1
        parts.append(raw[:cut])
        raw = raw[cut:]
        limit = 74  # continuation lines start with a space
    parts.append(raw)
    return b"\r\n ".join(parts).decode("utf-8")


def build(rows):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Assay Energy//Ledger Watch dates//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Assay Ledger Watch",
    ]
    for row in rows:
        day = dt.date.fromisoformat(row["date"])
        captured = dt.date.fromisoformat(row["source_captured"])
        uid = hashlib.sha1(f"{row['date']}|{row['event']}".encode("utf-8")).hexdigest()
        description = (f"Projects affected: {row['projects_affected']}\n"
                       f"Source: {row['source_url']}\n"
                       f"Source captured: {row['source_captured']}")
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}@ledger.assayenergy",
            f"DTSTAMP:{captured:%Y%m%d}T000000Z",
            f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
            f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{escape(row['event'])}",
            f"DESCRIPTION:{escape(description)}",
            f"URL:{row['source_url']}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "".join(fold(l) + "\r\n" for l in lines)


def main():
    with SRC.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise SystemExit(f"{SRC}: expected columns {COLUMNS}, got {reader.fieldnames}")
        rows = sorted(reader, key=lambda r: r["date"])
    for row in rows:
        missing = [c for c in COLUMNS if not row[c].strip()]
        if missing:
            raise SystemExit(f"{SRC}: row {row['date']!r} missing {missing}")
    OUT.write_bytes(build(rows).encode("utf-8"))
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} events")


if __name__ == "__main__":
    main()
