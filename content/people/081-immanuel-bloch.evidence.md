# Evidence Map — 081-immanuel-bloch (Immanuel Bloch)

Verified: 2026-05-30

## Source list

1. **Wikipedia** (https://en.wikipedia.org/wiki/Immanuel_Bloch): PhD year, PhD advisor, career timeline, awards.
2. **LMU Quantum Optics Group profile** (https://www.quantum-munich.de/104554/bloch-immanuel-prof-dr): Current title, since year at LMU, Google Scholar link, research areas, MCQST spokesperson role.
3. **MPQ person page** (https://www.mpq.mpg.de/person/34641/4571983): Division name ("Quantum Many Body Systems"), Rydberg experiment groups (Sr Rydberg, Yb Rydberg).
4. **CrossRef / journal pages**: DOI verification for all six key papers.
5. **OpenAlex** (https://openalex.org/A5032954061): Metrics (citation count, h_index, publication count), location geocode.

## Field-level evidence

### `current_position`
- **`title`**: "Professor of Experimental Physics"
  - *Source*: LMU Quantum Optics Group profile; MPQ press release (2008 appointment as Scientific Director).
- **`institution`**: Ludwig-Maximilians-Universität München
  - *Source*: LMU profile, Wikipedia.
- **`since_year`**: 2009
  - *Source*: LMU profile states he was "full professor at the University of Mainz (2003–2009)" and returned to Munich in 2009.

### `education[0]`
- **`degree`**: PhD (Physics), LMU Munich, 2000
  - *Source*: Wikipedia.
- **`advisor`**: Theodor W. Hänsch (id: 000-theodor-w-hansch)
  - *Source*: Wikipedia. Hänsch is Nobel laureate (2005) and is in the database as 000-theodor-w-hansch.
- **`thesis`**: "Atomlaser und Phasenkohärenz atomarer Bose-Einstein-Kondensate" (2000)
  - *Source*: Wikipedia.

### `platforms`
- **`neutral_atom`**: Core platform — optical lattices, ultracold gases throughout career.
- **`rydberg_array`**: Added based on MPQ profile listing active "Strontium Rydberg Experiment" and "Ytterbium Rydberg" groups within Bloch's division.

### `applications`
- **`simulation`**: Primary application — Hubbard model, many-body physics, quantum gas microscopes.
- **`computing`**: Added due to Rydberg array groups and quantum information processing focus in division.

### `key_papers`

| # | Title | Year | DOI | Role | Rationale |
|---|-------|------|-----|------|-----------|
| 1 | Quantum phase transition from a superfluid to a Mott insulator | 2002 | 10.1038/415039a | co_author | Landmark paper; one of most cited cold-atom experiments |
| 2 | Many-body physics with ultracold gases (Rev. Mod. Phys.) | 2008 | 10.1103/RevModPhys.80.885 | co_author | Canonical review; 5845+ citations |
| 3 | Single-atom-resolved fluorescence imaging of an atomic Mott insulator | 2010 | 10.1038/nature09378 | co_author | Quantum gas microscope technique paper |
| 4 | Quantum simulations with ultracold quantum gases (Nature Physics) | 2012 | 10.1038/nphys2259 | co_author | Review of quantum simulation landscape |
| 5 | Light-cone-like spreading of correlations in a quantum many-body system | 2012 | 10.1038/nature10748 | senior_author | Lieb-Robinson bound experimental observation |
| 6 | Quantum simulations with ultracold atoms in optical lattices (Science) | 2017 | 10.1126/science.aal3837 | co_author | Review of quantum gas microscope + optical lattice simulations |

### `lineage_check`
- **`advisor_verified`**: true — Theodor W. Hänsch confirmed via Wikipedia; present in DB as 000-theodor-w-hansch.
- **`postdoc_verified`**: false — No postdoctoral position identified; Bloch appears to have moved directly from PhD to junior group leader at MPQ (Hänsch group).

### `links`
- **`google_scholar`**: https://scholar.google.com/citations?user=kX5_lc8AAAAJ — confirmed via LMU profile page.
- **`group_page`**: https://www.quantum-munich.de/104554/bloch-immanuel-prof-dr
- **`institution_profile`**: https://www.mpq.mpg.de/person/34641/4571983

## Data quality notes

- **`metrics`**: Kept from OpenAlex (2026-05-26 snapshot). Google Scholar shows ~87,000+ citations and h-index 118, substantially higher. Metrics source field correctly reflects openalex.
- **`postdocs`**: Not added — no postdoctoral stint identified; he was a junior group leader within Hänsch's group at MPQ directly after PhD.
- **`thesis.link`**: Not available online.
