import glob, yaml, json
import frontmatter

affiliations = set()
for path in glob.glob('content/people/*.md'):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            post = frontmatter.load(f)
            if 'current_position' in post.metadata and 'institution' in post.metadata['current_position']:
                affiliations.add(post.metadata['current_position']['institution'])
            if 'affiliations' in post.metadata:
                for affil in post.metadata['affiliations']:
                    if 'name' in affil:
                        affiliations.add(affil['name'])
        except Exception as e:
            pass

print("ALL UNIQUE AFFILIATIONS IN PEOPLE PROFILES:")
for a in sorted(affiliations):
    print(" - " + a)
