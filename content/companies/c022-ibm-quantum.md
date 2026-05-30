---
aliases:
- IBM Quantum
- IBM Q
- IBM Q Network
- IBM Quantum Experience
applications:
- computing
- simulation
approach:
  architecture_tags:
  - transmon
  - heavy_hex_lattice
  - fixed_frequency_qubits
  - tunable_couplers
  - modular_architecture
  differentiators:
  - First to offer cloud-accessible quantum computing to the public (IBM Quantum Experience,
    May 2016), democratising access to quantum hardware worldwide
  - Largest open-source quantum software ecosystem via Qiskit — over 6 million installs
    and 300,000 installations per month as of 2025
  - Demonstrated evidence for quantum utility on a 127-qubit Eagle processor in Nature
    (June 2023), executing circuits beyond the reach of brute-force classical simulation
  - IBM Quantum System Two (Yorktown Heights, 2023) is the industry's first modular
    quantum computer, housing three Heron processors with a shared cryogenic infrastructure
  - Publicly committed roadmap to quantum-centric supercomputing extending to 2033
    (Starling 200-qubit / 100 M gates by 2029; Blue Jay 2,000-qubit / 1 B gates by 2033)
  elevator_pitch: IBM Quantum is IBM's quantum computing division, operating the world's
    largest fleet of cloud-accessible superconducting quantum processors and the Qiskit
    open-source software stack, pursuing a decade-long roadmap toward quantum-centric
    supercomputing.
entity_type: company
founded_year: 2016
id: c022-ibm-quantum
last_verified_at: '2026-05-30'
links:
  website: https://www.ibm.com/quantum
  wikipedia: https://en.wikipedia.org/wiki/IBM_Quantum_Platform
location:
  city: Yorktown Heights
  country: United States
  lat: 41.2034
  lon: -73.8688
  precision: city
  region: New York
milestones:
- date: '2016-05-04'
  claim: IBM launched IBM Quantum Experience — the first cloud-based service giving
    the public hands-on access to a real quantum processor (5 superconducting qubits)
    hosted at the T.J. Watson Research Center, Yorktown Heights.
  source: https://uk.newsroom.ibm.com/2016-May-04-IBM-Makes-Quantum-Computing-Available-on-IBM-Cloud-to-Accelerate-Innovation
- date: '2017-03-07'
  claim: Released Qiskit (Quantum Information Software Kit) as an open-source Python
    SDK, the first publicly available quantum software development kit, enabling users
    to build and run quantum circuits on IBM hardware and simulators.
  source: https://en.wikipedia.org/wiki/Qiskit
- date: '2017-12-14'
  claim: Launched the IBM Q Network — an ecosystem of Fortune 500 companies, academic
    institutions, and national labs (initial 12 members including JPMorgan Chase,
    Daimler, Samsung, Barclays, Oak Ridge National Lab, University of Oxford) with
    early commercial access to IBM Q systems.
  source: https://www.prnewswire.com/news-releases/ibm-announces-collaboration-with-leading-fortune-500-companies-academic-institutions-and-national-research-labs-to-accelerate-quantum-computing-300571228.html
- date: '2019-01-08'
  claim: Unveiled IBM Q System One at CES 2019 — the world's first integrated commercial
    quantum computing system, housing a 20-qubit processor in a 9-foot borosilicate
    glass enclosure designed for continuous operation outside a research lab.
  source: https://www.prnewswire.com/news-releases/ibm-unveils-worlds-first-integrated-quantum-computing-system-for-commercial-use-300774332.html
- date: '2020-08-20'
  claim: Achieved Quantum Volume 64 on a 27-qubit system — doubling the previous
    record of QV 32 — through a combination of dynamical decoupling, compiler optimisations,
    shorter two-qubit gates, and excited-state promoted readout.
  source: https://iopscience.iop.org/article/10.1088/2058-9565/abe519
