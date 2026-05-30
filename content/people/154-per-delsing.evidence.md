# Evidence Map — Per Delsing (154-per-delsing)

Verified: 2026-05-26

---

## active: active

*   **`active`**: `active`
    *   *Source*: https://www.chalmers.se/en/persons/delsing/ — listed as Full Professor (not emeritus)
    *   *Source*: https://api.openalex.org/authors/A5073844805 — 340 works, continuous affiliation through 2026; recent publication March 2026 "Quantum Acoustics with Tunable Nonlinearity in the Superstrong Coupling Regime"
    *   *Note*: ORCID employment shows "Professor, Chalmers University of Technology" start 1997, no end date.

---

## current_position

*   **`current_position.title`**: `Full Professor in Quantum Technology, Microtechnology and Nanoscience`
    *   *Source*: https://www.chalmers.se/en/persons/delsing/ (page heading/title field)
    *   *Quote*: "Full Professor, Quantum Technology, Microtechnology and Nanoscience"
*   **`current_position.institution`**: `Chalmers University of Technology`
    *   *Source*: https://www.chalmers.se/en/persons/delsing/ — official Chalmers staff profile
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-1222-3506/employments — "Professor, Chalmers University of Technology, Department of Microtechnology and nanoscience, start 1997, ongoing"
*   **`current_position.confidence`**: `confirmed`
    *   *Rationale*: Title and institution read directly from official Chalmers staff directory page and confirmed by ORCID employment record.
*   **`current_position.verified_at`**: `2026-05-26`

---

## ORCID correction

*   The skeleton profile contained ORCID `0000-0001-1222-3506` (incorrect — 404 on ORCID).
*   Correct ORCID is `0000-0002-1222-3506`, confirmed by:
    *   https://pub.orcid.org/v3.0/0000-0002-1222-3506/personal-details — name "Per Delsing", profile created 2016-04-15
    *   https://api.openalex.org/authors/A5073844805 — OpenAlex links this author to orcid `0000-0002-1222-3506`
    *   https://www.chalmers.se/en/persons/delsing/ — Chalmers profile page references this ORCID

---

## links.openalex

*   **`links.openalex`**: `https://openalex.org/A5073844805`
    *   *Source*: https://api.openalex.org/authors?search=Per+Delsing — primary result: A5073844805, display_name "Per Delsing", institution Chalmers, works_count 340, h_index 55, cited_by_count 11701, affiliation from 1988–2026
    *   *Note*: A secondary record A5103291504 (2 works, created 2025) is a disambiguation stub and was not used.

---

## applications

*   **`applications`**: `[computing, simulation, sensing_metrology]`
    *   *Source (computing)*: https://www.chalmers.se/en/departments/mc2/research/quantum-technology/ — "quantum-processor design and technology, quantum computer software" as QTL research direction led by Delsing's group; WACQT quantum computer hardware
    *   *Source (simulation)*: https://doi.org/10.1126/science.1257219 — "Propagating phonons coupled to an artificial atom" (Science 2014) — quantum simulation of 1D phonon waveguide physics
    *   *Source (sensing_metrology)*: https://doi.org/10.1038/nature03375 — "Current measurement by real-time counting of single electrons" (Nature 2005) — high-precision single-electron counting; single-electron transistor work
    *   *Note*: Also works on quantum acoustics (SAW) and quantum thermodynamics, which map to fundamental_physics, but the three listed above are most directly output-facing.

---

## key_papers

*   **`key_papers[0]`**: "Observation of the dynamical Casimir effect in a superconducting circuit" (2011)
    *   *Source*: https://doi.org/10.1038/nature10561 — Nature 479, 376–379 (2011)
    *   *Note*: 952 citations (OpenAlex); Per Delsing is last/senior author (8th of 8); landmark demonstration of photon generation from vacuum fluctuations in a SC circuit.
*   **`key_papers[1]`**: "Propagating phonons coupled to an artificial atom" (2014)
    *   *Source*: https://doi.org/10.1126/science.1257219 — Science 346, 207–211 (2014)
    *   *Note*: 493 citations (OpenAlex); Per Delsing last author (6th of 6); founding paper of quantum acoustics with SC qubits.
*   **`key_papers[2]`**: "Demonstration of a Single-Photon Router in the Microwave Regime" (2011)
    *   *Source*: https://doi.org/10.1103/physrevlett.107.073601 — Phys. Rev. Lett. 107, 073601 (2011)
    *   *Note*: 471 citations (OpenAlex); Per Delsing last author (6th of 6); quantum optics with SC circuits.
