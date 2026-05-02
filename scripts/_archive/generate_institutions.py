#!/usr/bin/env python3
"""
Generate institution markdown files from people.json data.

Reads all researcher profiles, extracts unique institutions from current_position,
education, and postdoc fields, then generates skeleton institution files with
auto-populated member/alumni directories.

Usage:
    python scripts/generate_institutions.py
"""
import json, os, sys, re, unicodedata

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE_JSON = os.path.join(ROOT, 'website', 'static', 'data', 'people.json')
INST_DIR = os.path.join(ROOT, 'content', 'institutions')

# ── Name Deduplication Map ──────────────────────────────────────────────────
# Maps variant names → canonical name
CANONICAL = {
    "IQOQI Innsbruck (ÖAW) & University of Innsbruck": "University of Innsbruck",
    "University of Innsbruck & IQOQI Innsbruck (ÖAW)": "University of Innsbruck",
    "NIST Boulder": "National Institute of Standards and Technology (NIST), Boulder",
    "Georgia Tech": "Georgia Institute of Technology",
    "Georgia Institute of Technology": "Georgia Institute of Technology",
}

# ── Institution Metadata ────────────────────────────────────────────────────
# Pre-filled data for priority institutions (≥2 members or otherwise important).
# Institutions not in this dict will get skeleton files.
METADATA = {
    "Duke University": {
        "aliases": ["Duke"],
        "city": "Durham", "region": "North Carolina", "country": "United States",
        "lat": 36.0014, "lon": -78.9382,
        "institution_type": "university",
        "short_description": "Duke University is a prestigious private research university in Durham, North Carolina, home to a major ion-trap quantum computing program.",
        "focus_areas": ["Quantum Computing", "Quantum Information Science", "Ion Trap Engineering", "Physics"],
        "website": "https://www.duke.edu/",
        "wikipedia": "https://en.wikipedia.org/wiki/Duke_University",
    },
    "Centre for Quantum Technologies, National University of Singapore": {
        "aliases": ["CQT", "CQT Singapore", "NUS CQT"],
        "city": "Singapore", "region": "", "country": "Singapore",
        "lat": 1.2966, "lon": 103.7764,
        "institution_type": "research_center",
        "short_description": "The Centre for Quantum Technologies (CQT) is a national research center of excellence at the National University of Singapore, focused on the fundamental physics of quantum mechanics and the building of quantum devices.",
        "focus_areas": ["Quantum Computing", "Quantum Information", "Quantum Optics", "Trapped Ions", "Neutral Atoms"],
        "website": "https://www.quantumlah.org/",
        "wikipedia": "https://en.wikipedia.org/wiki/Centre_for_Quantum_Technologies",
    },
    "University of Innsbruck": {
        "aliases": ["UIBK", "Innsbruck", "IQOQI Innsbruck"],
        "city": "Innsbruck", "region": "Tyrol", "country": "Austria",
        "lat": 47.2654, "lon": 11.3927,
        "institution_type": "university",
        "short_description": "The University of Innsbruck is a world-leading center for trapped-ion quantum computing and quantum simulation, hosting pioneering groups at both the Institute for Experimental Physics and the IQOQI (Austrian Academy of Sciences).",
        "focus_areas": ["Quantum Computing", "Quantum Simulation", "Quantum Networking", "Trapped Ions", "Cold Atoms"],
        "website": "https://www.uibk.ac.at/",
        "wikipedia": "https://en.wikipedia.org/wiki/University_of_Innsbruck",
    },
    "Osaka University": {
        "aliases": ["Osaka U", "Handai"],
        "city": "Osaka", "region": "Osaka Prefecture", "country": "Japan",
        "lat": 34.8225, "lon": 135.5249,
        "institution_type": "university",
        "short_description": "Osaka University is a leading national university in Japan, with strong programs in physics including trapped-ion experiments and quantum optics.",
        "focus_areas": ["Physics", "Quantum Optics", "Trapped Ions", "AMO Physics"],
        "website": "https://www.osaka-u.ac.jp/en",
        "wikipedia": "https://en.wikipedia.org/wiki/Osaka_University",
    },
    "ETH Zürich": {
        "aliases": ["ETH Zurich", "ETHZ", "Swiss Federal Institute of Technology"],
        "city": "Zürich", "region": "Zurich", "country": "Switzerland",
        "lat": 47.3769, "lon": 8.5417,
        "institution_type": "university",
        "short_description": "ETH Zürich is one of the world's leading universities for science and technology, hosting premier trapped-ion quantum information groups.",
        "focus_areas": ["Quantum Computing", "Quantum Information", "Trapped Ions", "Condensed Matter Physics"],
        "website": "https://ethz.ch/en.html",
        "wikipedia": "https://en.wikipedia.org/wiki/ETH_Zurich",
    },
    "Institute for Quantum Computing, University of Waterloo": {
        "aliases": ["IQC", "IQC Waterloo", "University of Waterloo IQC"],
        "city": "Waterloo", "region": "Ontario", "country": "Canada",
        "lat": 43.4779, "lon": -80.5479,
        "institution_type": "research_center",
        "short_description": "The Institute for Quantum Computing (IQC) at the University of Waterloo is a world-class research center for quantum information science and technology.",
        "focus_areas": ["Quantum Computing", "Quantum Information", "Trapped Ions", "Quantum Cryptography"],
        "website": "https://uwaterloo.ca/institute-for-quantum-computing/",
        "wikipedia": "https://en.wikipedia.org/wiki/Institute_for_Quantum_Computing",
    },
    "Massachusetts Institute of Technology": {
        "aliases": ["MIT"],
        "city": "Cambridge", "region": "Massachusetts", "country": "United States",
        "lat": 42.3601, "lon": -71.0942,
        "institution_type": "university",
        "short_description": "The Massachusetts Institute of Technology (MIT) is a world-renowned research university with pioneering contributions to quantum computing, cold atoms, and trapped-ion systems.",
        "focus_areas": ["Quantum Computing", "AMO Physics", "Quantum Information", "Quantum Simulation"],
        "website": "https://www.mit.edu/",
        "wikipedia": "https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology",
    },
    "National Institute of Standards and Technology (NIST), Boulder": {
        "aliases": ["NIST", "NIST Boulder", "NIST Ion Storage Group"],
        "city": "Boulder", "region": "Colorado", "country": "United States",
        "lat": 39.9951, "lon": -105.2615,
        "institution_type": "government_lab",
        "short_description": "NIST Boulder is a U.S. government research laboratory that has been at the forefront of trapped-ion physics, precision measurement, and quantum information since the pioneering work of David Wineland.",
        "focus_areas": ["Precision Measurement", "Quantum Computing", "Optical Clocks", "Trapped Ions"],
        "website": "https://www.nist.gov/",
        "wikipedia": "https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology",
    },
    "National Physical Laboratory (NPL)": {
        "aliases": ["NPL", "NPL Teddington"],
        "city": "Teddington", "region": "London", "country": "United Kingdom",
        "lat": 51.4247, "lon": -0.3451,
        "institution_type": "government_lab",
        "short_description": "The National Physical Laboratory (NPL) is the UK's national measurement standards laboratory, leading research in optical clocks and precision measurement with trapped ions.",
        "focus_areas": ["Precision Measurement", "Optical Clocks", "Quantum Metrology", "Trapped Ions"],
        "website": "https://www.npl.co.uk/",
        "wikipedia": "https://en.wikipedia.org/wiki/National_Physical_Laboratory_(United_Kingdom)",
    },
    "Seoul National University": {
        "aliases": ["SNU"],
        "city": "Seoul", "region": "", "country": "South Korea",
        "lat": 37.4602, "lon": 126.9526,
        "institution_type": "university",
        "short_description": "Seoul National University is South Korea's most prestigious university, with growing research groups in quantum information and trapped-ion systems.",
        "focus_areas": ["Physics", "Quantum Information", "Trapped Ions", "AMO Physics"],
        "website": "https://en.snu.ac.kr/",
        "wikipedia": "https://en.wikipedia.org/wiki/Seoul_National_University",
    },
    "Tsinghua University": {
        "aliases": ["Tsinghua", "THU"],
        "city": "Beijing", "region": "", "country": "China",
        "lat": 40.0003, "lon": 116.3267,
        "institution_type": "university",
        "short_description": "Tsinghua University is one of China's most elite research universities, with leading programs in quantum computing and quantum information science.",
        "focus_areas": ["Quantum Computing", "Quantum Information", "Physics", "Computer Science"],
        "website": "https://www.tsinghua.edu.cn/en/",
        "wikipedia": "https://en.wikipedia.org/wiki/Tsinghua_University",
    },
    "University of California, Los Angeles": {
        "aliases": ["UCLA"],
        "city": "Los Angeles", "region": "California", "country": "United States",
        "lat": 34.0689, "lon": -118.4452,
        "institution_type": "university",
        "short_description": "UCLA is a leading public research university with strong programs in AMO physics, including trapped molecular ions and laser-cooled atomic systems.",
        "focus_areas": ["AMO Physics", "Molecular Physics", "Trapped Ions", "Quantum Simulation"],
        "website": "https://www.ucla.edu/",
        "wikipedia": "https://en.wikipedia.org/wiki/University_of_California,_Los_Angeles",
    },
    "University of Sussex": {
        "aliases": ["Sussex"],
        "city": "Brighton", "region": "East Sussex", "country": "United Kingdom",
        "lat": 50.8660, "lon": -0.0873,
        "institution_type": "university",
        "short_description": "The University of Sussex hosts the Sussex Centre for Quantum Technologies, a leading hub for trapped-ion quantum computing and scalable quantum engineering.",
        "focus_areas": ["Quantum Computing", "Quantum Engineering", "Trapped Ions", "Scalable Architectures"],
        "website": "https://www.sussex.ac.uk/",
        "wikipedia": "https://en.wikipedia.org/wiki/University_of_Sussex",
    },
    "University of Tokyo": {
        "aliases": ["UTokyo", "Todai"],
        "city": "Tokyo", "region": "", "country": "Japan",
        "lat": 35.7128, "lon": 139.7621,
        "institution_type": "university",
        "short_description": "The University of Tokyo is Japan's most prestigious university, with strong research programs in experimental physics including trapped-ion quantum information.",
        "focus_areas": ["Physics", "Quantum Information", "Trapped Ions", "AMO Physics"],
        "website": "https://www.u-tokyo.ac.jp/en/",
        "wikipedia": "https://en.wikipedia.org/wiki/University_of_Tokyo",
    },
    "VU Amsterdam": {
        "aliases": ["VU", "Vrije Universiteit Amsterdam"],
        "city": "Amsterdam", "region": "", "country": "Netherlands",
        "lat": 52.3340, "lon": 4.8660,
        "institution_type": "university",
        "short_description": "VU Amsterdam (Vrije Universiteit Amsterdam) is a major Dutch research university with strong programs in precision measurements and fundamental physics.",
        "focus_areas": ["Precision Measurement", "Fundamental Physics", "AMO Physics", "Optical Frequency Metrology"],
        "website": "https://vu.nl/en",
        "wikipedia": "https://en.wikipedia.org/wiki/Vrije_Universiteit_Amsterdam",
    },
    # ── Single-member institutions (basic metadata) ─────────────────────
    "Aarhus University": {
        "aliases": ["AU"], "city": "Aarhus", "region": "", "country": "Denmark",
        "lat": 56.1629, "lon": 10.2039, "institution_type": "university",
        "short_description": "Aarhus University is one of Denmark's largest research universities, with active programs in AMO physics and cold molecular ions.",
        "focus_areas": ["AMO Physics", "Molecular Physics", "Cold Ions"],
        "website": "https://www.au.dk/en/", "wikipedia": "https://en.wikipedia.org/wiki/Aarhus_University",
    },
    "Ewha Womans University": {
        "aliases": ["Ewha"], "city": "Seoul", "region": "", "country": "South Korea",
        "lat": 37.5618, "lon": 126.9468, "institution_type": "university",
        "short_description": "Ewha Womans University is a prestigious private university in Seoul, South Korea, with emerging research in quantum information science.",
        "focus_areas": ["Physics", "Quantum Information"],
        "website": "https://www.ewha.ac.kr/ewhaen/", "wikipedia": "https://en.wikipedia.org/wiki/Ewha_Womans_University",
    },
    "Georgia Institute of Technology": {
        "aliases": ["Georgia Tech", "GT"], "city": "Atlanta", "region": "Georgia", "country": "United States",
        "lat": 33.7756, "lon": -84.3963, "institution_type": "university",
        "short_description": "Georgia Institute of Technology is a top-tier public research university in Atlanta with emerging programs in quantum science and engineering.",
        "focus_areas": ["Quantum Science", "Physics", "Engineering"],
        "website": "https://www.gatech.edu/", "wikipedia": "https://en.wikipedia.org/wiki/Georgia_Institute_of_Technology",
    },
    "Griffith University": {
        "aliases": ["Griffith"], "city": "Brisbane", "region": "Queensland", "country": "Australia",
        "lat": -27.5557, "lon": 153.0460, "institution_type": "university",
        "short_description": "Griffith University is an Australian research university based in Brisbane with research in quantum optics and atom-photon interfaces.",
        "focus_areas": ["Quantum Optics", "AMO Physics"],
        "website": "https://www.griffith.edu.au/", "wikipedia": "https://en.wikipedia.org/wiki/Griffith_University",
    },
    "Imperial College London": {
        "aliases": ["Imperial", "ICL"], "city": "London", "region": "", "country": "United Kingdom",
        "lat": 51.4988, "lon": -0.1749, "institution_type": "university",
        "short_description": "Imperial College London is a world-leading science and technology university with research groups in precision measurement and trapped-ion physics.",
        "focus_areas": ["Physics", "Quantum Optics", "Precision Measurement", "Trapped Ions"],
        "website": "https://www.imperial.ac.uk/", "wikipedia": "https://en.wikipedia.org/wiki/Imperial_College_London",
    },
    "Indian Institute of Science Education and Research (IISER) Pune": {
        "aliases": ["IISER Pune"], "city": "Pune", "region": "Maharashtra", "country": "India",
        "lat": 18.5493, "lon": 73.8029, "institution_type": "research_institute",
        "short_description": "IISER Pune is a premier Indian research and teaching institute with growing activities in cold and ultracold molecule-ion physics.",
        "focus_areas": ["AMO Physics", "Cold Molecules", "Ion-Neutral Chemistry"],
        "website": "https://www.iiserpune.ac.in/", "wikipedia": "https://en.wikipedia.org/wiki/Indian_Institute_of_Science_Education_and_Research,_Pune",
    },
    "Institute for Basic Science (IBS), South Korea": {
        "aliases": ["IBS"], "city": "Daejeon", "region": "", "country": "South Korea",
        "lat": 36.3722, "lon": 127.3620, "institution_type": "research_institute",
        "short_description": "The Institute for Basic Science (IBS) is South Korea's flagship basic research institute, with a dedicated Center for Quantum Information that conducts world-class trapped-ion experiments.",
        "focus_areas": ["Quantum Information", "Trapped Ions", "Quantum Computing"],
        "website": "https://www.ibs.re.kr/eng.do", "wikipedia": "https://en.wikipedia.org/wiki/Institute_for_Basic_Science",
    },
    "IonQ, Inc.": {
        "aliases": ["IonQ"], "city": "College Park", "region": "Maryland", "country": "United States",
        "lat": 38.9897, "lon": -76.9378, "institution_type": "company",
        "short_description": "IonQ is a leading quantum computing company building general-purpose trapped-ion quantum computers, founded by Christopher Monroe and Jungsang Kim.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "Quantum Hardware"],
        "website": "https://ionq.com/", "wikipedia": "https://en.wikipedia.org/wiki/IonQ",
    },
    "Johannes Gutenberg University Mainz": {
        "aliases": ["JGU Mainz", "Uni Mainz"], "city": "Mainz", "region": "Rhineland-Palatinate", "country": "Germany",
        "lat": 49.9929, "lon": 8.2473, "institution_type": "university",
        "short_description": "Johannes Gutenberg University Mainz is a major German research university with an active trapped-ion quantum computing group.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "Experimental Physics"],
        "website": "https://www.uni-mainz.de/eng/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Mainz",
    },
    "Kyoto University": {
        "aliases": ["Kyodai"], "city": "Kyoto", "region": "", "country": "Japan",
        "lat": 35.0267, "lon": 135.7808, "institution_type": "university",
        "short_description": "Kyoto University is one of Japan's top research universities with contributions to fundamental physics and quantum optics.",
        "focus_areas": ["Physics", "Quantum Optics", "AMO Physics"],
        "website": "https://www.kyoto-u.ac.jp/en", "wikipedia": "https://en.wikipedia.org/wiki/Kyoto_University",
    },
    "MIT Lincoln Laboratory": {
        "aliases": ["Lincoln Lab", "MIT LL"], "city": "Lexington", "region": "Massachusetts", "country": "United States",
        "lat": 42.4584, "lon": -71.2680, "institution_type": "government_lab",
        "short_description": "MIT Lincoln Laboratory is a federally funded research center that develops advanced technologies for national security, including trapped-ion quantum systems.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "Defense Technology"],
        "website": "https://www.ll.mit.edu/", "wikipedia": "https://en.wikipedia.org/wiki/MIT_Lincoln_Laboratory",
    },
    "National Institute of Information and Communications Technology (NICT)": {
        "aliases": ["NICT"], "city": "Koganei", "region": "Tokyo", "country": "Japan",
        "lat": 35.7107, "lon": 139.4895, "institution_type": "government_lab",
        "short_description": "NICT is Japan's national research institute for information and communications technologies, conducting research in optical clocks and frequency standards using trapped ions.",
        "focus_areas": ["Optical Clocks", "Frequency Standards", "Trapped Ions"],
        "website": "https://www.nict.go.jp/en/", "wikipedia": "https://en.wikipedia.org/wiki/National_Institute_of_Information_and_Communications_Technology",
    },
    "Okinawa Institute of Science and Technology (OIST)": {
        "aliases": ["OIST"], "city": "Onna", "region": "Okinawa", "country": "Japan",
        "lat": 26.4615, "lon": 127.8314, "institution_type": "research_institute",
        "short_description": "OIST is an interdisciplinary graduate university in Okinawa, Japan, with growing research programs in quantum information and ion-trap experiments.",
        "focus_areas": ["Quantum Information", "Trapped Ions", "AMO Physics"],
        "website": "https://www.oist.jp/", "wikipedia": "https://en.wikipedia.org/wiki/Okinawa_Institute_of_Science_and_Technology",
    },
    "Palacký University Olomouc": {
        "aliases": ["UPOL", "Palacký University"], "city": "Olomouc", "region": "", "country": "Czech Republic",
        "lat": 49.5955, "lon": 17.2518, "institution_type": "university",
        "short_description": "Palacký University Olomouc is the oldest university in Moravia with active research in quantum optics and single-ion experiments.",
        "focus_areas": ["Quantum Optics", "Single-Ion Experiments", "Physics"],
        "website": "https://www.upol.cz/en/", "wikipedia": "https://en.wikipedia.org/wiki/Palack%C3%BD_University_Olomouc",
    },
    "POSTECH": {
        "aliases": ["Pohang University of Science and Technology"], "city": "Pohang", "region": "North Gyeongsang", "country": "South Korea",
        "lat": 36.0111, "lon": 129.3238, "institution_type": "university",
        "short_description": "POSTECH (Pohang University of Science and Technology) is a top South Korean research university with emerging programs in quantum information and trapped-ion experiments.",
        "focus_areas": ["Physics", "Quantum Information", "Trapped Ions"],
        "website": "https://www.postech.ac.kr/eng/", "wikipedia": "https://en.wikipedia.org/wiki/POSTECH",
    },
    "Peking University": {
        "aliases": ["PKU", "Beida"], "city": "Beijing", "region": "", "country": "China",
        "lat": 39.9869, "lon": 116.3059, "institution_type": "university",
        "short_description": "Peking University is one of China's most prestigious research universities, with research groups in cold atoms and quantum optics.",
        "focus_areas": ["AMO Physics", "Cold Atoms", "Quantum Optics"],
        "website": "https://english.pku.edu.cn/", "wikipedia": "https://en.wikipedia.org/wiki/Peking_University",
    },
    "Physikalisch-Technische Bundesanstalt (PTB)": {
        "aliases": ["PTB"], "city": "Braunschweig", "region": "Lower Saxony", "country": "Germany",
        "lat": 52.2919, "lon": 10.4607, "institution_type": "government_lab",
        "short_description": "PTB is Germany's national metrology institute, conducting world-leading research in optical clocks and precision measurements with trapped ions.",
        "focus_areas": ["Precision Measurement", "Optical Clocks", "Quantum Metrology", "Trapped Ions"],
        "website": "https://www.ptb.de/cms/en.html", "wikipedia": "https://en.wikipedia.org/wiki/Physikalisch-Technische_Bundesanstalt",
    },
    "Saarland University": {
        "aliases": ["Universität des Saarlandes", "UdS"], "city": "Saarbrücken", "region": "Saarland", "country": "Germany",
        "lat": 49.2547, "lon": 7.0413, "institution_type": "university",
        "short_description": "Saarland University is a German university with research programs in quantum optics and trapped-ion quantum information processing.",
        "focus_areas": ["Quantum Information", "Trapped Ions", "Quantum Optics"],
        "website": "https://www.uni-saarland.de/en/home.html", "wikipedia": "https://en.wikipedia.org/wiki/Saarland_University",
    },
    "Sandia National Laboratories": {
        "aliases": ["Sandia", "SNL"], "city": "Albuquerque", "region": "New Mexico", "country": "United States",
        "lat": 35.0584, "lon": -106.5381, "institution_type": "government_lab",
        "short_description": "Sandia National Laboratories is a major U.S. government research facility with programs in quantum computing using microfabricated ion traps.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "Microfabricated Ion Traps", "National Security"],
        "website": "https://www.sandia.gov/", "wikipedia": "https://en.wikipedia.org/wiki/Sandia_National_Laboratories",
    },
    "Simon Fraser University": {
        "aliases": ["SFU"], "city": "Burnaby", "region": "British Columbia", "country": "Canada",
        "lat": 49.2781, "lon": -122.9199, "institution_type": "university",
        "short_description": "Simon Fraser University is a major Canadian research university with active programs in AMO physics and trapped-ion experiments.",
        "focus_areas": ["AMO Physics", "Trapped Ions", "Quantum Information"],
        "website": "https://www.sfu.ca/", "wikipedia": "https://en.wikipedia.org/wiki/Simon_Fraser_University",
    },
    "Stellenbosch University": {
        "aliases": ["SU", "Maties"], "city": "Stellenbosch", "region": "Western Cape", "country": "South Africa",
        "lat": -33.9321, "lon": 18.8602, "institution_type": "university",
        "short_description": "Stellenbosch University is a leading South African research university with the National Laser Centre and research in quantum control of trapped ions.",
        "focus_areas": ["Quantum Control", "Trapped Ions", "Laser Physics"],
        "website": "https://www.sun.ac.za/english", "wikipedia": "https://en.wikipedia.org/wiki/Stellenbosch_University",
    },
    "Stockholm University": {
        "aliases": ["SU Stockholm"], "city": "Stockholm", "region": "", "country": "Sweden",
        "lat": 59.3639, "lon": 18.0583, "institution_type": "university",
        "short_description": "Stockholm University is a major Swedish research university with research groups in trapped-ion quantum information.",
        "focus_areas": ["Quantum Information", "Trapped Ions", "AMO Physics"],
        "website": "https://www.su.se/english/", "wikipedia": "https://en.wikipedia.org/wiki/Stockholm_University",
    },
    "Sungkyunkwan University (SKKU)": {
        "aliases": ["SKKU"], "city": "Suwon", "region": "Gyeonggi", "country": "South Korea",
        "lat": 37.2939, "lon": 126.9753, "institution_type": "university",
        "short_description": "SKKU is a leading South Korean university with emerging quantum information research programs.",
        "focus_areas": ["Physics", "Quantum Information"],
        "website": "https://www.skku.edu/eng/", "wikipedia": "https://en.wikipedia.org/wiki/Sungkyunkwan_University",
    },
    "Technion – Israel Institute of Technology": {
        "aliases": ["Technion", "IIT"], "city": "Haifa", "region": "", "country": "Israel",
        "lat": 32.7770, "lon": 35.0218, "institution_type": "university",
        "short_description": "The Technion is Israel's oldest university and a leading institute of technology, with strong programs in physics including cold ion-molecule experiments.",
        "focus_areas": ["Physics", "Cold Chemistry", "Ion-Molecule Interactions", "AMO Physics"],
        "website": "https://www.technion.ac.il/en/", "wikipedia": "https://en.wikipedia.org/wiki/Technion_%E2%80%93_Israel_Institute_of_Technology",
    },
    "Ulm University": {
        "aliases": ["Uni Ulm"], "city": "Ulm", "region": "Baden-Württemberg", "country": "Germany",
        "lat": 48.4225, "lon": 9.9565, "institution_type": "university",
        "short_description": "Ulm University is a German research university with active trapped-ion and cold molecular ion research groups.",
        "focus_areas": ["Trapped Ions", "Cold Molecular Ions", "AMO Physics"],
        "website": "https://www.uni-ulm.de/en/", "wikipedia": "https://en.wikipedia.org/wiki/Ulm_University",
    },
    "University of Amsterdam": {
        "aliases": ["UvA"], "city": "Amsterdam", "region": "", "country": "Netherlands",
        "lat": 52.3559, "lon": 4.9554, "institution_type": "university",
        "short_description": "The University of Amsterdam is a major Dutch research university with trapped-ion research groups in its Institute of Physics.",
        "focus_areas": ["Trapped Ions", "Quantum Simulation", "AMO Physics"],
        "website": "https://www.uva.nl/en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Amsterdam",
    },
    "University of Basel": {
        "aliases": ["Uni Basel"], "city": "Basel", "region": "Basel-Stadt", "country": "Switzerland",
        "lat": 47.5581, "lon": 7.5833, "institution_type": "university",
        "short_description": "The University of Basel hosts research groups in quantum physics and trapped-ion precision spectroscopy within its Department of Physics.",
        "focus_areas": ["Precision Spectroscopy", "Trapped Ions", "Quantum Physics"],
        "website": "https://www.unibas.ch/en.html", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Basel",
    },
    "University of Bonn": {
        "aliases": ["Uni Bonn"], "city": "Bonn", "region": "North Rhine-Westphalia", "country": "Germany",
        "lat": 50.7274, "lon": 7.0842, "institution_type": "university",
        "short_description": "The University of Bonn is a leading German research university with experimental groups in quantum optics and trapped-ion physics.",
        "focus_areas": ["Quantum Optics", "Trapped Ions", "Cold Atoms"],
        "website": "https://www.uni-bonn.de/en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Bonn",
    },
    "University of Buenos Aires": {
        "aliases": ["UBA"], "city": "Buenos Aires", "region": "", "country": "Argentina",
        "lat": -34.5997, "lon": -58.3735, "institution_type": "university",
        "short_description": "The University of Buenos Aires is Argentina's largest and most prestigious university, with research in quantum optics and trapped-ion experiments.",
        "focus_areas": ["Quantum Optics", "Trapped Ions", "AMO Physics"],
        "website": "https://www.uba.ar/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Buenos_Aires",
    },
    "University of Calgary": {
        "aliases": ["UCalgary", "U of C"], "city": "Calgary", "region": "Alberta", "country": "Canada",
        "lat": 51.0776, "lon": -114.1300, "institution_type": "university",
        "short_description": "The University of Calgary is a major Canadian research university with programs in quantum technologies and nanophotonics.",
        "focus_areas": ["Quantum Technologies", "Nanophotonics", "AMO Physics"],
        "website": "https://www.ucalgary.ca/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Calgary",
    },
    "University of California, Berkeley": {
        "aliases": ["UC Berkeley", "Berkeley", "Cal"], "city": "Berkeley", "region": "California", "country": "United States",
        "lat": 37.8719, "lon": -122.2585, "institution_type": "university",
        "short_description": "UC Berkeley is a world-class public research university with pioneering trapped-ion quantum computing and AMO physics groups.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "AMO Physics"],
        "website": "https://www.berkeley.edu/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_California,_Berkeley",
    },
    "University of Granada": {
        "aliases": ["UGR"], "city": "Granada", "region": "Andalusia", "country": "Spain",
        "lat": 37.1809, "lon": -3.6006, "institution_type": "university",
        "short_description": "The University of Granada is a major Spanish research university with experimental programs in Penning trap mass spectrometry for nuclear and particle physics.",
        "focus_areas": ["Penning Traps", "Mass Spectrometry", "Nuclear Physics"],
        "website": "https://www.ugr.es/en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Granada",
    },
    "University of Groningen": {
        "aliases": ["RUG"], "city": "Groningen", "region": "", "country": "Netherlands",
        "lat": 53.2194, "lon": 6.5665, "institution_type": "university",
        "short_description": "The University of Groningen is a leading Dutch research university with work in fundamental physics and precision measurements.",
        "focus_areas": ["Fundamental Physics", "Precision Measurement", "AMO Physics"],
        "website": "https://www.rug.nl/?lang=en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Groningen",
    },
    "University of Kassel": {
        "aliases": ["Uni Kassel"], "city": "Kassel", "region": "Hesse", "country": "Germany",
        "lat": 51.3131, "lon": 9.4560, "institution_type": "university",
        "short_description": "The University of Kassel is a German university with research groups in precision spectroscopy and highly charged ions.",
        "focus_areas": ["Precision Spectroscopy", "Highly Charged Ions", "Atomic Physics"],
        "website": "https://www.uni-kassel.de/uni/en/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Kassel",
    },
    "University of Oregon": {
        "aliases": ["UO", "U of O"], "city": "Eugene", "region": "Oregon", "country": "United States",
        "lat": 44.0448, "lon": -123.0726, "institution_type": "university",
        "short_description": "The University of Oregon is a public research university where Nobel laureate David Wineland holds an appointment working on quantum physics.",
        "focus_areas": ["Quantum Physics", "AMO Physics"],
        "website": "https://www.uoregon.edu/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Oregon",
    },
    "University of Oxford": {
        "aliases": ["Oxford", "Oxon"], "city": "Oxford", "region": "Oxfordshire", "country": "United Kingdom",
        "lat": 51.7520, "lon": -1.2577, "institution_type": "university",
        "short_description": "The University of Oxford is one of the world's oldest and most prestigious universities, with leading trapped-ion quantum computing research in its Department of Physics.",
        "focus_areas": ["Quantum Computing", "Trapped Ions", "Quantum Error Correction", "Quantum Networks"],
        "website": "https://www.ox.ac.uk/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Oxford",
    },
    "University of Siegen": {
        "aliases": ["Uni Siegen"], "city": "Siegen", "region": "North Rhine-Westphalia", "country": "Germany",
        "lat": 50.9093, "lon": 8.0226, "institution_type": "university",
        "short_description": "The University of Siegen is a German university with research in trapped-ion quantum information processing using microwave techniques.",
        "focus_areas": ["Quantum Information", "Trapped Ions", "Microwave Control"],
        "website": "https://www.uni-siegen.de/start/index.html.en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Siegen",
    },
    "University of Sydney": {
        "aliases": ["USYD", "Sydney"], "city": "Sydney", "region": "New South Wales", "country": "Australia",
        "lat": -33.8882, "lon": 151.1877, "institution_type": "university",
        "short_description": "The University of Sydney hosts leading quantum control and trapped-ion research, including work on quantum sensing and noise-engineered quantum gates.",
        "focus_areas": ["Quantum Control", "Trapped Ions", "Quantum Sensing"],
        "website": "https://www.sydney.edu.au/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Sydney",
    },
    "University of Trento": {
        "aliases": ["UniTrento", "UNITN"], "city": "Trento", "region": "Trentino-Alto Adige", "country": "Italy",
        "lat": 46.0664, "lon": 11.1501, "institution_type": "university",
        "short_description": "The University of Trento is an Italian research university with work in integrated photonics and quantum technologies.",
        "focus_areas": ["Integrated Photonics", "Quantum Technologies", "Physics"],
        "website": "https://www.unitn.it/en", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Trento",
    },
    "University of Washington": {
        "aliases": ["UW", "UDub"], "city": "Seattle", "region": "Washington", "country": "United States",
        "lat": 47.6553, "lon": -122.3035, "institution_type": "university",
        "short_description": "The University of Washington is a major U.S. research university with experimental trapped-ion physics programs.",
        "focus_areas": ["Trapped Ions", "AMO Physics", "Quantum Information"],
        "website": "https://www.washington.edu/", "wikipedia": "https://en.wikipedia.org/wiki/University_of_Washington",
    },
}


