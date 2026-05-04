import os
import glob
import re

count = 0
for filepath in glob.glob('content/people/*.md'):
    if filepath.endswith('.evidence.md'):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '  link: null' in content and 'thesis:' in content:
        new_content = content.replace('  link: null', '  link: \"Unknown\"')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f'Updated {filepath}')

print(f'Total updated: {count}')
