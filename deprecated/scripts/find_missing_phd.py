import glob
import os
import yaml
import re

def parse_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML in {file_path}: {exc}")
            return None
    return None

def check_phd_data(file_path):
    data = parse_frontmatter(file_path)
    if not data:
        return
    
    name = data.get('name', 'Unknown')
    education = data.get('education', [])
    if not education:
        print(f"{os.path.basename(file_path)}: Missing education section")
        return

    phd_found = False
    for edu in education:
        degree = edu.get('degree', '')
        if 'PhD' in degree or 'DPhil' in degree:
            phd_found = True
            missing = []
            if not edu.get('institution'):
                missing.append('institution')
            if not edu.get('year'):
                missing.append('year')
            if not edu.get('advisor'):
                missing.append('advisor')
            
            if missing:
                print(f"{os.path.basename(file_path)}: PhD found but missing {', '.join(missing)}")
            
            # Check thesis
            thesis = data.get('thesis', {})
            if not thesis or (not thesis.get('title') and not thesis.get('link')):
                 print(f"{os.path.basename(file_path)}: Missing thesis info")
            
            break
    
    if not phd_found:
        print(f"{os.path.basename(file_path)}: No PhD entry found")

def main():
    files = glob.glob(os.path.join('content', 'people', '*.md'))
    for file in files:
        check_phd_data(file)

if __name__ == "__main__":
    main()
