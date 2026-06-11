# -*- coding: utf-8 -*-
"""Fix the confirmed-dead links:
- replace with verified known-new URLs (checked live before writing)
- wikipedia: use Wikidata sitelinks (en > de > fr > he > nl), else remove link+source
- sources that 404: swap to a live Wayback snapshot when one exists, else drop the entry
- guessed LinkedIn slugs that 404: remove
- leave bot-blocked (999/timeout-only) URLs alone"""
import glob, json, re, sys
import requests
import urllib3
urllib3.disable_warnings()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
session = requests.Session()

def alive(url):
    try:
        r = session.get(url, headers=UA, timeout=20, allow_redirects=True, verify=False)
        return r.status_code < 400, r.url
    except Exception:
        return False, None

def wayback(url):
    """Return a live snapshot URL or None."""
    try:
        r = session.get(f"https://web.archive.org/web/2/{url}", headers=UA, timeout=30, allow_redirects=True)
        if r.status_code == 200 and '/web/' in r.url and 'web.archive.org' in r.url:
            return r.url
    except Exception:
        pass
    return None

def repl_in_file(path, old, new, expect=None):
    raw = open(path, encoding='utf-8').read()
    n = raw.count(old)
    if n == 0:
        print(f"  MISS {path}: {old[:60]}")
        return False
    raw = raw.replace(old, new)
    open(path, 'w', encoding='utf-8').write(raw)
    return True

def remove_link_key(path, key, url):
    """Remove a `  key: url` line from the links block."""
    raw = open(path, encoding='utf-8').read()
    pat = re.compile(rf'^  {re.escape(key)}: {re.escape(url)}\s*\n', re.M)
    raw2, n = pat.subn('', raw)
    if n:
        open(path, 'w', encoding='utf-8').write(raw2)
        print(f"  removed links.{key} from {path.split('/')[-1]}")
    else:
        print(f"  WARN no match removing {key} in {path}")

def remove_source_entry(path, url):
    """Remove a sources list entry (note+url in either order) containing the dead url."""
    raw = open(path, encoding='utf-8').read()
    pats = [
        re.compile(rf'^- note: [^\n]*(?:\n  [^\n]*)*\n  url: {re.escape(url)}\s*\n', re.M),
        re.compile(rf'^- url: {re.escape(url)}\s*\n(?:  note: [^\n]*(?:\n  [^\n]*)*\n)?', re.M),
    ]
    for p in pats:
        raw2, n = p.subn('', raw)
        if n:
            open(path, 'w', encoding='utf-8').write(raw2)
            print(f"  dropped source {url[:60]} from {path.split('/')[-1]}")
            return True
    print(f"  WARN could not drop source in {path}: {url[:70]}")
    return False

P = 'content/people/'
C = 'content/companies/'
I = 'content/institutions/'

