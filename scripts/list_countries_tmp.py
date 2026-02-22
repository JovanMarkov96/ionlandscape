import glob, yaml, json
import frontmatter
from collections import Counter

countries = Counter()

# Paths to check
paths = [
    'content/people/*.md',
    'content/institutions/*.md',
    'content/companies/*.md'
]

for pattern in paths:
    for filepath in glob.glob(pattern):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                post = frontmatter.load(f)
                # People might have locations in different places or just 'country' under location
                if 'location' in post.metadata and isinstance(post.metadata['location'], dict):
                    if 'country' in post.metadata['location']:
                        countries[post.metadata['location']['country']] += 1
            except Exception as e:
                pass

print("--- UNIQUE COUNTRIES ---")
for country, count in countries.most_common():
    print(f"[{count}] {country}")