*   **`key_papers[3]`**: "Current measurement by real-time counting of single electrons" (2005)
    *   *Source*: https://doi.org/10.1038/nature03375 — Nature 434, 361–364 (2005)
    *   *Note*: 234 citations (OpenAlex); Per Delsing last author (3rd of 3); metrological single-electron counting.
*   **`key_papers[4]`**: "The 2019 surface acoustic waves roadmap" (2019)
    *   *Source*: https://doi.org/10.1088/1361-6463/ab1b04 — J. Phys. D 52, 353001 (2019)
    *   *Note*: 391 citations (OpenAlex); Per Delsing first author (1st of 40+); field-defining SAW roadmap paper.

---

## education / postdocs

*   **`education[0].degree`**: `PhD (Physics)`
    *   *Source*: https://research.chalmers.se/en/person/delsing — Chalmers Research profile lists doctoral thesis from 1990.
    *   *Quote*: Doctoral thesis (1990): "Single electron tunneling in ultrasmall tunnel junctions"
*   **`education[0].institution`**: `Chalmers University of Technology`
    *   *Rationale*: Delsing's entire career is at Chalmers; earliest publications (1984–1990) are from the Department of Physics, Chalmers.
*   **`education[0].year`**: `1990`
    *   *Source*: https://research.chalmers.se/en/person/delsing
    *   *Consistency check*: ORCID employment starts 1991 as Assistant Professor (University of Gothenburg), consistent with PhD completion at Chalmers in 1990.
*   **`education[0].advisor`**: `Tord Claeson` (inferred, not confirmed)
    *   *Source*: https://research.chalmers.se/en/person/f4atc — Tord Claeson, Full Professor of Physics at Chalmers from 1982; research focus on superconducting tunneling and electron properties of solids.
    *   *Evidence*: Delsing and Claeson co-authored the foundational single-electron tunneling papers (Phys. Rev. B 42, 7439, 1990; Zeitschrift für Physik B 1989-1990) that correspond directly to the thesis topic. Claeson was the professor of the group in which Delsing did his PhD-era research. No source explicitly names Claeson as supervisor.
    *   *Confidence*: `inferred`
*   **`postdocs`**: Not populated.
    *   *Note*: No postdoc record found on ORCID, Chalmers page, or OpenAlex. Employment record goes directly from PhD to Assistant Professor 1991. Left unpopulated.

---

## lineage_check

*   **`lineage_check.advisor_verified`**: `false` — Tord Claeson is inferred from co-authorship and group membership at Chalmers in 1989-1990, but no source explicitly names him as PhD supervisor.
*   **`lineage_check.postdoc_verified`**: `false` — no postdoc record found in any authoritative source.
*   **`lineage_check.last_checked`**: `2026-05-26`

---

## metrics

*   **`metrics`**: h_index 55, citation_count 11701, publication_count 340
    *   *Source*: https://api.openalex.org/authors/A5073844805 — retrieved 2026-05-26

---

## verification_source_count: 5

Sources used:
1. https://www.chalmers.se/en/persons/delsing/ — official Chalmers staff profile (title, institution, active status)
2. https://pub.orcid.org/v3.0/0000-0002-1222-3506/employments — ORCID employment history (Professor start 1997, prior roles 1991–1997)
3. https://api.openalex.org/authors/A5073844805 — OpenAlex author record (metrics, affiliation, topics, ORCID confirmation)
4. https://www.chalmers.se/en/departments/mc2/research/quantum-technology/ — QTL page (group structure, research focus areas)
5. https://research.chalmers.se/en/person/delsing — Chalmers Research profile (doctoral thesis 1990, thesis title "Single electron tunneling in ultrasmall tunnel junctions")

Additional sources consulted (papers, DOIs):
- https://doi.org/10.1038/nature10561 (Nature 2011, dynamical Casimir effect)
- https://doi.org/10.1126/science.1257219 (Science 2014, quantum acoustics)
- https://doi.org/10.1103/physrevlett.107.073601 (PRL 2011, single-photon router)
- https://doi.org/10.1038/nature03375 (Nature 2005, single-electron counting)
- https://doi.org/10.1088/1361-6463/ab1b04 (J. Phys. D 2019, SAW roadmap)
