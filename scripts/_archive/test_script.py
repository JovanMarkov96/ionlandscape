import frontmatter
with open('content/institutions/i007-georgia-institute-of-technology.md', 'r', encoding='utf-8') as f:
    post = frontmatter.load(f)
post['group_count'] = 1
with open('test_dump.md', 'w', encoding='utf-8') as f:
    f.write(frontmatter.dumps(post))