- date: '2021-11-16'
  claim: Unveiled Eagle — IBM's first 127-qubit quantum processor and the first quantum
    chip whose state space cannot be reliably represented by a classical computer —
    at the IBM Quantum Summit 2021. Eagle introduced a multi-level wiring heavy-hexagonal
    lattice to minimise qubit crosstalk.
  source: https://newsroom.ibm.com/2021-11-16-IBM-Unveils-Breakthrough-127-Qubit-Quantum-Processor
- date: '2022-11-09'
  claim: Unveiled Osprey — a 433-qubit processor with more than three times the qubits
    of Eagle — at the IBM Quantum Summit 2022, alongside details of next-generation
    IBM Quantum System Two architecture for quantum-centric supercomputing.
  source: https://newsroom.ibm.com/2022-11-09-IBM-Unveils-400-Qubit-Plus-Quantum-Processor-and-Next-Generation-IBM-Quantum-System-Two
- date: '2023-06-14'
  claim: Published "Evidence for the utility of quantum computing before fault tolerance"
    in Nature — demonstrating that a 127-qubit Eagle processor could compute expectation
    values for a 2D Ising model at circuit depths beyond the reach of brute-force
    classical simulation.
  source: https://www.nature.com/articles/s41586-023-06096-3
- date: '2023-12-04'
  claim: Unveiled Condor (1,121-qubit, world's first quantum processor to exceed
    1,000 qubits) and Heron (133-qubit, 3–5x improvement in error performance over
    Eagle with tunable couplers), and announced IBM Quantum System Two — the first
    modular quantum computer — operational at Yorktown Heights with three Heron processors.
  source: https://newsroom.ibm.com/2023-12-04-IBM-Debuts-Next-Generation-Quantum-Processor-IBM-Quantum-System-Two,-Extends-Roadmap-to-Advance-Era-of-Quantum-Utility
modality: both
name: IBM Quantum
people:
  leadership:
  - name: Jay Gambetta
    role: VP of Quantum Computing (2019–2025); Director of IBM Research (from Oct 2025)
    source: https://en.wikipedia.org/wiki/Jay_Gambetta
  - name: Dario Gil
    role: Senior VP and Director of IBM Research
    source: https://newsroom.ibm.com/2022-11-09-IBM-Unveils-400-Qubit-Plus-Quantum-Processor-and-Next-Generation-IBM-Quantum-System-Two
platforms:
- superconducting
products:
- description: IBM's first 127-qubit superconducting transmon processor using a heavy-hexagonal
    lattice; introduced November 2021 as the first quantum chip exceeding 100 qubits.
    Quantum Volume 128. Used in the 2023 Nature quantum utility demonstration.
  name: Eagle
  stage: ga
  source: https://newsroom.ibm.com/2021-11-16-IBM-Unveils-Breakthrough-127-Qubit-Quantum-Processor
- description: 433-qubit superconducting processor announced November 2022; more
    than triple the qubits of Eagle with enhanced packaging and high I/O density.
  name: Osprey
  stage: deprecated
  source: https://newsroom.ibm.com/2022-11-09-IBM-Unveils-400-Qubit-Plus-Quantum-Processor-and-Next-Generation-IBM-Quantum-System-Two
- description: 1,121-qubit superconducting processor announced December 2023; the
    world's first processor to exceed 1,000 qubits, featuring a honeycomb heavy-hex
    layout and over a mile of high-density cryogenic flex wiring in a single dilution
    refrigerator. Research/demonstration device.
  name: Condor
  stage: deprecated
  source: https://newsroom.ibm.com/2023-12-04-IBM-Debuts-Next-Generation-Quantum-Processor-IBM-Quantum-System-Two,-Extends-Roadmap-to-Advance-Era-of-Quantum-Utility
- description: 133-qubit superconducting processor with fixed-frequency qubits and
    tunable couplers delivering 3–5x improvement in gate error performance over Eagle;
    backbone of IBM Quantum System Two (modular). Announced and made available December
    2023.
  name: Heron
  stage: ga
  source: https://newsroom.ibm.com/2023-12-04-IBM-Debuts-Next-Generation-Quantum-Processor-IBM-Quantum-System-Two,-Extends-Roadmap-to-Advance-Era-of-Quantum-Utility
