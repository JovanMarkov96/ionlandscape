# Evidence Map — 204-nir-davidson (Nir Davidson)

Verified: 2026-05-31

## Source list

1. **Weizmann Lab Homepage** (`complex/NirDavidson/home`): Current position, department, and research areas.
2. **OpenAlex** (`A5029308836`, ORCID `0000-0001-7526-851X`): Metrics, topics, publication record.
3. **Press / biographical search**: Stanford postdoc with Steven Chu, dark-trap work, Q-Factor co-founding.

## Field-level evidence

*   **`current_position`**: Professor of Physics, Department of Physics of Complex Systems, Weizmann Institute of Science.
    *   *Source*: Weizmann lab homepage. Former Dean of the Faculty of Physics.

*   **`postdocs[0]`**: Stanford University, Steven Chu.
    *   *Source*: Weizmann Wonder Wander ("Absolute Zero") and multiple bios — he first demonstrated the blue-detuned "dark trap" as a postdoc in Steve Chu's lab at Stanford, working alongside Mark Kasevich and Charles Adams.

*   **`education[1]` (PhD)**: Weizmann Institute of Science — marked `confidence: reported`.
    *   *Source*: Inferred from his early publication record in diffractive/laser optics with Asher A. Friesem and Erez Hasman (e.g. "Holographic axilens", Opt. Lett. 1991). Advisor not independently confirmed; flagged for Wave-3 verification.

*   **`affiliations[0]`**: Q-Factor, Co-founder. Linked to `c018-q-factor`.
    *   *Source*: Q-Factor stealth-emergence coverage (2026); company file lists him among founders.

*   **`key_papers[0]`**: "Long Atomic Coherence Times in an Optical Dipole Trap" (PRL 1995) — co_author, his Stanford postdoc landmark. DOI: 10.1103/PhysRevLett.74.1311
*   **`key_papers[1]`**: "Excitation Spectrum of a Bose-Einstein Condensate" (PRL 2002) — senior author. DOI: 10.1103/PhysRevLett.88.120407
*   **`key_papers[2]`**: "Observing Geometric Frustration with Thousands of Coupled Lasers" (PRL 2013) — senior author. DOI: 10.1103/PhysRevLett.110.184102

*   **`metrics`**: h-index 52, 8916 citations, 452 works (OpenAlex, 2026-05-31).

## Data quality notes

*   **`education` PhD advisor/year**: not confirmed; inferred from co-authorship. `lineage_check.advisor_verified: false`.
*   **`postdocs[0].years`**: unknown — exact Stanford dates not located.
