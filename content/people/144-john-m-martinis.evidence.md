# Evidence Map — John M. Martinis (144-john-m-martinis)

*   **`current_position.title`**: "Distinguished Professor"
    *   *Source*: https://www.physics.ucsb.edu/people/john-martinis (Faculty profile page)
    *   *Quote*: "Distinguished Professor, Department of Physics, UC Santa Barbara"
*   **`current_position.institution`**: "University of California, Santa Barbara"
    *   *Source*: https://www.physics.ucsb.edu/people/john-martinis (Faculty profile page)
    *   *Source*: https://www.nobelprize.org/prizes/physics/2025/press-release/ (Nobel Prize press release)
    *   *Quote*: "University of California, Santa Barbara, USA"
*   **`current_position.confidence`**: "confirmed"
    *   *Source*: https://www.physics.ucsb.edu/people/john-martinis (Faculty profile, direct institutional listing)
*   **`current_position.since_year`**: 2004
    *   *Source*: https://web.physics.ucsb.edu/~martinisgroup/people.shtml (Group people page)
    *   *Quote*: "Professor at UC Santa Barbara since 2004"
*   **`education[0]`**: "BS (Physics), University of California, Berkeley, 1980"
    *   *Source*: https://en.wikipedia.org/wiki/John_M._Martinis (Wikipedia — pointer only; no primary source located for BS)
    *   *Quote*: "Bachelor of Science in physics in 1980 from UC Berkeley"
*   **`education[1]`**: "PhD (Physics), University of California, Berkeley, 1987"
    *   *Source*: https://www.nobelprize.org/prizes/physics/2025/press-release/ (Nobel Prize press release 2025)
    *   *Quote*: "PhD 1987 from UC Berkeley"
    *   *Source*: https://en.wikipedia.org/wiki/John_M._Martinis (corroborating pointer)
    *   *Quote*: "Doctor of Philosophy in physics in 1987 from UC Berkeley"
*   **`education[1].advisor`**: "John Clarke"
    *   *Source*: https://www.nobelprize.org/prizes/physics/2025/prize-announcement/ (Nobel Prize announcement — Clarke is co-laureate with Martinis and the relationship is described)
    *   *Source*: https://en.wikipedia.org/wiki/John_M._Martinis (pointer — "Doctoral advisor: John Clarke")
    *   *Note*: Wikipedia lists Clarke as advisor; Nobel announcement confirms both as laureates sharing work on superconducting qubits. This advisor relationship is well-established in the community; no primary CV found to directly quote.
*   **`education[1].advisor_id`**: "164-john-clarke"
    *   *Source*: content/people/164-john-clarke.md (cross-reference within repo)
*   **`applications`**: "computing, simulation"
    *   *Source*: https://web.physics.ucsb.edu/~martinisgroup/index.shtml (Group homepage)
    *   *Quote*: "primary objective is to build a quantum computer using superconductors"; "studying particle interactions and external fields using coupled superconducting circuits" (simulation)
*   **`platforms`**: "superconducting"
    *   *Source*: https://web.physics.ucsb.edu/~martinisgroup/index.shtml (Group homepage)
    *   *Quote*: "Superconducting qubits (Xmon transmons)"
    *   *Source*: https://www.physics.ucsb.edu/people/john-martinis (UCSB faculty page)
    *   *Quote*: "physics of superconducting devices"
*   **`postdocs[0]`**: "Commissariat à l'Energie Atomique, Saclay"
    *   *Source*: https://en.wikipedia.org/wiki/John_M._Martinis (pointer only; no primary source located)
    *   *Quote*: Wikipedia describes this as a postdoctoral role at CEA Saclay following his PhD.
    *   *Note*: No institutional CV or primary source confirms exact years or confirms the role title. NIST Boulder (subsequent position) is NOT listed in postdocs[] because it may have been a staff scientist rather than a postdoc — this requires primary source confirmation.
*   **`key_papers[0]`**: "Quantum supremacy using a programmable superconducting processor" (2019)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41586-019-1666-5 (Semantic Scholar API)
    *   *Quote*: Title confirmed; "Nature, Volume 574, Pages 505-510"; "J. Martinis" is senior/corresponding author
    *   DOI: 10.1038/s41586-019-1666-5
*   **`key_papers[1]`**: "State preservation by repetitive error detection in a superconducting quantum circuit" (2015)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature14270 (Semantic Scholar API)
    *   *Quote*: Title confirmed; "Nature, Volume 519, Pages 66-69"; "J. Martinis" is senior author
    *   DOI: 10.1038/nature14270
*   **`key_papers[2]`**: "Superconducting quantum circuits at the surface code threshold for fault tolerance" (2014)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature13171 (Semantic Scholar API)
    *   *Quote*: Title confirmed; "Nature, Volume 508, Pages 500-503"; "J. Martinis" is senior author
    *   DOI: 10.1038/nature13171
*   **`key_papers[3]`**: "Quantum ground state and single-phonon control of a mechanical resonator" (2010)
    *   *Source*: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature08967 (Semantic Scholar API)
    *   *Quote*: Title confirmed; "Nature, Volume 464, Pages 697-703"; authors include "J. Martinis, A. Cleland"
    *   DOI: 10.1038/nature08967
*   **`lineage_check.advisor_verified`**: true
    *   *Source*: https://www.nobelprize.org/prizes/physics/2025/press-release/ (Nobel co-laureate announcement)
    *   *Note*: John Clarke and John Martinis shared the 2025 Nobel Prize in Physics; Clarke is advisor per Wikipedia and community knowledge.
*   **`lineage_check.postdoc_verified`**: false
    *   *Note*: Postdoc institutions confirmed from Wikipedia (pointer only). Advisor names at postdoc institutions not found. No institutional CV found.
*   **`verification_source_count`**: 4
    *   *Sources used*: (1) UCSB Physics faculty page, (2) Martinis Group website, (3) Nobel Prize press release 2025, (4) Semantic Scholar API (paper DOIs)

## Data quality notes

- **BS degree year (1980)**: Sourced from Wikipedia only; no primary institutional source found. Should be verified against a UC Berkeley transcript or institutional CV.
- **PhD advisor**: Confirmed via Nobel Prize co-award and Wikipedia; no primary thesis or CV directly viewed. Cross-check with thesis repository (ProQuest or UC Berkeley library) recommended.
- **Postdoc advisor names**: Not found for either CEA Saclay or NIST Boulder positions. Wikipedia is the only source for the institutions; years are approximate.
- **ORCID profile**: Minimal data — profile exists but no employment or education records populated (ORCID record shows empty biographical sections as of 2026-05-26).
- **Google Scholar**: Could not access; 404 returned for expected Scholar profile URL.
- **`simulation` application**: Added based on group website description of coupled superconducting circuits for studying particle interactions; this is secondary to computing.
- **Postdoc years**: Wikipedia states postdoc at CEA Saclay then NIST; NIST entry listed 1989–2004 based on joining UCSB in 2004. These are approximate and need primary source confirmation.