- description: Open-source Python SDK for quantum computing, first released March
    2017. Enables circuit construction, compilation, execution on IBM hardware and
    simulators. Over 6 million installs as of 2025; de facto standard for gate-model
    quantum programming.
  name: Qiskit
  stage: ga
  source: https://en.wikipedia.org/wiki/Qiskit
- description: IBM's first modular quantum computer, operational at Yorktown Heights
    from December 2023. Houses multiple IBM Heron processors with shared cryogenic
    infrastructure; cornerstone of IBM's quantum-centric supercomputing architecture.
  name: IBM Quantum System Two
  stage: ga
  source: https://newsroom.ibm.com/2023-12-04-IBM-Debuts-Next-Generation-Quantum-Processor-IBM-Quantum-System-Two,-Extends-Roadmap-to-Advance-Era-of-Quantum-Utility
roadmap:
- target_date: '2029-12-31'
  target_claim: Deploy Starling — a 200-qubit processor capable of executing 100
    million gates — as a step toward fault-tolerant quantum computing (IBM Quantum
    Innovation Roadmap to 2029).
  source: https://arxiv.org/html/2410.00916v1
- target_date: '2033-12-31'
  target_claim: Deploy Blue Jay — a 2,000-qubit processor capable of executing 1
    billion gates — realising quantum-centric supercomputing at scale.
  source: https://arxiv.org/html/2410.00916v1
schema_version: 1
short_summary: IBM Quantum (est. 2016, Yorktown Heights NY) is IBM's quantum computing
  division operating the world's first public cloud quantum service (IBM Quantum Experience,
  2016) and the largest fleet of superconducting processors. Its hardware roadmap
  progressed from 127-qubit Eagle (2021) through 433-qubit Osprey (2022) to 1,121-qubit
  Condor and 133-qubit Heron (2023), with Heron powering the modular IBM Quantum
  System Two. The division also publishes Qiskit, the most widely used open-source
  quantum SDK. IBM targets 200-qubit / 100 M-gate Starling by 2029 and a 2,000-qubit
  / 1 B-gate Blue Jay system by 2033.
sort_name: IBM Quantum
sources:
- url: https://en.wikipedia.org/wiki/IBM_Quantum_Platform
- url: https://en.wikipedia.org/wiki/Jay_Gambetta
- url: https://en.wikipedia.org/wiki/Qiskit
- url: https://uk.newsroom.ibm.com/2016-May-04-IBM-Makes-Quantum-Computing-Available-on-IBM-Cloud-to-Accelerate-Innovation
  note: First cloud quantum computer announcement, May 2016
- url: https://newsroom.ibm.com/2021-11-16-IBM-Unveils-Breakthrough-127-Qubit-Quantum-Processor
  note: Eagle 127-qubit processor announcement, November 2021
- url: https://newsroom.ibm.com/2022-11-09-IBM-Unveils-400-Qubit-Plus-Quantum-Processor-and-Next-Generation-IBM-Quantum-System-Two
  note: Osprey 433-qubit processor and IBM Quantum System Two, November 2022
- url: https://www.nature.com/articles/s41586-023-06096-3
  note: Quantum utility paper, Nature June 2023
- url: https://newsroom.ibm.com/2023-12-04-IBM-Debuts-Next-Generation-Quantum-Processor-IBM-Quantum-System-Two,-Extends-Roadmap-to-Advance-Era-of-Quantum-Utility
  note: Condor 1121-qubit, Heron 133-qubit, and System Two launch, December 2023
- url: https://iopscience.iop.org/article/10.1088/2058-9565/abe519
  note: Quantum Volume 64 demonstration paper, QST March 2021
- url: https://arxiv.org/html/2410.00916v1
  note: IBM quantum computers evolution and roadmap review, 2024
status:
  operating_status: private
updated_at: '2026-05-30'
verification_source_count: 10
---
