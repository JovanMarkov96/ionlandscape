# Evidence Map — Christopher R. Monroe (004-christopher-monroe)

Primary authoritative source for the 2026-06-04 deep enrichment: Monroe's own CV,
**https://iontrap.duke.edu/files/2025/03/Monroe_CV-Mar2025.pdf** (Mar 2025). Wikipedia
and the Duke ECE profile corroborate. Quotes below are from the CV unless noted.

## Source list
- Duke CV (Mar 2025): https://iontrap.duke.edu/files/2025/03/Monroe_CV-Mar2025.pdf
- Duke ECE profile: https://ece.duke.edu/people/christopher-monroe/
- Lab site: https://iontrap.duke.edu/
- Duke Quantum Center: https://quantum.duke.edu/
- IonQ: https://www.ionq.com/company
- Wikipedia: https://en.wikipedia.org/wiki/Christopher_Monroe

## Field-level evidence

* **`current_position`**: "Gilhuly Family Presidential Distinguished Professor; Professor of Electrical and Computer Engineering and Physics; Founding Director, Duke Quantum Center" (Duke, since 2021)
    * *Quote (CV, Positions)*: "2021– Duke Quantum Center — Founding Director"; "2021– Duke University — Gilhuly Family Presidential Distinguished Professor"; "Professor of Physics"; "Professor of Electrical and Computer Engineering".
* **`education[0]`**: "S.B., Physics, MIT, 1987 (Advisor: Michael Feld)"
    * *Quote (CV, Education)*: "1987 S.B., Physics, Massachusetts Institute of Technology, Cambridge MA (Advisor: Michael Feld)".
* **`education[1]`**: "Ph.D., Physics, University of Colorado Boulder, 1992 (Advisor: Carl Wieman)"
    * *Quote (CV, Education)*: "1992 Ph.D., Physics, University of Colorado, Boulder, CO (Advisor: Carl Wieman)". Thesis topic (laser cooling/trapping of cesium toward BEC) inferred from his 1989–1993 Wieman-group cesium-trapping papers.
* **`postdocs[0]`**: "NIST Boulder — David J. Wineland — 1992–2000"
    * *Quote (CV, Positions)*: "1992–1994 National Inst. of Stand. Tech., Boulder — NRC Postdoctoral Researcher (Mentor: David Wineland)"; "1994–2000 — Staff Physicist and Project Leader".
    * Significance: Wineland shared the **2012 Nobel Prize in Physics**. Monroe was first author on the first quantum logic gate (1995) and first single-atom Schrödinger-cat state (1996) in Wineland's Ion Storage Group. Resolves to a `postdoc_advisor` edge → `006-david-wineland`.
* **Position history** (`Career` section in body):
    * *Quote (CV, Positions)*: Michigan "2000–2003 Associate Professor, Physics", "2003–2007 Professor, Physics", "2006–2007 Director, FOCUS"; Maryland "2007–2021 Bice Zorn Professor of Physics", "Fellow, Joint Quantum Institute (JQI)", "2014–2021 Fellow … (QuICS)", "2015–2021 Distinguished University Professor".
* **`affiliations[0]`**: "IonQ, Inc. — Co-founder and former Chief Scientist (2016–2023); CEO (2018–2019)"
    * *Quote (CV, Positions)*: "2016–2023 IonQ, Inc. — Co-Founder and Chief Scientist"; "2018–2019 — Chief Executive Officer". IonQ company page: "Founded in 2015 by Dr. Chris Monroe and Dr. Jungsang Kim".
* **`ion_species`**: ["171Yb+", "9Be+", "111Cd+", "138Ba+"]
    * 9Be+: NIST-era logic gate / cat-state work (CV pubs "Demonstration of a Universal Quantum Logic Gate", 1995).
    * 111Cd+ / Cd+: Michigan-era (CV pubs "Magneto-optical trapping of cadmium" 2007; "Sympathetic cooling of trapped Cd+ isotopes" 2002; "Zero-point cooling … of Trapped Cd+ ions" 2004).
    * 171Yb+: principal hyperfine qubit at Maryland/Duke (CV pubs "Manipulation and detection of a trapped Yb+ hyperfine qubit" 2007).
    * 138Ba+: dual-species networking co-ion (CV pubs on multi-species / dual-species modular networking, 2017–2025).
* **`applications`**: computing; simulation; networking; fundamental_physics; sensing_metrology
    * fundamental_physics: Bell-inequality tests ("Experimental Violation of a Bell's Inequality with Efficient Detection", Nature 2001; "Random Numbers Certified by Bell's Theorem", Nature 2010); CV "Foundations of Quantum Mechanics" research interest.
    * sensing_metrology: "entanglement-enhanced rotation angle estimation" (PRL 2001); "Heisenberg-Scaling Measurement Protocol … with Quantum Sensor Networks" (PRA 2019); single atoms as electric-field probes.
* **`key_papers`**: 10 landmark papers selected from the CV publication list (logic gate 1995, cat state 1996, atom–photon entanglement 2004, remote-ion entanglement 2007, teleportation 2009, Bell-certified RNG 2010, modular architecture 2014, programmable QC 2016, discrete time crystal 2017, 53-qubit simulator 2017). DOIs are standard publisher DOIs for the cited PRL/Science/Nature/PRA articles.
* **Honors and awards** (body `Selected honors and awards`):
    * *Quote (CV, Fellowships and Awards)*: "Member, National Academy of Sciences (2016)"; "American Physical Society Arthur Schawlow Prize for Laser Science (2015)"; "American Physical Society I.I. Rabi Award (2001)"; "US Presidential Early Career Award for Scientists and Engineers (1997)"; "Willis E. Lamb Award … (2019)"; "Fellow, Optical Society of America (2020)"; "Fellow, AAAS (2012)"; "Fellow, APS (2005)"; "Fellow, UK Institute of Physics (2002)"; "International Quantum Communication Award, Tamagawa University, Japan (2000)".
* **`metrics`**: unchanged (OpenAlex snapshot, h_index 92 / citations 49278, retrieved 2026-05-25). Note: Monroe's own CV self-reports ≈70,000 citations and h≈110 (2025); the OpenAlex figures are kept for cross-dataset consistency.
* **`links`**: added `duke_quantum_center` (https://quantum.duke.edu/); others carried over and re-verified.

## Data quality notes
- Location lat/lon carried over from prior data (Durham, NC); not re-geocoded this pass.
- PhD thesis exact title not located; topic recorded in `thesis.note` / `education[1].note` from his cesium-trapping publication record.
- `metrics` and `key_papers` are curated source-of-truth in the .md only; they are not serialized into people.json by the build.
- No Nobel Prize for Monroe himself; the Nobel link is via his postdoc mentor David Wineland (2012).
