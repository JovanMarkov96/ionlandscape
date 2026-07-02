import os
import glob
import re

count = 0
for filepath in glob.glob('content/people/*.md'):
    if filepath.endswith('.evidence.md'):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'postdocs: []' in content:
        new_content = content.replace('postdocs: []', 'postdocs:\n- advisor: null\n  institution: \"Unknown\"\n  years: null\n  confidence: not_found')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f'Updated {filepath}')

print(f'Total updated: {count}')