def slugify(name):
    """Convert institution name to a filesystem-safe slug."""
    # Normalize unicode
    s = unicodedata.normalize('NFKD', name)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


def generate_md(idx, canonical_name, meta, current_members, alumni):
    """Generate a markdown frontmatter string for an institution."""
    slug = slugify(canonical_name)
    inst_id = f"i{idx:03d}-{slug}"
    
    aliases = meta.get('aliases', [])
    city = meta.get('city', '')
    region = meta.get('region', '')
    country = meta.get('country', '')
    lat = meta.get('lat', '')
    lon = meta.get('lon', '')
    inst_type = meta.get('institution_type', 'university')
    desc = meta.get('short_description', '')
    focus = meta.get('focus_areas', [])
    website = meta.get('website', '')
    wikipedia = meta.get('wikipedia', '')
    
    # Build directory
    members_yaml = "\n".join(f'    - "{m}"' for m in sorted(current_members)) if current_members else ""
    alumni_yaml = "\n".join(f'    - "{a}"' for a in sorted(alumni)) if alumni else ""
    
    aliases_str = json.dumps(aliases, ensure_ascii=False)
    focus_str = json.dumps(focus, ensure_ascii=False)
    
    md = f'''---
id: "{inst_id}"
name: "{canonical_name}"
sort_name: "{canonical_name}"
entity_type: "institution"

aliases: {aliases_str}

location:
  city: "{city}"
  region: "{region}"
  country: "{country}"
  lat: {lat}
  lon: {lon}

institution_type: "{inst_type}"

short_description: "{desc}"
focus_areas: {focus_str}

links:
  website: "{website}"
  department: ""
  quantum_center: ""
  wikipedia: "{wikipedia}"
  linkedin: ""

media:
  logo_path: ""
  hero_image_path: ""

directory:
  current_members:
{members_yaml}
  alumni:
{alumni_yaml}
  member_count: {len(current_members)}
  alumni_count: {len(alumni)}

sources:
  - url: "{website}"
    note: "Official website"
---
'''
    return inst_id, md


