---
aliases:
- Quandela SAS
applications:
- computing
- simulation
- software_control
approach:
  architecture_tags:
  - semiconductor_quantum_dot
  - single_photon_source
  - linear_optical_qc
  - photonic_integrated_circuits
  - boson_sampling
  - spoqc
  - spin_optical_quantum_computing
  - hybrid_quantum_classical
  differentiators:
  - Near-unity indistinguishability eDelight quantum-dot single-photon sources --
    InGaAs quantum dots embedded in photonic cavities, fabricated at Quandela's Massy
    cleanroom -- provide the brightest and most indistinguishable solid-state photon
    sources commercially available, underpinning all Quandela QPUs
  - 'Full-stack, data-centre-compatible systems: MosaiQ-series quantum computers are
    air-cooled (8 kW), require no vibration isolation, and install in any data centre
    alongside classical HPC -- Belenos (12 qubits) achieves 99.6% single-qubit and
    99.0% two-qubit gate fidelity at 576 QOPS'
  - Lucy (12-qubit Belenos variant), delivered to EuroHPC and GENCI at CEA's TGCC
    (October 2025), is the world's most powerful photonic quantum computer in an HPC
    supercomputing environment and Europe's first photonic QPU integrated with a Tier-0
    supercomputer
  - Open-source Perceval SDK (Python) provides a hardware-agnostic photonic quantum
    programming framework supporting Quandela cloud QPUs, simulators, and third-party
    backends; 202+ GitHub stars and 37 releases (v1.2.1 as of May 2026)
  - SPOQC (Spin-Optical Quantum Computing) long-term fault-tolerance roadmap targets
    ~100,000x component reduction relative to all-photonic error-correction schemes,
    leveraging spin-qubit integration with photonic circuits
  elevator_pitch: Quandela (founded 2017, Massy; spun out of CNRS C2N, Palaiseau)
    is a full-stack French photonic quantum computing company building semiconductor
    quantum-dot single-photon sources and MosaiQ-series photonic quantum computers.
    Its Belenos QPU (12 qubits, 99.6%/99.0% gate fidelity, 576 QOPS) was delivered
    to CEA's TGCC for EuroHPC as Lucy in October 2025 -- the world's most powerful
    photonic QPU in an HPC environment. Quandela offers cloud access via OVHcloud
    and its own cloud platform (2,400+ users), and the open-source Perceval SDK. The
    company has raised EUR 68.5M+ (seed EUR 15M 2021, Series A EUR 53.5M 2023), employs
    130+ FTE, and operates two manufacturing plants in the Paris-Saclay area.
