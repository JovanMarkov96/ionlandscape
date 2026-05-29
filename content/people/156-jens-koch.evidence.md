# Evidence Map — Jens Koch (156-jens-koch)

Prepared: 2026-05-26. All sources accessed on that date unless noted.

---

## current_position

*   **`current_position.title`**: "Professor of Physics and Astronomy"
    *   *Source*: https://physics.northwestern.edu/people/faculty/core-faculty/jens-koch.html (header of faculty profile)
    *   *Quote*: "Professor, Department of Physics and Astronomy, Northwestern University"

*   **`current_position.institution`**: "Northwestern University"
    *   *Source*: https://physics.northwestern.edu/people/faculty/core-faculty/jens-koch.html
    *   *Source*: https://orcid.org/0000-0002-5047-631X (employment record: "Professor, Physics and Astronomy, Northwestern University, Evanston, IL, US")

*   **`current_position.since_year`**: not recoverable
    *   The ORCID employment XML record shows the entry was created on 2016-08-02 but this is the ORCID record creation date, not necessarily the employment start date. The Northwestern faculty page does not state a hire year. Field left null.

*   **`current_position.confidence`**: confirmed
    *   Two independent sources (Northwestern faculty page + ORCID) agree on Professor title and Northwestern institution.

---

## education

*   **`education[0].degree`**: "PhD (Physics)"
*   **`education[0].institution`**: "Freie Universität Berlin"
*   **`education[0].year`**: 2006
    *   *Source*: https://physics.northwestern.edu/people/faculty/core-faculty/jens-koch.html (education section)
    *   *Quote*: "PhD, Freie Universität Berlin (Germany), 2006"

*   **`education[0].advisor`**: null
    *   Advisor name not stated on Northwestern faculty page or ORCID profile. FU Berlin thesis repository not accessible via public search. Field left null; institution and year are confirmed.

---

## postdocs

*   **`postdocs[0].institution`**: "Yale University"
*   **`postdocs[0].years`**: "2006–2009" (approximate; end year not confirmed from public sources)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1103/PhysRevA.76.042319
    *   *Evidence*: The transmon paper (PRA 2007) lists Koch as first author. The paper was produced in the Schoelkopf and Devoret groups at Yale. Koch received his PhD from FU Berlin in 2006; the Yale affiliation on this 2007 paper and subsequent papers through ~2009 (e.g., PRL 2009, DOI 10.1103/PhysRevLett.103.217004) indicates a Yale postdoc beginning in 2006. Northwestern employment is the only position on his ORCID record.

*   **`postdocs[0].advisor`**: "Robert Schoelkopf"
*   **`postdocs[0].advisor_id`**: 145-robert-schoelkopf
    *   *Source*: Transmon paper author list — Koch (first author), …, Devoret, Girvin, Schoelkopf (senior authors). Schoelkopf is listed as corresponding/last author; the Schoelkopf Lab (RSL) at Yale was the primary host group.
    *   *Note*: Michel Devoret (146-michel-devoret) was co-senior author and jointly supervised this work. The 2009 PRL paper (Koch, Manucharyan, Devoret, Glazman) also places Koch in the Devoret group. Schoelkopf named as primary advisor based on RSL being the host lab and Schoelkopf as last author on the transmon paper.

---

## key_papers

*   **`key_papers[0]`**: "Charge-insensitive qubit design derived from the Cooper pair box" (2007) — the transmon paper
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1103/PhysRevA.76.042319
    *   *Quote*: Authors — "J. Koch, Terri M. Yu, J. Gambetta, A. Houck, D. Schuster, J. Majer, A. Blais, M. Devoret, S. Girvin, R. Schoelkopf"; Journal: Physical Review A; Year: 2007; DOI: 10.1103/PhysRevA.76.042319; Citations: 2,921
    *   Role: first_author (Koch listed first; introduced the transmon qubit design)

*   **`key_papers[1]`**: "Charging effects in the inductively shunted Josephson junction" (2009)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1103/PhysRevLett.103.217004
    *   *Quote*: Authors — "J. Koch, V. Manucharyan, M. Devoret, L. Glazman"; Journal: Physical Review Letters; Year: 2009; DOI: 10.1103/PhysRevLett.103.217004; Citations: 106
    *   Role: co_author (first among four authors; theory paper with Devoret group)

*   **`key_papers[2]`**: "Time-reversal-symmetry breaking in circuit-QED-based photon lattices" (2010)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1103/PhysRevA.82.043811
    *   *Quote*: Authors — "J. Koch, A. Houck, K. L. Hur, Steven Girvin"; Journal: Physical Review A; Year: 2010; DOI: 10.1103/PhysRevA.82.043811; Citations: 303
    *   Role: first_author (Koch listed first; foundational circuit QED photon lattice theory paper)

*   **`key_papers[3]`**: "scqubits: a Python package for superconducting qubits" (2021)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.22331/q-2021-11-17-583
    *   *Quote*: Authors — "Peter Groszkowski, J. Koch"; Journal: Quantum; Year: 2021; DOI: 10.22331/q-2021-11-17-583; Citations: 94
    *   Role: senior_author (Koch is senior/corresponding author; open-source superconducting qubit simulation toolkit widely adopted by the community)

---

## applications

*   **`applications: [computing, simulation]`**
    *   computing: primary stated focus — "theory, simulation, and advancement of hardware for quantum computing and quantum simulation using superconducting circuits and microwave photons" (Koch group website https://sites.northwestern.edu/koch/research/)
    *   computing: Northwestern faculty page — "quantum information processing with solid-state devices"
    *   simulation: Koch group website explicitly lists "quantum simulation using interacting photons in circuit-QED arrays" as a research thrust; photon lattice paper (PRА 2010) targets quantum simulation of condensed matter models

---

## platforms

*   **`platforms: [superconducting]`**
    *   *Source*: https://physics.northwestern.edu/people/faculty/core-faculty/jens-koch.html — "superconducting circuits as tools for quantum computation and quantum optics"
    *   *Source*: https://sites.northwestern.edu/koch/research/ — "superconducting circuits and microwave photons"

---

## lineage_check

*   `advisor_verified: false` — PhD advisor at Freie Universität Berlin not recoverable from any accessible public source. FU Berlin thesis repository search returned no accessible result.
*   `postdoc_verified: true` — Yale postdoc confirmed via co-authorship record: Koch appears as first author on the transmon paper (PRA 2007) with Yale affiliation in the Schoelkopf and Devoret groups, following his 2006 FU Berlin PhD.

---

## Other notes

*   **APS Fellowship (2024)** — Source: https://physics.northwestern.edu/people/faculty/core-faculty/jens-koch.html
*   Metrics block retained from OpenAlex Wave-2 harvest but is unreliable (openalex_id A5135797348 returns only 1 work); metrics not updated in this pass as no reliable h-index/citation source was accessible. Google Scholar profile URL not confirmed.
