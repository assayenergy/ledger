#!/usr/bin/env python3
# Disclosure: the author has a financial interest in land acquisition in the counties covered by
# this research.
"""
territory_compare.py -- county-level comparison of two electric retail service
territory layers for four Virginia counties.

Layers compared
  A. HIFLD "Electric Retail Service Territories" (ORNL / DOE CESER via DHS HIFLD
     Open). HIFLD Open was deactivated 2025-08-26; this script reads the copy
     re-hosted on ArcGIS Online by owner NBAM_Org, whose item description says it
     "was downloaded from HIFLD on 8/21/2025 and will not be updated".
  B. Virginia SCC "VA_Electric_2016" (ArcGIS Online owner account ending "_VASCC";
     the layer behind the SCC web map "Virginia Electric Service Territory Map").
County land polygons
  US Census TIGER/Line 2024 COUNTY polygons minus the union of TIGER/Line 2024
  AREAWATER polygons for each county ("TIGER minus AREAWATER" method; the
  cartographic-boundary files are NOT used).

Output: county-level aggregated areas only. No coordinates, points, parcels,
addresses or maps are written to stdout. All downloads are cached in
$ASSAY_TERRITORY_CACHE (default ~/.cache/assay-territory), outside any repo.

Requires: geopandas, shapely>=2, pyproj, requests.
"""
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import geopandas as gpd
import requests
from shapely import make_valid
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import polygonize, unary_union

# ----------------------------------------------------------------------------
# Source constants
# ----------------------------------------------------------------------------
ARCGIS_ITEM_API = "https://www.arcgis.com/sharing/rest/content/items/{}?f=json"

HIFLD_ITEM_ID = "597555ce8e4a4892a030784a7c657fdd"
HIFLD_LAYER_URL = ("https://services3.arcgis.com/OYP7N6mAJJCyH6hd/arcgis/rest/"
                   "services/Electric_Retail_Service_Territories_HIFLD/FeatureServer/0")
HIFLD_ORIGINAL_PAGE = ("https://hifld-geoplatform.hub.arcgis.com/datasets/"
                       "geoplatform::electric-retail-service-territories-2")  # deactivated
HIFLD_ARCHIVE_DOI = "https://doi.org/10.3886/E239091V2"  # DataLumos archive (not used here)

SCC_ITEM_ID = "3654b21beb0d489ea16b279c782d8d88"
SCC_WEBMAP_ITEM_ID = "785101f9c89f42b8bfc7055f91b2303d"
SCC_LAYER_URL = ("https://services3.arcgis.com/Ww6Zhg5FR2pLMf1C/arcgis/rest/"
                 "services/VA_Electric_2016/FeatureServer/0")

TIGER_COUNTY_URL = "https://www2.census.gov/geo/tiger/TIGER2024/COUNTY/tl_2024_us_county.zip"
TIGER_AREAWATER_URL = "https://www2.census.gov/geo/tiger/TIGER2024/AREAWATER/tl_2024_{geoid}_areawater.zip"

COUNTIES = {  # GEOID -> name
    "51183": "Sussex",
    "51181": "Surry",
    "51175": "Southampton",
    "51093": "Isle of Wight",
}

EQUAL_AREA = "EPSG:5070"  # NAD83 / Conus Albers
SQM_PER_SQMI = 1609.344 ** 2  # 2,589,988.110336 m^2 per sq mi
SLIVER_SQMI = 0.01  # display threshold only; all area is still counted

CACHE = Path(os.environ.get("ASSAY_TERRITORY_CACHE",
                            Path.home() / ".cache" / "assay-territory")).expanduser()

# ----------------------------------------------------------------------------
# Explicit crosswalk to a canonical key (EIA utility ID, which HIFLD carries in
# its ID field). Keys: HIFLD NAME (exact) and SCC Provider code (exact).
# Anything not listed is reported as UNMATCHED and kept under its raw name.
# ----------------------------------------------------------------------------
CANON = {  # canonical key -> display name
    "EIA19876": "Dominion Energy Virginia (Virginia Electric & Power Co)",
    "EIA21244": "Southside Electric Cooperative",
    "EIA15410": "Prince George Electric Cooperative",
    "EIA4117": "Community Electric Cooperative",
    "EIA12260": "Mecklenburg Electric Cooperative",
    "EIA19978": "Town of Wakefield (municipal)",
    "EIA6715": "City of Franklin (municipal)",
}
HIFLD_XWALK = {  # HIFLD NAME -> canonical (HIFLD ID must equal the EIA number)
    "VIRGINIA ELECTRIC & POWER CO": "EIA19876",
    "SOUTHSIDE ELECTRIC COOP, INC": "EIA21244",
    "PRINCE GEORGE ELECTRIC COOP": "EIA15410",
    "COMMUNITY ELECTRIC COOP": "EIA4117",
    "MECKLENBURG ELECTRIC COOPERATIVE": "EIA12260",
    "TOWN OF WAKEFIELD - (VA)": "EIA19978",
    "CITY OF FRANKLIN - (VA)": "EIA6715",
}
SCC_XWALK = {  # SCC Provider -> canonical
    "VEPCO": "EIA19876",          # Utility = "Dominion Virginia Power"
    "SSEC": "EIA21244",           # "Southside Electric Cooperative"
    "PGEC": "EIA15410",           # "Prince George Electric Cooperative"
    "CEC": "EIA4117",             # "Community Electric Cooperative"
    "MEC": "EIA12260",            # "Mecklenburg Electric Cooperative"
    "TownOfWakefield": "EIA19978",  # "Town of Wakefield"
    "Franklin": "EIA6715",        # "Franklin"
}
SCC_NO_UTILITY = {"none"}  # SCC polygons explicitly labelled Provider='none'


