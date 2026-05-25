# scripts/enrich/

Deterministic, API-driven enrichment scripts. Each script runs over the full
corpus (or a single entity with `--person / --company / --institution`), hits
a structured API, and writes results back to the relevant frontmatter fields.

**These are not LLM agent jobs.** They fill fields that a structured API
returns as JSON — no judgment, no web-page reading. Run them on a cadence to
keep the data fresh. See `private/GAME_PLAN.md §1` for the full rationale.

---

## metrics.py — Bibliometric snapshot from OpenAlex

Fills the `metrics{}` block on every person profile that has an ORCID link.

### What it fills

```yaml
metrics:
  h_index: 44
  citation_count: 9311
  publication_count: 219
  source: openalex
  retrieved_at: '2026-05-25'
```

These fields live in `content/people/<id>.md` under the `metrics:` key. The
JSON schema (`schemas/person.schema.json`) validates them.

### Source

[OpenAlex](https://openalex.org/) — free, no API key required. Author records
are looked up by ORCID:

```
GET https://api.openalex.org/authors/https://orcid.org/<orcid>
    ?mailto=ozerilab@weizmann.ac.il
```

Returns `summary_stats.h_index`, `cited_by_count`, and `works_count`. The
contact email puts requests into the OpenAlex "polite pool" (~10 req/s).

### How to run

```bash
# Full pass — enriches every person with an ORCID whose metrics are stale
python scripts/enrich/metrics.py

# Single person (useful for testing or spot-checks)
python scripts/enrich/metrics.py --person 001-roee-ozeri

# Preview without writing any files
python scripts/enrich/metrics.py --dry-run

# Force re-fetch even for entries that are still within the freshness window
python scripts/enrich/metrics.py --force

# Combine flags
python scripts/enrich/metrics.py --force --person 004-christopher-monroe --dry-run
```

### Freshness window

**90 days.** An entry is skipped if `metrics.source == "openalex"` and
`metrics.retrieved_at` is less than 90 days ago. Use `--force` to override.

### Cache

Results are cached in `scripts/utils/metrics_cache.json`, keyed by bare ORCID
(`0000-0001-7843-8801`, etc.). Re-runs within the freshness window make
**zero network calls** and complete in under a second.

To force a full re-fetch from the network (not just recopy from cache):
delete `scripts/utils/metrics_cache.json`, then run with `--force`.

### Output

- **Modified files:** `content/people/<id>.md` for each updated person (only
  the `metrics:` block changes; everything else is untouched).
- **Report:** `reports/metrics_report.md` — a table of every updated person
  (new values) plus two appendices: OpenAlex misses (have ORCID, no record)
  and no-ORCID entries. Read this after each run.
- **Cache:** `scripts/utils/metrics_cache.json` — auto-updated.

### Current coverage (as of 2026-05-25)

| Status | Count | Notes |
|---|---|---|
| Updated / has metrics | 44 | All with ORCIDs that OpenAlex resolved |
| OpenAlex miss | 9 | Have ORCID but no OpenAlex record; listed in report |
| No ORCID | 115 | Metrics cannot be auto-filled; add ORCID to profile to fix |

The 9 OpenAlex misses include: Häffner, Drewsen, Köhl, R. C. Thompson,
Patrick Gill, Paul Barclay, Matthias Keller, Brian McMahon, Daniel Rodríguez
Rubiales. For these, metrics must be filled manually or via Semantic Scholar.

### Validation

After running, verify profiles still pass schema validation:

```bash
python scripts/validation/validate_profiles.py --people
# Expected: 168 files, 0 failed
```

### Recommended cadence

Re-run every **90 days** (the freshness window). h-indices and citation counts
drift slowly; a quarterly pass keeps the data current without hammering the API.

---

---

## geocode.py — Location precision tiers + coordinate inheritance

Stamps `location.precision` on every entity that has coordinates, inherits
institution coordinates for people who lack their own, and geocodes any entity
with a known city but no lat/lon via Nominatim.

### What it fills

```yaml
location:
  city: College Park
  country: United States
  lat: 38.9897
  lon: -76.9402
  precision: city          # building | campus | city | inherited | none
  geocode_source: nominatim
  geocoded_at: '2026-05-25'
```

### Precision tiers

| Tier | Meaning |
|---|---|
| `building` | Exact street address geocoded |
| `campus` | Department/lab building (future campus-level pass) |
| `city` | City centroid — the current default for most entities |
| `inherited` | Person with no own location; copied from their institution |
| `none` | Nothing known; entity stays off the map |

### How to run

```bash
python scripts/enrich/geocode.py           # full pass (safe to re-run)
python scripts/enrich/geocode.py --dry-run  # preview without writing files
python scripts/enrich/geocode.py --force    # re-geocode even cached entries
```

### Cache

`scripts/utils/geocode_cache.json` — keyed by `"city||country"`. Nominatim
requires 1 req/s; the cache makes re-runs free. Never downgrades a higher
precision tier with a lower one.

### Report

`reports/geocode_report.md` — lists geocoded entries, inherited people, misses,
and off-map entities (no location data).

### Current coverage (2026-05-25)

- **144** entities stamped with `precision: city`
- **2** people got coordinates via institution inheritance
- **1** institution geocoded (IonQ Inc., College Park MD)
- **87** stubs / lineage-only people have no location data and stay off the map

### What this script does NOT do (future pass)

Campus-level address upgrades (institution → `precision: campus`) require
finding the physics dept / lab building address per institution from their own
website. That is a separate research pass tracked in `private/todo/04-geocoding.md`.

---

## Future scripts planned for this directory

| Script | Status | Purpose |
|---|---|---|
| `freshness_report.py` | planned | Scan all entities, emit staleness queue sorted by `last_verified_at` |
