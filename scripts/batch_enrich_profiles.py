#!/usr/bin/env python3
"""
batch_enrich_profiles.py

Batch enrichment tool for profiles based on a JSON input file.
Useful when the authoritative website is not directly accessible.

Input JSON format:
[
  {
    "name": "Jonathan P. Home",
    "institution": "ETH Zürich",
    "homepage": "https://iqe.phys.ethz.ch/...",
    "country": "Switzerland",
    "verified_sources": [
      "https://www.phys.ethz.ch/..."
    ]
  },
  ...
]

Usage:
    python scripts/batch_enrich_profiles.py input_data.json [--dry-run]
"""

import os
import sys
import json
import argparse
import glob
import frontmatter
from datetime import datetime
from typing import Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")


class BatchEnricher:
    """Batch profile enrichment tool."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.profiles = {}
        self.load_profiles()
        self.stats = {
            'processed': 0,
            'updated': 0,
            'created': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def load_profiles(self):
        """Load existing profiles."""
        for md_path in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
            try:
                post = frontmatter.load(md_path)
                name = post.metadata.get('name', '').lower().strip()
                if name:
                    self.profiles[name] = {
                        'path': md_path,
                        'metadata': post.metadata,
                        'content': post.content
                    }
            except Exception as e:
                print(f"Error loading {md_path}: {e}")
    
    def normalize_name(self, name: str) -> str:
        """Normalize name for matching."""
        import re
        # Remove special characters, convert to lowercase
        return re.sub(r'[^\w\s]', '', name.lower().strip())
    
    def find_profile(self, name: str) -> Optional[Dict]:
        """Find profile by name."""
        norm_name = self.normalize_name(name)
        
        # Direct match
        if norm_name in self.profiles:
            return self.profiles[norm_name]
        
        # Fuzzy match
        for profile_name, profile_data in self.profiles.items():
            if self.names_match(norm_name, profile_name):
                return profile_data
        
        return None
    
    @staticmethod
    def names_match(name1: str, name2: str) -> bool:
        """Check if names match (fuzzy)."""
        # Simple: check if one is substring of other or last names match
        if name1 in name2 or name2 in name1:
            return True
        
        parts1 = name1.split()
        parts2 = name2.split()
        
        if parts1 and parts2 and parts1[-1] == parts2[-1]:
            # Last names match
            return True
        
        return False
    
    def enrich_profile(self, data: Dict):
        """Enrich a single profile with provided data."""
        name = data.get('name')
        if not name:
            print("  ❌ Missing name in input data")
            self.stats['errors'] += 1
            return
        
        print(f"\n📝 Processing: {name}")
        
        existing = self.find_profile(name)
        
        if existing:
            print(f"  ✓ Found existing profile: {existing['metadata'].get('id')}")
            self.update_existing_profile(existing, data)
        else:
            print(f"  ℹ  Profile not found")
            print(f"  → Would need to create new profile (requires more complete data)")
            self.stats['skipped'] += 1
        
        self.stats['processed'] += 1
    
    def update_existing_profile(self, profile: Dict, data: Dict):
        """Update existing profile with new data."""
        post = frontmatter.load(profile['path'])
        metadata = post.metadata
        
        updates_made = []
        
        # Update homepage if provided and not already set
        if 'homepage' in data and data['homepage']:
            current_homepage = metadata.get('links', {}).get('homepage')
            if not current_homepage:
                if 'links' not in metadata:
                    metadata['links'] = {}
                metadata['links']['homepage'] = data['homepage']
                updates_made.append('homepage')
        
        # Update group page if provided
        if 'group_page' in data and data['group_page']:
            current_group_page = metadata.get('links', {}).get('group_page')
            if not current_group_page:
                if 'links' not in metadata:
                    metadata['links'] = {}
                metadata['links']['group_page'] = data['group_page']
                updates_made.append('group_page')
        
        # Update institution if provided and current is empty
        if 'institution' in data and data['institution']:
            current_inst = metadata.get('current_position', {}).get('institution')
            if not current_inst:
                if 'current_position' not in metadata:
                    metadata['current_position'] = {}
                metadata['current_position']['institution'] = data['institution']
                updates_made.append('institution')
        
        # Log sources if provided
        sources = data.get('verified_sources', [])
        if sources:
            print(f"  📚 Sources:")
            for source in sources:
                print(f"    - {source}")
        
        if updates_made:
            print(f"  ✏️  Updates: {', '.join(updates_made)}")
            
            if not self.dry_run:
                # Update timestamp
                metadata['updated_at'] = datetime.now().strftime('%Y-%m-%d')
                
                # Write back
                with open(profile['path'], 'wb') as f:
                    frontmatter.dump(post, f)
                
                print(f"  ✅ Saved")
                self.stats['updated'] += 1
            else:
                print(f"  🔍 DRY RUN - no changes made")
        else:
            print(f"  ℹ  No updates needed")
    
    def print_summary(self):
        """Print summary statistics."""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Processed: {self.stats['processed']}")
        print(f"Updated: {self.stats['updated']}")
        print(f"Created: {self.stats['created']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Errors: {self.stats['errors']}")


def main():
    parser = argparse.ArgumentParser(description='Batch enrich profiles from JSON')
    parser.add_argument('input_file', help='JSON file with profile data')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        return 1
    
    # Load input data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print("Error: Input JSON must be an array of objects")
        return 1
    
    print("=" * 80)
    print("Batch Profile Enrichment")
    print("=" * 80)
    print(f"Input file: {args.input_file}")
    print(f"Entries: {len(data)}")
    if args.dry_run:
        print("Mode: DRY RUN")
    print()
    
    enricher = BatchEnricher(dry_run=args.dry_run)
    
    for entry in data:
        enricher.enrich_profile(entry)
    
    enricher.print_summary()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
