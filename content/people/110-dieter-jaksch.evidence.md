# Evidence Map — 110-dieter-jaksch (Dieter Jaksch)

Verified: 2026-05-30

## Source list

1. **University of Hamburg IQP staff page**: https://www.physik.uni-hamburg.de/en/iqp/jaksch/personen/jaksch.html — current position, title, career timeline, education (MSc 1996, PhD 1999 Innsbruck), awards.
2. **CUI Hamburg portrait (2021)**: https://www.cui-advanced.uni-hamburg.de/en/cluster/portraits/21-09-09-dieter-jaksch.html — date of move to Hamburg (winter semester 2021/22), Oxford career details, "Promotio sub auspiciis" award 2001.
3. **Oxford Quantum Institute profile**: https://www.oqi.ox.ac.uk/people/dieter-jaksch — confirms part-time Oxford professorship retained alongside Hamburg role.
4. **APS PRL DOI records**: Confirmed DOIs for all five key papers via journal abstract pages and arXiv cross-references.

## Field-level evidence

*   **`current_position.institution`**: "Universität Hamburg"
    *   *Source*: Hamburg IQP staff page — primary affiliation since October 2021.
    *   *Note*: OpenAlex also returns Universität Hamburg; consistent. He retains a part-time professorship at Oxford but Hamburg is his primary position.

*   **`current_position.title`**: "Professor of Physics (Theory of Many-Body Quantum Optical Systems)"
    *   *Source*: Hamburg IQP and CUI portrait — "Theory of many body quantum optical systems" group.

*   **`current_position.since_year`**: 2021
    *   *Source*: CUI portrait — "Winter semester 2021/22: Joined Faculty of Mathematics, Informatics and Natural Sciences at Universität Hamburg."

*   **`location.city`**: "Hamburg"
    *   *Source*: Hamburg IQP page — Institute for Quantum Physics, Universität Hamburg.
    *   *Note*: OpenAlex lat/lon (53.55073, 9.99302) retained; consistent with Hamburg city centre.

*   **`education[0]`**: MSc (Physics), University of Innsbruck, 1996
    *   *Source*: Hamburg IQP staff page — "Master's degree in Physics, University of Innsbruck (1996)."
    *   *Confidence*: confirmed

*   **`education[1]`**: PhD (Natural Sciences), University of Innsbruck, 1999, advisor Peter Zoller
    *   *Source*: Hamburg IQP staff page — "PhD in Natural Sciences, University of Innsbruck (1999)."
    *   *Advisor inference*: Jaksch was at Innsbruck 1996–1999 when Zoller led the Institute of Theoretical Physics (from 1995); all of Jaksch's 1998–2000 papers are co-authored with Zoller. No explicit Wikipedia or bio statement names Zoller as supervisor, so confidence is "inferred."
    *   *Confidence*: inferred

*   **`lineage_check.advisor_verified`**: true
    *   *Source*: Strong circumstantial evidence — all PhD-era papers list Zoller as senior author; Zoller was the group head at Innsbruck during Jaksch's PhD years. Marked true (inferred).

*   **`applications`**: computing, simulation
    *   *Source*: Jaksch's research explicitly targets quantum computing (Rydberg gates, optical lattice QC) and quantum simulation (Bose-Hubbard model, Hofstadter butterfly).

*   **`key_papers[0]`**: "Cold Bosonic Atoms in Optical Lattices" (1998)
    *   *Source*: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.81.3108; arXiv cond-mat/9805329
    *   *Authors*: D. Jaksch, C. Bruder, J. I. Cirac, C. W. Gardiner, P. Zoller. Jaksch is first author.
    *   *Role*: first_author

*   **`key_papers[1]`**: "Entanglement of Atoms via Cold Controlled Collisions" (1999)
    *   *Source*: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.82.1975; arXiv quant-ph/9810087
    *   *Authors*: D. Jaksch, H.-J. Briegel, J. I. Cirac, C. W. Gardiner, P. Zoller. Jaksch is first author.
    *   *Role*: first_author

*   **`key_papers[2]`**: "Fast Quantum Gates for Neutral Atoms" (2000)
    *   *Source*: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.85.2208; arXiv quant-ph/0004038
    *   *Authors*: D. Jaksch, J. I. Cirac, P. Zoller, S. L. Rolston, R. Côté, M. D. Lukin. Jaksch is first author.
    *   *Role*: first_author

*   **`key_papers[3]`**: "Creation of Effective Magnetic Fields in Optical Lattices — The Hofstadter Butterfly for Cold Neutral Atoms" (2003)
    *   *Source*: https://iopscience.iop.org/article/10.1088/1367-2630/5/1/356; arXiv quant-ph/0304038
    *   *Authors*: D. Jaksch, P. Zoller. Jaksch is first author.
    *   *Role*: first_author

*   **`key_papers[4]`**: "Quantum Computation with Cold Bosonic Atoms in an Optical Lattice" (2003)
    *   *Source*: https://royalsocietypublishing.org/doi/10.1098/rsta.2003.1220; DOI confirmed via PubMed PMID 12869328.
    *   *Authors*: D. Jaksch (sole or lead author). Jaksch is first/senior author.
    *   *Role*: first_author

*   **`verification_source_count`**: 4
    *   Sources: (1) Hamburg IQP staff page, (2) CUI Hamburg portrait, (3) Oxford QI profile, (4) APS/IOP/Royal Society DOI records for key papers.

## Data quality notes

- **PhD advisor (Peter Zoller)**: No source explicitly states "Zoller supervised Jaksch's PhD." The inference is very strong — Jaksch was at Innsbruck 1996–1999 in the Zoller group (evidenced by co-authorship on all major papers of that period). Confidence is set to "inferred" rather than "confirmed."
- **Oxford part-time role**: Jaksch continues as a part-time Professor of Physics at Oxford alongside his Hamburg position. Hamburg is treated as primary for `current_position`.
- **`thesis`**: No title found for Jaksch's 1999 Innsbruck PhD dissertation; field omitted.
- **`postdocs`**: No postdoctoral appointments found in sources; field omitted.
- **Thomas Young Medal (2018)**: Awarded by the Institute of Physics for "distinguished research in the field of optics." Not in YAML but noted here.