# ----------------------------------------------------------------------------
# Download helpers
# ----------------------------------------------------------------------------
def _get(url, **kw):
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=300, **kw)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))


def download(url, name):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if not p.exists():
        tmp = p.with_suffix(p.suffix + ".part")
        with _get(url, stream=True) as r, open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
        tmp.rename(p)
    return p


def ms_to_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date().isoformat() if ms else "n/a"


def fetch_layer(layer_url, bbox_4326, tag):
    """Fetch every feature intersecting the study envelope, one feature per request
    (some territory polygons are very large). Cached as GeoJSON."""
    out = CACHE / f"{tag}_studyarea.geojson"
    if out.exists():
        return gpd.read_file(out)
    base = {"geometry": ",".join(f"{v:.6f}" for v in bbox_4326),
            "geometryType": "esriGeometryEnvelope", "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects", "where": "1=1"}
    ids = _get(layer_url + "/query", params={**base, "returnIdsOnly": "true", "f": "json"}).json()
    if "error" in ids:
        sys.exit(f"{tag}: query error {ids['error']}")
    feats = []
    for oid in sorted(ids["objectIds"]):
        gj = _get(layer_url + "/query", params={"objectIds": oid, "outFields": "*",
                                                "outSR": 4326, "f": "geojson"}).json()
        feats.extend(gj["features"])
    fc = {"type": "FeatureCollection", "features": feats}
    out.write_text(json.dumps(fc))
    return gpd.read_file(out)


# ----------------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------------
def clean(g):
    """make_valid, keep only polygonal parts, then zero-buffer."""
    g = make_valid(g)
    parts = []
    for p in getattr(g, "geoms", [g]):
        if isinstance(p, Polygon):
            parts.append(p)
        elif isinstance(p, MultiPolygon):
            parts.extend(p.geoms)
    return MultiPolygon(parts).buffer(0) if parts else Polygon()


def sqmi(a_m2):
    return a_m2 / SQM_PER_SQMI


