# Profile Schemas

This document is the human-readable reference for the three Ion Landscape
profile schemas: **person**, **company**, and **institution**. Machine-
readable JSON Schemas live in `schemas/` and are the source of truth for
validation; this document is the source of truth for *intent*. When the two
disagree, fix this document and the schemas in the same commit.

| Entity type   | JSON Schema                              | Version |
|---------------|------------------------------------------|---------|
| Person        | `schemas/person.schema.json`             | v2      |
| Company       | `schemas/company.schema.json`            | v1      |
| Institution   | `schemas/institution.schema.json`        | v1      |
| Vocabularies  | `schemas/vocabularies.yaml`              | -       |

> **Note on v1/v2 transition.** The original `schemas/profile.schema.json`
> validated only people and is referenced by current CI. It remains in place
> until the Stage 2 migration script rewrites all entries to the new schemas
> and updates the validator to use them. During the transition, expect
> existing entries to *not* yet validate against the v2/v1 schemas described
> below — that is the migration's job.

---

## Shared conventions

These apply to all three entity types.

### Identifiers

```yaml
id: string  # see per-entity pattern below
schema_version: integer  # required, locks the schema this entry is written for
entity_type: "person" | "company" | "institution"
```

| Entity type   | `id` pattern              | Example                     |
|---------------|---------------------------|-----------------------------|
| Person        | `^\d{3}-[a-z0-9-]+$`      | `001-roee-ozeri`            |
| Company       | `^c\d{3}-[a-z0-9-]+$`     | `c001-quantum-art`          |
| Institution   | `^i\d{3}-[a-z0-9-]+$`     | `i058-quantum-hub`          |

The numeric portion is a zero-padded sequence and is permanent for the life
of the entry. When you add a new entry, take `max + 1` from the existing set.

### Location

Required for every entity:

```yaml
location:
  city: string
  region: string | null
  country: string
  lat: number | null   # WGS-84
  lon: number | null
```

### Provenance fields (all entities)

```yaml
last_verified_at: date           # ISO date of last manual/automated re-check
verification_source_count: int   # how many distinct authoritative sources back this entry
sources:                         # top-level fallback when per-field provenance isn't structurally possible
  - url: string
    note: string | null
```

Per-field source URLs are preferred where the schema permits (most arrays
of objects: education, postdocs, milestones, funding rounds, mous, etc.).
Use the top-level `sources` block for entries where field-level attribution
is impractical.

### Stub entries

Any entity may carry `stub: true` if it exists only to satisfy a graph
reference (e.g. an advisor mentioned by another profile but not yet
researched). Stubs have minimal fields populated and exist to keep the
relationship graph complete. They are visible in queries but flagged.

### Auto fields

```yaml
created_at: date
updated_at: date
```

The `directory` block on companies and institutions is also auto-populated
by `scripts/core/build_index.py` and should not be hand-edited (changes
will be overwritten on next build).

---

## Controlled vocabularies

The full vocabulary lives in `schemas/vocabularies.yaml`; the JSON schemas
inline the enum values. Summary of the five canonical axes used across
schemas:

### Platforms (12)

`trapped_ion`, `neutral_atom`, `rydberg_array`, `superconducting`,
`nv_center`, `color_center`, `photonic`, `trapped_molecule`, `topological`,
`silicon_spin`, `quantum_dot`, `cavity_qed_hybrid`.

### Applications (7)

`computing`, `simulation`, `networking`, `sensing_metrology`,
`optical_clocks`, `fundamental_physics`, `software_control`.

### Company modality (4)

`hardware`, `software`, `both`, `services`.

### Person activity (4)

`active`, `retired`, `deceased`, `unknown`.

### Institution type (8)

`university`, `national_lab`, `dedicated_quantum_centre`, `research_centre`,
`consortium`, `government_agency`, `industry_research_lab`, `non_profit`.

For company funding stages, office functions, edge types, national programs,
and networks: see `schemas/vocabularies.yaml` directly. National programs and
networks are kept as open lists (string, not enum) so they can grow without
schema bumps; we strongly recommend reusing the canonical ids in the YAML.

---

## Person schema (v2)

`schemas/person.schema.json` validates `content/people/*.md`.

### Required fields

```yaml
schema_version: 2
id: string              # NNN-slug
entity_type: person
name: string
location: { city, country, ... }
group_type: "experimental" | "theory" | "mixed"
platforms: [enum]       # may be empty for theorists
active: "active" | "retired" | "deceased" | "unknown"
```

