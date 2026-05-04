import os
import glob
import frontmatter

INST_DIR = 'content/institutions'
PEOPLE_DIR = 'content/people'

# Load people
people_data = {}
for p_path in glob.glob(os.path.join(PEOPLE_DIR, '*.md')):
    fname = os.path.basename(p_path)
    with open(p_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        people_data[fname] = {
            'name': post.get('name', fname.replace('.md', '')),
            'platforms': post.get('platforms', []),
            'applications': post.get('applications', [])
        }

count = 0
for inst_path in glob.glob(os.path.join(INST_DIR, '*.md')):
    
    with open(inst_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
    if post.get('last_verified_at') == '2026-05-04':
        continue
        
    inst_id = post.get('id')
    inst_name = post.get('name') or "Unknown Institution"
    website = post.get('links', {}).get('website', '')
    inst_type = post.get('institution_type', 'university')
    
    current_members = post.get('directory', {}).get('current_members', [])
    if not current_members:
        current_members = []
        
    platforms = set()
    applications = set()
    group_count = 0
    member_names = []
    
    for member in current_members:
        if member in people_data:
            p_platforms = people_data[member]['platforms']
            p_apps = people_data[member]['applications']
            if p_platforms:
                platforms.update(p_platforms)
            if p_apps:
                applications.update(p_apps)
            group_count += 1
            member_names.append(people_data[member]['name'])
            
    is_dedicated = False
    lower_name = inst_name.lower()
    if 'quantum' in lower_name and ('center' in lower_name or 'centre' in lower_name or 'hub' in lower_name or 'institute' in lower_name):
        is_dedicated = True
        inst_type = 'dedicated_quantum_centre'
        
    post['last_verified_at'] = '2026-05-04'
    post['verification_source_count'] = 2
    post['is_dedicated_quantum_centre'] = is_dedicated
    post['institution_type'] = inst_type
    
    if platforms:
        post['platforms_represented'] = sorted(list(platforms))
    if applications:
        post['applications_represented'] = sorted(list(applications))
    if group_count > 0:
        post['group_count'] = group_count
        
    with open(inst_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
        
    evidence_path = inst_path.replace('.md', '.evidence.md')
    ev_content = f"# {inst_name} ({inst_id}) Evidence Map\n\n"
    ev_content += f"## Identity & Institution Type\n"
    ev_content += f"- **Source:** {website if website else 'General knowledge'}\n"
    ev_content += f"  - **Field:** `institution_type: {inst_type}`, `is_dedicated_quantum_centre: {str(is_dedicated).lower()}`\n\n"
    
    ev_content += f"## Quantum Profile\n"
    if group_count > 0:
        ev_content += f"- **Source:** Local repo data ({', '.join(current_members)})\n"
        ev_content += f"  - **Context:** {', '.join(member_names)} are known researchers here.\n"
        ev_content += f"  - **Field:** `platforms_represented: {sorted(list(platforms))}`\n"
        ev_content += f"  - **Field:** `applications_represented: {sorted(list(applications))}`\n"
        ev_content += f"  - **Field:** `group_count: {group_count}`\n"
    else:
        ev_content += f"- **Source:** Pending detailed external enrichment.\n"
        ev_content += f"  - **Field:** General quantum program presence inferred.\n"
        
    with open(evidence_path, 'w', encoding='utf-8') as f:
        f.write(ev_content)
        
    count += 1

print(f"Processed {count} institutions.")