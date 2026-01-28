# Profile Schema Documentation

This document defines the allowed YAML frontmatter fields for Ion Landscape profiles.

## Field Categories

Fields are categorized by:
- **Required**: Must be present in every profile
- **Recommended**: Should be included when available
- **Optional**: Include only if verified from authoritative sources
- **Auto-generated**: Set automatically by tools

## Complete Schema

### Identity (Required)

```yaml
id: string  # Format: "NNN-slug" (e.g., "016-jonathan-home")
name: string  # Full name as commonly used (e.g., "Jonathan P. Home")
sort_name: string  # For alphabetical sorting (e.g., "Home, Jonathan P.")
```

### Current Position (Required)

```yaml
current_position:
  institution: string  # Current primary affiliation
  title: string  # Academic title (e.g., "Professor", "Assistant Professor")
```

### Location (Required)

```yaml
location:
  city: string  # City name
  country: string  # Country name
  region: string | null  # State/province/canton (optional)
  lat: float | null  # Latitude (decimal degrees)
  lon: float | null  # Longitude (decimal degrees)
```

**Coordinates:** Should be verified from reliable geocoding. Can be `null` if not yet determined.

### Classification (Required)

```yaml
group_type: "experimental" | "theory"
labels: array<string>  # Should match group_type: ["Experimental group"] or ["Theory group"]
```

**Rules:**
- Experimental: Has lab infrastructure, hardware, measurements
- Theory: Analytical/numerical work, no lab infrastructure

### Platforms (Recommended)

```yaml
platforms: array<string>
```

**Common values:**
- "Trapped ions"
- "Neutral atoms"
- "Superconducting qubits"
- "Photonics"
- "NV centers"

**Rules:**
- Use standard names consistently
- Based on actual research work
- Can have multiple platforms

### Education (Recommended)

```yaml
education: array<object>
```

**Structure for each degree:**

```yaml
- degree: string  # Format: "PhD (Physics)", "MSc (Physics)", "BSc (Physics)"
  institution: string | null
  year: int | null  # Four-digit year
  advisor: string | null  # Full name of PhD/MSc advisor
  confidence: "confirmed" | "academictree_only" | "not_found" | "ambiguous" | null
  note: string | null  # Explanation of verification status
```

**Confidence levels:**
- `confirmed`: Verified from official university records, thesis, or faculty page
- `academictree_only`: Found only on AcademicTree (not independently verified)
- `not_found`: Attempted verification but information not publicly available
- `ambiguous`: Multiple conflicting sources

**PhD-specific rules:**
- Only add advisor if verified from authoritative source
- Acceptable sources: thesis PDF, university records, official CV, faculty bio
- AcademicTree alone is NOT sufficient for "confirmed" status
- If uncertain, use appropriate confidence level and add note

### Postdocs (Optional)

```yaml
postdocs: array<object>
```

**Structure:**

```yaml
- advisor: string  # Full name of postdoc advisor/host
  institution: string
  year: int | null  # Start year or approximate year
```

**Rules:**
- Only add if verified from CV, bio, or official records
- If timeline unclear, year can be `null`

### Thesis (Optional, high bar)

```yaml
thesis:
  title: string | null
  year: int | null
  link: string | null  # Direct link to PDF or repository entry
  note: string | null  # Explanation if title/link not found
```

**Acceptable sources:**
- Institutional repositories (ORA, DSpace, etc.)
- ProQuest
- WorldCat
- Direct links from faculty pages

**If not found:**
```yaml
thesis:
  title: null
  year: null
  link: null
  note: "Thesis not found in public repositories; may be available via library request"
```

### Research Focus (Optional)

```yaml
research_focus: array<string>  # Maximum 2 items
```

**Allowed values:**
- `quantum_computing`
- `quantum_simulation`
- `optical_clocks`
- `metrology`
- `quantum_networking`
- `quantum_logic_spectroscopy`
- `other`

**Rules:**
- Assign ONLY if clearly stated on group website or in multiple papers
- Choose dominant focus areas (max 2)
- If uncertain or truly mixed, use `other`
- Do not guess based on single paper

### Ion Species (Optional, very high bar)

```yaml
ion_species: array<string>
```

**Format examples:**
- `Ca+`
- `Yb+`
- `Sr+`
- `Ba+`
- `Be+`

**Rules:**
- Only add if EXPLICITLY stated on:
  - Group website
  - Thesis abstract/introduction
  - Multiple experimental papers
- Must be current or recent work
- Do NOT infer from old papers
- If uncertain, leave empty

### Keywords (Optional)

```yaml
keywords: array<string>
```

**Examples:**
- "trapped-ion quantum computing"
- "quantum metrology"
- "optical clocks"
- "quantum error correction"
- "quantum simulation"

**Rules:**
- Use lowercase
- Hyphenate compound terms consistently
- Based on actual research themes
- Avoid generic terms

### Links (Recommended)

```yaml
links:
  homepage: string | null  # Personal or group website
  group_page: string | null  # University group page
  google_scholar: string | null  # Full Google Scholar profile URL
  orcid: string | null  # Full ORCID URL (https://orcid.org/0000-...)
  institution_profile: string | null  # University faculty profile
  # Other domain-specific links as needed
```

