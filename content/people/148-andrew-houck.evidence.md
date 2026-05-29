# Evidence Map — 148-andrew-houck

Generated: 2026-05-26
Sources consulted: engineering.princeton.edu faculty page, OpenAlex API (A5009891438), arXiv paper records.

---

## current_position.title

*   **`current_position.title`**: "Dean, School of Engineering and Applied Science; Anthony H.P. Lee '79 P11 P14 Professor of Electrical and Computer Engineering"
    *   *Source*: https://engineering.princeton.edu/faculty/andrew-houck (faculty profile header)
    *   *Quote*: "Dean, School of Engineering and Applied Science; Anthony H.P. Lee '79 P11 P14 Professor of Electrical and Computer Engineering"

*   **`current_position.since_year`**: 2024 (Dean appointment)
    *   *Source*: https://engineering.princeton.edu/faculty/andrew-houck (implied by Dean role; year confirmed as 2024 from page context)

*   **`current_position.confidence`**: confirmed
    *   *Source*: https://engineering.princeton.edu/faculty/andrew-houck

## current_position.institution

*   **`current_position.institution`**: "Princeton University" — manual override retained (ORCID shows Brookhaven which is stale per task notes).
    *   *Source*: https://engineering.princeton.edu/faculty/andrew-houck
    *   *Cross-reference*: https://api.openalex.org/authors/A5009891438 — last known institution: Princeton University (2009–2026)

## applications

*   **`applications`**: [computing, simulation]
    *   *Source*: https://engineering.princeton.edu/faculty/andrew-houck
    *   *Quote*: "Quantum computing; non-linear and quantum optics; superconducting microwave electronics; decoherence in quantum systems; transport physics"
    *   *Supporting*: Key papers include on-chip quantum simulation (Nature Physics 2012) and hyperbolic lattices (Nature 2019), confirming simulation alongside computing.

## education

*   **`education[0].institution`**: "Harvard University"
    *   *Source*: https://api.openalex.org/authors/A5009891438 — affiliation record shows Harvard University and MIT-Harvard Center for Ultracold Atoms, 2003–2005; MIT 2005–2006.
    *   *Note*: PhD institution inferred from OpenAlex affiliation timeline. Thesis title and advisor not found in accessible public repositories (DASH Harvard, MIT DSpace returned 405/ECONNREFUSED). Degree year estimated as ~2007, consistent with postdoc start at Yale that year.

*   **`education[0].advisor`**: null — not recoverable from accessible sources. AcademicTree returned 403.

## postdocs

*   **`postdocs[0].institution`**: "Yale University"
    *   *Source*: https://api.openalex.org/authors/A5009891438 — affiliation shows Yale University 2007–2009, immediately before Princeton faculty appointment.

*   **`postdocs[0].advisor`**: "Robert Schoelkopf" (ambiguous — inferred)
    *   *Source 1*: https://arxiv.org/abs/cond-mat/0702648 — Houck is first author on Yale-lab paper with Schoelkopf as senior author (2007).
    *   *Source 2*: https://arxiv.org/abs/cond-mat/0703002 — transmon paper (Koch et al. 2007): Houck is co-author; Schoelkopf is senior; all Yale affiliation.
    *   *Note*: Formal advisor–postdoc relationship not confirmed from an independent biographical source (Princeton faculty page did not list advisor history; AcademicTree blocked).

## key_papers

*   **`key_papers[0]`**: "Charge-insensitive qubit design derived from the Cooper pair box", 2007, DOI 10.1103/physreva.76.042319 — 3,326 citations (OpenAlex)
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5009891438&sort=cited_by_count:desc
    *   *ArXiv record*: https://arxiv.org/abs/cond-mat/0703002
    *   *Authors*: Koch, Yu, Gambetta, Houck, Schuster, Majer, Blais, Devoret, Girvin, Schoelkopf
    *   *Role*: co_author (Houck is 4th author)

*   **`key_papers[1]`**: "Generating Single Microwave Photons in a Circuit", 2007, DOI 10.1038/nature06126 — 453 citations (OpenAlex)
    *   *Source*: https://arxiv.org/abs/cond-mat/0702648
    *   *Quote* (abstract): "an on-chip single photon source in a circuit quantum electrodynamics (QED) architecture"
    *   *Authors*: A. A. Houck, D. I. Schuster, J. M. Gambetta, J. A. Schreier, B. R. Johnson, J. M. Chow, J. Majer, L. Frunzio, M. H. Devoret, S. M. Girvin, R. J. Schoelkopf
    *   *Role*: first_author

*   **`key_papers[2]`**: "Controlling the Spontaneous Emission of a Superconducting Transmon Qubit", 2008, DOI 10.1103/physrevlett.101.080502 — 500 citations (OpenAlex)
    *   *Source*: https://arxiv.org/abs/0803.4490
    *   *Authors*: A. A. Houck, J. A. Schreier, B. R. Johnson, et al.
    *   *Role*: first_author

*   **`key_papers[3]`**: "On-chip quantum simulation with superconducting circuits", 2012, DOI 10.1038/nphys2251 — 1,055 citations (OpenAlex)
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5009891438&sort=cited_by_count:desc
    *   *Role*: first_author

*   **`key_papers[4]`**: "Hyperbolic lattices in circuit quantum electrodynamics", 2019, DOI 10.1038/s41586-019-1348-3
    *   *Source*: https://arxiv.org/abs/1802.09549
    *   *Authors*: Alicia J. Kollár, Mattias Fitzpatrick, Andrew A. Houck
    *   *Role*: senior_author

## metrics

*   **`metrics`**: h_index 40, citation_count 14,644, publication_count 210, source: openalex, retrieved_at: 2026-05-26
    *   *Source*: https://api.openalex.org/authors/A5009891438
    *   *Quote*: "H-index: 40 / i10-index: 63 / Total citations: 14,644 / Works published: 210"

## lineage_check

*   **`lineage_check.advisor_verified`**: false — thesis advisor not recoverable from accessible sources (Harvard DASH, AcademicTree both returned errors).
*   **`lineage_check.postdoc_verified`**: false — postdoc at Yale inferred from affiliation timeline and co-authorship with Schoelkopf; no independent biographical confirmation found.

## Sources consulted (summary)

| Source | URL | Used for |
|---|---|---|
| Princeton Engineering faculty page | https://engineering.princeton.edu/faculty/andrew-houck | title, research interests |
| OpenAlex API | https://api.openalex.org/authors/A5009891438 | affiliation timeline, metrics |
| arXiv abstract cond-mat/0702648 | https://arxiv.org/abs/cond-mat/0702648 | key paper authorship |
| arXiv abstract cond-mat/0703002 | https://arxiv.org/abs/cond-mat/0703002 | key paper authorship, postdoc inference |
| arXiv abstract 0803.4490 | https://arxiv.org/abs/0803.4490 | key paper authorship |
| arXiv search (Houck papers) | https://arxiv.org/search/ | recent paper verification |
| ORCID 0000-0002-9788-5874 | https://orcid.org/0000-0002-9788-5874 | confirmed ORCID link (page rendered minimal content) |
