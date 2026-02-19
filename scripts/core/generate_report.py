import os
import glob
import re
import yaml
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")
REPORT_FILE = os.path.join(BASE_DIR, "reports", "missing_fields_report.md")

def parse_frontmatter(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1))
    except:
        return {}

def main():
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    total_profiles = len(files)
    
    # Fields to check
    # Essential: orcid, google_scholar, group_page, advisor, phd_year
    missing_counts = Counter()
    profile_status = []

    for fpath in sorted(files):
        meta = parse_frontmatter(fpath)
        pid = meta.get("id", os.path.basename(fpath))
        name = meta.get("name", "Unknown")
        
        links = meta.get("links", {})
        education = meta.get("education", [])
        
        # Check specific fields
        missing = []
        if not links.get("orcid"):
            missing.append("ORCID")
            missing_counts["ORCID"] += 1
        if not links.get("google_scholar"):
            missing.append("Google Scholar")
            missing_counts["Google Scholar"] += 1
        # group_page logic: might be in links.group_page or links.homepage
        if not (links.get("group_page") or links.get("homepage")):
            missing.append("Group Page")
            missing_counts["Group Page"] += 1
            
        # Education check (PhD)
        phd_found = False
        for edu in education:
            if "PhD" in edu.get("degree", "") or "DPhil" in edu.get("degree", "") or "Doctor" in edu.get("degree", ""):
                if edu.get("advisor") and edu.get("year"):
                    phd_found = True
        
        if not phd_found:
            missing.append("PhD Advisor/Year")
            missing_counts["PhD Advisor/Year"] += 1
            
        profile_status.append({
            "id": pid,
            "name": name,
            "missing": missing
        })

    # Generate Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Missing Fields Report\n\n")
        f.write(f"**Total Verified Profiles:** {total_profiles}\n\n")
        
        f.write("## Summary Statistics\n")
        f.write("| Field | Missing Count | Coverage % |\n")
        f.write("|---|---|---|\n")
        
        for field, count in missing_counts.items():
            coverage = ((total_profiles - count) / total_profiles) * 100
            f.write(f"| {field} | {count} | {coverage:.1f}% |\n")
            
        f.write("\n## Detailed Breakdown\n")
        f.write("| Profile | Missing Fields |\n")
        f.write("|---|---|\n")
        
        for p in profile_status:
            if p["missing"]:
                missing_str = ", ".join(p["missing"])
                f.write(f"| {p['name']} (`{p['id']}`) | {missing_str} |\n")
            else:
                 f.write(f"| {p['name']} (`{p['id']}`) | ✅ Complete |\n")

    print(f"Report generated at {REPORT_FILE}")

if __name__ == "__main__":
    main()
