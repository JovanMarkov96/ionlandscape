# Evidence Map — 083-markus-greiner (Markus Greiner)

Verified: 2026-05-30

## Source list

1. **Greiner Lab personal page** (https://greiner.physics.harvard.edu/people/mgreiner.html): Full title, PhD year, PhD advisor, PhD institution, year joined Harvard (2005), postdoc at JILA (2003–2005).
2. **Harvard Physics Department profile** (https://www.physics.harvard.edu/people/facpages/greiner): Current position at Harvard, title.
3. **Simons Foundation profile** (https://www.simonsfoundation.org/people/markus-greiner/): Career timeline, postdoc with Deborah Jin at JILA, title "George Vasmer Leverett Professor of Physics".
4. **Wikipedia** (https://en.wikipedia.org/wiki/Markus_Greiner): PhD year/advisor/institution, awards, career history.
5. **OpenAlex** (https://openalex.org/A5027431609): Metrics (citation count, h_index, publication count), location geocode.
6. **CrossRef / journal pages**: DOI verification for all five key papers.

## Field-level evidence

### `current_position`
- **`title`**: "George Vasmer Leverett Professor of Physics"
  - *Source*: Simons Foundation profile, Harvard Physics Department profile, MPHQ profile.
- **`institution`**: Harvard University
  - *Source*: All sources agree.
- **`since_year`**: 2005
  - *Source*: Greiner Lab personal page states he joined Harvard as Assistant Professor in 2005. Promoted to full Professor in January 2012.

### `education[0]`
- **`degree`**: PhD (Physics), LMU Munich, 2003
  - *Source*: Greiner Lab personal page, Wikipedia, Simons Foundation.
- **`advisor`**: Theodor W. Hänsch (id: 000-theodor-w-hansch)
  - *Source*: Greiner Lab personal page (lists "T. Hänsch"), Wikipedia. Hänsch is Nobel laureate (2005) and is present in the database as 000-theodor-w-hansch.
- **`thesis`**: "Ultracold quantum gases in three-dimensional optical lattice potentials" (2003, LMU Munich)
  - *Source*: LMU eDOC repository (https://edoc.ub.uni-muenchen.de/968/); awarded DAMOP 2004 best thesis prize and William L. McMillan Award.

### `lineage_check`
- **`advisor_verified`**: true — Theodor W. Hänsch confirmed via Greiner Lab personal page and Wikipedia; present in DB as 000-theodor-w-hansch.
- **`postdoc_verified`**: true — Postdoctoral position (2003–2005) at JILA with Deborah Jin confirmed via Simons Foundation profile and Greiner Lab page.

### `platforms`
- **`neutral_atom`**: Core platform — ultracold atoms, optical lattices, quantum gas microscopes throughout career.

### `applications`
- **`simulation`**: Primary application — Mott insulator transition, Hubbard model, fermionic quantum simulation, many-body physics.

### `key_papers`

| # | Title | Year | DOI | Role | Rationale |
|---|-------|------|-----|------|-----------|
| 1 | Quantum phase transition from a superfluid to a Mott insulator in a gas of ultracold atoms | 2002 | 10.1038/415039a | first_author | Landmark paper; Greiner is first author; Nature 415, 39–44 |
| 2 | Collapse and revival of the matter wave field of a Bose–Einstein condensate | 2002 | 10.1038/nature00968 | first_author | Greiner first author; Nature 419, 51–54 |
| 3 | A quantum gas microscope for detecting single atoms in a Hubbard-regime optical lattice | 2009 | 10.1038/nature08482 | senior_author | Greiner is senior/corresponding author; Nature 462, 74–77 |
| 4 | Site-resolved imaging of a fermionic Mott insulator | 2016 | 10.1126/science.aad9041 | senior_author | Greiner is senior author; Science 351, 953 |
| 5 | Quantum thermalization through entanglement in an isolated many-body system | 2016 | 10.1126/science.aaf6725 | senior_author | Greiner is senior/corresponding author; Science 353, 794–800 |

### `links`
- **`group_page`**: https://greiner.physics.harvard.edu/ — official lab website.
- **`institution_profile`**: https://www.physics.harvard.edu/people/facpages/greiner — Harvard Physics Department.
- **`orcid`**: https://orcid.org/0000-0002-2935-2363 — from skeleton.
- **`openalex`**: https://openalex.org/A5027431609 — from skeleton.

## Data quality notes

- **`metrics`**: Kept from OpenAlex (2026-05-26 snapshot). OpenAlex h-index (57) is substantially lower than what Google Scholar would report for Greiner (~100+), because the 2002 Mott insulator paper alone has ~7000+ citations. Metrics source field correctly reflects openalex.
- **`since_year`**: Set to 2005 (year first joined Harvard faculty as Assistant Professor), consistent with the approach used for Bloch and others in the database.
- **`title`**: "George Vasmer Leverett Professor" is a named/endowed chair; this is Greiner's current title. He became full professor in 2012.
- **`advisor_id`**: 000-theodor-w-hansch — same advisor as Immanuel Bloch (081-immanuel-bloch), making Greiner and Bloch academic siblings who co-authored the landmark 2002 Mott insulator paper.
