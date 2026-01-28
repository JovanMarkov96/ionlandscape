#!/usr/bin/env python3
"""
ingest_profiles.py

Automated profile ingestion and verification for Ion Landscape.
Fetches data from authoritative ion-trapping website and enriches/creates profiles.

Usage:
    python scripts/ingest_profiles.py [--dry-run] [--limit N]
"""

import os
import sys
import glob
import json
import re
import argparse
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import frontmatter
from urllib.parse import urljoin, urlparse

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "people")
LOG_DIR = os.path.join(BASE_DIR, "scripts", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Constants
SEED_URL = "https://quantumoptics.at/en/links/ion-trapping-worldwide.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; IonLandscapeBot/1.0; +https://github.com/JovanMarkov96/ionlandscape)'
}

# Allowed fields to modify
ALLOWED_FIELDS = {
    'group_type', 'labels', 'research_focus', 'education', 'thesis',
    'homepage', 'group_page', 'google_scholar', 'orcid', 'institution_profile',
    'active', 'ion_species', 'links', 'current_position'
}

# Research focus options
RESEARCH_FOCUS_OPTIONS = [
    'quantum_computing', 'quantum_simulation', 'optical_clocks',
    'metrology', 'quantum_networking', 'quantum_logic_spectroscopy', 'other'
]


class ProfileIngestionLogger:
    """Logger for tracking profile ingestion activities."""
    
    def __init__(self, log_file: str = None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(LOG_DIR, f"ingestion_{timestamp}.log")
        self.log_file = log_file
        self.entries = []
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.entries.append(entry)
        print(entry)
        
    def save(self):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.entries))
        print(f"\nLog saved to: {self.log_file}")


