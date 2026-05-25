#!/usr/bin/env python3
"""Populate links.website for institutions so the Sources/Links sections are diversified."""
import frontmatter, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INST_DIR = os.path.join(ROOT, "content", "institutions")

DOMAINS = {
    "i001-weizmann-institute-of-science.md": "https://www.weizmann.ac.il/",
    "i002-aarhus-university.md": "https://international.au.dk/",
    "i003-centre-for-quantum-technologies-national-university-of-singapore.md": "https://www.quantumlah.org/",
    "i004-duke-university.md": "https://duke.edu/",
    "i005-eth-zurich.md": "https://ethz.ch/en.html",
    "i006-ewha-womans-university.md": "https://www.ewha.ac.kr/ewhaen/index.do",
    "i007-georgia-institute-of-technology.md": "https://www.gatech.edu/",
    "i008-griffith-university.md": "https://www.griffith.edu.au/",
    "i009-imperial-college-london.md": "https://www.imperial.ac.uk/",
    "i010-indian-institute-of-science-education-and-research-iiser-pune.md": "https://www.iiserpune.ac.in/",
    "i011-institute-for-basic-science-ibs-south-korea.md": "https://www.ibs.re.kr/eng.do",
    "i012-institute-for-quantum-computing-university-of-waterloo.md": "https://uwaterloo.ca/institute-for-quantum-computing/",
    "i014-johannes-gutenberg-university-mainz.md": "https://www.uni-mainz.de/eng/",
    "i015-kyoto-university.md": "https://www.kyoto-u.ac.jp/en",
    "i016-mit-lincoln-laboratory.md": "https://www.ll.mit.edu/",
    "i017-massachusetts-institute-of-technology.md": "https://www.mit.edu/",
    "i018-national-institute-of-information-and-communications-technology-nict.md": "https://www.nict.go.jp/en/",
    "i019-national-institute-of-standards-and-technology-nist-boulder.md": "https://www.nist.gov/",
    "i020-national-physical-laboratory-npl.md": "https://www.npl.co.uk/",
    "i021-okinawa-institute-of-science-and-technology-oist.md": "https://www.oist.jp/",
    "i022-osaka-university.md": "https://www.osaka-u.ac.jp/en",
    "i023-postech.md": "https://www.postech.ac.kr/eng/",
    "i024-palacky-university-olomouc.md": "https://www.upol.cz/en/",
    "i025-peking-university.md": "https://english.pku.edu.cn/",
    "i026-physikalisch-technische-bundesanstalt-ptb.md": "https://www.ptb.de/cms/en.html",
    "i027-saarland-university.md": "https://www.uni-saarland.de/en/home.html",
    "i028-sandia-national-laboratories.md": "https://www.sandia.gov/",
    "i029-seoul-national-university.md": "https://en.snu.ac.kr/",
    "i030-simon-fraser-university.md": "https://www.sfu.ca/",
    "i031-stellenbosch-university.md": "https://www.sun.ac.za/english",
    "i032-stockholm-university.md": "https://www.su.se/english/",
    "i033-sungkyunkwan-university-skku.md": "https://www.skku.edu/eng/",
    "i034-technion-israel-institute-of-technology.md": "https://www.technion.ac.il/en/",
    "i035-tsinghua-university.md": "https://www.tsinghua.edu.cn/en/",
    "i036-ulm-university.md": "https://www.uni-ulm.de/en/",
    "i037-university-of-amsterdam.md": "https://www.uva.nl/en",
    "i038-university-of-basel.md": "https://www.unibas.ch/en.html",
    "i039-university-of-bonn.md": "https://www.uni-bonn.de/en",
    "i040-university-of-buenos-aires.md": "https://www.uba.ar/internacionales/",
    "i041-university-of-calgary.md": "https://www.ucalgary.ca/",
    "i042-university-of-california-berkeley.md": "https://www.berkeley.edu/",
    "i043-university-of-california-los-angeles.md": "https://www.ucla.edu/",
    "i044-university-of-granada.md": "https://www.ugr.es/en",
    "i045-university-of-groningen.md": "https://www.rug.nl/",
    "i046-university-of-innsbruck.md": "https://www.uibk.ac.at/en/",
    "i047-university-of-kassel.md": "https://www.uni-kassel.de/uni/en/",
    "i048-university-of-oregon.md": "https://www.uoregon.edu/",
    "i049-university-of-oxford.md": "https://www.ox.ac.uk/",
    "i050-university-of-siegen.md": "https://www.uni-siegen.de/start/index.html.en",
    "i051-university-of-sussex.md": "https://www.sussex.ac.uk/",
    "i052-university-of-sydney.md": "https://www.sydney.edu.au/",
    "i053-university-of-tokyo.md": "https://www.u-tokyo.ac.jp/en/",
    "i054-university-of-trento.md": "https://www.unitn.it/en",
    "i055-university-of-washington.md": "https://www.washington.edu/",
    "i056-vu-amsterdam.md": "https://vu.nl/en",
    "i057-open-quantum-design.md": "https://openquantumdesign.org/",
    "i059-cqiqc.md": "https://cqiqc.physics.utoronto.ca/",
}

for fname, url in DOMAINS.items():
    fpath = os.path.join(INST_DIR, fname)
    if not os.path.exists(fpath):
        print("MISSING:", fname)
        continue
    post = frontmatter.load(fpath)
    links = post.metadata.get("links", {}) or {}
    if not links.get("website"):
        links["website"] = url
        post.metadata["links"] = links
        with open(fpath, "wb") as f:
            frontmatter.dump(post, f)
        print("Added website:", fname)
    else:
        print("Already has website:", fname)

print("Done")