def main():
    with open(PEOPLE_JSON, 'r', encoding='utf-8') as f:
        people = json.load(f)
    
    # Build institution -> members/alumni maps
    inst_map = {}
    
    for p in people:
        md_file = p.get('md_filename', '')
        cp = p.get('current_position', {})
        if isinstance(cp, dict) and cp.get('institution'):
            raw = cp['institution'].strip()
            canonical = CANONICAL.get(raw, raw)
            if canonical not in inst_map:
                inst_map[canonical] = {'current_members': set(), 'alumni': set()}
            inst_map[canonical]['current_members'].add(md_file)
        
        cp_inst = (cp.get('institution', '').strip() if isinstance(cp, dict) else '')
        cp_canonical = CANONICAL.get(cp_inst, cp_inst)
        
        for edu in (p.get('education') or []):
            if isinstance(edu, dict) and edu.get('institution'):
                raw = edu['institution'].strip()
                canonical = CANONICAL.get(raw, raw)
                if canonical not in inst_map:
                    inst_map[canonical] = {'current_members': set(), 'alumni': set()}
                if canonical != cp_canonical:
                    inst_map[canonical]['alumni'].add(md_file)
        
        for pd_entry in (p.get('postdocs') or []):
            if isinstance(pd_entry, dict) and pd_entry.get('institution'):
                raw = pd_entry['institution'].strip()
                canonical = CANONICAL.get(raw, raw)
                if canonical not in inst_map:
                    inst_map[canonical] = {'current_members': set(), 'alumni': set()}
                if canonical != cp_canonical:
                    inst_map[canonical]['alumni'].add(md_file)
    
    # Filter to only current_position institutions
    cp_insts = set()
    for p in people:
        cp = p.get('current_position', {})
        if isinstance(cp, dict) and cp.get('institution'):
            raw = cp['institution'].strip()
            cp_insts.add(CANONICAL.get(raw, raw))
    
    os.makedirs(INST_DIR, exist_ok=True)
    
    # Check existing files
    existing_files = {f for f in os.listdir(INST_DIR) if f.endswith('.md')}
    existing_names = set()
    for fname in existing_files:
        path = os.path.join(INST_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('name:'):
                    existing_names.add(line.split(':', 1)[1].strip().strip('"'))
                    break
    
    created = 0
    skipped = 0
    idx = len(existing_files) + 1  # Start numbering after existing
    
    for canonical in sorted(cp_insts):
        if canonical in existing_names:
            print(f"  SKIP (exists): {canonical}")
            skipped += 1
            continue
        
        meta = METADATA.get(canonical, {})
        members = sorted(inst_map.get(canonical, {}).get('current_members', set()))
        alumni = sorted(inst_map.get(canonical, {}).get('alumni', set()))
        
        inst_id, md_content = generate_md(idx, canonical, meta, members, alumni)
        filename = f"{inst_id}.md"
        filepath = os.path.join(INST_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"  CREATE: {filename} ({len(members)} members, {len(alumni)} alumni)")
        created += 1
        idx += 1
    
    # Update Weizmann with directory data
    weizmann_path = os.path.join(INST_DIR, 'i001-weizmann-institute-of-science.md')
    if os.path.exists(weizmann_path):
        wis_data = inst_map.get('Weizmann Institute of Science', {})
        members = sorted(wis_data.get('current_members', set()))
        alumni = sorted(wis_data.get('alumni', set()))
        
        with open(weizmann_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace directory section
        members_yaml = "\n".join(f'    - "{m}"' for m in members) if members else ""
        alumni_yaml = "\n".join(f'    - "{a}"' for a in alumni) if alumni else ""
        
        import re as regex
        content = regex.sub(
            r'directory:.*?alumni_count: \d+',
            f'directory:\n  current_members:\n{members_yaml}\n  alumni:\n{alumni_yaml}\n  member_count: {len(members)}\n  alumni_count: {len(alumni)}',
            content, flags=regex.DOTALL
        )
        with open(weizmann_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  UPDATE: Weizmann Institute ({len(members)} members, {len(alumni)} alumni)")
    
    print(f"\nDone! Created {created}, skipped {skipped} existing.")


if __name__ == '__main__':
    main()
