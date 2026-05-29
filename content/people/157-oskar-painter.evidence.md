# Evidence Map — Oskar Painter (157-oskar-painter)

Verified: 2026-05-26. Four authoritative sources consulted.

---

## `current_position.title`

*   **`current_position.title`**: "John G. Braun Professor of Applied Physics and Physics"
    *   *Source*: https://www.amazon.science/blog/amazon-announces-ocelot-quantum-chip (author bio section)
    *   *Quote*: "Oskar Painter is director of quantum hardware at Amazon Web Services and John G. Braun Professor of Applied Physics and Physics at Caltech."
    *   *Source (corroborating)*: https://www.amazon.science/author/oskar-painter (author bio)

## `current_position.confidence`

Set to `confirmed` — title confirmed verbatim from two independent Amazon Science pages.

## `affiliations[0]` — Amazon Web Services

*   **`affiliations[0].name`**: "Amazon Web Services"
*   **`affiliations[0].role`**: "Director of Quantum Hardware"
    *   *Source*: https://www.amazon.science/blog/amazon-announces-ocelot-quantum-chip (author bio, 2025-02-27)
    *   *Quote*: "Oskar Painter is director of quantum hardware at Amazon Web Services"
    *   *Source (corroborating)*: https://api.openalex.org/authors/A5108167374 — lists Amazon (US) as affiliation 2024-2025

## `platforms`

*   **`platforms`**: `[superconducting, photonic, cavity_qed_hybrid]`
    *   *Source*: https://painterlab.caltech.edu/research/ — research section describes "Superconducting quantum circuits," "Quantum optomechanics," "Nanophotonics and waveguide QED"
    *   *Source*: https://painterlab.caltech.edu — group subtitle "Quantum Photonics @ Caltech"

## `applications`

*   **`applications`**: `[computing, simulation, sensing_metrology, networking]`
    *   *Source*: https://painterlab.caltech.edu/research/ — "Quantum computing and communication," "Quantum simulation," "Optomechanical sensors for precision measurements," "Quantum networking"
    *   *Quote*: "Applications target quantum computing, quantum communication, and quantum metrology"

## `education`

*   **`education[0].institution`**: "California Institute of Technology" (inferred from OpenAlex affiliation start 1996; PhD at Caltech in Applied Physics is widely attributed but no direct primary-source CV was accessible)
    *   *Source*: https://api.openalex.org/authors/A5108167374 — affiliation 1996-2025 at Caltech
    *   *Note*: Advisor not confirmed from any authoritative source accessed. PhD year not confirmed. `confidence` set to `not_found`. Caltech thesis repository was inaccessible (ECONNREFUSED). This field should be re-verified using Caltech thesis catalog or a CV PDF.

## `key_papers`

All five papers confirmed as senior-author works from the Painter Lab publications page (https://painterlab.caltech.edu/publications/).

1.  **"Hardware-efficient quantum error correction using concatenated bosonic qubits"** (2025, Nature, vol. 638, pp. 92–93)
    *   *Source*: https://painterlab.caltech.edu/publications/ — listed as Putterman et al., Painter senior author
    *   DOI: 10.1038/s41586-025-08642-7

2.  **"Preserving Phase Coherence and Linearity in Cat Qubits with Exponential Bit-Flip Suppression"** (2025, Phys. Rev. X 15, 011070)
    *   *Source*: https://painterlab.caltech.edu/publications/ — listed as Putterman et al., Painter senior author

3.  **"Quantum entanglement between optical and microwave photonic qubits"** (2024, Phys. Rev. X 14, 031055)
    *   *Source*: https://painterlab.caltech.edu/publications/ — listed as Meesala et al., Painter senior author

4.  **"A scalable superconducting quantum simulator with long-range connectivity based on a photonic bandgap metamaterial"** (2023, Science 379, 278–283)
    *   *Source*: https://painterlab.caltech.edu/publications/ — listed as Zhang et al., Painter senior author

5.  **"Demonstrating a long-coherence dual-rail erasure qubit using tunable transmons"** (2024, Phys. Rev. X 14, 011051)
    *   *Source*: https://painterlab.caltech.edu/publications/ — listed as Levine et al., Painter senior author

## `metrics`

*   h_index: 80, citation_count: 30730, publication_count: 384
    *   *Source*: https://api.openalex.org/authors/A5108167374 — retrieved 2026-05-26

## Sources not accessed / gaps

*   **ORCID profile** (https://orcid.org/0000-0002-1581-9209) returned no parseable content — ORCID page rendered without data in fetch context.
*   **Caltech faculty profile** — multiple URL patterns attempted (pma.caltech.edu/people/..., caltech.edu/about/faculty/...) all returned 404.
*   **PhD advisor** — not confirmed from any accessible authoritative source. AcademicTree returned 403. Thesis library returned ECONNREFUSED.
*   **Postdoc history** — no postdoc positions found in accessible sources; field left empty.