**Rules:**
- URLs must be complete (include https://)
- Verify links are active before adding
- Use official/authoritative pages only
- ORCID format: `https://orcid.org/0000-XXXX-XXXX-XXXX`

### Affiliations (Optional)

```yaml
affiliations: array<object>
```

**Structure:**

```yaml
- name: string  # Company or organization name
  role: string  # E.g., "Founder", "CTO", "Scientific Advisor"
  type: "company" | "nonprofit" | "government" | "other"
```

**Rules:**
- Only add if publicly disclosed
- Verify from company website or LinkedIn
- Include startups, consultancies, advisory roles

### Activity Status (Optional)

```yaml
active: boolean
```

**Definition:**
- `true`: Recent publications (last ~5 years) OR active group page OR recent news
- `false`: No recent activity, retired, or passed away

**Rules:**
- Check Google Scholar for recent papers
- Check group website for recent updates
- If uncertain, omit field (defaults to assumed active)

### Timestamps (Auto-generated)

```yaml
created_at: string  # Format: "YYYY-MM-DD"
updated_at: string  # Format: "YYYY-MM-DD"
```

**Rules:**
- Set automatically by creation/update tools
- Updated whenever frontmatter changes
- ISO 8601 date format

## Read-Only Fields

These fields exist but should NOT be modified by ingestion tools:

- **Content body**: Prose biography below frontmatter
- **Custom fields**: Any domain-specific fields not listed above

## Null vs. Empty Array vs. Omitted

**Use `null` for:**
- Single-value fields where information is not available
- Example: `advisor: null`

**Use empty array `[]` for:**
- Array fields when explicitly known to be empty
- Example: `postdocs: []` (no postdoc positions)

**Omit field entirely when:**
- Optional field has no data
- Haven't attempted verification yet

## Validation Rules

Profiles should validate against these rules:

1. **Required fields present**: id, name, current_position, location, group_type
2. **Type correctness**: Strings are strings, ints are ints, etc.
3. **Enum values**: group_type, confidence, research_focus use allowed values
4. **Coordinate ranges**: lat ∈ [-90, 90], lon ∈ [-180, 180]
5. **Year reasonability**: 1950 ≤ year ≤ current_year + 1
6. **URL format**: Links start with http:// or https://
7. **Label consistency**: labels match group_type
8. **Research focus limit**: Maximum 2 items

## Example Valid Profile

```yaml
---
id: 016-jonathan-home
name: Jonathan P. Home
sort_name: Home, Jonathan P.
current_position:
  institution: ETH Zürich
  title: Full Professor
location:
  city: Zürich
  country: Switzerland
  region: Zürich
  lat: 47.4083
  lon: 8.5072
group_type: experimental
labels:
  - Experimental group
platforms:
  - Trapped ions
education:
  - degree: PhD (Physics)
    institution: University of Oxford
    year: 2006
    advisor: Andrew Steane
    confidence: confirmed
    note: null
postdocs: []
affiliations: []
research_focus:
  - quantum_computing
  - quantum_error_correction
keywords:
  - trapped-ion quantum computing
  - quantum error correction
  - integrated ion traps
ion_species:
  - Ca+
links:
  homepage: https://iqe.phys.ethz.ch/...
  group_page: https://www.phys.ethz.ch/.../jhome.html
  google_scholar: https://scholar.google.com/citations?user=...
  orcid: https://orcid.org/0000-0002-4093-1550
thesis:
  title: "High Fidelity Operations for Quantum Information Processing"
  year: 2006
  link: https://ora.ox.ac.uk/objects/uuid:...
  note: null
active: true
created_at: '2026-01-26'
updated_at: '2026-01-28'
---

Jonathan P. Home is a professor at ETH Zürich...
```

## Field Addition Policy

**Can you add new fields?**

- ✅ Yes, if documented and justified
- ✅ Must be added to this schema documentation
- ✅ Should be optional unless truly universal
- ❌ Do not create duplicate or overlapping fields
- ❌ Do not add fields for single-profile use cases

**Process for adding new fields:**

1. Discuss in issue or PR
2. Update this schema documentation
3. Update validation scripts
4. Add to multiple profiles consistently
5. Update build script if needed

## Sources and Verification

Every non-obvious fact should be backed by a source:

**Document sources by:**
1. Adding `note` field with source citation
2. Including source URLs in commit message
3. Creating source tracking file in `scripts/logs/`

**Source hierarchy (most to least authoritative):**
1. Official university pages
2. Institutional repositories
3. ORCID (for self-reported data)
4. CV PDFs on institutional domains
5. Google Scholar (for activity only)
6. AcademicTree (lead, not confirmation)

**Never use as sole source:**
- Wikipedia
- Personal blogs
- Social media
- Unverified user-submitted databases

## Questions?

See [INGESTION_GUIDE.md](INGESTION_GUIDE.md) for workflow documentation.
See [QUICKSTART.md](QUICKSTART.md) for practical examples.
