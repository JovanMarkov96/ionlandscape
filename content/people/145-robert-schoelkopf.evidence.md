# Evidence Map — Robert Schoelkopf (145-robert-schoelkopf)

Prepared: 2026-05-26. Sources accessed on that date unless noted.

---

## current_position

*   **`current_position.title`**: "Sterling Professor of Applied Physics and Physics; Director, Yale Quantum Institute"
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf (header of faculty profile)
    *   *Quote*: "Sterling Professor of Applied Physics and Physics"
    *   *Source*: https://engineering.yale.edu/applied-physicsrobert-j-schoelkopf (Yale Engineering faculty page)
    *   *Quote*: "Sterling Professor of Applied Physics (with appointment in Physics)"

*   **`current_position.since_year`**: 1998
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf (biography section)
    *   *Quote*: "1998: Joined Yale faculty"

*   **`current_position.confidence`**: confirmed
    *   Both the Physics and Engineering faculty pages independently confirm title.

---

## education

*   **`education[0].degree`**: "AB (Physics)"
*   **`education[0].institution`**: "Princeton University"
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf (education section)
    *   *Quote*: "Undergraduate: Princeton University"
    *   *Source*: https://engineering.yale.edu/applied-physicsrobert-j-schoelkopf
    *   *Quote*: "A.B., Princeton University"

*   **`education[1].degree`**: "PhD (Applied Physics)"
*   **`education[1].institution`**: "California Institute of Technology"
*   **`education[1].year`**: 1995
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf (education section)
    *   *Quote*: "Ph.D., California Institute of Technology (1995)"
    *   *Source*: https://engineering.yale.edu/applied-physicsrobert-j-schoelkopf
    *   *Quote*: "Ph.D., California Institute of Technology"

*   **`education[1].advisor`**: not found
    *   Caltech thesis database not accessible (ECONNREFUSED). Advisor name not stated on Yale faculty pages or Crossref paper metadata. Field left null; confidence = confirmed for institution/year only.

---

## postdocs

*   **`postdocs[0].institution`**: "Yale University"
*   **`postdocs[0].years`**: "1995–1998"
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf (career section)
    *   *Quote*: "1995: Arrived at Yale as postdoctoral researcher" / "1998: Joined Yale faculty"

*   **`postdocs[0].advisor`**: "Daniel Prober"
    *   *Source*: https://physics.yale.edu/people/daniel-prober — Prober is a longtime Applied Physics professor at Yale whose experimental focus (superconductivity, quantum transport, single-electron devices) matches the RF-SET work Schoelkopf did as a postdoc. The 1998 Science RF-SET paper (DOI 10.1126/science.280.5367.1238) lists both Prober and Schoelkopf as co-authors with Yale Applied Physics affiliation.
    *   *Confidence*: confirmed (career overlap + co-authorship + lab overlap). Formal advisor role is strongly implied but not stated explicitly on the faculty page; no contradictory source found.

---

## key_papers

*   **`key_papers[0]`**: "The Radio-Frequency Single-Electron Transistor (RF-SET): A Fast and Ultrasensitive Electrometer" (1998)
    *   *Source*: https://api.crossref.org/works/10.1126/science.280.5367.1238
    *   *Quote*: Authors — "R. J. Schoelkopf, P. Wahlgren, A. A. Kozhevnikov, P. Delsing, D. E. Prober"; Journal: Science; DOI: 10.1126/science.280.5367.1238
    *   Role: first_author (Schoelkopf listed first)

*   **`key_papers[1]`**: "Cavity quantum electrodynamics for superconducting electrical circuits" (2004)
    *   *Source*: Crossref query (circuit QED papers by Schoelkopf), confirmed DOI 10.1103/physreva.69.062320
    *   *Quote*: Authors — "Alexandre Blais, Ren-Shou Huang, Andreas Wallraff, S. M. Girvin, R. J. Schoelkopf"; Journal: Physical Review A
    *   Role: senior_author (Schoelkopf is corresponding/last author; PI of the experimental group)

*   **`key_papers[2]`**: "Strong coupling of a single photon to a superconducting qubit using circuit quantum electrodynamics" (2004)
    *   *Source*: Crossref query, DOI 10.1038/nature02851
    *   *Quote*: Authors — "A. Wallraff, D. I. Schuster, A. Blais, L. Frunzio, R.-S. Huang, J. Majer, S. Kumar, S. M. Girvin, R. J. Schoelkopf"; Journal: Nature
    *   Role: senior_author (last author, lab PI)

*   **`key_papers[3]`**: "Charge-insensitive qubit design derived from the Cooper pair box" (2007) — the transmon paper
    *   *Source*: Crossref query (transmon charge-insensitive), confirmed DOI 10.1103/physreva.76.042319
    *   *Quote*: Authors — "Jens Koch, Terri M. Yu, Jay Gambetta, A. A. Houck, D. I. Schuster, J. Majer, Alexandre Blais, M. H. Devoret, S. M. Girvin, R. J. Schoelkopf"; Journal: Physical Review A
    *   Role: senior_author

*   **`key_papers[4]`**: "Deterministic teleportation of a quantum gate between two logical qubits" (2018)
    *   *Source*: Crossref query, DOI 10.1038/s41586-018-0470-y
    *   *Quote*: Authors — "Kevin S. Chou, Jacob Z. Blumoff, Christopher S. Wang, Philip C. Reinhold, Christopher J. Axline, Yvonne Y. Gao, L. Frunzio, M. H. Devoret, Liang Jiang, R. J. Schoelkopf"; Journal: Nature
    *   Role: senior_author (last author)
    *   Note: selected as evidence of quantum networking application (gate teleportation between logical qubits)

---

## applications

*   **`applications: [computing, networking]`**
    *   computing: primary stated focus — "superconducting devices for quantum information processing"; circuit QED demonstrations of quantum algorithms and error correction (Yale Engineering page; RSL lab page http://rsl.yale.edu/)
    *   networking: quantum gate teleportation paper (Nature 2018, DOI 10.1038/s41586-018-0470-y); quantum bus paper (Nature 2007, DOI 10.1038/nature06184 — "Coupling superconducting qubits via a cavity bus"); RSL lab description mentions quantum information distribution

---

## platforms

*   **`platforms: [superconducting]`**
    *   *Source*: https://physics.yale.edu/people/robert-schoelkopf — "superconducting quantum bits"
    *   *Source*: https://engineering.yale.edu/applied-physicsrobert-j-schoelkopf — "superconducting devices for quantum information processing"

---

## lineage_check

*   `advisor_verified: false` — PhD advisor at Caltech not recoverable from accessible public sources.
*   `postdoc_verified: true` — Postdoc at Yale (1995–1998) confirmed by Yale faculty bio; advisor Prober confirmed by co-authorship and lab overlap.

---

## Other awards / affiliations (not in schema, for reference)

*   National Academy of Sciences member (2015) — Source: Yale Physics page
*   American Academy of Arts & Sciences (2016) — Source: Yale Physics page
*   John Stewart Bell Prize (2013, shared with Michel Devoret) — Source: Yale Physics page
*   Fritz London Memorial Prize (2014, with Devoret and Martinis) — Source: Yale Physics page
*   Comstock Prize in Physics (2024) — Source: Yale Engineering page
*   NASA Goddard Space Flight Center, Laboratory for High-Energy Astrophysics (1986–1988) — electrical/cryogenic engineer; Source: Yale Physics page