customers:
- OVHcloud (France)
- Exaion / EDF Group (Canada)
- EuroHPC Joint Undertaking / GENCI at CEA-TGCC (France)
entity_type: company
founded_year: 2017
funding:
  rounds:
  - amount_usd: 16400000
    date: '2021-11-16'
    lead_investor: Omnes
    notes: €15M (~$16.4M USD); announced November 16, 2021; to develop first cloud-accessible
      photonic quantum computer by 2022.
    other_investors:
    - Fonds Innovation Défense (Bpifrance / Agence de l'innovation de défense)
    - Quantonation
    round: Seed
    source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
    stage: seed
  - amount_usd: 57800000
    date: '2023-11-07'
    lead_investors:
    - SERENA
    - Crédit Mutuel Innovation
    notes: €53.5M (~$57.8M USD); 2nd-largest quantum financing round in the EU in
      2023; company had 73 employees at close; aligned with France 2030 initiative.
    other_investors:
    - Omnes
    - Bpifrance (Fonds Innovation Défense)
    - Quantonation
    round: Series A
    source: https://www.frenchweb.fr/serie-a-50-millions-deuros-pour-quandela-afin-daccelerer-le-developpement-de-ses-ordinateurs-quantiques-photoniques/460000
    stage: series_a
  total_raised_usd: 74200000
id: c034-quandela
last_verified_at: '2026-05-30'
links:
  linkedin: https://www.linkedin.com/company/quandela
  news: https://quandela.com/news/
  website: https://quandela.com
location:
  address: 7, Rue Léonard de Vinci, 91300 Massy, France
  city: Massy
  country: France
  lat: 48.7258
  lon: 2.266
  precision: building
  region: Île-de-France
media:
  logo_path: /logos/c034-quandela.png
milestones:
- claim: Quandela SAS founded in Palaiseau (Paris-Saclay) as a spin-out of the Centre
    de Nanosciences et de Nanotechnologies (C2N, CNRS / Université Paris-Saclay) by
    Pascale Senellart, Valérian Giesz, and Niccolo Somaschi, commercialising solid-state
    quantum-dot single-photon sources developed in Senellart's CNRS research group.
  date: '2017-01-01'
  source: https://www.serena.vc/portfolio/quandela
- claim: Raised €15M seed round (led by Omnes, with Fonds Innovation Défense managed
    by Bpifrance / AID, and Quantonation) to develop Europe's first cloud-accessible
    photonic quantum computer; Quandela employed ~20 people at this stage; planned
    first cloud-deployed quantum computer by end of 2022.
  date: '2021-11-16'
  source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
- claim: Released Perceval, an open-source Python SDK for programming photonic quantum
    circuits and accessing Quandela QPUs via cloud; the framework is hardware-agnostic
    and supports both simulation and real hardware execution through Quandela Cloud.
  date: '2022-09-01'
  source: https://github.com/Quandela/Perceval
- claim: Launched MosaiQ — a modular photonic quantum computer platform (6–24 qubits)
    — and Ascella (MosaiQ 6), a 6-qubit photonic QPU accessible via the Quandela Cloud
    platform; Ascella became the first European photonic quantum computer deployed
    outside a laboratory and accessible online.
  date: '2022-10-01'
  source: https://www.serena.vc/portfolio/quandela
- claim: Inaugurated Europe's first cloud-based quantum computing service in partnership
    with OVHcloud, providing public access to the Ascella (6-qubit) QPU via cloud.quandela.com;
    first commercial photonic quantum computing cloud service in Europe.
  date: '2023-02-22'
  source: https://postquantum.com/quantum-computing-companies/quandela/
- claim: 'First industrial sale of a MosaiQ system: OVHcloud became the first private-sector
    customer to purchase and host a Quandela MosaiQ quantum computer in their data
    centre, integrating it into OVHcloud''s Quantum-as-a-Service platform.'
  date: '2023-09-01'
  source: https://www.serena.vc/portfolio/quandela
- claim: Raised €53.5M Series A (led by SERENA and Crédit Mutuel Innovation, with
    Omnes, Bpifrance / Fonds Innovation Défense, and Quantonation participating) —
    described as the 2nd-largest quantum tech financing round in the EU in 2023; at
    closing the company employed 73 people and operated under the France 2030 initiative.
  date: '2023-11-07'
  source: https://www.frenchweb.fr/serie-a-50-millions-deuros-pour-quandela-afin-daccelerer-le-developpement-de-ses-ordinateurs-quantiques-photoniques/460000
- claim: Opened a dedicated quantum computer assembly and manufacturing facility in
    Massy (Paris-Saclay area), establishing Quandela's first industrial cleanroom
    for eDelight single-photon source fabrication and QPU integration; production
    capacity targeted at ~4 complete quantum computers per year from 2025.
  date: '2023-12-01'
  source: https://postquantum.com/quantum-computing-companies/quandela/
- claim: Deployed a MosaiQ system at the Exaion (EDF Group subsidiary) data centre
    in Sherbrooke, Canada — the company's first international deployment and first
    quantum computer installation in North America — as part of Quandela's Canada
    expansion.
  date: '2024-01-01'
  source: https://postquantum.com/quantum-computing-companies/quandela/
- claim: Received the "Breakthrough Deep Tech Innovation" award at La French Tech
    2024 ceremony, recognising Quandela as a leading French deep-tech company.
  date: '2024-10-01'
  source: https://postquantum.com/quantum-computing-companies/quandela/
- claim: Launched Belenos (MosaiQ 12) — a 12-qubit second-generation photonic quantum
    computer with 12 fully entangled qubits, 99.6% single-qubit gate fidelity, 99.0%
    two-qubit gate fidelity, 576 QOPS, 24 modes with all-to-all connectivity, and
    8 kW power consumption — offering 4,000x more computing power than MosaiQ-6 Ascella;
    made available on Quandela Cloud to 1,200+ registered users across 30 countries.
  date: '2025-05-01'
  source: https://quandela.com/news/belenos/
- claim: Delivered Lucy — a 12-qubit photonic quantum computer (Belenos variant, with
    cryogenic modules by attocube systems) — to CEA's Très Grand Centre de calcul
    (TGCC) for EuroHPC Joint Undertaking and GENCI under the EuroQCS-France consortium;
    Lucy is the world's most powerful photonic quantum computer in an HPC supercomputing
    environment; 80% European components; assembled in 12 months at Quandela's Massy
    and Palaiseau facilities; integration with the Joliot-Curie supercomputer underway.
  date: '2025-10-23'
  source: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
- claim: Lucy officially inaugurated at CEA's TGCC by French Minister Anne Le Hénanff
    and Bruno Bonnell; presented as the world's most powerful photonic quantum computer;
    integrated with the Joliot-Curie supercomputer for hybrid HPC-quantum workflows
    under the France 2030 initiative and EuroHPC program; freely accessible to European
    research and industry.
  date: '2026-04-14'
  source: https://quandela.com/news/
- claim: Belenos made available on OVHcloud's Quantum Platform with pay-as-you-go
    per-second billing, extending European sovereign cloud quantum access to OVHcloud's
    enterprise customer base; second Quandela QPU deployed on the OVHcloud QaaS platform
    after MosaiQ 6.
  date: '2026-04-17'
  source: https://quandela.com/news/
- claim: Appointed Cyril Dujardin (COO, 25+ years in deep tech / critical infrastructure)
    and Michel Zecri (VP Industrialization, 20+ years in semiconductors and aerospace
    manufacturing) to the leadership team; Michel Paulin appointed Chairman of the
    Board to support industrial scale-up phase.
  date: '2026-05-29'
  source: https://quandela.com/news/
modality: both
name: Quandela
offices:
- function: r_and_d
  location:
    city: Palaiseau
    country: France
    region: Île-de-France
  source: https://quandela.com/about/
- function: manufacturing
  location:
    city: Massy
    country: France
    region: Île-de-France
  source: https://postquantum.com/quantum-computing-companies/quandela/
- function: r_and_d
  location:
    city: Munich
    country: Germany
    region: Bavaria
  source: https://www.linkedin.com/company/quandela/
partnerships:
- name: OVHcloud
  source: https://quandela.com/news/
  type: go_to_market
- name: EuroHPC Joint Undertaking
  source: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
  type: customer
- name: GENCI
  source: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
  type: customer
- name: CEA (Commissariat à l'énergie atomique et aux énergies alternatives)
  source: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
  type: customer
- name: Exaion (EDF Group)
  source: https://postquantum.com/quantum-computing-companies/quandela/
  type: customer
- name: attocube systems
  source: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
  type: supply
- name: Mila (Quebec AI Institute)
  source: https://quantumcomputingreport.com/quandela-mila-qml/
  type: research
- name: Safran
  source: https://quandela.com/news/
  type: research
- name: Seoul National University (ISRC)
  source: https://quandela.com/news/
  type: research
- name: CNRS / C2N
  source: https://postquantum.com/quantum-computing-companies/quandela/
  type: research
people:
  founders:
  - name: Pascale Senellart
    person_id: 180-pascale-senellart
    role: Co-founder and Chief Scientific Officer
    source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
  - name: Valérian Giesz
    role: Co-founder
    source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
  - name: Niccolo Somaschi
    role: Co-founder and CEO
    source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
  headcount: 130
  headcount_retrieved_at: '2026-05-30'
  headcount_source: https://quandela.com/about/
  leadership:
  - name: Niccolo Somaschi
    role: Co-founder and CEO
    source: https://quandela.com/news/belenos/
  - name: Pascale Senellart
    person_id: 180-pascale-senellart
    role: Co-founder and Chief Scientific Officer
    source: https://www.serena.vc/portfolio/quandela
  - name: Jean Senellart
    role: Co-founder and CTO
    source: https://www.linkedin.com/company/quandela/
  - name: Cyril Dujardin
    role: Chief Operating Officer
    source: https://quandela.com/news/
  - name: Michel Zecri
    role: Vice President of Industrialization
    source: https://quandela.com/news/
  - name: Michel Paulin
    role: Chairman of the Board
    source: https://quandela.com/news/
  spun_out_of:
  - name: Centre National de la Recherche Scientifique
    source: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
    spinout_year: 2017
  - name: Centre National de la Recherche Scientifique
    source: https://www.quantonation.com/portfolio/quandela/
    spinout_year: 2017
platforms:
- photonic
products:
- description: InGaAs quantum-dot single-photon source product for researchers; produces
    near-unity indistinguishability photons from electrically controlled semiconductor
    quantum dots embedded in photonic cavities; plug-and-play benchtop unit; predecessor
    commercial name was Fresnel before rebranding to Prometheus. Supplies the photon
    sources used in all MosaiQ QPUs.
  name: Prometheus
  release_date: '2020-01-01'
  source: https://quandela.com/products/
  stage: ga
- description: Open-source Python framework for programming photonic quantum circuits,
    simulating algorithms, and accessing Quandela QPUs via cloud API. Supports linear-optics
    circuit design, state-vector simulation, hybrid quantum-classical workflows, and
    Qiskit/myQLM interoperability. 202 GitHub stars, 37 releases (v1.2.1 as of May
    2026). Repository at github.com/Quandela/Perceval.
  name: Perceval SDK
  release_date: '2022-09-01'
  source: https://github.com/Quandela/Perceval
  stage: ga
- description: First MosaiQ QPU — 6-qubit (6-mode) photonic quantum computer; first
    European photonic QPU deployed outside a laboratory and accessible via cloud;
    hosted on Quandela Cloud and OVHcloud; launched October 2022, first European cloud
    quantum service February 2023. Succeeded by Belenos.
  name: Ascella (MosaiQ 6)
  release_date: '2022-10-01'
  source: https://www.serena.vc/portfolio/quandela
  stage: deprecated
- description: Second-generation photonic quantum computer — 12 fully entangled photonic
    qubits, 24 modes with all-to-all connectivity, 99.6% single-qubit gate fidelity,
    99.0% two-qubit gate fidelity, 576 QOPS, 8 kW power, air-cooled and data-centre
    compatible; 4,000x more computing power than Ascella. Available on Quandela Cloud
    and OVHcloud with pay-as-you-go pricing. The EuroHPC Lucy installation is a Belenos
    variant equipped with attocube cryogenic modules.
  name: Belenos (MosaiQ 12)
  release_date: '2025-05-01'
  source: https://quandela.com/news/belenos/
  stage: ga
- description: Third-generation photonic quantum computer (24 qubits), available for
    on-premises delivery. Part of the MosaiQ modular platform. Lead time 8–10 months
    for bespoke configurations.
  name: Canopus (MosaiQ 24)
  release_date: '2025-01-01'
  source: https://quandela.com/products/
  stage: limited_release
- description: Quantum-certified random number generator product based on photon entanglement
    from Quandela's single-photon sources; for cybersecurity applications.
  name: Entropy
  release_date: '2024-01-01'
  source: https://quandela.com/products/
  stage: ga
qubit_type: Photonic (quantum-dot single-photon)
roadmap:
- source: https://postquantum.com/quantum-computing-companies/quandela/
  target_claim: Demonstrate first logical qubit using SPOQC (Spin-Optical Quantum
    Computing) architecture, combining spin qubits with photonic circuits.
  target_date: '2025-12-31'
- source: https://www.linkedin.com/company/quandela/
  target_claim: Begin operations at planned 1,000 m² semiconductor manufacturing facility
    in Munich, Germany — targeting process-compatible photonic quantum chip production
    in partnership with Korean and European semiconductor infrastructure.
  target_date: '2026-12-31'
- source: https://postquantum.com/quantum-computing-companies/quandela/
  target_claim: Deliver error-correction compilers and decoders; second Massy manufacturing
    facility operational, scaling production to meet growing on-premises QPU demand.
  target_date: '2027-12-31'
- source: https://postquantum.com/quantum-computing-companies/quandela/
  target_claim: Deploy ~50 logical qubits; enable multi-processor networking for distributed
    photonic quantum computing.
  target_date: '2028-12-31'
- source: https://postquantum.com/quantum-computing-companies/quandela/
  target_claim: Operate hundreds of logical qubits in a fault-tolerant, universal
    photonic quantum computer using the SPOQC architecture — a 100,000x component
    reduction vs. all-photonic error-correction approaches.
  target_date: '2030-12-31'
schema_version: 1
short_summary: Quandela (founded 2017, Massy; CNRS C2N spin-out) is a full-stack French
  photonic quantum computing company specialising in semiconductor quantum-dot single-photon
  sources and MosaiQ-series photonic quantum computers. Its Belenos QPU (12 qubits,
  99.6%/99.0% gate fidelity, 576 QOPS) was delivered to CEA's TGCC for EuroHPC as
  Lucy in October 2025 — the world's most powerful photonic QPU in an HPC supercomputing
  environment. Quandela provides cloud access via OVHcloud and its own platform (2,400+
  users) and the open-source Perceval SDK. Co-founded by Pascale Senellart (CNRS,
  also in our DB as 180-pascale-senellart), Valérian Giesz, and Niccolo Somaschi (CEO),
  the company has raised €68.5M+ (Seed €15M 2021; Series A €53.5M 2023) and employs
  130+ FTE across two production plants.
sort_name: Quandela
sources:
- note: Seed round November 16, 2021; €15M; Omnes (lead), Fonds Innovation Défense
    (Bpifrance/AID), Quantonation; three founders named (Senellart, Giesz, Somaschi);
    Senellart's CNRS silver medal noted; ~20 employees at round; Prometheus product
    mentioned; planned QPU cloud by 2022
  url: https://www.frenchweb.fr/quandela-leve-15-millions-deuros-pour-proposer-un-premier-ordinateur-quantique-photonique-en-2022/436734
- note: Series A November 7, 2023; €53.5M; SERENA + Crédit Mutuel Innovation (co-leads);
    Omnes, Bpifrance/AID, Quantonation (returning); 73 employees at close; France
    2030; 2nd-largest EU quantum round in 2023; founders re-confirmed
  url: https://www.frenchweb.fr/serie-a-50-millions-deuros-pour-quandela-afin-daccelerer-le-developpement-de-ses-ordinateurs-quantiques-photoniques/460000
- note: Investor portfolio page; all three founders confirmed (Somaschi, Senellart,
    Giesz); Ascella first cloud QPU outside lab (fall 2022); first industrial sale
    to OVHcloud (fall 2023); partners include EDF, MBDA, ONERA; SERENA Bertrand Diard
    quote on photonics approach
  url: https://www.serena.vc/portfolio/quandela
- note: Comprehensive profile — founding at C2N/CNRS, Massy HQ, 100+ employees (2024);
    product line (MosaiQ 6/12/24, Prometheus, Perceval, Entropy); Exaion/EDF Sherbrooke
    deployment; cleanroom facility (late 2023); DGA PROQCIMA selection (2024); SPOQC
    fault-tolerance roadmap; performance metrics (99.6%/99.0% fidelity, 576 QOPS);
    Munich second factory planned 2027; 4 QPUs deployed as of 2024
  url: https://postquantum.com/quantum-computing-companies/quandela/
- note: Official about page — 130+ FTE, 2 manufacturing plants, 5 deployed QCs, 2,392
    cloud users, 15+ corporate clients, 70+ papers/patents; eDelight as core technology;
    HQ in Massy
  url: https://quandela.com/about/
- note: Belenos (MosaiQ 12) product page — 12 qubits, 24 modes, 99.6%/99.0% fidelity,
    576 QOPS, 8 kW air-cooled; Perceval/Qiskit/myQLM compatible; 4,000x vs MosaiQ-6;
    CEO Somaschi quote; cloud available
  url: https://quandela.com/news/belenos/
- note: Lucy delivery October 23, 2025; 12 photonic qubits; EuroHPC + GENCI (EuroQCS-France
    consortium); CEA TGCC; attocube cryogenic modules; assembled 12 months; 80% European
    components; Joliot-Curie integration; acceptance phase; full operation early 2026;
    University of Bucharest, ICHEC, Forschungszentrum Juelich in consortium
  url: https://thequantuminsider.com/2025/10/23/quandela-delivers-photonic-quantum-computer-to-eurohpc-and-genci-at-ceas-tgcc/
- note: 2026 news items — Lucy inauguration April 14, 2026; Belenos on OVHcloud April
    17, 2026; leadership appointments (Dujardin COO, Zecri VP Industrialization, Paulin
    Chairman) May 29, 2026; Safran AQeFLU partnership May 7, 2026; SNU ISRC MOU April
    3, 2026; Franco-German quantum declaration May 12, 2026
  url: https://quandela.com/news/
- note: Perceval open-source SDK; 202 stars; 37 releases; v1.2.1 latest (May 20, 2026);
    760 commits; Python; C-optimised simulation backends; linear optics circuit design
    and cloud QPU access
  url: https://github.com/Quandela/Perceval
- note: Product page — MosaiQ series (Ascella/Belenos/Canopus), Entropy RNG, Perceval
    SDK, Prometheus light sources, Merlin AI framework, Quantum Toolbox, cloud offers;
    8–10 month delivery lead time for bespoke systems
  url: https://quandela.com/products/
- note: C2N spin-off confirmed; €53.5M described as Series B (Quantonation label)
    and "2nd-largest EU quantum round in 2023"; full-stack model; 2030 scalable industrial
    target
  url: https://www.quantonation.com/portfolio/quandela/
- note: HQ confirmed 7 Rue Léonard de Vinci, Massy 91300; 152 employees on LinkedIn
    (May 2026); founding 2017; Jean Senellart in leadership; Munich manufacturing
    site planned (1,000 m², early 2027); 2,500+ cloud users; OVHcloud, CEA, EuroHPC
    deployments confirmed
  url: https://www.linkedin.com/company/quandela/
status:
  operating_status: private
updated_at: '2026-05-30'
verification_source_count: 12
---