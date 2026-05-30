# Evidence Map — 084-antoine-browaeys (Antoine Browaeys)

Verified: 2026-05-30

## Source list

1. **Université Paris-Saclay profile**: PhD year (2000), advisor (Alain Aspect), institution, postdoc at NIST.
   URL: https://www.universite-paris-saclay.fr/en/news/antoine-browaeys-quest-quantum-computing-using-cold-atoms
2. **CNRS person page**: Joined CNRS 2003 (Chargé de recherche), promoted to Directeur de recherche 2013.
   URL: https://www.cnrs.fr/fr/personne/antoine-browaeys-0
3. **Simons Foundation biography**: Title "Research Director at CNRS", postdoc at NIST with W.D. Phillips, Pasqal co-founder.
   URL: https://www.simonsfoundation.org/people/antoine-browaeys/
4. **Optica biography**: Awards including Herbert Walther Award 2026, CNRS Silver Medal, election to French Academy of Sciences.
   URL: https://www.optica.org/history/biographies/bios/antoine_browaeys/
5. **Institut d'Optique team page**: Group leader, "Quantum Optics – Atoms" team, office R0.08, Palaiseau.
   URL: https://atom-tweezers-io.org/people/

## Field-level evidence

- **`current_position.title`**: "Directeur de recherche (Research Director)"
  - Source 2: CNRS person page confirms title and promotion year 2013.

- **`current_position.institution`**: "Institut d'Optique Graduate School / Laboratoire Charles Fabry, CNRS"
  - Sources 1, 3, 5: Consistent across Simons Foundation, CNRS page, and team website.

- **`current_position.since_year`**: 2013
  - Source 2: Promoted to Directeur de recherche in 2013. (Joined CNRS in 2003 as Chargé de recherche.)

- **`location`**: Palaiseau, Île-de-France, France (lat 48.7136, lon 2.1692)
  - Institut d'Optique Graduate School is located in Palaiseau, not Paris. Coordinates corrected from OpenAlex Paris geocode.

- **`education[0].degree`**: PhD (Physics), 2000
  - Source 1: Paris-Saclay article explicitly states PhD year 2000 and topic (magnetic trapping of metastable helium).

- **`education[0].advisor`**: Alain Aspect
  - Sources 1, 4: Both Simons Foundation and Paris-Saclay article confirm Alain Aspect as PhD advisor.

- **`education[0].institution`**: Université Paris-Sud / Laboratoire Charles Fabry
  - Source 1: Confirmed.

- **`postdocs[0]`**: NIST, William D. Phillips, ~2000–2003
  - Sources 1, 3: Simons Foundation and Paris-Saclay article both state postdoc at NIST with W.D. Phillips after 2000 PhD.

- **`thesis.title`**: "Piégeage magnétique d'un gaz d'hélium métastable"
  - Source 2 (CNRS page): PhD subject described as "magnetic trapping of metastable helium gas."

- **`affiliations[0]`**: Pasqal, Co-founder and Scientific Advisor
  - Sources 1, 3: Multiple sources confirm 2019 founding of Pasqal with Georges-Olivier Reymond.

- **`key_papers[0]`**: "Observation of collective excitation of two individual atoms in the Rydberg blockade regime", Nature Physics 5, 115–118 (2009), DOI: 10.1038/nphys1183
  - Authors: Gaëtan, Miroshnychenko, Wilk et al. (Browaeys senior/corresponding author)
  - Source: Web search confirmed full citation.

- **`key_papers[1]`**: "Entanglement of two individual neutral atoms using Rydberg blockade", Phys. Rev. Lett. 104, 010502 (2010), DOI: 10.1103/PhysRevLett.104.010502
  - Authors: Wilk, Gaëtan, Evellin, Wolters, Miroshnychenko, Grangier, Browaeys
  - Source: arXiv:0908.0454 confirmed full citation.

- **`key_papers[2]`**: "An atom-by-atom assembler of defect-free arbitrary two-dimensional atomic arrays", Science 354, 1021–1023 (2016), DOI: 10.1126/science.aah3778
  - Authors: Barredo, de Léséleuc, Lienhard, Lahaye, Browaeys
  - Source: Web search and PubMed confirmed.

- **`key_papers[3]`**: "Many-body physics with individually controlled Rydberg atoms", Nature Physics 16, 132–142 (2020), DOI: 10.1038/s41567-019-0733-z
  - Authors: Browaeys, Lahaye (review article, Browaeys first author)
  - Source: Web search confirmed volume, pages, DOI.

- **`key_papers[4]`**: "Quantum simulation of 2D antiferromagnets with hundreds of Rydberg atoms", Nature 595, 233–238 (2021), DOI: 10.1038/s41586-021-03585-1
  - Authors: Scholl, Schuler, Williams, Eberharter, Barredo, Schymik, Lienhard, Henry, Lang, Lahaye, Läuchli, Browaeys
  - Source: Web search confirmed full citation.

- **`lineage_check.advisor_verified`**: true — Alain Aspect confirmed by multiple sources.
- **`lineage_check.postdoc_verified`**: true — NIST / W.D. Phillips confirmed by multiple sources.

## Data quality notes

- Location corrected from Paris (OpenAlex geocode) to Palaiseau. Institut d'Optique is in Palaiseau (~25 km south of Paris).
- `since_year` set to 2013 (promotion to Directeur de recherche). Joined CNRS initially in 2003.
- The 256-atom programmable quantum simulator paper (Ebadi et al., Nature 2021, DOI: 10.1038/s41586-021-03582-4) was excluded — it is a Harvard/MIT-led experiment; Browaeys is not a co-author.
- `verification_source_count`: 5 (Université Paris-Saclay, CNRS page, Simons Foundation, Optica biography, Institut d'Optique team page).
