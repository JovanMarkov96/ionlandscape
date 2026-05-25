#!/usr/bin/env python3
"""Add focus_areas and platforms_represented to institution MD files."""
import frontmatter, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INST_DIR = os.path.join(ROOT, "content", "institutions")

data = {
    "i002-aarhus-university.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i003-centre-for-quantum-technologies-national-university-of-singapore.md": {"focus_areas": ["Quantum Computing", "Quantum Communication"], "platforms_represented": ["trapped_ion"]},
    "i004-duke-university.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i005-eth-zurich.md": {"focus_areas": ["Quantum Simulation", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i006-ewha-womans-university.md": {"focus_areas": ["AMO Physics", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i007-georgia-institute-of-technology.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i008-griffith-university.md": {"focus_areas": ["Quantum Sensing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i009-imperial-college-london.md": {"focus_areas": ["Quantum Computing", "Quantum Communication"], "platforms_represented": ["trapped_ion"]},
    "i010-indian-institute-of-science-education-and-research-iiser-pune.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i011-institute-for-basic-science-ibs-south-korea.md": {"focus_areas": ["Quantum Sensing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i012-institute-for-quantum-computing-university-of-waterloo.md": {"focus_areas": ["Quantum Computing", "Quantum Information"], "platforms_represented": ["trapped_ion"]},
    "i014-johannes-gutenberg-university-mainz.md": {"focus_areas": ["Quantum Simulation", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i015-kyoto-university.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i016-mit-lincoln-laboratory.md": {"focus_areas": ["Quantum Computing", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i017-massachusetts-institute-of-technology.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i018-national-institute-of-information-and-communications-technology-nict.md": {"focus_areas": ["Quantum Communication", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i019-national-institute-of-standards-and-technology-nist-boulder.md": {"focus_areas": ["Quantum Standards", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i020-national-physical-laboratory-npl.md": {"focus_areas": ["Quantum Sensing", "Quantum Standards"], "platforms_represented": ["trapped_ion"]},
    "i021-okinawa-institute-of-science-and-technology-oist.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i022-osaka-university.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i023-postech.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i024-palacky-university-olomouc.md": {"focus_areas": ["Quantum Optics", "Quantum Information"], "platforms_represented": ["trapped_ion"]},
    "i025-peking-university.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i026-physikalisch-technische-bundesanstalt-ptb.md": {"focus_areas": ["Quantum Standards", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i027-saarland-university.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i028-sandia-national-laboratories.md": {"focus_areas": ["Quantum Computing", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i029-seoul-national-university.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i030-simon-fraser-university.md": {"focus_areas": ["Quantum Computing", "Quantum Information"], "platforms_represented": ["trapped_ion"]},
    "i031-stellenbosch-university.md": {"focus_areas": ["Quantum Optics", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i032-stockholm-university.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i033-sungkyunkwan-university-skku.md": {"focus_areas": ["AMO Physics", "Quantum Computing"], "platforms_represented": ["trapped_ion"]},
    "i034-technion-israel-institute-of-technology.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i035-tsinghua-university.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i036-ulm-university.md": {"focus_areas": ["Quantum Sensing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i037-university-of-amsterdam.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i038-university-of-basel.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i039-university-of-bonn.md": {"focus_areas": ["Quantum Simulation", "AMO Physics"], "platforms_represented": ["trapped_ion", "neutral_atom"]},
    "i040-university-of-buenos-aires.md": {"focus_areas": ["AMO Physics", "Quantum Information"], "platforms_represented": ["trapped_ion"]},
    "i041-university-of-calgary.md": {"focus_areas": ["Quantum Communication", "Quantum Information"], "platforms_represented": ["trapped_ion"]},
    "i042-university-of-california-berkeley.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion", "neutral_atom"]},
    "i043-university-of-california-los-angeles.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i044-university-of-granada.md": {"focus_areas": ["Quantum Simulation", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i045-university-of-groningen.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i046-university-of-innsbruck.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i047-university-of-kassel.md": {"focus_areas": ["AMO Physics", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i048-university-of-oregon.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i049-university-of-oxford.md": {"focus_areas": ["Quantum Computing", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i050-university-of-siegen.md": {"focus_areas": ["Quantum Sensing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i051-university-of-sussex.md": {"focus_areas": ["Quantum Computing", "Quantum Sensing"], "platforms_represented": ["trapped_ion"]},
    "i052-university-of-sydney.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i053-university-of-tokyo.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i054-university-of-trento.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i055-university-of-washington.md": {"focus_areas": ["Quantum Computing", "AMO Physics"], "platforms_represented": ["trapped_ion"]},
    "i056-vu-amsterdam.md": {"focus_areas": ["AMO Physics", "Quantum Simulation"], "platforms_represented": ["trapped_ion"]},
    "i057-open-quantum-design.md": {"focus_areas": ["Quantum Hardware", "Quantum Computing"], "platforms_represented": ["trapped_ion"]},
    "i059-cqiqc.md": {"focus_areas": ["Quantum Information", "Quantum Foundations"], "platforms_represented": ["trapped_ion"]},
}

for fname, updates in data.items():
    fpath = os.path.join(INST_DIR, fname)
    if not os.path.exists(fpath):
        print("MISSING:", fname)
        continue
    post = frontmatter.load(fpath)
    changed = False
    for key, val in updates.items():
        if not post.metadata.get(key):
            post.metadata[key] = val
            changed = True
    if changed:
        with open(fpath, "wb") as f:
            frontmatter.dump(post, f)
        print("Updated:", fname)
    else:
        print("Already has:", fname)

print("Done")