def main():
    print("=" * 78)
    print("Electric retail territory comparison: HIFLD vs Virginia SCC 2016")
    print(f"Run date (UTC): {dt.datetime.now(dt.timezone.utc).date()}   cache: {CACHE}")
    print("=" * 78)

    # ---- metadata / vintage --------------------------------------------------
    meta = {}
    for tag, item, layer in [("HIFLD", HIFLD_ITEM_ID, HIFLD_LAYER_URL),
                             ("SCC", SCC_ITEM_ID, SCC_LAYER_URL)]:
        it = _get(ARCGIS_ITEM_API.format(item)).json()
        ly = _get(layer, params={"f": "json"}).json()
        ei = ly.get("editingInfo") or {}
        meta[tag] = it
        print(f"\n[{tag}] item {item}  owner={it.get('owner')}  title={it.get('title')!r}")
        print(f"   service: {layer}")
        print(f"   item created={ms_to_date(it.get('created'))}  item modified={ms_to_date(it.get('modified'))}")
        print(f"   layer editingInfo.lastEditDate={ms_to_date(ei.get('lastEditDate'))}  "
              f"dataLastEditDate={ms_to_date(ei.get('dataLastEditDate'))}")

    # ---- county land polygons ---------------------------------------------------
    cz = download(TIGER_COUNTY_URL, "tl_2024_us_county.zip")
    counties = gpd.read_file(f"zip://{cz}", where="STATEFP='51'")
    counties = counties[counties.GEOID.isin(COUNTIES)].to_crs(EQUAL_AREA).set_index("GEOID")
    land = {}
    for geoid in COUNTIES:
        wz = download(TIGER_AREAWATER_URL.format(geoid=geoid), f"tl_2024_{geoid}_areawater.zip")
        water = gpd.read_file(f"zip://{wz}").to_crs(EQUAL_AREA)
        cgeom = make_valid(counties.loc[geoid, "geometry"])
        land[geoid] = clean(cgeom.difference(clean(unary_union(water.geometry.values))))

    bbox = gpd.GeoSeries(list(counties.geometry), crs=EQUAL_AREA).to_crs(4326).total_bounds
    pad = 0.01
    bbox = (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad)

    # ---- territory layers -------------------------------------------------------
    hifld = fetch_layer(HIFLD_LAYER_URL, bbox, "hifld").to_crs(EQUAL_AREA)
    scc = fetch_layer(SCC_LAYER_URL, bbox, "scc").to_crs(EQUAL_AREA)
    # repair invalid rings (self-intersections) before any overlay
    hifld["geometry"] = [clean(g) for g in hifld.geometry]
    scc["geometry"] = [clean(g) for g in scc.geometry]

    unmatched = []
    def canon_h(row):
        k = HIFLD_XWALK.get(row["NAME"])
        if k is None:
            unmatched.append(("HIFLD", row["NAME"], row["ID"]))
            return "RAW-HIFLD:" + row["NAME"]
        if f"EIA{row['ID']}" != k:
            unmatched.append(("HIFLD-ID-MISMATCH", row["NAME"], row["ID"]))
        return k

    def canon_s(row):
        if row["Provider"] in SCC_NO_UTILITY:
            return None
        k = SCC_XWALK.get(row["Provider"])
        if k is None:
            unmatched.append(("SCC", row["Provider"], row["Utility"]))
            return "RAW-SCC:" + row["Provider"]
        return k

    hifld["canon"] = hifld.apply(canon_h, axis=1)
    scc["canon"] = scc.apply(canon_s, axis=1)

    # ---- crosswalk print --------------------------------------------------------
    print("\nCROSSWALK (canonical key = EIA utility ID carried in HIFLD 'ID')")
    print(f"{'canonical':<10} {'display':<55}")
    for k, v in CANON.items():
        h = [n for n, c in HIFLD_XWALK.items() if c == k]
        s = [f"{p} ({scc.loc[scc.Provider == p, 'Utility'].iloc[0].strip() if (scc.Provider == p).any() else 'not in study bbox'})"
             for p, c in SCC_XWALK.items() if c == k]
        print(f"{k:<10} {v:<55}\n{'':<10}   HIFLD NAME: {h}\n{'':<10}   SCC Provider: {s}")
    print("SCC Provider 'none' (Utility blank) is treated as NO UTILITY.")
    print("HIFLD features in bbox:", sorted(set(hifld.NAME)))
    print("SCC features in bbox:  ", sorted(set(scc.Provider)))

    # ---- per-county partition --------------------------------------------------
    rows = []
    for geoid, cname in COUNTIES.items():
        L = land[geoid]
        land_m2 = L.area
        h_parts = [(c, make_valid(g.intersection(L))) for c, g in zip(hifld.canon, hifld.geometry)]
        s_parts = [(c, make_valid(g.intersection(L))) for c, g in zip(scc.canon, scc.geometry)
                   if c is not None]
        s_none = [make_valid(g.intersection(L)) for c, g in zip(scc.canon, scc.geometry) if c is None]
        h_parts = [(c, g) for c, g in h_parts if not g.is_empty and g.area > 0]
        s_parts = [(c, g) for c, g in s_parts if not g.is_empty and g.area > 0]

        # planar partition of the county land by every boundary in both layers
        lines = [L.boundary] + [g.boundary for _, g in h_parts + s_parts] + \
                [g.boundary for g in s_none if not g.is_empty]
        faces = [f for f in polygonize(unary_union(lines)) if f.area > 0]
        acc = {"agree": 0.0, "differ_disjoint": 0.0, "differ_partial": 0.0,
               "only_hifld": 0.0, "only_scc": 0.0, "neither": 0.0,
               "hifld_overlap": 0.0, "scc_overlap": 0.0}
        pair_differ = {}
        covered = 0.0
        for f in faces:
            p = f.representative_point()
            if not L.covers(p):
                continue
            a = f.intersection(L).area
            covered += a
            H = frozenset(c for c, g in h_parts if g.covers(p))
            S = frozenset(c for c, g in s_parts if g.covers(p))
            if len(H) > 1: acc["hifld_overlap"] += a
            if len(S) > 1: acc["scc_overlap"] += a
            if H and S:
                if H == S:
                    acc["agree"] += a
                else:
                    acc["differ_partial" if H & S else "differ_disjoint"] += a
                    key = ("+".join(sorted(H)), "+".join(sorted(S)))
                    pair_differ[key] = pair_differ.get(key, 0.0) + a
            elif H:
                acc["only_hifld"] += a
            elif S:
                acc["only_scc"] += a
            else:
                acc["neither"] += a

        by_h, by_s = {}, {}
        for c, g in h_parts: by_h[c] = by_h.get(c, 0.0) + g.area
        for c, g in s_parts: by_s[c] = by_s.get(c, 0.0) + g.area
        rows.append(dict(geoid=geoid, name=cname, land=land_m2, faces_area=covered,
                         aland=float(counties.loc[geoid, "ALAND"]), **acc,
                         by_h=by_h, by_s=by_s, pairs=pair_differ,
                         scc_none=sum(g.area for g in s_none)))

    # ---- report ------------------------------------------------------------------
    def pct(x, tot): return 100.0 * x / tot
    print("\n" + "=" * 78)
    print("RESULTS (sq mi, EPSG:5070 planar areas; 1 sq mi = 2,589,988.110336 m^2)")
    print("=" * 78)
    for r in rows:
        T = r["land"]
        print(f"\n### {r['name']} County (GEOID {r['geoid']})")
        print(f"County land area (TIGER 2024 county minus AREAWATER): {sqmi(T):9.2f} sq mi"
              f"   [TIGER ALAND attribute: {sqmi(r['aland']):.2f} sq mi]")
        cats = [("Both layers name the SAME utility set", "agree"),
                ("DIFFERENT: no utility in common", "differ_disjoint"),
                ("DIFFERENT: sets overlap but not equal", "differ_partial"),
                ("No utility in SCC layer (HIFLD only)", "only_hifld"),
                ("No utility in HIFLD layer (SCC only)", "only_scc"),
                ("No utility in either layer", "neither")]
        s = 0.0
        for lab, k in cats:
            s += r[k]
            print(f"  {lab:<42} {sqmi(r[k]):9.2f} sq mi  {pct(r[k], T):6.2f}%")
        diff = r["differ_disjoint"] + r["differ_partial"]
        print(f"  {'-' * 42} {'-' * 9}")
        print(f"  {'Sum of categories':<42} {sqmi(s):9.2f} sq mi  {pct(s, T):6.2f}%"
              f"   (county land {sqmi(T):.2f}; residual {sqmi(T - s):+.4f})")
        print(f"  => NAMED UTILITY DIFFERS: {sqmi(r['differ_disjoint']):.2f} + {sqmi(r['differ_partial']):.2f}"
              f" = {sqmi(diff):.2f} sq mi = {pct(diff, T):.2f}% of land")
        print(f"  Overlap (>1 utility at a spot) - HIFLD: {sqmi(r['hifld_overlap']):.2f} sq mi;"
              f" SCC: {sqmi(r['scc_overlap']):.2f} sq mi")
        if r["scc_none"] > 0:
            print(f"  SCC polygons labelled Provider='none' within county land: {sqmi(r['scc_none']):.2f} sq mi")
        if r["pairs"]:
            print("  Differing area by (HIFLD set -> SCC set):")
            small = 0.0
            for (h, sc), a in sorted(r["pairs"].items(), key=lambda kv: -kv[1]):
                if sqmi(a) < SLIVER_SQMI:
                    small += a
                    continue
                print(f"     {h:<34} -> {sc:<18} {sqmi(a):8.2f} sq mi")
            print(f"     {'(combos each < %.2f sq mi, summed)' % SLIVER_SQMI:<56} {sqmi(small):8.2f} sq mi")
        for lab, d in (("HIFLD", r["by_h"]), ("SCC", r["by_s"])):
            tot = sum(d.values())
            print(f"  Area by utility, {lab} (overlaps counted once per utility):")
            for c, a in sorted(d.items(), key=lambda kv: -kv[1]):
                print(f"     {c:<10} {CANON.get(c, c)[:48]:<48} {sqmi(a):8.2f} sq mi {pct(a, T):6.2f}%")
            print(f"     {'sum':<59} {sqmi(tot):8.2f} sq mi {pct(tot, T):6.2f}%")

    print("\nUNMATCHED / FLAGGED NAMES (not guessed; kept under raw name):")
    if not unmatched:
        print("  none")
    for src, nm, extra in sorted(set(unmatched)):
        key = ("RAW-HIFLD:" if src.startswith("HIFLD") else "RAW-SCC:") + nm
        a = sum(r["by_h" if src.startswith("HIFLD") else "by_s"].get(key, 0.0) for r in rows)
        print(f"  {src}: {nm!r} ({extra}) -> area inside the four counties' land: {sqmi(a):.4f} sq mi")
    print("\nSources:")
    print(f"  HIFLD layer: {HIFLD_LAYER_URL} (item {HIFLD_ITEM_ID}); original {HIFLD_ORIGINAL_PAGE}")
    print(f"  SCC layer:   {SCC_LAYER_URL} (item {SCC_ITEM_ID}; web map {SCC_WEBMAP_ITEM_ID})")
    print(f"  Counties:    {TIGER_COUNTY_URL}")
    print(f"  Water:       {TIGER_AREAWATER_URL}")


if __name__ == "__main__":
    main()