# ---------- 1. verified replacements for live-navigation links ----------
REPLACEMENTS = [
    # (file, kind, key, old_url, candidate_new_urls (first alive wins))
    (P+'035-stefan-willitsch.md', 'link', 'group_page', 'https://willitsch.chemie.unibas.ch/', ['https://coldions.chemie.unibas.ch/']),
    (P+'041-isaac-chuang.md', 'link', 'group_page', 'https://quanta.mit.edu/', ['http://feynman.mit.edu/ike/homepage/index.html', 'http://feynman.mit.edu/ike']),
    (P+'211-ignacio-cirac.md', 'both', 'homepage', 'https://www.mpq.mpg.de/cirac', ['https://www.mpq.mpg.de/6497312/theory']),
    (P+'221-gerhard-rempe.md', 'both', 'homepage', 'https://www.mpq.mpg.de/rempe', ['https://www.mpq.mpg.de/2386/quantumdynamics']),
    (P+'153-goran-wendin.md', 'link', 'institution_profile', 'https://www.chalmers.se/en/persons/goran-wendin/', ['https://research.chalmers.se/en/person/wendin']),
    (P+'184-anthony-laing.md', 'link', 'group_page', 'https://www.bristol.ac.uk/qet-labs/research/laing-group/', ['https://www.bristol.ac.uk/physics/research/quantum/', 'https://www.bristol.ac.uk/qet-labs/']),
    (P+'123-t-h-taminiau.md', 'link', 'group_page', 'https://taminiaulab.qutech.nl/', ['https://qutech.nl/lab/taminiau-lab/', 'http://taminiaulab.qutech.nl/']),
    (P+'281-john-m-doyle.md', 'both', 'group_page', 'https://jdoyle.hsites.harvard.edu/', ['https://www.doylegroup.harvard.edu/', 'https://projects.iq.harvard.edu/doylegroup']),
    (P+'185-ulrik-andersen.md', 'link', 'group_page', 'https://bigq.dtu.dk/', ['https://www.fysik.dtu.dk/english/research/qpit', 'https://bigq.fysik.dtu.dk/']),
    (P+'121-liang-jiang.md', 'link', 'lab', 'https://jianggroup.uchicago.edu', ['https://jiang.uchicago.edu', 'https://pme.uchicago.edu/group/jiang-group']),
    (P+'233-shay-hacohen-gourgy.md', 'both', 'homepage', 'https://phsites.technion.ac.il/hacohen-gourgy/', ['https://hacohen-gourgy.net.technion.ac.il/', 'https://phsites.technion.ac.il/shay/']),
    (P+'019-michael-koehl.md', 'link', 'group_page', 'https://www.koellab.uni-bonn.de/', ['https://www.qpe.uni-bonn.de/', 'https://www.pi.uni-bonn.de/koehl/en']),
    (P+'033-dzmitry-matsukevich.md', 'link', 'homepage', 'https://cqt.nus.edu.sg/people/principal-investigators/dzmitry-matsukevich/', ['https://www.cqt.sg/people/dzmitry-matsukevich/', 'https://cqt.sg/people/dzmitry-matsukevich/']),
    (C+'c002-ionq.md', 'source', None, 'https://ionq.com/quantum-hardware', ['https://ionq.com/quantum-systems']),
    (C+'c062-quobly.md', 'source', None, 'https://www.quobly.io/about-us/', ['https://www.quobly.io/quobly', 'https://www.quobly.io/']),
    (C+'c006-quera-computing.md', 'link', 'news', 'https://www.quera.com/press-releases', ['https://www.quera.com/news', 'https://www.quera.com/newsroom']),
    (I+'i014-johannes-gutenberg-university-mainz.md', 'link', 'website', 'https://www.uni-mainz.de/eng/', ['https://www.uni-mainz.de/en/', 'https://www.uni-mainz.de/']),
]

print("== replacements ==")
for path, kind, key, old, cands in REPLACEMENTS:
    new = None
    for cand in cands:
        ok, final = alive(cand)
        if ok:
            new = cand
            break
    if new:
        if repl_in_file(path, old, new):
            print(f"  OK {path.split('/')[-1]:38s} {key or 'source'} -> {new}")
    else:
        # no candidate alive: remove
        if kind in ('link', 'both') and key:
            remove_link_key(path, key, old)
        if kind in ('both', 'source'):
            remove_source_entry(path, old)

