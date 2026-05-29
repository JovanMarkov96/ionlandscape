# Evidence Map — S. M. Girvin (147-s-m-girvin)

*   **`current_position.title`**: "Sterling Professor of Physics and Professor of Applied Physics"
    *   *Source*: https://girvin.sites.yale.edu/ (homepage bio)
    *   *Quote*: "Sterling Professor of Physics and Professor of Applied Physics, Yale University"
    *   *Source*: https://physics.yale.edu/people/steven-girvin (Yale Physics faculty page)

*   **`current_position.institution`**: "Yale University"
    *   *Source*: https://girvin.sites.yale.edu/ (homepage)
    *   *Source*: https://pub.orcid.org/v3.0/0000-0002-6470-5494/employments (ORCID employment record)
    *   *Quote*: "Sterling Professor of Physics and Professor of Applied Physics, Yale University, start 2001"

*   **`current_position.confidence`**: "confirmed"
    *   *Source*: https://physics.yale.edu/people/steven-girvin (direct institutional faculty listing)

*   **`education[0]`**: "BS (Physics), Bates College, 1971"
    *   *Source*: https://physics.yale.edu/people/steven-girvin (Yale Physics faculty page)
    *   *Quote*: "B.S., Bates College (1971)"

*   **`education[1]`**: "MS, University of Maine, 1973"
    *   *Source*: https://physics.yale.edu/people/steven-girvin (Yale Physics faculty page)
    *   *Quote*: "M.S., University of Maine (1973)"

*   **`education[2]`**: "PhD (Theoretical Physics), Princeton University, 1977"
    *   *Source*: https://physics.yale.edu/people/steven-girvin (Yale Physics faculty page)
    *   *Quote*: "Ph.D. in Theoretical Physics, Princeton University (1977)"
    *   *Source*: https://girvin.sites.yale.edu/ (bio)
    *   *Quote*: "Ph.D. in theoretical physics from Princeton University in 1977"

*   **`education[2].advisor`**: null
    *   *Note*: PhD advisor name not found on Yale faculty page, girvin.sites.yale.edu bio, or ORCID record. No primary CV available. Left null; requires primary source confirmation.

*   **`postdocs`**: empty array
    *   *Note*: No postdoc positions found on girvin.sites.yale.edu, Yale faculty page, or ORCID. The bio states he joined Yale in 2001; prior institutional affiliations (Indiana University is mentioned in collaborators' paper affiliations) not confirmed as postdoc. Left empty pending primary source.

*   **`applications`**: "computing, simulation"
    *   *Source*: https://girvin.sites.yale.edu/ (homepage bio)
    *   *Quote*: "quantum computing using superconducting systems, quantum error correction, and quantum information processing"
    *   *Source*: https://physics.yale.edu/people/steven-girvin
    *   *Quote*: Research described as quantum computing and quantum information; simulation inferred from foundational circuit QED theory work enabling analog quantum simulation.

*   **`key_papers[0]`**: "Strong coupling of a single photon to a superconducting qubit using circuit quantum electrodynamics" (2004)
    *   *Source*: https://api.openalex.org/works/https://doi.org/10.1038/nature02851
    *   *Quote*: Authors: Wallraff, Schuster, Blais, Frunzio, Huang, Majer, Kumar, Girvin, Schoelkopf; Nature Vol. 431, pp. 162-167
    *   DOI: 10.1038/nature02851; 3,758 citations (OpenAlex, retrieved 2026-05-26)

*   **`key_papers[1]`**: "Cavity quantum electrodynamics for superconducting electrical circuits: An architecture for quantum computation" (2004)
    *   *Source*: https://api.openalex.org/works/https://doi.org/10.1103/physreva.69.062320
    *   *Quote*: Authors: Blais, Huang, Wallraff, Girvin, Schoelkopf; Physical Review A 69, 062320
    *   DOI: 10.1103/physreva.69.062320; 2,963 citations (OpenAlex, retrieved 2026-05-26)

*   **`key_papers[2]`**: "Charge-insensitive qubit design derived from the Cooper pair box" (2007)
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5046083937&sort=cited_by_count:desc (OpenAlex top works)
    *   DOI: 10.1103/physreva.76.042319; 3,326 citations (OpenAlex, retrieved 2026-05-26)

*   **`key_papers[3]`**: "Introduction to quantum noise, measurement, and amplification" (2010)
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5046083937&sort=cited_by_count:desc (OpenAlex top works)
    *   DOI: 10.1103/revmodphys.82.1155; 1,917 citations (OpenAlex, retrieved 2026-05-26)

*   **`key_papers[4]`**: "Coupling superconducting qubits via a cavity bus" (2007)
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5046083937&sort=cited_by_count:desc (OpenAlex top works)
    *   DOI: 10.1038/nature06184; 1,370 citations (OpenAlex, retrieved 2026-05-26)

*   **`lineage_check.advisor_verified`**: false
    *   *Note*: PhD advisor at Princeton (1977) not found in any source consulted. girvin.sites.yale.edu bio does not name the advisor. Requires Princeton thesis repository or primary CV.

*   **`lineage_check.postdoc_verified`**: false
    *   *Note*: No postdoc positions identified from any authoritative source.

*   **`verification_source_count`**: 3
    *   *Sources used*: (1) girvin.sites.yale.edu (personal site/bio), (2) physics.yale.edu/people/steven-girvin (Yale faculty page), (3) OpenAlex API (top cited works, ORCID employments)

## Data quality notes

- **PhD advisor**: Not found. The bio at girvin.sites.yale.edu only states "Ph.D. in theoretical physics from Princeton University in 1977" without naming the advisor. Princeton University Library or ProQuest dissertation search recommended.
- **Postdocs**: Girvin's bio jumps from PhD (1977) to Yale (2001 start). Intermediate affiliations (e.g., Indiana University Bloomington appears in co-author affiliation on the 2004 PRA paper) are not confirmed as postdoc vs. faculty positions. No postdoc block added.
- **MS degree**: Listed on Yale faculty page. Institution is University of Maine, year 1973; no advisor named.
- **`simulation` application**: Added because circuit QED theory directly enables quantum simulation with superconducting circuits; this is consistent with VISION.md scope ("quantum simulation — condensed matter").
- **ORCID**: Employment record populated (Yale, 2001–present); education section empty.
- **Google Scholar**: 404 returned for expected Scholar URL; OpenAlex metrics used instead.
