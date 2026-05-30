# Evidence Map — Ronald Hanson (112-ronald-hanson)

*   **`current_position.title`**: "Distinguished Professor in Quantum Computing and Quantum Internet"
    *   *Source*: https://qutech.nl/2020/12/04/professor-ronald-hanson-appointed-distinguished-professor-in-quantum-computing-and-quantum-internet/ (QuTech press release, December 2020)
    *   *Quote*: "Professor Ronald Hanson appointed Distinguished Professor in Quantum Computing and Quantum Internet"
*   **`current_position.institution`**: "Delft University of Technology"
    *   *Source*: https://qutech.nl/person/ronald-hanson/ (QuTech person profile)
    *   *Note*: OpenAlex shows "Stanford" as a stale affiliation; QuTech/TU Delft is confirmed as his current institution.
*   **`current_position.confidence`**: "confirmed"
    *   *Source*: https://qutech.nl/person/ronald-hanson/ (institutional page, direct listing)
*   **`current_position.since_year`**: 2012
    *   *Source*: https://qutech.nl/2020/12/04/professor-ronald-hanson-appointed-distinguished-professor-in-quantum-computing-and-quantum-internet/ (QuTech press release)
    *   *Quote*: Appointed Antoni van Leeuwenhoek Professor in 2012 (full professor). Distinguished Professor title added in 2020.
*   **`links.group_page`**: https://qutech.nl/lab/hanson-lab/
    *   *Source*: https://qutech.nl/person/ronald-hanson/ (QuTech person profile — lab link)
*   **`links.institution_profile`**: https://qutech.nl/person/ronald-hanson/
    *   *Source*: Direct URL confirmed by fetch.
*   **`education[0]`**: "PhD, Delft University of Technology, 2005"
    *   *Source*: https://en.wikipedia.org/wiki/Ronald_Hanson (Wikipedia — pointer)
    *   *Quote*: "graduated with a PhD in physics from Delft University of Technology in 2005"
    *   *Source*: https://arxiv.org/abs/cond-mat/0610433 (PhD review paper on quantum dots, co-authored with Kouwenhoven)
*   **`education[0].advisor`**: "Leo Kouwenhoven"
    *   *Source*: https://en.wikipedia.org/wiki/Ronald_Hanson (Wikipedia — pointer)
    *   *Quote*: "supervised by Leo Kouwenhoven"
    *   *Note*: Leo Kouwenhoven is NOT in the ionlandscape database (IDs 080–175 searched; no match found). `advisor_id` set to null.
*   **`key_papers[0]`**: "Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres" (2015)
    *   *Source*: https://www.nature.com/articles/nature15759 (Nature journal page)
    *   *Quote*: Nature 526, 682–686 (2015); lead author B. Hensen, R. Hanson last/senior author
    *   DOI: 10.1038/nature15759
*   **`key_papers[1]`**: "Unconditional quantum teleportation between distant solid-state quantum bits" (2014)
    *   *Source*: https://www.science.org/doi/abs/10.1126/science.1253512 (Science journal page)
    *   *Quote*: Science, Vol. 345, 2014; lead author W. Pfaff, R. Hanson senior/corresponding author
    *   DOI: 10.1126/science.1253512
*   **`key_papers[2]`**: "Realization of a multinode quantum network of remote solid-state qubits" (2021)
    *   *Source*: https://www.science.org/doi/10.1126/science.abg1919 (Science journal page)
    *   *Quote*: Science, Vol. 372, Issue 6539, April 2021; lead author M. Pompili, R. Hanson senior author
    *   DOI: 10.1126/science.abg1919
*   **`key_papers[3]`**: "Spins in few-electron quantum dots" (2007)
    *   *Source*: https://link.aps.org/doi/10.1103/RevModPhys.79.1217 (Rev. Mod. Phys. journal page)
    *   *Quote*: Rev. Mod. Phys. 79, 1217 (2007); R. Hanson is first author
    *   DOI: 10.1103/RevModPhys.79.1217
*   **`key_papers[4]`**: "Quantum internet — a vision for the road ahead" (2018)
    *   *Source*: https://www.science.org/doi/10.1126/science.aam9288 (Science journal page)
    *   *Quote*: Science, Vol. 362, 2018; authors include S. Wehner, D. Elkouss, R. Hanson
    *   DOI: 10.1126/science.aam9288
*   **`lineage_check.advisor_verified`**: false
    *   *Note*: Leo Kouwenhoven is confirmed as advisor via Wikipedia and search results, but he does not appear in the ionlandscape database (no file matching "kouwenhoven" found in content/people/). He works on topological/Majorana qubits (not NV centers), explaining his absence from the NV/SC wave.
*   **`lineage_check.postdoc_verified`**: false
    *   *Note*: Postdoc at University of California, Santa Barbara (2005–2007) with David Awschalom confirmed (Wikipedia). Awschalom IS in the database as 115-d-d-awschalom.md, but postdoc supervisor field is not modeled in current schema.
*   **`verification_source_count`**: 4
    *   *Sources used*: (1) QuTech person profile + press release, (2) Wikipedia (Ronald Hanson), (3) Science/Nature journal DOI pages, (4) arXiv/Rev. Mod. Phys. for early papers

## Data quality notes

- **Distinguished Professor title**: Appointed December 2020; previously held Antoni van Leeuwenhoek full professorship since 2012 and was QuTech Scientific Director 2017–2020 (founding PI since 2014).
- **OpenAlex stale affiliation**: OpenAlex shows Stanford as affiliation — this is stale data from QFARM seminar or visiting period. Confirmed Delft/QuTech as current institution.
- **PhD advisor**: Leo Kouwenhoven confirmed via Wikipedia and the 2007 Rev. Mod. Phys. review paper co-authored with Kouwenhoven. No thesis record directly accessed.
- **Postdoc with Awschalom**: Ronald Hanson did a postdoc at UCSB with David Awschalom (2005–2007). Awschalom is in the database as 115-d-d-awschalom but the current schema does not have a `postdocs[]` array; not added to education[].
- **QuTech founding**: One of four founding professors when QuTech was established in 2014; served as Scientific Director 2016/2017–2020; first QDNL Executive Board chairman 2021–2023; co-founded Delft Networks startup 2024.
- **Bell test paper role**: B. Hensen is lead author; R. Hanson is the senior/PI author on the paper. Role set to `senior_author`.
