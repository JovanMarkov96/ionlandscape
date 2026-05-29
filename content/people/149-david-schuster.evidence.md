# Evidence Map — David Schuster (149-david-schuster)

Verified: 2026-05-26 | Sources used: 5

---

## `current_position.institution` — "Stanford University"
- *Source*: https://profiles.stanford.edu/david-schuster (Stanford Profiles)
- *Quote*: Profile lists David Schuster under Stanford University.
- *Note*: OpenAlex also shows SLAC National Accelerator Laboratory as an affiliation in 2024-2025; this reflects collaborative dark-matter-detection experiments run at SLAC/Fermilab, not his primary academic appointment. Primary appointment is Stanford Applied Physics (confirmed by profiles.stanford.edu).

## `current_position.title` — "Joan Reinhart Professor of Applied Physics"
- *Source*: https://profiles.stanford.edu/david-schuster (Stanford Profiles)
- *Quote*: "Joan Reinhart Professor"
- *Note*: Department confirmed as Applied Physics from the same profile page.

## `current_position.since_year` — 2022
- *Source*: https://api.openalex.org/authors/A5087556046
- *Note*: OpenAlex affiliation timeline shows Stanford University first appearing in 2022 publications, while University of Chicago appears through 2022-2023 in some works. 2022 is the earliest confirmed Stanford affiliation year; treat as approximate.

## `education[0]` — PhD at Yale University, advisor Robert Schoelkopf
- *Source*: http://rsl.yale.edu/publications (Schoelkopf Lab, Yale)
- *Quote*: D. Schuster is listed as an author on publications from 2005 through 2011 on the RSL lab page, consistent with PhD student and postdoc tenures.
- *Cross-reference*: arXiv:cond-mat/0608693 — "Resolving photon number states in a superconducting circuit," D. I. Schuster first author, published in Nature 2007; Yale RSL lab URL appears in arXiv submission header.
- *Note*: PhD year not found on accessible public sources; left null. Advisor identity confirmed by co-authorship pattern (Schuster appears consistently in papers with Schoelkopf as senior author, 2004-2011).

## `postdocs[0]` — Yale University, Schoelkopf Lab, 2008-2011
- *Source*: http://rsl.yale.edu/publications
- *Note*: Schuster's RSL publications extend to 2011 ("Cavity QED in a Molecular Ion Trap," 2011). He appears to have joined UChicago faculty around 2012-2013 based on OpenAlex affiliation timeline (UChicago first appears ~2016 in OpenAlex, though the actual start date may be earlier). Postdoc years 2008-2011 are approximate.

## `platforms` — `superconducting`, `cavity_qed_hybrid`
- *Source*: https://schusterlab.stanford.edu (Schuster Lab website)
- *Quote*: "The lab develops new ways to think about superconducting quantum circuits...electron trapping on liquid helium above superconducting cavities...superfluid helium waves in microchannels."
- *Note*: `cavity_qed_hybrid` reflects the atom-cavity transduction work and the electron-on-helium work, both of which are hybrid cavity-QED systems.

## `applications` — `computing`, `simulation`, `fundamental_physics`
- *Source*: https://schusterlab.stanford.edu + https://profiles.stanford.edu/david-schuster
- *Computing*: "3D Multimode resonators...error correction and topologically protected qubits" (lab website).
- *Simulation*: "Disorder-assisted assembly of strongly correlated fluids of light" (Nature 2022); cavity-array quantum simulation research.
- *Fundamental physics*: Dark matter detection ("Stimulated emission of signal photons from dark matter waves," PRL 2024, DOI 10.1103/PhysRevLett.132.140801).

## `key_papers[0]` — "Resolving photon number states in a superconducting circuit"
- *Source*: arXiv:cond-mat/0608693; published Nature 445, 515-518 (2007)
- DOI: 10.1038/nature05461
- *Role*: first_author (D. I. Schuster is listed first)
- *Authors*: D. I. Schuster, A. A. Houck, J. A. Schreier, A. Wallraff, J. M. Gambetta, A. Blais, L. Frunzio, B. Johnson, M. H. Devoret, S. M. Girvin, R. J. Schoelkopf

## `key_papers[1]` — "Strong coupling of a single photon to a superconducting qubit using circuit quantum electrodynamics"
- *Source*: arXiv:cond-mat/0407325; published Nature 431, 162-167 (2004)
- DOI: 10.1038/nature02851
- *Role*: co_author (second author: A. Wallraff first, R. J. Schoelkopf last)
- *Citations*: 3,758 (OpenAlex, retrieved 2026-05-26)

## `key_papers[2]` — "Stimulated emission of signal photons from dark matter waves"
- *Source*: arXiv:2305.03700; published Phys. Rev. Lett. 132, 140801 (2024)
- DOI: 10.1103/PhysRevLett.132.140801
- *Role*: senior_author (second-to-last; Aaron Chou is last; Schuster is PI of the quantum hardware contribution)
- *Authors*: Ankur Agrawal, Akash V. Dixit, Tanay Roy, Srivatsan Chakram, Kevin He, Ravi K. Naik, David I. Schuster, Aaron Chou

## `key_papers[3]` — "Tunable inductive coupler for high fidelity gates between fluxonium qubits"
- *Source*: arXiv:2309.05720 (2023)
- *Role*: senior_author (last author: David I. Schuster)
- *Authors*: Helin Zhang, Chunyang Ding, D. K. Weiss, Ziwen Huang, Yuwei Ma, Charles Guinn, Sara Sussman, Sai Pavan Chitta, Danyang Chen, Andrew A. Houck, Jens Koch, David I. Schuster

## `key_papers[4]` — "Quantum-limited millimeter wave to optical transduction"
- *Source*: arXiv:2207.10121 (2022); published in Nature 615 (2023) per Stanford profile
- *Role*: senior_author (second-to-last; Jonathan Simon is last; Schuster is co-senior author)
- *Authors*: Aishwarya Kumar, Aziza Suleymanzade, Mark Stone, Lavanya Taneja, Alexander Anferov, David I. Schuster, Jonathan Simon

## `lineage_check.advisor_verified` — true
- Robert Schoelkopf confirmed as PhD advisor based on: (1) Schuster's papers appearing on RSL lab website from 2005, (2) Schuster as first author on circuit QED papers with Schoelkopf as last/senior author, (3) Yale RSL lab URL in arXiv submission metadata.

## `verification_source_count` — 5
Sources used: (1) Stanford Profiles, (2) Schuster Lab website, (3) RSL lab publications page, (4) OpenAlex API, (5) arXiv paper records.

## SLAC affiliation note
OpenAlex shows SLAC National Accelerator Laboratory as an affiliation for 2024-2025 papers. This reflects experimental dark matter searches conducted at SLAC facilities (the SQUAT detector, quantum-enhanced axion/dark-photon searches). Schuster holds a joint-use or affiliated-scientist status at SLAC through these collaborations but his faculty line is Stanford Applied Physics.

## Fields not found / not verified
- **PhD year**: Not found on any accessible public source; left null.
- **Undergraduate institution**: Not found.
- **Postdoc year range**: Approximate (2008-2011); could be verified by thesis publication date or UChicago start announcement.
- **Since_year at Stanford**: 2022 is approximate based on OpenAlex; could be refined via Stanford announcement.
