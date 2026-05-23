import glob
import yaml
import re

for filepath in glob.glob('content/companies/*.md'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if match:
            fm = yaml.safe_load(match.group(1))
            name = str(fm.get('name'))
            logo = fm.get('logo_path')
            milestones = len(fm.get('milestones') or [])
            funding = len(fm.get('funding') or [])
            website = fm.get('website')
            print(f"{name:30} | Logo: {'YES' if logo else 'NO':3} | Milestones: {milestones:2} | Funding: {funding:2} | Web: {'YES' if website else 'NO'}")
