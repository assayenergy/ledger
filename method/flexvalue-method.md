# FlexValue v0: Methodology

How I calculated the flexibility discount ($/MWh and % vs. firm load) for 10 ERCOT nodes,
what data it's built on, and where the model is deliberately conservative or simplified.

## What this measures

For a hypothetical 1 MW load at a given ERCOT pricing node, how much cheaper is electricity
if that load can flex (curtail itself during expensive hours) versus running flat, 24/7,
all year ("firm load")? I express the answer as a **discount**: $/MWh saved, and the
percentage of firm-load cost that represents.

## The three flex tiers

| Tier | Notice required | Max hours/year curtailed | What it can do |
|---|---|---|---|
| **A** | ≤10 minutes | 400 | Chase real-time price spikes and the 4 coincident-peak (4CP) intervals directly |
| **B** | ≤1 hour | 200 | Plan around day-ahead prices, with limited same-day adjustment |
| **C** | Day-ahead only | 87 (~top 1% of hours) | Scheduled avoidance of the day-ahead market's most expensive hours only |

These are v0 defaults, not regulatory standards, and easy to change.

## The three value components

1. **Energy avoidance**: the flex load skips its tier's most expensive hours and pays the
   average price of the hours it *does* consume, instead of the flat 8,760-hour firm-load
   average. Tier A picks hours using actual real-time prices, which is effectively perfect
   hindsight since it can react within 10 minutes. Tier C only sees day-ahead prices, a day
   in advance. Tier B splits the difference: a day-ahead shortlist, refined with same-day
   information.
2. **ECRS ancillary revenue**, Tier A only, and conservatively so. The load offers its
   flexibility into ERCOT's ECRS reserve product for its annual hour budget, earning the
   average clearing price, with a 25% haircut for imperfect market participation. Tiers B and
   C earn nothing here. That's a deliberately conservative choice on my part, not a claim
   that they couldn't.
3. **4CP transmission avoidance**: Texas transmission utilities bill large loads based on
   their demand during the 4 highest-demand 15-minute intervals of the year (one in each of
   June, July, August, and September; details below). A load that isn't consuming during
   those moments avoids that charge. I modeled Tiers A and B as fully avoiding it, 100%
   success. Tier C only has day-ahead notice, so I set it at 50% success, since the exact
   4CP interval is only known after the fact. This is usually the single largest component,
   so I've split it out. That way you can evaluate, or discount, this assumption on its own.

The total discount is the sum of all three, each expressed as $/MWh of energy the flex load
actually consumes that year.

## The 10 nodes

**4 ERCOT trading hubs** (West, North, Houston, South): standard, citable benchmarks.

**6 resource nodes**, chosen to tell a differentiated story near real, publicly announced
large-load clusters:

| Node | Near | Story |
|---|---|---|
| Odessa (Ector Co.) | Cipher Mining's Odessa bitcoin facility | Permian |
| Red Canyon wind farm (Scurry Co.) | Marathon Digital's Garden City site | Permian-adjacent |
| Roscoe wind farm (Nolan Co.) | Sweetwater wind corridor | West Texas wind |
| Trent wind farm (Nolan Co.) | OpenAI/Oracle's "Stargate" 1.2 GW AI campus (Abilene) | West Texas wind / AI mega-load |
| Midlothian gas plant (Ellis Co.) | Google's Midlothian/Red Oak hyperscale campuses | DFW south |
| Forney gas plant (Kaufman Co.) | Richardson Telecom Corridor data centers | DFW east |

Large loads (data centers, miners) generally don't have their own ERCOT settlement point.
They settle at their zone's price instead. Where the named locality had no generation bus of
its own, I used the nearest real, verifiable resource node in the same county or congestion
pocket as the local price proxy. That's the standard way to get a sub-zonal locational signal
for a site that isn't itself a settlement point.

Two nodes carry a lower-confidence utility assignment, marked † throughout: Red Canyon and
Roscoe, both in Nolan/Scurry County, are assigned to Oncor by adjacency to a confirmed
Oncor-owned substation nearby, not by direct confirmation for that specific site. I haven't
verified this precisely. This pocket of West Texas genuinely has overlapping Oncor and
AEP Texas North territory.

## Data sources

- **Prices**: ERCOT Settlement Point Prices (SPP), real-time (15-min) and day-ahead (hourly),
  pulled via the [gridstatus](https://github.com/kmax12/gridstatus) library. Hubs and load
  zones go back to Jan 2023, from ERCOT's official annual bulk archive products. The 6
  resource nodes only go back to Jan 2024, since ERCOT's authenticated Public API doesn't
  retain settlement-point-level history before December 2023.
- **Ancillary prices**: ERCOT day-ahead ECRS/RRS/Non-Spin/Reg-Up/Reg-Down clearing prices,
  same source, Jan 2023 to present.
- **4CP intervals**: ERCOT's own published Four Coincident Peak calculations, exact date and
  15-minute interval, for 2023 through 2025. 2026 isn't published yet; ERCOT releases these
  each November after the summer season closes.
- **Transmission tariffs**: official PUCT-filed monthly rate reports plus each utility's own
  tariff filings (Oncor, CenterPoint, AEP Texas), "Transmission" customer class, 4CP demand
  charge. I verified these in July 2026.
- **Calibration**: Riot Platforms and Cipher Mining's SEC 10-Q/8-K disclosures of real-world
  curtailment credits and all-in power costs.

## Known limitations (v0)

- **The 4CP charge dominates the result.** That's by design. I show it as its own line so
  you can discount or exclude it if the 100%/100%/50% avoidance-success assumptions look too
  generous to you.
- **ECRS revenue is deliberately conservative**: one ancillary product, one tier, a 25%
  haircut. It ends up the smallest of the three components everywhere in this dataset.
- **Firm-load baseline is a flat 1 MW, 8,760 hours/year profile.** That's a simplification,
  stated openly. A real facility's load shape would shift these numbers.
- **Wind-node and DFW-node curtailment timing look more alike than you'd expect.** About 86%
  of Tier A's curtailed hours overlap between a West Texas wind node and a DFW gas-plant node
  in 2025. System-wide scarcity pricing (ERCOT's evening net-load peak) drives most of the
  highest-priced hours everywhere, regardless of local wind supply. Local basis shows up more
  in the average price level, and in how often prices go negative, than in which specific
  hours turn out to be the most expensive.
- **Hub-level 4CP rates use a simplification.** Hubs span multiple utilities, so there's no
  single correct transmission rate for one. Three of the four hubs use Oncor's rate (the
  largest ERCOT utility by load), and Houston Hub uses CenterPoint's (its core, unambiguous
  territory). Neither is a precise load-weighted blend.
- **2026 figures are year-to-date.** I scaled the flex-tier hour budgets down proportionally
  so they're comparable to full prior years, rather than just partial-year undercounts.