# ---------- 2. removals (no replacement exists) ----------
REMOVE_LINKS = [
    (P+'005-christian-roos.md', 'thesis_pdf', 'https://quantumoptics.at/images/publications/dissertation/roos-diss.pdf'),
    (P+'017-rainer-blatt.md', 'cv_pdf', 'https://quantumoptics.at/images/people/rainer.blatt/rb_cv_2023_english.pdf'),
    (P+'058-atsushi-noguchi.md', 'homepage', 'https://southasianpaleolithic.net'),
    (P+'059-shuichi-hasegawa.md', 'group_page', 'https://www.nuclear.jp/~hasegawa/index_e.html'),
    (P+'061-taeyoung-choi.md', 'group_page', 'http://qion.ewha.ac.kr/'),
    (P+'062-dan-cho.md', 'group_page', 'http://nems.snu.ac.kr/'),
    (P+'062-dan-cho.md', 'homepage', 'http://nems.snu.ac.kr/'),
    (P+'063-taehyun-kim.md', 'group_page', 'http://qis.snu.ac.kr/'),
    (P+'064-junki-kim.md', 'group_page', 'https://queti.skku.edu/'),
    (P+'064-junki-kim.md', 'homepage', 'https://queti.skku.edu/'),
    (P+'065-luyan-sun.md', 'group_page', 'http://hqs.iiis.tsinghua.edu.cn/'),
    (P+'072-brian-mcmahon.md', 'group_page', 'https://gtri.gatech.edu/researcher/brian-mcmahon'),
    (P+'118-lee-c-bassett.md', 'group_page', 'https://nanoquant.seas.upenn.edu/'),
    (P+'164-john-clarke.md', 'group_page', 'http://research.physics.berkeley.edu/clarke/overview.html'),
    (P+'176-jian-wei-pan.md', 'google_scholar', 'https://scholar.google.com/citations?user=-q3Yb14AAAAJ'),
    (P+'188-rupert-ursin.md', 'institution_profile', 'https://www.iqoqi-vienna.at/people/ursin-group/rupert-ursin/'),
    (C+'c017-eleqtron.md', 'news', 'https://eleqtron.com/en/news/'),
]
LINKEDIN_DEAD = [
    (C+'c006-quera-computing.md', 'https://www.linkedin.com/company/quera-computing'),
    (C+'c043-quantum-motion.md', 'https://www.linkedin.com/company/quantum-motion'),
    (C+'c044-silicon-quantum-computing.md', 'https://www.linkedin.com/company/silicon-quantum-computing'),
    (C+'c050-kets-quantum-security.md', 'https://www.linkedin.com/company/kets-quantum-security'),
    (C+'c056-m-squared-lasers.md', 'https://www.linkedin.com/company/m-squared-lasers'),
    (C+'c058-qlm-technology.md', 'https://www.linkedin.com/company/qlm-technology'),
    (C+'c060-quantopticon.md', 'https://www.linkedin.com/company/quantopticon'),
    (C+'c076-qant.md', 'https://www.linkedin.com/company/q-ant'),
    (C+'c082-menlo-systems.md', 'https://www.linkedin.com/company/menlo-systems-gmbh'),
    (C+'c085-id-quantique.md', 'https://www.linkedin.com/company/id-quantique'),
    (C+'c090-multiverse-computing.md', 'https://www.linkedin.com/company/multiverse-computing'),
    (C+'c091-qilimanjaro-quantum-tech.md', 'https://www.linkedin.com/company/qilimanjaro-quantum-tech'),
    (C+'c093-qti-quantum-telecommunications-italy.md', 'https://www.linkedin.com/company/qti-srl'),
    (C+'c103-beit.md', 'https://www.linkedin.com/company/beit-inc'),
    (C+'c107-pixel-photonics.md', 'https://www.linkedin.com/company/pixel-photonics'),
]
print("\n== removals ==")
for path, key, url in REMOVE_LINKS:
    remove_link_key(path, key, url)
for path, url in LINKEDIN_DEAD:
    remove_link_key(path, 'linkedin', url)

# ---------- 3. wikipedia via Wikidata sitelinks ----------
wd = json.load(open('reports/wikidata_people.json', encoding='utf-8'))
WIKI_DEAD = [
    ('226-philippe-grangier', P+'226-philippe-grangier.md', 'https://en.wikipedia.org/wiki/Philippe_Grangier'),
    ('232-netanel-lindner', P+'232-netanel-lindner.md', 'https://en.wikipedia.org/wiki/Netanel_Lindner'),
    ('282-jorg-schmiedmayer', P+'282-jorg-schmiedmayer.md', 'https://en.wikipedia.org/wiki/J%C3%B6rg_Schmiedmayer'),
    ('292-lieven-m-k-vandersypen', P+'292-lieven-m-k-vandersypen.md', 'https://en.wikipedia.org/wiki/Lieven_Vandersypen'),
    ('294-martin-plenio', P+'294-martin-plenio.md', 'https://en.wikipedia.org/wiki/Martin_Plenio'),
    ('311-randy-hulet', P+'311-randy-hulet.md', 'https://en.wikipedia.org/wiki/Randall_Hulet'),
    ('323-tilman-pfau', P+'323-tilman-pfau.md', 'https://en.wikipedia.org/wiki/Tilman_Pfau'),
]
print("\n== wikipedia ==")
ORDER = ['enwiki', 'dewiki', 'frwiki', 'hewiki', 'nlwiki', 'itwiki', 'eswiki']
for pid, path, old in WIKI_DEAD:
    qid = (wd.get(pid) or {}).get('qid')
    new = None
    if qid:
        try:
            r = session.get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json", headers=UA, timeout=25)
            sl = r.json()['entities'][qid].get('sitelinks', {})
            for k in ORDER:
                if k in sl:
                    lang = k[:-4]
                    title = sl[k]['title'].replace(' ', '_')
                    new = f"https://{lang}.wikipedia.org/wiki/{requests.utils.quote(title)}"
                    break
        except Exception as e:
            print(f"  ERR {pid}: {e}")
    if new and alive(new)[0]:
        repl_in_file(path, old, new)
        print(f"  OK {pid} -> {new}")
    else:
        remove_link_key(path, 'wikipedia', old)
        remove_source_entry(path, old)

