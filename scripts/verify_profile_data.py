#!/usr/bin/env python3
"""
verify_profile_data.py

Verify profile metadata against authoritative sources.
Can be used to validate existing profiles or verify new data before ingestion.

Usage:
    python scripts/verify_profile_data.py [person-id]
    python scripts/verify_profile_data.py --all
"""

import os
import sys
import argparse
import glob
import frontmatter
import requests
from typing import Dict, List, Optional
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; IonLandscapeBot/1.0)'
}


class ProfileVerifier:
    """Verifies profile data against authoritative sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.checks = []
    
    def verify_profile(self, profile_path: str) -> Dict:
        """Verify a single profile."""
        post = frontmatter.load(profile_path)
        meta = post.metadata
        
        person_id = meta.get('id', '')
        name = meta.get('name', '')
        
        print(f"\n{'=' * 80}")
        print(f"Verifying: {name} ({person_id})")
        print(f"{'=' * 80}\n")
        
        results = {
            'id': person_id,
            'name': name,
            'checks': [],
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        self._check_required_fields(meta, results)
        
        # Check field types and formats
        self._check_field_types(meta, results)
        
        # Check links accessibility
        self._check_links(meta, results)
        
        # Verify classifications
        self._check_classifications(meta, results)
        
        # Print results
        self._print_results(results)
        
        return results
    
    def _check_required_fields(self, meta: Dict, results: Dict):
        """Check that required fields are present."""
        required = ['id', 'name', 'current_position', 'location', 'group_type']
        
        for field in required:
            if field not in meta or meta[field] is None:
                results['errors'].append(f"Missing required field: {field}")
            elif isinstance(meta[field], dict) and not meta[field]:
                results['warnings'].append(f"Empty required field: {field}")
            else:
                results['checks'].append(f"✓ Has {field}")
    
    def _check_field_types(self, meta: Dict, results: Dict):
        """Verify field types match expected schema."""
        
        # Check education structure
        if 'education' in meta and meta['education']:
            for i, edu in enumerate(meta['education']):
                if not isinstance(edu, dict):
                    results['errors'].append(f"education[{i}] is not a dict")
                    continue
                
                # Check year is int or None
                if 'year' in edu and edu['year'] is not None:
                    if not isinstance(edu['year'], int):
                        results['warnings'].append(f"education[{i}].year should be int, got {type(edu['year']).__name__}")
                
                # Check confidence field if present
                if 'confidence' in edu:
                    valid_confidence = ['confirmed', 'academictree_only', 'not_found', 'ambiguous']
                    if edu['confidence'] not in valid_confidence:
                        results['warnings'].append(f"education[{i}].confidence has invalid value: {edu['confidence']}")
        
        # Check thesis structure
        if 'thesis' in meta and meta['thesis']:
            thesis = meta['thesis']
            if isinstance(thesis, dict):
                if 'year' in thesis and thesis['year'] is not None:
                    if not isinstance(thesis['year'], int):
                        results['warnings'].append(f"thesis.year should be int, got {type(thesis['year']).__name__}")
        
        # Check location structure
        if 'location' in meta and meta['location']:
            loc = meta['location']
            if isinstance(loc, dict):
                if 'lat' in loc and loc['lat'] is not None:
                    if not isinstance(loc['lat'], (int, float)):
                        results['warnings'].append(f"location.lat should be numeric")
                if 'lon' in loc and loc['lon'] is not None:
                    if not isinstance(loc['lon'], (int, float)):
                        results['warnings'].append(f"location.lon should be numeric")
    
    def _check_links(self, meta: Dict, results: Dict):
        """Check that links are accessible."""
        if 'links' not in meta or not meta['links']:
            results['warnings'].append("No links defined")
            return
        
        links = meta['links']
        for key, url in links.items():
            if not url:
                continue
            
            try:
                # Quick HEAD request to check accessibility
                response = self.session.head(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    results['checks'].append(f"✓ Link accessible: {key}")
                elif response.status_code == 405:  # Method not allowed, try GET
                    response = self.session.get(url, timeout=10, stream=True)
                    if response.status_code == 200:
                        results['checks'].append(f"✓ Link accessible: {key}")
                else:
                    results['warnings'].append(f"Link returned {response.status_code}: {key} ({url})")
            except requests.exceptions.Timeout:
                results['warnings'].append(f"Link timeout: {key} ({url})")
            except requests.exceptions.RequestException as e:
                results['warnings'].append(f"Link error: {key} - {str(e)[:50]}")
    
    def _check_classifications(self, meta: Dict, results: Dict):
        """Verify classification fields are valid."""
        
        # Check group_type
        if 'group_type' in meta:
            if meta['group_type'] not in ['experimental', 'theory', None]:
                results['errors'].append(f"Invalid group_type: {meta['group_type']}")
        
        # Check research_focus
        if 'research_focus' in meta and meta['research_focus']:
            valid_focus = [
                'quantum_computing', 'quantum_simulation', 'optical_clocks',
                'metrology', 'quantum_networking', 'quantum_logic_spectroscopy', 'other'
            ]
            for focus in meta['research_focus']:
                if focus not in valid_focus:
                    results['warnings'].append(f"Non-standard research_focus: {focus}")
        
        # Check labels consistency with group_type
        if 'labels' in meta and 'group_type' in meta:
            expected_label = "Experimental group" if meta['group_type'] == 'experimental' else "Theory group"
            if meta['labels'] and expected_label not in meta['labels']:
                results['warnings'].append(f"Label mismatch: group_type={meta['group_type']} but labels={meta['labels']}")
    
    def _print_results(self, results: Dict):
        """Print verification results."""
        
        if results['checks']:
            print("Checks passed:")
            for check in results['checks']:
                print(f"  {check}")
        
        if results['warnings']:
            print("\n⚠️  Warnings:")
            for warning in results['warnings']:
                print(f"  - {warning}")
        
        if results['errors']:
            print("\n❌ Errors:")
            for error in results['errors']:
                print(f"  - {error}")
        
        if not results['warnings'] and not results['errors']:
            print("\n✅ All checks passed!")


def main():
    parser = argparse.ArgumentParser(description='Verify profile data')
    parser.add_argument('person_id', nargs='?', help='Person ID to verify (e.g., 001-roee-ozeri)')
    parser.add_argument('--all', action='store_true', help='Verify all profiles')
    args = parser.parse_args()
    
    verifier = ProfileVerifier()
    
    if args.all:
        # Verify all profiles
        files = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")))
        print(f"Verifying {len(files)} profiles...\n")
        
        all_results = []
        for file_path in files:
            result = verifier.verify_profile(file_path)
            all_results.append(result)
        
        # Summary
        print(f"\n{'=' * 80}")
        print("SUMMARY")
        print(f"{'=' * 80}")
        
        total_errors = sum(len(r['errors']) for r in all_results)
        total_warnings = sum(len(r['warnings']) for r in all_results)
        
        print(f"Profiles verified: {len(all_results)}")
        print(f"Total errors: {total_errors}")
        print(f"Total warnings: {total_warnings}")
        
        if total_errors > 0:
            print("\n❌ Some profiles have errors")
            return 1
        elif total_warnings > 0:
            print("\n⚠️  Some profiles have warnings")
            return 0
        else:
            print("\n✅ All profiles passed validation")
            return 0
    
    elif args.person_id:
        # Verify specific profile
        file_path = os.path.join(CONTENT_DIR, f"{args.person_id}.md")
        if not os.path.exists(file_path):
            print(f"Error: Profile not found: {file_path}")
            return 1
        
        result = verifier.verify_profile(file_path)
        
        if result['errors']:
            return 1
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
