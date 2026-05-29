# Evidence Map — K. W. Lehnert (152-k-w-lehnert)

Prepared: 2026-05-26. All sources accessed on that date.

---

## current_position

*   **`current_position.title`**: "Eugene Higgins Professor of Physics"
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert (faculty profile header)
    *   *Quote*: "Eugene Higgins Professor of Physics"

*   **`current_position.institution`**: "Yale University"
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert (faculty profile)
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-0750-9649/record (ORCID employment record — "Professor, Yale University Physics Department, 2024–present")

*   **`current_position.since_year`**: 2024
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-0750-9649/record
    *   *Quote*: "Professor of Physics at Yale University (effective July 1, 2024)"

*   **`current_position.confidence`**: confirmed
    *   Yale Physics faculty page and ORCID employment section independently confirm position and start year.

*   **Note on previous institution**: Lehnert was at JILA / University of Colorado Boulder from 2003 (joined as Associate Fellow) until mid-2024 (served as JILA Chair 2022–2024). OpenAlex retains the Boulder affiliation which is now stale. ORCID and Yale faculty page are the authoritative current sources.

---

## education

*   **`education[0].degree`**: "PhD (Physics)"
*   **`education[0].institution`**: "University of California, Santa Barbara"
*   **`education[0].year`**: 1999
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert (biography section)
    *   *Quote*: "Lehnert earned his Ph.D. in 1999 from UC Santa Barbara"
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-0750-9649/record (education section confirms UCSB)

*   **`education[0].advisor`**: null
    *   Advisor name not stated on Yale faculty page or ORCID record. ProQuest thesis access returned redirect loops. A 2000 Applied Physics Letters paper (DOI 10.1063/1.125706) lists Lehnert in the UCSB Physics Department alongside E. G. Gwinn and S. J. Allen, but co-authorship alone is insufficient to confirm advisor relationship. Field left null.

---

## postdocs

*   **`postdocs[0].institution`**: "Yale University"
*   **`postdocs[0].advisor`**: "Robert Schoelkopf"
*   **`postdocs[0].advisor_id`**: 145-robert-schoelkopf
*   **`postdocs[0].years`**: "1999–2003"
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert (biography section)
    *   *Quote*: "served as a postdoctoral researcher at Yale (1999-2003) collaborating with Robert Schoelkopf on superconducting circuit qubits"
    *   Schoelkopf confirmed at Yale from 1998 onward (see 145-robert-schoelkopf.md).

---

## career timeline (not in schema — for reference)

*   2003: Joined JILA as Associate Fellow
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert
*   2007: Promoted to JILA Fellow
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert
*   2022–2024: JILA Chair
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert
*   July 2024: Joined Yale as Eugene Higgins Professor of Physics
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-0750-9649/record

---

## applications

*   **`applications: [computing, sensing_metrology]`**
    *   *computing*: HAYSTAC collaboration uses squeezed states in microwave cavities — quantum-enhanced measurement for quantum information science; Lehnert lab description mentions "Analog Quantum Circuits" and "Quantum Transduction" enabling quantum networks (campuspress.yale.edu/lehnertlab/)
    *   *sensing_metrology*: primary stated focus — "Quantum-Enhanced Sensing of Fundamental Phenomena"; HAYSTAC axion searches (Nature 2021, DOI 10.1038/s41586-021-03249-z); squeezed vacuum for dark matter search (PRX 2019, DOI 10.1103/PhysRevX.9.021023)
    *   *Source*: https://campuspress.yale.edu/lehnertlab/ (five research themes listed)
    *   *Source*: https://www.colorado.edu/physics/konrad-lehnert (CU Boulder profile: "implementing quantum-limited measurements in astrophysics and condensed matter experiments")

---

## platforms

*   **`platforms: [superconducting]`**
    *   *Source*: https://campuspress.yale.edu/lehnertlab/ — "Analog Quantum Circuits", "Quantum Acoustics" using superconducting circuits and Josephson parametric amplifiers
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert — "Microwave quantum circuits; Mesoscopic electronics; Quantum nanomechanics"

---

## key_papers

*   **`key_papers[0]`**: "A quantum-enhanced search for dark matter axions" (2021)
    *   *Source*: arXiv:2008.01853; Nature 591, 333–337 (2021)
    *   DOI: 10.1038/s41586-021-03249-z
    *   *Note*: HAYSTAC experiment; uses vacuum squeezing to double axion search rate — flagship sensing/metrology paper.

*   **`key_papers[1]`**: "Optomechanical Ground-State Cooling in a Continuous and Efficient Electro-Optic Transducer" (2022)
    *   *Source*: arXiv:2112.13429; Physical Review X 12, 021062 (2022)
    *   DOI: 10.1103/PhysRevX.12.021062
    *   *Note*: Demonstrates quantum transduction between microwave and optical domains with 47% efficiency and 3.2-photon added noise.

*   **`key_papers[2]`**: "Nonclassical energy squeezing of a macroscopic mechanical oscillator" (2020)
    *   *Source*: arXiv:2005.04260; Nature Physics 16, 915–920 (2020)
    *   DOI: 10.1038/s41567-020-0929-9
    *   *Note*: Creates sub-Poissonian phonon-number states in a macroscopic oscillator using quadratic coupling.

*   **`key_papers[3]`**: "Squeezed vacuum used to accelerate the search for a weak classical signal" (2019)
    *   *Source*: arXiv:1809.06470; Physical Review X 9, 021023 (2019)
    *   DOI: 10.1103/PhysRevX.9.021023
    *   *Note*: Demonstrates 2.12× scan rate enhancement using squeezed microwave states — precursor to HAYSTAC quantum enhancement.

*   **`key_papers[4]`**: "Widely tunable on-chip microwave circulator for superconducting quantum circuits" (2017)
    *   *Source*: arXiv:1707.04565; Physical Review X 7, 041043 (2017)
    *   DOI: 10.1103/PhysRevX.7.041043
    *   *Note*: On-chip circulator with >20 dB isolation and GHz-wide tunable operation — core enabling technology for SC quantum circuits.

---

## keywords

*   Refined from OpenAlex defaults to match actual research themes:
    *   *Source*: https://campuspress.yale.edu/lehnertlab/ (five stated research areas)
    *   *Source*: arXiv paper titles retrieved 2026-05-26

---

## honors (not in schema — for reference)

*   Fellow, American Physical Society
*   Fellow, American Association for the Advancement of Science
*   Department of Commerce Silver Medal
*   Colorado Governor's Award for High Impact Research
*   Vannevar Bush Faculty Fellowship (2020)
    *   *Source*: https://physics.yale.edu/people/konrad-lehnert

---

## lineage_check

*   `advisor_verified: false` — PhD advisor at UCSB not recoverable from accessible public sources (Yale bio, ORCID, ProQuest all fail or omit name).
*   `postdoc_verified: true` — Yale postdoc (1999–2003) with Robert Schoelkopf confirmed by Yale faculty bio; Schoelkopf is in repo as 145-robert-schoelkopf.md.
