# Evidence Map — 106-thomas-pohl (Thomas Pohl)

Verified: 2026-05-30

## Source list

1. **Aarhus University News (2017)**: Appointment as Niels Bohr Professor; PhD year (2005), postdoc at Harvard-Smithsonian (ITAMP), Group Leader at MPIPKS since 2008. URL: https://phys.au.dk/en/news/item/artikel/ny-professor-thomas-pohl/
2. **ORCID record (0000-0002-4093-3644)**: Employment history confirming move to TU Wien (October 2023) and prior Aarhus University position (2017–2023). URL: https://orcid.org/0000-0002-4093-3644
3. **TU Wien Pohl Group page**: Current group at Institute for Theoretical Physics, TU Wien. URL: https://www.tuwien.at/en/phy/itp/pohl-group
4. **MPIPKS staff page (Jan-Michael Rost)**: Confirms Rost leads the Finite Systems division where Pohl did his PhD and early career. URL: https://www.pks.mpg.de/finite-systems/people/prof-dr-jan-michael-rost
5. **OpenAlex profile**: Metrics (h-index 54, citations 9630, 220 publications). URL: https://openalex.org/A5048498875

## Field-level evidence

*   **`current_position.institution`**: TU Wien
    *   *Source*: ORCID record; employment start October 1, 2023 at TU Wien Institute for Theoretical Physics.

*   **`current_position.title`**: "Professor of Theoretical Physics"
    *   *Source*: ORCID record (thomas.pohl@itp.tuwien.ac.at affiliation).

*   **`current_position.since_year`**: 2023
    *   *Source*: ORCID record — start date October 1, 2023.

*   **`location`**: Vienna, Austria
    *   *Source*: Updated from Aarhus to Vienna following confirmed TU Wien appointment.

*   **`education[0]`**: PhD (Physics), MPIPKS Dresden, 2005
    *   *Source*: Aarhus University appointment news (2017); year 2005 stated explicitly.

*   **`education[0].advisor`**: Jan-Michael Rost (inferred)
    *   *Source*: Pohl worked in the Finite Systems division at MPIPKS, which is led by Jan-Michael Rost. The 2005–2008 Harvard postdoc and the MPIPKS group leadership timeline are consistent with Rost being his PhD supervisor. Confidence: inferred (not directly confirmed in a primary source found).

*   **`postdocs[0]`**: ITAMP Fellowship, Harvard-Smithsonian Center for Astrophysics, 2005–2008
    *   *Source*: Aarhus University news article states "following his doctorate, Pohl held an ITAMP Postdoctoral Fellowship (2005)... Since 2008 he has been a Group Leader at MPIPKS." Confidence: confirmed.

*   **`applications`**: [computing, simulation]
    *   *Source*: Research focuses on Rydberg quantum gates, photon-photon interactions for quantum computing, and quantum simulation of many-body systems.

*   **`key_papers[0]`**: "Dynamical Crystallization in the Dipole Blockade of Ultracold Atoms" — Pohl, Demler, Lukin. PRL 104, 043002 (2010).
    *   DOI: 10.1103/PhysRevLett.104.043002. Pohl is first author.

*   **`key_papers[1]`**: "Photon-Photon Interactions via Rydberg Blockade" — Gorshkov, Otterbach, Fleischhauer, Pohl, Lukin. PRL 107, 133602 (2011).
    *   DOI: 10.1103/PhysRevLett.107.133602. Pohl is co-author (4th of 5).

*   **`key_papers[2]`**: "Quantum nonlinear optics with single photons enabled by strongly interacting atoms" — Peyronel, Firstenberg, Liang, Hofferberth, Gorshkov, Pohl, Lukin, Vuletić. Nature 488, 57 (2012).
    *   DOI: 10.1038/nature11361. Pohl performed theoretical analysis alongside Gorshkov.

*   **`key_papers[3]`**: "Observation of spatially ordered structures in a two-dimensional Rydberg gas" — Schauß, Cheneau, Endres, Fukuhara, Hild, Omran, Pohl, Gross, Kuhr, Bloch. Nature 491, 87 (2012).
    *   DOI: 10.1038/nature11596. Pohl is theory co-author.

*   **`key_papers[4]`**: "Coherent Photon Manipulation in Interacting Atomic Ensembles" — Murray, Pohl. PRX 7, 031007 (2017).
    *   DOI: 10.1103/PhysRevX.7.031007. Pohl is senior/corresponding author.

*   **`key_papers[5]`**: "Photon-photon interactions in Rydberg-atom arrays" — Zhang, Walther, Mølmer, Pohl. Quantum 6, 674 (2022).
    *   DOI: 10.22331/q-2022-03-30-674. Pohl is senior author.

*   **`lineage_check.advisor_verified`**: false
    *   Jan-Michael Rost is strongly inferred as PhD advisor (MPIPKS Finite Systems division, consistent career timeline) but no primary source explicitly names him as Pohl's supervisor.

*   **`lineage_check.postdoc_verified`**: true
    *   ITAMP Fellowship at Harvard-Smithsonian confirmed in Aarhus news article.

## Data quality notes

*   **`current_position.institution`** was previously listed as Aarhus University (OpenAlex-inferred). Corrected to TU Wien based on ORCID record showing appointment from October 2023.
*   **`location`**: Updated from Aarhus, Denmark to Vienna, Austria.
*   **`thesis.title`**: Not found in any accessible online source.
*   **`education[0].advisor`**: Confidence set to `inferred`; Jan-Michael Rost is the head of the Finite Systems division at MPIPKS and a co-author with Pohl on early publications (2005), strongly suggesting advisor relationship.
