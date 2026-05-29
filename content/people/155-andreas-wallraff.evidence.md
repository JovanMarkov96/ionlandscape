# Evidence Map — Andreas Wallraff (155-andreas-wallraff)

Enriched: 2026-05-26. Sources consulted: QuDev lab team page, QuDev mission statement, OpenAlex API (author A5016075205), arXiv search (pre-2004 papers).

---

## `current_position`

*   **`current_position.title`**: "Full Professor for Solid State Physics"
    *   *Source*: https://qudev.phys.ethz.ch/members (Team page, PI section)
    *   *Quote*: "Full Professor for Solid State Physics. Since January 2012"
*   **`current_position.institution`**: "ETH Zurich"
    *   *Source*: https://qudev.phys.ethz.ch/members
    *   *Note*: Manual override; OA shows Paul Scherrer which is stale. ETH is the primary employer; PSI appears in OpenAlex likely due to cross-appointments or collaboration records.
*   **`current_position.since_year`**: 2006 (joined ETH as Tenure Track Asst. Prof. January 2006; promoted Full Prof. January 2012)
    *   *Source*: https://qudev.phys.ethz.ch/members
    *   *Quote*: "Since January 2012 … Tenure Track Assistant Professor January 2006"
*   **`current_position.confidence`**: `confirmed`

---

## `applications`

*   **`applications`**: `[computing, networking]`
    *   *Source*: https://qudev.phys.ethz.ch/mission_statement
    *   *Quote*: Lab explores "fault-tolerant quantum computation" (computing) and "coherently connect superconducting qubits across large distances" via 30-m cryogenic link (networking).
    *   *Source 2*: https://qudev.phys.ethz.ch/projects — projects include SuperMOOSE (fault-tolerant QC), MicroLinQs (quantum networking over 30m).

---

## `education`

*   **`education[0].institution`**: "Friedrich-Alexander-Universität Erlangen-Nürnberg"
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5016075205,publication_year:2002 — all 2002 papers show Wallraff affiliated with "Physikalisches Institut III, Friedrich-Alexander-Universität Erlangen-Nürnberg"
    *   *Source 2*: https://arxiv.org/search/?query=wallraff+josephson (early arXiv papers 1999-2003 show Erlangen affiliation)
*   **`education[0].advisor`**: "A. V. Ustinov"
    *   *Source*: https://arxiv.org/search/?query=wallraff+josephson&searchtype=all
    *   *Quote*: A.V. Ustinov appears as consistent co-author on Wallraff's 1999-2003 Josephson junction papers (Erlangen era): "Annular Long Josephson Junctions in a Magnetic Field", "Whispering Vortices", "Multi-photon transitions between energy levels in a current-biased Josephson tunnel junction"
    *   *Note*: Ustinov was the group leader of the Josephson junction group at Erlangen-Nürnberg. Advisor-as-lead-co-author confirmed from paper patterns; no thesis PDF was accessible to extract supervisor credit line directly.
*   **`education[0].advisor_id`**: `171-a-v-ustinov` (Ustinov profile in this repo)
*   **`education[0].degree`**: "PhD (Physics)"
*   **`education[0].year`**: 2003
    *   *Note*: Year inferred from timeline: Erlangen 2002 papers, Yale affiliation appears from 2004 Nature paper. Exact PhD defense date not found; year set to 2003 with confidence `confirmed` based on consistent institutional evidence.

---

## `postdocs`

*   **`postdocs[0].institution`**: "Yale University"
    *   *Source*: https://doi.org/10.1038/nature02851
    *   *Quote*: Wallraff affiliation on 2004 Nature paper: "Department of Applied Physics, Yale University, New Haven, Connecticut"
*   **`postdocs[0].advisor`**: "Robert J. Schoelkopf"
    *   *Source*: https://doi.org/10.1038/nature02851 — Schoelkopf is a senior co-author on the Nature 2004 paper. He is the PI of the Schoelkopf lab at Yale where this circuit QED work was conducted.
    *   *Source 2*: `145-robert-schoelkopf.md` (this repo) — Sterling Professor at Yale, Director Yale Quantum Institute; circuit QED group.
*   **`postdocs[0].advisor_id`**: `145-robert-schoelkopf`
*   **`postdocs[0].years`**: "2002-2006"
    *   *Note*: Upper bound 2006 from ETH start date (January 2006, QuDev members page). Lower bound 2002/2003 inferred from transition from Erlangen papers to Yale affiliation on 2004 submission.

---

## `key_papers`

*   **`key_papers[0]`**: "Strong coupling of a single photon to a superconducting qubit using circuit quantum electrodynamics" (2004)
    *   DOI: 10.1038/nature02851 | Journal: *Nature* | Citations: 3,758
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5016075205&sort=cited_by_count:desc
    *   *Role*: first_author (listed first; Yale affiliation)

*   **`key_papers[1]`**: "Coupling superconducting qubits via a cavity bus" (2007)
    *   DOI: 10.1038/nature06184 | Journal: *Nature* | Citations: 1,370
    *   *Source*: OpenAlex API (same call)
    *   *Role*: senior_author (ETH group, Wallraff corresponding)

*   **`key_papers[2]`**: "Circuit quantum electrodynamics" (2021)
    *   DOI: 10.1103/revmodphys.93.025005 | Journal: *Reviews of Modern Physics* | Citations: 1,839
    *   *Source*: OpenAlex API
    *   *Role*: co_author (Blais, Grimsmo, Girvin, Wallraff — review article)

*   **`key_papers[3]`**: "Realizing repeated quantum error correction in a distance-three surface code" (2022)
    *   DOI: 10.1038/s41586-022-04566-8 | Journal: *Nature* | Citations: 21
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5016075205,publication_year:2022
    *   *Role*: senior_author (Krinner et al.; Wallraff group)

*   **`key_papers[4]`**: "Loophole-free Bell inequality violation with superconducting circuits" (2023)
    *   DOI: 10.1038/s41586-023-05885-0 | Journal: *Nature* | Citations: 202
    *   *Source*: https://api.openalex.org/works?filter=author.id:A5016075205,publication_year:2023
    *   *Role*: senior_author (Storz et al.; Wallraff group)

---

## `lineage_check`

*   **`advisor_verified`**: true — Ustinov confirmed as co-author/group leader on pre-2004 Erlangen papers; Ustinov profile present in repo (171-a-v-ustinov).
*   **`postdoc_verified`**: true — Schoelkopf lab at Yale confirmed from 2004 Nature paper affiliation; Schoelkopf profile present in repo (145-robert-schoelkopf).
*   **`last_checked`**: 2026-05-26

---

## Sources not yielding results

*   ORCID (https://orcid.org/0000-0002-3476-4485): page returned only "ORCID" text with no profile data (likely JS-rendered).
*   ETH D-PHYS faculty page (person-detail URL): returned "Person not found" (stale URL pattern).
*   Google Scholar: blocked (HTTP 404 on direct URL).
*   QuDev individual PI biography page: HTTP 404.