# company wikis
print("\n== company wikis ==")
for path, old, cands in [
    (C+'c029-infleqtion.md', 'https://en.wikipedia.org/wiki/Infleqtion', ['https://en.wikipedia.org/wiki/ColdQuanta']),
    (C+'c023-oxford-quantum-circuits.md', 'https://en.wikipedia.org/wiki/Oxford_Quantum_Circuits', []),
    (I+'i122-russian-quantum-center.md', 'https://en.wikipedia.org/wiki/Russian_Quantum_Center', ['https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%D0%BE%D0%B2%D1%8B%D0%B9_%D1%86%D0%B5%D0%BD%D1%82%D1%80']),
]:
    new = next((c for c in cands if alive(c)[0]), None)
    if new:
        repl_in_file(path, old, new)
        print(f"  OK -> {new[:70]}")
    else:
        remove_link_key(path, 'wikipedia', old)
        remove_source_entry(path, old)

# ---------- 4. dead sources -> wayback or drop ----------
DEAD_SOURCES = [
    (C+'c001-quantum-art.md', 'https://www.prnewswire.com/news-releases/quantum-art-raises-100-million-in-series-a-funding-302328222.html'),
    (C+'c014-quantum-source-labs.md', 'https://en.wikipedia.org/wiki/Quantum_Source_Labs'),
    (C+'c029-infleqtion.md', 'https://techcrunch.com/2021/08/02/coldquanta-raises-110-million-to-advance-its-cold-atom-quantum-technologies/'),
    (C+'c029-infleqtion.md', 'https://www.infleqtion.com/hilbert'),
    (C+'c029-infleqtion.md', 'https://www.prnewswire.com/news-releases/infleqtion-and-sandboxaq-partner-to-advance-quantum-sensing-and-navigation-solutions-301849782.html'),
    (C+'c030-psiquantum.md', 'https://gf.com/dresden-press-release/psiquantum-and-globalfoundries-build-worlds-first-full-scale-quantum-computer/'),
    (C+'c088-zurich-instruments.md', 'https://www.rohde-schwarz.com/us/about/news-press/all-news/rohde-schwarz-strengthens-position-in-quantum-technology-market-by-acquiring-zurich-instruments-ag-press-release-detailpage_229356-1094656.html'),
    (C+'c098-molecular-quantum-solutions.md', 'https://www.inam.berlin/post/founderfriday-mqs-a-service-solution-for-the-pharma-biotech-and-chemical-industries'),
    (C+'c083-parityqc.md', 'https://www.iect.at/en/parityqc-im-interview-en/'),
]
print("\n== dead sources ==")
for path, url in DEAD_SOURCES:
    wb = wayback(url)
    if wb:
        if repl_in_file(path, url, wb):
            print(f"  wayback {url[:60]}")
    else:
        remove_source_entry(path, url)

# ---------- 5. atlantic-quantum dead website -> wayback ----------
wb = wayback('https://atlantic-quantum.com')
if wb:
    repl_in_file(C+'c039-atlantic-quantum.md', 'https://atlantic-quantum.com', wb)
    print(f"\natlantic-quantum website -> {wb}")
else:
    remove_link_key(C+'c039-atlantic-quantum.md', 'website', 'https://atlantic-quantum.com')

print("\ndone")
