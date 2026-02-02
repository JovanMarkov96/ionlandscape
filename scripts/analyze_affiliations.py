import os
import frontmatter
import glob

PEOPLE_DIR = os.path.join(os.path.dirname(__file__), '../content/people')

def analyze_affiliations():
    files = glob.glob(os.path.join(PEOPLE_DIR, "*.md"))
    multi_affil_people = []

    print(f"Scanning {len(files)} profiles...")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                post = frontmatter.load(f)
                data = post.metadata
                
                # Check current position
                current_inst = data.get('current_position', {}).get('institution', 'Unknown')
                location = data.get('location', {})
                city = location.get('city', 'Unknown')
                country = location.get('country', 'Unknown')
                
                # Check for joint appointments in the institution string
                joint_separators = [' & ', ' / ', ' and ', ' + ', ', ']
                is_joint = any(sep in current_inst for sep in joint_separators)
                
                # Check additional affiliations (any type for now, but focus on academic implied)
                # We want to see if they have ANY multiple affiliations
                
                affiliations = data.get('affiliations', [])
                
                if is_joint or (affiliations and len(affiliations) > 0):
                    person_info = {
                        'id': data.get('id'),
                        'name': data.get('name'),
                        'current': {
                            'institution': current_inst,
                            'city': city,
                            'country': country
                        },
                        'extra_affiliations': affiliations,
                        'is_joint_string': is_joint
                    }
                    multi_affil_people.append(person_info)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    print(f"\nFound {len(multi_affil_people)} people with potential multiple affiliations:\n")
    
    for p in multi_affil_people:
        print(f"Name: {p['name']} ({p['id']})")
        print(f"  Primary String: {p['current']['institution']}")
        print(f"  Location: {p['current']['city']}, {p['current']['country']}")
        
        if p['is_joint_string']:
             print("  [!] Joint appointment detected in primary institution string.")
        
        if p['extra_affiliations']:
            print("  Additional Listed Affiliations:")
            for aff in p['extra_affiliations']:
                atype = aff.get('type', 'unknown')
                name = aff.get('name', 'Unknown')
                role = aff.get('role', '')
                print(f"    - {name} ({atype}) - {role}")
        print("-" * 40)

if __name__ == "__main__":
    analyze_affiliations()
