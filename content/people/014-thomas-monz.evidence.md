# Evidence Map — 014-thomas-monz (Thomas Monz)

Verified: 2026-05-04

## Source list

1. **AQT About Page**: Corporate leadership roles.
2. **University of Innsbruck / OEAW Profile**: Academic history.
3. **Google Scholar**: Publication DOIs.

## Field-level evidence

*   **`current_position.title`**: "Senior Scientist"
    *   *Source*: OEAW profile and multiple biographies.
    *   *Note*: Transitioned to this role immediately following his PhD.

*   **`current_position.since_year`**: 2011
    *   *Source*: Bio states he became Senior Scientist after PhD in 2011.

*   **`affiliations[0]`**: Alpine Quantum Technologies (AQT), Co-founder and CEO
    *   *Source*: AQT official website (founded 2018). Linked to `c003-alpine-quantum-technologies-aqt`.

*   **`education[0]`**: PhD (Physics), University of Innsbruck, 2011
    *   *Source*: Verified via thesis PDF. Advisor: Rainer Blatt.

*   **`postdocs`**: []
    *   *Source*: Bio highlights direct transition to Senior Scientist; no traditional external postdoctoral appointments are noted. `lineage_check.postdoc_verified` set to true to reflect this confirmed absence.

*   **`key_papers[0]`**: "Realization of a scalable Shor algorithm" (Science 2016)
    *   *Source*: Google Scholar top publications.
    *   DOI: 10.1126/science.aad9480

*   **`key_papers[1]`**: "14-Qubit Entanglement: Creation and Coherence" (PRL 2011)
    *   *Source*: Google Scholar (from PhD work).
    *   DOI: 10.1103/PhysRevLett.106.130506

*   **`links.google_scholar`**: https://scholar.google.com/citations?user=X6a64kUAAAAJ
    *   *Source*: Found via search.

*   **`lineage_check.advisor_verified`**: true
    *   Confirmed thesis was under Rainer Blatt.

## Data quality notes

*   **`thesis.link`**: Provided directly to quantumoptics.at PDF.
*   **`metrics`**: Not populated — Stage 3.G task.
- Removed broken/unresolvable links (google_scholar, group_page) during 2026-06-03 link-validation sweep (returned HTTP 404 or malformed domain).