class SourceTracker:
    """Tracks sources used for each fact."""
    
    def __init__(self):
        self.sources = {}
        
    def add(self, person_id: str, source_url: str, note: str = ""):
        if person_id not in self.sources:
            self.sources[person_id] = []
        self.sources[person_id].append({
            'url': source_url,
            'note': note,
            'timestamp': datetime.now().isoformat()
        })
        
    def get(self, person_id: str) -> List[Dict]:
        return self.sources.get(person_id, [])
    
    def save_report(self, output_file: str):
        """Save source tracking report."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.sources, f, indent=2, ensure_ascii=False)


class ProfileManager:
    """Manages profile loading, creation, and updates."""
    
    def __init__(self, content_dir: str, logger: ProfileIngestionLogger):
        self.content_dir = content_dir
        self.logger = logger
        self.profiles = {}
        self.load_existing_profiles()
        
    def load_existing_profiles(self):
        """Load all existing markdown profiles."""
        for md_path in glob.glob(os.path.join(self.content_dir, "*.md")):
            try:
                post = frontmatter.load(md_path)
                person_id = post.metadata.get('id')
                name = post.metadata.get('name', '')
                
                if person_id:
                    self.profiles[person_id] = {
                        'path': md_path,
                        'metadata': post.metadata,
                        'content': post.content,
                        'name': name
                    }
                    # Also index by normalized name
                    norm_name = self.normalize_name(name)
                    self.profiles[norm_name] = self.profiles[person_id]
                    
            except Exception as e:
                self.logger.log(f"Error loading {md_path}: {e}", "ERROR")
                
        self.logger.log(f"Loaded {len(set([p['path'] for p in self.profiles.values()]))} existing profiles")
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize name for comparison."""
        return re.sub(r'[^\w\s]', '', name.lower().strip())
    
    def find_profile(self, name: str, institution: str = None) -> Optional[Dict]:
        """Find profile by name and optionally institution."""
        norm_name = self.normalize_name(name)
        
        # Direct match
        if norm_name in self.profiles:
            return self.profiles[norm_name]
        
        # Fuzzy match by name similarity
        for profile_data in set([p for p in self.profiles.values()]):
            profile_norm = self.normalize_name(profile_data['name'])
            if self._names_similar(norm_name, profile_norm):
                # If institution provided, verify it matches
                if institution:
                    profile_inst = profile_data['metadata'].get('current_position', {}).get('institution', '')
                    if institution.lower() in profile_inst.lower() or profile_inst.lower() in institution.lower():
                        return profile_data
                else:
                    return profile_data
        
        return None
    
    @staticmethod
    def _names_similar(name1: str, name2: str) -> bool:
        """Check if two normalized names are similar."""
        # Simple heuristic: check if one contains the other or Levenshtein distance is small
        if name1 in name2 or name2 in name1:
            return True
        
        # Check if last names match (simple heuristic)
        parts1 = name1.split()
        parts2 = name2.split()
        if parts1 and parts2 and parts1[-1] == parts2[-1]:
            return True
            
        return False
    
    def get_next_id(self) -> str:
        """Get next available ID number."""
        existing_ids = []
        for profile in set([p for p in self.profiles.values()]):
            pid = profile['metadata'].get('id', '')
            match = re.match(r'(\d+)-', pid)
            if match:
                existing_ids.append(int(match.group(1)))
        
        if existing_ids:
            return str(max(existing_ids) + 1).zfill(3)
        return "001"
    
    def create_profile(self, metadata: Dict, content: str = "") -> str:
        """Create a new profile and return the file path."""
        person_id = metadata.get('id')
        if not person_id:
            raise ValueError("Profile must have an ID")
        
        filename = f"{person_id}.md"
        filepath = os.path.join(self.content_dir, filename)
        
        # Ensure required fields
        if 'created_at' not in metadata:
            metadata['created_at'] = datetime.now().strftime('%Y-%m-%d')
        if 'updated_at' not in metadata:
            metadata['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        
        # Create frontmatter post
        post = frontmatter.Post(content, **metadata)
        
        # Write file
        with open(filepath, 'wb') as f:
            frontmatter.dump(post, f)
        
        self.logger.log(f"Created new profile: {filename}")
        return filepath
    
    def update_profile(self, profile_path: str, updates: Dict, preserve_content: bool = True):
        """Update an existing profile."""
        post = frontmatter.load(profile_path)
        
        # Apply updates only to allowed fields
        for key, value in updates.items():
            if key in ALLOWED_FIELDS:
                post.metadata[key] = value
        
        # Update timestamp
        post.metadata['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        
        # Write back
        with open(profile_path, 'wb') as f:
            frontmatter.dump(post, f)
        
        self.logger.log(f"Updated profile: {os.path.basename(profile_path)}")


class WebScraper:
    """Scrapes and extracts data from web sources."""
    
    def __init__(self, logger: ProfileIngestionLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_ion_trapping_list(self) -> List[Dict]:
        """Fetch the authoritative list of ion trapping groups."""
        try:
            response = self.session.get(SEED_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            groups = []
            
            # Parse the structure - this needs to be adapted based on actual HTML structure
            # Looking for patterns like: PI Name, Institution, Country
            # This is a placeholder that would need actual website structure analysis
            
            # For now, return empty list if parsing fails
            # Real implementation would parse the HTML structure
            self.logger.log(f"Fetched ion trapping list from {SEED_URL}")
            
            # Try to find tables or lists with researcher information
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        # Extract data (this is a generic parser, needs customization)
                        group_info = {
                            'raw_text': ' '.join([cell.get_text().strip() for cell in cells]),
                            'cells': [cell.get_text().strip() for cell in cells]
                        }
                        groups.append(group_info)
            
            # Also look for lists
            lists = soup.find_all(['ul', 'ol'])
            for ul in lists:
                items = ul.find_all('li')
                for item in items:
                    text = item.get_text().strip()
                    if text and len(text) > 10:  # Reasonable minimum length
                        groups.append({
                            'raw_text': text,
                            'links': [a.get('href') for a in item.find_all('a', href=True)]
                        })
            
            self.logger.log(f"Extracted {len(groups)} potential groups/entries")
            return groups
            
        except Exception as e:
            self.logger.log(f"Error fetching ion trapping list: {e}", "ERROR")
            return []
    
    def verify_group_page(self, url: str) -> Dict:
        """Verify and extract information from a group page."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            info = {
                'verified': True,
                'url': url,
                'title': soup.title.string if soup.title else '',
                'text_content': soup.get_text()[:1000]  # First 1000 chars for analysis
            }
            
            # Look for indicators of experimental vs theory
            text_lower = soup.get_text().lower()
            if any(keyword in text_lower for keyword in ['lab', 'apparatus', 'vacuum', 'laser', 'trap']):
                info['likely_experimental'] = True
            if any(keyword in text_lower for keyword in ['simulation', 'theoretical', 'theory', 'numerical']):
                info['likely_theory'] = True
            
            return info
            
        except Exception as e:
            self.logger.log(f"Error verifying {url}: {e}", "WARNING")
            return {'verified': False, 'url': url, 'error': str(e)}


def parse_group_entry(entry: Dict) -> Optional[Dict]:
    """Parse a group entry from the scraped data."""
    raw_text = entry.get('raw_text', '')
    
    # Try to extract PI name and institution
    # This is a heuristic parser that would need refinement based on actual data format
    
    # Common patterns:
    # "PI Name, Institution, Country"
    # "PI Name (Institution)"
    # "PI Name - Institution"
    
    parsed = {}
    
    # Look for patterns
    if ',' in raw_text:
        parts = [p.strip() for p in raw_text.split(',')]
        if len(parts) >= 2:
            parsed['name'] = parts[0]
            parsed['institution'] = parts[1]
            if len(parts) >= 3:
                parsed['country'] = parts[2]
    
    # Extract links if available
    if 'links' in entry and entry['links']:
        parsed['homepage'] = entry['links'][0]  # First link is often homepage
    
    return parsed if parsed else None


def main():
    parser = argparse.ArgumentParser(description='Ingest and verify ion trapping profiles')
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes')
    parser.add_argument('--limit', type=int, help='Limit number of profiles to process')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Initialize
    logger = ProfileIngestionLogger()
    source_tracker = SourceTracker()
    profile_manager = ProfileManager(CONTENT_DIR, logger)
    scraper = WebScraper(logger)
    
    logger.log("=" * 80)
    logger.log("Ion Landscape Automated Profile Ingestion")
    logger.log("=" * 80)
    
    if args.dry_run:
        logger.log("DRY RUN MODE - No changes will be made")
    
    # Fetch the authoritative list
    logger.log("\nFetching ion trapping groups list...")
    groups = scraper.fetch_ion_trapping_list()
    
    if not groups:
        logger.log("No groups found. Check network connection or website structure.", "ERROR")
        logger.log("\nNOTE: This script requires web access to fetch the authoritative list.")
        logger.log("If the website is not accessible, you can:")
        logger.log("1. Manually download the HTML and place it in scripts/data/")
        logger.log("2. Provide a JSON file with group information")
        logger.save()
        return 1
    
    # Process each group
    processed = 0
    created = 0
    updated = 0
    skipped = 0
    
    for i, group_entry in enumerate(groups):
        if args.limit and processed >= args.limit:
            break
        
        logger.log(f"\n--- Processing entry {i+1}/{len(groups)} ---")
        
        # Parse the entry
        parsed = parse_group_entry(group_entry)
        if not parsed or 'name' not in parsed:
            logger.log(f"Could not parse entry: {group_entry.get('raw_text', '')[:100]}", "WARNING")
            skipped += 1
            continue
        
        name = parsed['name']
        institution = parsed.get('institution', '')
        
        logger.log(f"Processing: {name} ({institution})")
        
        # Check if profile exists
        existing = profile_manager.find_profile(name, institution)
        
        if existing:
            logger.log(f"Found existing profile: {existing['name']}")
            
            # Verify and enrich
            updates = {}
            
            # Add homepage if missing
            if 'homepage' in parsed and not existing['metadata'].get('links', {}).get('homepage'):
                if 'links' not in updates:
                    updates['links'] = existing['metadata'].get('links', {}).copy()
                updates['links']['homepage'] = parsed['homepage']
                source_tracker.add(existing['metadata']['id'], parsed['homepage'], 'homepage')
            
            # Apply updates if any
            if updates and not args.dry_run:
                profile_manager.update_profile(existing['path'], updates)
                updated += 1
            elif updates:
                logger.log(f"Would update: {list(updates.keys())}")
            else:
                logger.log("No updates needed")
        else:
            logger.log(f"Profile not found - would need to create new profile")
            logger.log(f"  Name: {name}")
            logger.log(f"  Institution: {institution}")
            
            # Would create new profile here, but we need more verified data
            # For now, just log it as requiring manual review
            logger.log("  → Flagged for manual review (needs more verified data)")
            skipped += 1
        
        processed += 1
    
    # Summary
    logger.log("\n" + "=" * 80)
    logger.log("SUMMARY")
    logger.log("=" * 80)
    logger.log(f"Total entries processed: {processed}")
    logger.log(f"Profiles updated: {updated}")
    logger.log(f"Profiles created: {created}")
    logger.log(f"Entries skipped/flagged: {skipped}")
    
    # Save reports
    logger.save()
    
    if source_tracker.sources:
        source_file = os.path.join(LOG_DIR, f"sources_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        source_tracker.save_report(source_file)
        logger.log(f"\nSource tracking saved to: {source_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