### Conditional requirements

- If `group_type` is `experimental` or `mixed`, then `applications` must be
  a non-empty array.
- If `platforms` includes `trapped_ion`, then `ion_species` must be a
  non-empty array.

### Recommended fields

```yaml
sort_name: "Last, First"
current_position:
  institution: string
  title: string
  since_year: integer | null
applications: [enum]      # research-application axis (independent of platforms)
atomic_species: [string]  # when neutral_atom or rydberg_array
education:
  - degree: string
    institution: string
    year: integer
    advisor: string
    advisor_id: string | null     # NEW — link to person id when known
    confidence: enum
    source: uri
postdocs:
  - institution: string
    advisor: string
    advisor_id: string | null     # NEW
    years: string
    source: uri
thesis: { title, year, link, note }
links: { homepage, group_page, google_scholar, orcid, institution_profile, ... }
keywords: [string]                 # free-form; prefer applications + platforms
affiliations:
  - name: string
    role: string
    type: "company" | "institution" | "consultancy" | "advisory_board" | "editorial" | "other"
    entity_id: string | null       # NEW — c-prefixed company or i-prefixed institution
    source: uri
```

### Optional / enrichment fields

```yaml
key_papers:                # max 10 representative papers
  - title: string
    year: integer
    doi: string
    role: "first_author" | "senior_author" | "corresponding" | "co_author"
metrics:                   # populated by API enrichment in later stages
  h_index: integer
  citation_count: integer
  publication_count: integer
  source: "google_scholar" | "scopus" | "orcid_works" | "semantic_scholar"
  retrieved_at: date
lineage_check:
  advisor_verified: bool
  postdoc_verified: bool
  last_checked: date
```

### Notable changes from v1

- **`research_focus` removed** — replaced by `applications` (controlled
  vocabulary, allows >2 entries, shared across entity types).
- **`active`** changed from optional boolean to required enum.
- **`platforms`** is now a controlled vocabulary, not free-form strings.
- **`schema_version`, `entity_type`** added as required.
- **`atomic_species`** added (mirrors `ion_species` for neutral atoms).
- **`key_papers`, `metrics`, `lineage_check`** added as enrichment slots.
- **`advisor_id`, `entity_id`** added so cross-references are unambiguous
  in the relationship graph.
- **`last_verified_at`, `verification_source_count`** added (provenance).

---

## Company schema (v1)

`schemas/company.schema.json` validates `content/companies/*.md`.

### Required fields

```yaml
schema_version: 1
id: string                  # cNNN-slug
entity_type: company
name: string
location: { city, country, ... }   # HQ location
platforms: [enum]                  # for software-only, list the platforms it targets
modality: "hardware" | "software" | "both" | "services"
status:
  operating_status: "private" | "public" | "acquired" | "defunct" | "non_profit" | "stealth"
```

### Recommended fields

```yaml
sort_name: string
aliases: [string]
founded_year: integer
short_summary: string                  # >= 10 chars
applications: [enum]                   # what the technology is for
approach:
  elevator_pitch: string
  differentiators: [string]            # max 5
  architecture_tags: [string]
focus_areas: [string]
products:
  - name: string
    description: string
    stage: "concept" | "prototype" | "limited_release" | "ga" | "deprecated"
    release_date: date
    source: uri
  # OR a string for shorthand: products: ["Product Name"]
people:
  founders:
    - name: string
      role: string
      person_id: string | null   # NNN-slug, when in this repo
      source: uri
  leadership:
    - name: string
      role: string
      person_id: string | null
      source: uri
  spun_out_of:
    - name: string
      institution_id: string | null   # iNNN-slug
      spinout_year: integer
      source: uri
  headcount: integer | null
  headcount_source: uri
  headcount_retrieved_at: date
funding:
  total_raised_usd: number
  last_round_date: date
  rounds:
    - stage: enum   # see funding_stages in vocabularies.yaml
      round: string                 # free-form label, secondary to `stage`
      date: date
      amount_usd: number
      lead_investor: string
      lead_investors: [string]      # plural variant when multi-lead
      other_investors: [string]
      source: uri
      announcement_url: uri
offices:
  - location: { city, country, ... }
    function: "hq" | "r_and_d" | "manufacturing" | "sales_support" | "data_center"
    headcount: integer | null
    source: uri
milestones:
  - date: date
    claim: string
    source: uri
roadmap:
  - target_date: date
    target_claim: string
    source: uri               # required for roadmap entries (no speculation)
```

