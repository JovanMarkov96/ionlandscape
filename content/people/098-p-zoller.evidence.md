# Evidence Map — 098-p-zoller (Peter Zoller)

Verified: 2026-05-30

## Source list

1. **Wikipedia — Peter Zoller**: https://en.wikipedia.org/wiki/Peter_Zoller — education, career timeline, postdocs, awards.
2. **IQOQI Innsbruck staff page**: https://iqoqi.at/en/people/staff/staff/peter-zoller — current/emeritus position, Innsbruck location.
3. **Lincei CV PDF**: https://www.lincei.it/sites/default/files/2024-10/3092_CV.pdf — contact email Peter.Zoller@uibk.ac.at confirms University of Innsbruck affiliation.
4. **Semantic Scholar / ADS / APS DOI records**: Confirmed DOIs for all four key papers.

## Field-level evidence

*   **`name`**: "Peter Zoller"
    *   *Source*: Wikipedia, IQOQI staff page, CV PDF — all use "Peter Zoller".
    *   *Note*: Previous skeleton had abbreviated "P. Zoller"; corrected to full name.

*   **`sort_name`**: "Zoller, Peter"
    *   *Source*: Derived from full name; replaces "Zoller, P."

*   **`current_position.title`**: "Emeritus Professor of Theoretical Physics"
    *   *Source*: IQOQI staff page lists him as "Emeritus Research Director"; Wikipedia states his chair at Innsbruck (1994–2024) as Professor of Theoretical Physics. Combined as Emeritus Professor.

*   **`current_position.institution`**: "University of Innsbruck"
    *   *Source*: https://iqoqi.at/en/people/staff/staff/peter-zoller — "Zoller Group - Quantum Optics and Quantum Information (based at University of Innsbruck)"
    *   *Note*: Previous skeleton had "Austrian Academy of Sciences" from OpenAlex; overridden per ORCID-first / web-first strategy. University of Innsbruck is the primary academic home.

*   **`current_position.since_year`**: 1994
    *   *Source*: Wikipedia — "At the end of 1994, he accepted a chair at the University of Innsbruck."

*   **`current_position.confidence`**: "confirmed"
    *   *Source*: IQOQI staff page (direct institutional listing).

*   **`location.city`**: "Innsbruck"
    *   *Source*: IQOQI address "Technikerstraße 21a, 6020 Innsbruck, Austria"; Wikipedia bio.
    *   *Note*: Previous skeleton had Vienna (lat 48.208, lon 16.372) — an OpenAlex error. Corrected to Innsbruck.

*   **`location.lat`**: 47.2627, **`location.lon`**: 11.3945
    *   *Source*: https://latitude.to/map/at/austria/cities/innsbruck — GPS coordinates of Innsbruck city center.

*   **`location.region`**: "Tyrol"
    *   *Source*: Innsbruck is the capital of the federal state of Tyrol, Austria.

*   **`education[0]`**: PhD (Physics), University of Innsbruck, 1977, advisor Fritz Ehlotzky
    *   *Source*: Wikipedia — "received his doctorate in February 1977 ... The Stark effect" and "Advisor: Fritz Ehlotzky" per Optica biography and search results.
    *   *Confidence*: confirmed

*   **`thesis.title`**: "The Stark effect"
    *   *Source*: Wikipedia — "doctorate ... with a thesis on the Stark effect."

*   **`postdocs[0]`**: University of Southern California, advisor Peter Lambropoulos, 1978–1979
    *   *Source*: Wikipedia — "In 1978/79, he was a Max Kade Fellow with Peter Lambropoulos at the University of Southern California."

*   **`postdocs[1]`**: University of Waikato, New Zealand, advisor Dan Walls, 1980
    *   *Source*: Wikipedia — "in 1980 he stayed in the group of Dan Walls at the University of Waikato, New Zealand."

*   **`platforms`**: neutral_atom, rydberg_array
    *   *Source*: Retained from skeleton; consistent with his primary research areas (optical lattices, Rydberg simulators). Note: Zoller also co-proposed trapped-ion gates but his primary theoretical platform focus is neutral atoms/Rydberg.

*   **`applications`**: computing, simulation
    *   *Source*: Wikipedia and IQOQI — "pioneering research on quantum computing, quantum simulation and quantum communication."

*   **`key_papers[0]`**: "Quantum Computations with Cold Trapped Ions" (1995)
    *   *Source*: https://ui.adsabs.harvard.edu/abs/1995PhRvL..74.4091C (ADS); DOI 10.1103/PhysRevLett.74.4091
    *   *Authors*: J. I. Cirac, P. Zoller. Zoller is co-author (not first; Cirac is first).
    *   *Role*: co_author

*   **`key_papers[1]`**: "Cold Bosonic Atoms in Optical Lattices" (1998)
    *   *Source*: https://link.aps.org/doi/10.1103/PhysRevLett.81.3108; DOI 10.1103/PhysRevLett.81.3108
    *   *Authors*: D. Jaksch, C. Bruder, J. I. Cirac, C. W. Gardiner, P. Zoller. Zoller is last/senior author.
    *   *Role*: senior_author

*   **`key_papers[2]`**: "Entanglement of Atoms via Cold Controlled Collisions" (1999)
    *   *Source*: https://arxiv.org/abs/quant-ph/9810087; DOI 10.1103/PhysRevLett.82.1975
    *   *Authors*: D. Jaksch, H.-J. Briegel, J. I. Cirac, C. W. Gardiner, P. Zoller. Zoller is last/senior author.
    *   *Role*: senior_author

*   **`key_papers[3]`**: "A Rydberg Quantum Simulator" (2010)
    *   *Source*: https://www.nature.com/articles/nphys1614; DOI 10.1038/nphys1614 (Nature Physics, vol. 6, pp. 382–388)
    *   *Authors*: H. Weimer, M. Müller, I. Lesanovsky, P. Zoller, H. P. Büchler. Zoller is senior/corresponding author.
    *   *Role*: senior_author

*   **`lineage_check.advisor_verified`**: true
    *   *Source*: Wikipedia lists Fritz Ehlotzky as PhD advisor; consistent with Optica biography and web search results.

*   **`lineage_check.postdoc_verified`**: true
    *   *Source*: Wikipedia directly names Peter Lambropoulos (USC) and Dan Walls (Waikato) as postdoc hosts with years.

*   **`verification_source_count`**: 4
    *   Sources: (1) Wikipedia, (2) IQOQI Innsbruck staff page, (3) Lincei CV PDF, (4) DOI/ADS paper records.

## Data quality notes

- **`current_position.title`**: IQOQI page lists "Emeritus Research Director" for his IQOQI role (ended 2024). His University of Innsbruck title is "Emeritus Professor"; the combined label used here accurately reflects both.
- **OpenAlex institution (Vienna)**: OpenAlex mistakenly geolocated him at Vienna (Austrian Academy of Sciences headquarters). His actual base is Innsbruck — corrected via IQOQI staff page and CV.
- **PhD thesis link**: No open-access link found for the 1977 dissertation.
- **Advisor_id for Fritz Ehlotzky**: Not in the repo; left null.
- **`platforms`**: Does not include `trapped_ion` even though Cirac–Zoller is a trapped-ion paper, because Zoller's group is primarily a neutral-atom/Rydberg theory group. Adding `trapped_ion` could be considered if the platform taxonomy intends to capture theoretical proposals as well.
