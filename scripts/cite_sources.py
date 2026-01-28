#!/usr/bin/env python3
"""
cite_sources.py

Helper tool to document sources used for profile data.
Creates structured source citations that can be referenced in commits.

Usage:
    python scripts/cite_sources.py 016-jonathan-home [--add-citation]
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITATIONS_FILE = os.path.join(BASE_DIR, "scripts", "data", "source_citations.json")


class SourceCitationManager:
    """Manages source citations for profiles."""
    
    def __init__(self):
        self.citations = self.load_citations()
    
    def load_citations(self) -> Dict:
        """Load existing citations."""
        if os.path.exists(CITATIONS_FILE):
            with open(CITATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_citations(self):
        """Save citations to file."""
        os.makedirs(os.path.dirname(CITATIONS_FILE), exist_ok=True)
        with open(CITATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.citations, f, indent=2, ensure_ascii=False)
    
    def add_citation(self, person_id: str, source_url: str, field: str, note: str = ""):
        """Add a source citation."""
        if person_id not in self.citations:
            self.citations[person_id] = []
        
        citation = {
            'url': source_url,
            'field': field,
            'note': note,
            'added': datetime.now().isoformat()
        }
        
        self.citations[person_id].append(citation)
        self.save_citations()
        print(f"✅ Added citation for {person_id}: {field}")
    
    def get_citations(self, person_id: str) -> List[Dict]:
        """Get citations for a person."""
        return self.citations.get(person_id, [])
    
    def format_commit_message(self, person_id: str, name: str) -> str:
        """Format a commit message with sources."""
        citations = self.get_citations(person_id)
        
        if not citations:
            return f"data: verify & enrich profile — {name}\n\nNo sources documented yet."
        
        # Group by field
        by_field = {}
        unique_urls = set()
        
        for citation in citations:
            field = citation['field']
            if field not in by_field:
                by_field[field] = []
            by_field[field].append(citation)
            unique_urls.add(citation['url'])
        
        # Build message
        message = f"data: verify & enrich profile — {name}\n\n"
        
        # List fields updated
        message += "Updated fields:\n"
        for field in sorted(by_field.keys()):
            message += f"- {field}\n"
        
        message += "\nSources:\n"
        for url in sorted(unique_urls):
            message += f"- {url}\n"
        
        # Add field-specific notes if any
        notes = []
        for field, cites in by_field.items():
            for cite in cites:
                if cite.get('note'):
                    notes.append(f"{field}: {cite['note']}")
        
        if notes:
            message += "\nNotes:\n"
            for note in notes:
                message += f"- {note}\n"
        
        return message
    
    def interactive_add(self, person_id: str):
        """Interactively add citations."""
        print(f"\n{'=' * 80}")
        print(f"Add Source Citation for {person_id}")
        print(f"{'=' * 80}\n")
        
        while True:
            print("\nEnter source information (or 'done' to finish):")
            
            field = input("  Field name (e.g., 'advisor', 'thesis.title'): ").strip()
            if field.lower() == 'done':
                break
            
            if not field:
                print("  Field name is required")
                continue
            
            url = input("  Source URL: ").strip()
            if not url:
                print("  URL is required")
                continue
            
            note = input("  Note (optional): ").strip()
            
            self.add_citation(person_id, url, field, note)
            
            another = input("\n  Add another citation? [y/N]: ").strip().lower()
            if another not in ['y', 'yes']:
                break
        
        print(f"\n{'=' * 80}")
        print("Summary")
        print(f"{'=' * 80}\n")
        self.show_citations(person_id)
    
    def show_citations(self, person_id: str):
        """Display citations for a person."""
        citations = self.get_citations(person_id)
        
        if not citations:
            print(f"No citations found for {person_id}")
            return
        
        print(f"Citations for {person_id}:")
        print()
        
        for i, citation in enumerate(citations, 1):
            print(f"{i}. Field: {citation['field']}")
            print(f"   URL: {citation['url']}")
            if citation.get('note'):
                print(f"   Note: {citation['note']}")
            print(f"   Added: {citation['added']}")
            print()


def main():
    parser = argparse.ArgumentParser(description='Manage source citations')
    parser.add_argument('person_id', help='Person ID (e.g., 016-jonathan-home)')
    parser.add_argument('--add', action='store_true', help='Add new citation interactively')
    parser.add_argument('--show', action='store_true', help='Show existing citations')
    parser.add_argument('--commit-msg', action='store_true', help='Generate commit message')
    parser.add_argument('--name', help='Person name (for commit message)')
    args = parser.parse_args()
    
    manager = SourceCitationManager()
    
    if args.add:
        manager.interactive_add(args.person_id)
    elif args.show:
        manager.show_citations(args.person_id)
    elif args.commit_msg:
        name = args.name or args.person_id
        message = manager.format_commit_message(args.person_id, name)
        print(message)
        
        # Save to clipboard if available (optional enhancement)
        try:
            import pyperclip
            pyperclip.copy(message)
            print("\n📋 Commit message copied to clipboard!")
        except ImportError:
            pass
    else:
        # Default: show citations
        manager.show_citations(args.person_id)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