### Optional / enrichment fields

```yaml
partnerships:
  - name: string
    type: "technology" | "go_to_market" | "research" | "investor" | "customer" | "supply"
    source: uri
customers: [string]
patents:
  count: integer
  portfolio_url: uri
  retrieved_at: date
links: { website, careers, news, linkedin, wikipedia, ... }
media: { logo_path, hero_image_path }
```

### Status sub-fields

When `operating_status` is:
- `public`: populate `status.ticker` and `status.ipo_date`.
- `acquired`: populate `status.acquired` block (acquirer, date, type, deal value, announcement URL).
- `defunct`: populate `status.defunct_date`.

---

## Institution schema (v1)

`schemas/institution.schema.json` validates `content/institutions/*.md`.

### Required fields

```yaml
schema_version: 1
id: string                  # iNNN-slug
entity_type: institution
name: string
location: { city, country, ... }
institution_type: "university" | "national_lab" | "dedicated_quantum_centre"
                | "research_centre" | "consortium" | "government_agency"
                | "industry_research_lab" | "non_profit"
```

### Recommended fields

```yaml
sort_name: string
aliases: [string]
abbreviations: [string]
short_description: string
is_dedicated_quantum_centre: bool   # true even for university sub-centres
platforms_represented: [enum]
applications_represented: [enum]
focus_areas: [string]               # free-form; prefer applications_represented when known
group_count: integer | null
leadership:
  - name: string
    role: string                    # e.g. "Director, Quantum Initiative"
    person_id: string | null
    source: uri
national_programs: [string]         # see vocabularies.yaml; open list
networks: [string]                  # see vocabularies.yaml; open list
mous:
  - date: date
    partner: string
    summary: string
    source: uri
news:
  - date: date
    headline: string
    summary: string
    source: uri
links: { website, department, quantum_program, quantum_center, wikipedia, linkedin }
```

### Auto-populated

```yaml
directory:
  current_members: [filename]
  alumni: [filename]
  company_spinouts: [filename]
  member_count: integer
  alumni_count: integer
```

The `directory` block is rebuilt by `scripts/core/build_index.py` from
person and company affiliations. Hand edits will be overwritten.

---

## Authoritative sources, by entity type

This is the trust hierarchy used during ingestion (`docs/guides/ingestion.md`
covers the workflow).

### People

1. Official group / lab websites
2. Official university faculty pages
3. CV PDFs hosted on institutional domains
4. ORCID profiles (for self-asserted bibliography)
5. Published papers (for advisor confirmation)
6. AcademicTree Physics (lead, not final authority)

### Companies

1. Official corporate website (About / Team / Investor pages)
2. SEC filings (for public companies)
3. Official press releases
4. Government press releases (for grants and contracts)
5. Reputable trade press (Quantum Computing Report, IQT News, Nature News)
6. Tracxn / Crunchbase / Pitchbook (secondary; verify against primary)
7. LinkedIn (for current leadership; verify employment dates against primary)

### Institutions

1. Official institution website (quantum centre / department / strategy pages)
2. Government program pages (BMBF, NSF, EPSRC, EU Quantum Flagship, …)
3. Annual reports and strategic plans
4. Press releases for MoUs, building openings, major grants
5. Wikipedia (orientation only — never as a sole source)

### Never as a sole source

- Wikipedia
- Personal blogs and Twitter/X
- LinkedIn (for non-employment claims)
- Unverified user-submitted databases (AcademicTree for non-physics, …)

---

## Cross-references and the relationship graph

When you populate any field that names another entity in this repo
(advisor, founder, current institution, acquirer, spinout origin), populate
the corresponding `*_id` field with the canonical id. The Stage 6
relationship-graph build step ingests these ids and emits an edge dataset.
Free-form name strings remain (for display), but the ids are what the
graph queries against.

Edge types emitted:

`advised`, `postdoc_with`, `cofounded`, `affiliated_with`, `alumnus_of`,
`spun_out_of`, `acquired_by`, `current_member_of`.

See `schemas/vocabularies.yaml` for the canonical id list and notes.

---

## Questions?

- For the workflow itself, see [guides/ingestion.md](guides/ingestion.md).
- For a worked example, see [guides/example-workflow.md](guides/example-workflow.md).
- For the controlled vocabulary master list, see
  [`schemas/vocabularies.yaml`](../schemas/vocabularies.yaml).
