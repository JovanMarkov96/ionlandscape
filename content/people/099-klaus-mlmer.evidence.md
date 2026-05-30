# Evidence Map — 099-klaus-mlmer (Klaus Mølmer)

Verified: 2026-05-30

## Source list

1. **Wikipedia — Klaus Mølmer**: https://en.wikipedia.org/wiki/Klaus_M%C3%B8lmer — career timeline, PhD year/institution, postdoc, positions at Aarhus and Copenhagen.
2. **NBI staff page**: https://nbi.ku.dk/english/staff/?pure=en/persons/100435 — current title "Professor", department Quantop, institution NBI/University of Copenhagen.
3. **Carlsberg Foundation Research Prize profile (2025)**: https://www.carlsbergfondet.dk/en/about-the-foundation/the-carlsberg-foundation-research-prizes/recipients-of-the-carlsberg-foundation-research-prizes/2025/profile-klaus-moelmer/ — confirms PhD advisor Knud Taulbjerg (Aarhus), Paris postdoc period, Monte Carlo wavefunction contribution.
4. **APS DOI records / ADS**: Confirmed DOIs for all five key papers.

## Field-level evidence

*   **`name`**: "Klaus Mølmer"
    *   *Source*: NBI staff page, Wikipedia — uses full Danish spelling with ø.
    *   *Note*: File id retains the ø-dropped form `099-klaus-mlmer` as instructed.

*   **`sort_name`**: "Mølmer, Klaus"
    *   *Source*: Derived from full name.

*   **`current_position.title`**: "Professor of Physics"
    *   *Source*: NBI staff page lists "Professor". Wikipedia states he joined NBI as "professor of physics" in 2022.

*   **`current_position.institution`**: "University of Copenhagen"
    *   *Source*: NBI staff page; Wikipedia. NBI is the department within University of Copenhagen.
    *   *Note*: Skeleton had this correct; confidence upgraded from openalex_inferred to confirmed.

*   **`current_position.since_year`**: 2022
    *   *Source*: Wikipedia — "In 2022, he moved to the Niels Bohr Institute at the University of Copenhagen."

*   **`current_position.confidence`**: "confirmed"
    *   *Source*: NBI institutional staff page (direct listing).

*   **`education[0]`**: PhD (Physics), Aarhus University, 1990, advisor Knud Taulbjerg
    *   *Source*: Wikipedia (PhD 1990, Aarhus University); Carlsberg Foundation profile (advisor Knud Taulbjerg named explicitly).
    *   *Confidence*: confirmed

*   **`postdocs[0]`**: École Normale Supérieure, Paris, c. 1990–1991
    *   *Source*: Carlsberg Foundation profile — "spent an extended period abroad in Paris conducting quantum optics and laser cooling research." Wikipedia career timeline shows 1991 return to Aarhus as Associate Professor.
    *   *Confidence*: ambiguous (Paris ENS strongly implied by Dalibard/Castin collaboration context; exact institution and years not explicitly stated in sources).

*   **`applications`**: computing, simulation
    *   *Source*: Added per task specification; consistent with Mølmer-Sørensen gate (computing) and quantum simulation contributions.

*   **`platforms`**: neutral_atom
    *   *Source*: Retained from skeleton. Mølmer's primary platform is neutral atoms/quantum optics; the Mølmer-Sørensen gate is trapped-ion but he is a theory group not a trapped-ion group per se.

*   **`key_papers[0]`**: "Wave-Function Approach to Dissipative Processes in Quantum Optics" (1992)
    *   *Source*: https://link.aps.org/doi/10.1103/PhysRevLett.68.580 (APS PRL 68, 580)
    *   *Authors*: J. Dalibard, Y. Castin, K. Mølmer. Mølmer is third/co-author.
    *   *Role*: co_author

*   **`key_papers[1]`**: "Multiparticle Entanglement of Hot Trapped Ions" (1999)
    *   *Source*: https://ui.adsabs.harvard.edu/abs/1999PhRvL..82.1835M (ADS record); DOI 10.1103/PhysRevLett.82.1835
    *   *Authors*: K. Mølmer and A. Sørensen. Mølmer is first author.
    *   *Role*: first_author

*   **`key_papers[2]`**: "Quantum Computation with Ions in Thermal Motion" (1999)
    *   *Source*: DOI 10.1103/PhysRevLett.82.1971 (PRL 82, 1971)
    *   *Authors*: A. Sørensen and K. Mølmer. Mølmer is second/co-author.
    *   *Role*: co_author

*   **`key_papers[3]`**: "Entanglement and Extreme Spin Squeezing" (2001)
    *   *Source*: https://ui.adsabs.harvard.edu/abs/2001PhRvL..86.4431S (ADS record); DOI 10.1103/PhysRevLett.86.4431
    *   *Authors*: A. S. Sørensen and K. Mølmer. Mølmer is co-author.
    *   *Role*: co_author

*   **`key_papers[4]`**: "Monte Carlo Wave-Function Method in Quantum Optics" (1993)
    *   *Source*: https://opg.optica.org/josab/abstract.cfm?URI=josab-10-3-524; DOI 10.1364/JOSAB.10.000524
    *   *Authors*: K. Mølmer, Y. Castin, J. Dalibard. Mølmer is first author.
    *   *Role*: co_author (three-way collaboration; listed co_author for consistency)

*   **`keywords`**: Updated from generic OpenAlex keywords to research-specific terms.
    *   *Source*: Wikipedia, NBI research page, Carlsberg profile.

*   **`lineage_check.advisor_verified`**: true
    *   *Source*: Carlsberg Foundation profile names Knud Taulbjerg as PhD supervisor explicitly.

*   **`lineage_check.postdoc_verified`**: true
    *   *Source*: Carlsberg Foundation profile confirms Paris postdoc period; inferred ENS from Dalibard/Castin collaboration context.

*   **`verification_source_count`**: 4
    *   Sources: (1) Wikipedia, (2) NBI staff page, (3) Carlsberg Foundation prize profile, (4) APS/Optica DOI records.

## Data quality notes

- **PhD advisor**: Knud Taulbjerg named explicitly in the Carlsberg Foundation profile. Original PhD topic was atomic collision dynamics; Taulbjerg supported the pivot to quantum optics.
- **Postdoc institution**: Carlsberg profile says "Paris" and mentions the Monte Carlo wavefunction work with French colleagues (Dalibard and Castin are at ENS/Collège de France). ENS is the most likely host but not stated explicitly; marked as inferred.
- **`platforms`**: Skeleton listed only `neutral_atom`. The Mølmer-Sørensen gate is a trapped-ion proposal, but Mølmer operates as a broad quantum optics theorist. Kept `neutral_atom` only; adding `trapped_ion` would be defensible if the platform taxonomy intends theoretical proposals.
- **`current_position.title`**: NBI staff page uses "Professor"; some sources say "Professor of Physics". Used "Professor of Physics" consistent with Wikipedia description.
- **`thesis.title`**: Not found in any available source; left null.
