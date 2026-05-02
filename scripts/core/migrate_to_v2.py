#!/usr/bin/env python3
"""
migrate_to_v2.py — migrate content/{people,companies,institutions}/*.md
to the v2 person schema and v1 company / institution schemas.

What this script does:
  - Adds `schema_version`, `entity_type` to every entry.
  - Maps free-form `platforms` strings to controlled-vocabulary enums.
  - Drops items that aren't platforms in the new model (e.g. "Optical clocks"
    moves to `applications`; "Software" on a company moves to `modality`).
  - For people: derives `applications` from keywords + the old platforms list,
    falling back to `["computing"]` for experimental groups with no inferable
    application (these entries are flagged in the migration report for
    Stage-3 review).
  - For people: sets `active: "active"` (old boolean field is unused).
  - For companies: maps old `status.operating_status: "active"` to the new
    enum (`private` / `public`); IonQ special-cased to `public`.
  - For companies: infers `modality` (hardware / software / both / services).
  - Drops the unused `research_focus` field on people.
  - Adds the optional provenance fields with null values.

What this script does NOT do:
  - Any new research. It is shape conversion plus lossless inference.
  - Any per-field source attribution. That is Stage 3.
  - Any cross-entity id resolution (e.g. populating `advisor_id` from advisor
    name strings). That is also Stage 3.

Idempotent: re-running on already-migrated entries is a no-op.

Usage:
    python scripts/core/migrate_to_v2.py --dry-run
    python scripts/core/migrate_to_v2.py
"""

import argparse
import glob
import os
import sys
from pathlib import Path

import frontmatter
import yaml

ROOT = Path(__file__).resolve().parents[2]
PEOPLE_DIR = ROOT / "content" / "people"
COMPANIES_DIR = ROOT / "content" / "companies"
INSTITUTIONS_DIR = ROOT / "content" / "institutions"
REPORT_PATH = ROOT / "private" / "migration_report.md"

# ── Platform mapping ──────────────────────────────────────────────────────
# Old free-form strings → canonical enum values from schemas/vocabularies.yaml.
# A value of None means the string should be dropped (handled separately
# below if it's actually an application or modality signal).

PLATFORM_MAP = {
    "trapped ions": "trapped_ion",
    "trapped ion": "trapped_ion",
    "trapped-ion": "trapped_ion",
    "penning traps": "trapped_ion",
    "molecular ions": "trapped_molecule",
    "neutral atoms": "neutral_atom",
    "neutral atom": "neutral_atom",
    "ultracold atoms": "neutral_atom",
    "rydberg atoms": "rydberg_array",
    "rydberg arrays": "rydberg_array",
    "superconducting": "superconducting",
    "superconducting qubits": "superconducting",
    "superconducting quantum computing": "superconducting",
    "nv centers": "nv_center",
    "nv-centers": "nv_center",
    "nv center": "nv_center",
    "nitrogen-vacancy": "nv_center",
    "color centers": "color_center",
    "colour centres": "color_center",
    "photonic": "photonic",
    "photonics": "photonic",
    "photonic qubits": "photonic",
    "photonic quantum computing": "photonic",
    "hybrid photon-atom qubit architecture": "photonic",
    "trapped molecules": "trapped_molecule",
    "trapped molecule": "trapped_molecule",
    "topological": "topological",
    "topological qubits": "topological",
    "silicon spin": "silicon_spin",
    "silicon qubits": "silicon_spin",
    "spin qubits": "silicon_spin",
    "semiconductor-based quantum devices": "silicon_spin",
    "quantum dots": "quantum_dot",
    "cavity qed": "cavity_qed_hybrid",
    "cavity qed / ion–photon interfaces": "cavity_qed_hybrid",
    "hybrid systems": "cavity_qed_hybrid",
    "hybrid atom–ion systems": "cavity_qed_hybrid",
    # Drop entirely — handled via PLATFORM_TO_APPLICATION / signals instead.
    "optical clocks": None,
    "atomic clocks": None,
    "quantum information": None,
    "quantum computing": None,
    "quantum metrology": None,
    "quantum simulation": None,
    "quantum logic spectroscopy": None,
    "quantum communication": None,
    "quantum key distribution (qkd)": None,
    "quantum repeaters": None,
    "quantum-safe networking": None,
    "software": None,
    "control software": None,
    "quantum software development": None,
    "quantum software development platform": None,
    "quantum algorithm design tools": None,
    "hardware-agnostic circuit synthesis": None,
    "hybrid quantum-classical orchestration": None,
    "quantum control hardware": None,
    "quantum error mitigation & noise resilience software": None,
    "scalable million-qubit architectures": None,
    "quantum ecosystem development": None,
    "industry collaboration network": None,
    "ecosystem": None,
}

# Strings that imply an application axis (independent of whether they're
# also a real platform — they're processed first).
PLATFORM_TO_APPLICATION = {
    "optical clocks": "optical_clocks",
    "atomic clocks": "optical_clocks",
    "quantum metrology": "sensing_metrology",
    "quantum simulation": "simulation",
    "quantum computing": "computing",
    "quantum logic spectroscopy": "fundamental_physics",
    "quantum communication": "networking",
    "quantum key distribution (qkd)": "networking",
    "quantum repeaters": "networking",
    "quantum-safe networking": "networking",
    "quantum error mitigation & noise resilience software": "software_control",
}

# Old institution_type strings that don't match the new enum.
INSTITUTION_TYPE_MAP = {
    "research_center": "research_centre",
    "research_institute": "research_centre",
    "university_research_center": "research_centre",
    "government_lab": "national_lab",
    "company": "industry_research_lab",
    "nonprofit": "non_profit",
}

# Funding round-name → controlled stage enum.
ROUND_TO_STAGE = {
    "pre-seed": "pre_seed",
    "pre seed": "pre_seed",
    "seed": "seed",
    "seed & extensions": "seed",
    "seed extension": "seed",
    "extended seed": "seed",
    "series a": "series_a",
    "series b": "series_b",
    "series c": "series_c",
    "series d": "series_d",
    "series e": "series_e_plus",
    "series f": "series_e_plus",
    "ipo": "ipo",
    "grant": "grant",
    "government grant": "grant",
    "darpa": "government_contract",
    "convertible": "convertible_note",
    "convertible note": "convertible_note",
    "bridge": "bridge",
    "secondary": "secondary",
    "acquisition": "acquisition",
    "undisclosed": "undisclosed",
}

# Strings that signal modality on companies.
SOFTWARE_PLATFORMS = {
    "software", "control software", "quantum software development",
    "quantum software development platform", "quantum algorithm design tools",
    "hardware-agnostic circuit synthesis", "hybrid quantum-classical orchestration",
    "quantum error mitigation & noise resilience software",
}

HARDWARE_PLATFORMS = {
    "quantum control hardware",
}

# ── Application inference ────────────────────────────────────────────────
# Substring match on lowercased keywords / labels / focus_areas.

KEYWORD_APPLICATION_HINTS = {
    "quantum computing":           "computing",
    "trapped-ion quantum computing": "computing",
    "ion trap quantum computing":  "computing",
    "fault-tolerant":              "computing",
    "error correction":            "computing",
    "scalable quantum computing":  "computing",
    "quantum simulation":          "simulation",
    "many-body":                   "simulation",
    "lattice gauge":               "simulation",
    "quantum chemistry":           "simulation",
    "hubbard":                     "simulation",
    "quantum networking":          "networking",
    "quantum repeater":            "networking",
    "qkd":                         "networking",
    "quantum key distribution":    "networking",
    "quantum internet":            "networking",
    "quantum metrology":           "sensing_metrology",
    "quantum sensing":             "sensing_metrology",
    "magnetometry":                "sensing_metrology",
    "gravimetry":                  "sensing_metrology",
    "atomic clock":                "optical_clocks",
    "optical clock":               "optical_clocks",
    "frequency standard":          "optical_clocks",
    "fundamental physics":         "fundamental_physics",
    "edm":                         "fundamental_physics",
    "electron edm":                "fundamental_physics",
    "fine structure constant":     "fundamental_physics",
    "alpha variation":             "fundamental_physics",
    "qed test":                    "fundamental_physics",
    "beyond standard model":       "fundamental_physics",
    "control software":            "software_control",
    "compiler":                    "software_control",
    "quantum software":            "software_control",
    "quantum control":             "software_control",
    "noise mitigation":            "software_control",
}

# Platforms that, if present, justify defaulting applications to ["computing"]
# for experimental groups with no other inferable application.
COMPUTING_FALLBACK_PLATFORMS = {
    "trapped_ion", "neutral_atom", "rydberg_array", "superconducting",
    "nv_center", "color_center", "photonic", "silicon_spin", "quantum_dot",
    "topological", "trapped_molecule", "cavity_qed_hybrid",
}


# ── Migration helpers ────────────────────────────────────────────────────

class Report:
    """Collects what changed and what the script had to guess."""

    def __init__(self):
        self.migrated = []         # [(fname, entity_type)]
        self.skipped = []          # already migrated
        self.unmapped_platforms = []  # [(fname, value)]
        self.defaulted_applications = []  # [fname]
        self.defaulted_modality = []      # [fname]
        self.unmapped_status = []         # [(fname, value)]
        self.dropped_fields = []          # [(fname, key)] removed by scrub
        self.errors = []                  # [(fname, message)]


CANONICAL_PLATFORMS = {
    "trapped_ion", "neutral_atom", "rydberg_array", "superconducting",
    "nv_center", "color_center", "photonic", "trapped_molecule",
    "topological", "silicon_spin", "quantum_dot", "cavity_qed_hybrid",
}


def _map_platforms(old, fname, report, *, capture_modality=False):
    """Return (new_platforms, derived_applications, software_signal, hardware_signal)."""
    new_platforms = []
    derived_applications = []
    software = False
    hardware = False
    for p in (old or []):
        p_low = p.lower().strip()
        # Already-canonical values pass through (idempotency under --force).
        if p_low in CANONICAL_PLATFORMS:
            new_platforms.append(p_low)
            continue
        # Application signals are extracted unconditionally.
        if p_low in PLATFORM_TO_APPLICATION:
            derived_applications.append(PLATFORM_TO_APPLICATION[p_low])
        if capture_modality:
            if p_low in SOFTWARE_PLATFORMS:
                software = True
                continue
            if p_low in HARDWARE_PLATFORMS:
                hardware = True
                continue
        if p_low in PLATFORM_MAP:
            mapped = PLATFORM_MAP[p_low]
            if mapped:
                new_platforms.append(mapped)
        else:
            report.unmapped_platforms.append((fname, p))
    seen = set()
    new_platforms = [p for p in new_platforms if not (p in seen or seen.add(p))]
    return new_platforms, derived_applications, software, hardware


def _infer_applications_from_strings(strings):
    found = set()
    for s in strings:
        s_low = (s or "").lower()
        for hint, app in KEYWORD_APPLICATION_HINTS.items():
            if hint in s_low:
                found.add(app)
    return found


def _coerce_str(val):
    if val is None:
        return None
    if isinstance(val, str):
        return val
    return str(val)


def _infer_stage(round_label):
    if not round_label:
        return "undisclosed"
    rl = round_label.lower().strip()
    if rl in ROUND_TO_STAGE:
        return ROUND_TO_STAGE[rl]
    for key, stage in ROUND_TO_STAGE.items():
        if key in rl:
            return stage
    return "undisclosed"


def _normalize_funding(funding):
    """Normalize old funding shape to the v1 schema."""
    if not isinstance(funding, dict):
        return funding
    out = dict(funding)
    # Rename total_usd → total_raised_usd
    if "total_usd" in out:
        out["total_raised_usd"] = out.pop("total_usd")
    # Each round: ensure stage; preserve notes
    if isinstance(out.get("rounds"), list):
        new_rounds = []
        for r in out["rounds"]:
            if not isinstance(r, dict):
                continue
            nr = dict(r)
            if "stage" not in nr:
                nr["stage"] = _infer_stage(nr.get("round"))
            new_rounds.append(nr)
        out["rounds"] = new_rounds
    return out


def _normalize_milestones(ms):
    """Old milestones use {description, sources[]}; new uses {claim, source}."""
    if not isinstance(ms, list):
        return ms
    out = []
    for m in ms:
        if not isinstance(m, dict):
            continue
        nm = dict(m)
        if "claim" not in nm and "description" in nm:
            nm["claim"] = nm.pop("description")
        if "source" not in nm and "sources" in nm:
            srcs = nm.pop("sources")
            if isinstance(srcs, list) and srcs:
                first = srcs[0]
                if isinstance(first, dict):
                    nm["source"] = first.get("url")
                else:
                    nm["source"] = first
        # drop any other unrecognised fields
        nm = {k: v for k, v in nm.items() if k in ("date", "claim", "source")}
        out.append(nm)
    return out


def _normalize_education(edu_list):
    if not isinstance(edu_list, list):
        return edu_list
    allowed = {"degree", "institution", "year", "advisor", "advisor_id",
               "confidence", "note", "source"}
    return [{k: v for k, v in e.items() if k in allowed}
            for e in edu_list if isinstance(e, dict)]


def _normalize_postdocs(pd_list):
    if not isinstance(pd_list, list):
        return pd_list
    allowed = {"institution", "advisor", "advisor_id", "years", "year",
               "confidence", "note", "source"}
    out = []
    for p in pd_list:
        if not isinstance(p, dict):
            continue
        np = {k: v for k, v in p.items() if k in allowed}
        if isinstance(np.get("years"), int):
            np["years"] = str(np["years"])
        out.append(np)
    return out


def _normalize_ion_species(species):
    if not isinstance(species, list):
        return species
    out = []
    for s in species:
        if not isinstance(s, str):
            continue
        s_strip = s.strip()
        # Skip non-formula descriptive strings; the regex won't match.
        if " " in s_strip:
            continue
        out.append(s_strip)
    return out


def _normalize_affiliations(affs):
    if not isinstance(affs, list):
        return affs
    out = []
    type_map = {"nonprofit": "non_profit"}
    for a in affs:
        if not isinstance(a, dict):
            continue
        na = dict(a)
        t = na.get("type")
        if t in type_map:
            na["type"] = type_map[t]
        out.append(na)
    return out


def migrate_person(meta, fname, report, force=False):
    if not force and meta.get("schema_version") == 2:
        return None

    new = dict(meta)
    new["schema_version"] = 2
    new["entity_type"] = "person"

    # Normalize sub-structures
    if "education" in new:
        new["education"] = _normalize_education(new["education"])
    if "postdocs" in new:
        new["postdocs"] = _normalize_postdocs(new["postdocs"])
    if "ion_species" in new:
        new["ion_species"] = _normalize_ion_species(new["ion_species"])
    if "affiliations" in new:
        new["affiliations"] = _normalize_affiliations(new["affiliations"])

    # platforms
    new_platforms, derived_apps, _sw, _hw = _map_platforms(meta.get("platforms"), fname, report)
    new["platforms"] = new_platforms

    # applications — preserve any already-set values, then add inferred
    inferred = _infer_applications_from_strings(
        list(meta.get("keywords") or []) +
        list(meta.get("labels") or []) +
        list(meta.get("research_focus") or [])
    )
    apps = set(meta.get("applications") or []) | set(derived_apps) | inferred
    group_type = meta.get("group_type", "experimental")
    if group_type in ("experimental", "mixed") and not apps:
        if any(p in COMPUTING_FALLBACK_PLATFORMS for p in new_platforms):
            apps.add("computing")
            report.defaulted_applications.append(fname)
    new["applications"] = sorted(apps)

    # active enum
    old_active = meta.get("active")
    if isinstance(old_active, bool):
        new["active"] = "active" if old_active else "retired"
    elif isinstance(old_active, str) and old_active in ("active", "retired", "deceased", "unknown"):
        new["active"] = old_active
    else:
        new["active"] = "active"  # default

    # drop unused field
    new.pop("research_focus", None)

    # provenance
    new.setdefault("last_verified_at", None)
    new.setdefault("verification_source_count", None)

    new = _scrub(new, PERSON_ALLOWED, fname, report)
    report.migrated.append((fname, "person"))
    return new


def migrate_company(meta, fname, report, force=False):
    if not force and (
            meta.get("schema_version") == 1
            and meta.get("entity_type") == "company"
            and "modality" in meta):
        return None

    new = dict(meta)
    new["schema_version"] = 1
    new["entity_type"] = "company"

    # platforms + modality
    new_platforms, derived_apps, software_signal, hardware_signal = _map_platforms(
        meta.get("platforms"), fname, report, capture_modality=True)
    new["platforms"] = new_platforms

    if "modality" not in new:
        has_real_hw = bool(new_platforms) or hardware_signal
        if software_signal and has_real_hw:
            new["modality"] = "both"
        elif software_signal:
            new["modality"] = "software"
        elif has_real_hw:
            new["modality"] = "hardware"
        else:
            new["modality"] = "software"
            report.defaulted_modality.append(fname)

    # applications — preserve existing, add derived + inferred
    apps = set(meta.get("applications") or []) | set(derived_apps) | _infer_applications_from_strings(
        list(meta.get("focus_areas") or []) +
        list(meta.get("keywords") or [])
    )
    if apps:
        new["applications"] = sorted(apps)

    # status mapping
    status = dict(meta.get("status") or {})
    op = (status.get("operating_status") or "active").strip().lower()
    if op == "active":
        if fname.startswith("c002-ionq"):
            status["operating_status"] = "public"
        else:
            status["operating_status"] = "private"
    elif op in ("private", "public", "acquired", "defunct", "non_profit", "stealth"):
        status["operating_status"] = op
    else:
        report.unmapped_status.append((fname, op))
        status["operating_status"] = "private"

    # nested acquired block — clean up booleans for is_acquired
    if "acquired" in status and status["acquired"]:
        acq = status["acquired"]
        if not isinstance(acq, dict):
            status["acquired"] = None
    new["status"] = status

    # Normalize funding + milestones
    if "funding" in new:
        new["funding"] = _normalize_funding(new["funding"])
    if "milestones" in new:
        new["milestones"] = _normalize_milestones(new["milestones"])

    # provenance
    new.setdefault("last_verified_at", None)
    new.setdefault("verification_source_count", None)

    new = _scrub(new, COMPANY_ALLOWED, fname, report)
    report.migrated.append((fname, "company"))
    return new


# Allowed top-level keys per the new schemas. Anything outside these is
# dropped by the migration (early entries inherited fields from cross-template
# copying — e.g. an institution carrying a company-shaped `funding` block).
INSTITUTION_ALLOWED = {
    "schema_version", "id", "entity_type", "name", "sort_name", "aliases",
    "abbreviations", "location", "institution_type",
    "is_dedicated_quantum_centre", "short_description", "platforms_represented",
    "applications_represented", "focus_areas", "group_count", "leadership",
    "national_programs", "networks", "mous", "directory", "news", "links",
    "media", "sources", "last_verified_at", "verification_source_count",
    "stub", "created_at", "updated_at",
}

PERSON_ALLOWED = {
    "schema_version", "id", "entity_type", "name", "sort_name", "location",
    "current_position", "group_type", "active", "labels", "platforms",
    "applications", "ion_species", "atomic_species", "education", "postdocs",
    "thesis", "links", "keywords", "affiliations", "key_papers", "metrics",
    "lineage_check", "last_verified_at", "verification_source_count", "stub",
    "created_at", "updated_at",
}

COMPANY_ALLOWED = {
    "schema_version", "id", "entity_type", "name", "sort_name", "aliases",
    "location", "founded_year", "status", "platforms", "modality",
    "applications", "short_summary", "approach", "focus_areas", "products",
    "people", "funding", "offices", "milestones", "roadmap", "partnerships",
    "customers", "patents", "links", "media", "sources",
    "last_verified_at", "verification_source_count", "stub",
    "created_at", "updated_at",
}


def _scrub(meta, allowed, fname, report):
    extras = [k for k in meta.keys() if k not in allowed]
    if extras:
        report.dropped_fields.extend((fname, k) for k in extras)
    return {k: v for k, v in meta.items() if k in allowed}


def migrate_institution(meta, fname, report, force=False):
    if not force and (
            meta.get("schema_version") == 1
            and meta.get("entity_type") == "institution"
            and meta.get("institution_type") not in INSTITUTION_TYPE_MAP
            and not any(k in meta for k in ("platforms", "approach", "products", "people", "status", "funding", "milestones", "short_summary"))):
        return None

    new = dict(meta)
    new["schema_version"] = 1
    new["entity_type"] = "institution"

    # institution_type: map old values to new enum, then default if missing
    if new.get("institution_type") in INSTITUTION_TYPE_MAP:
        new["institution_type"] = INSTITUTION_TYPE_MAP[new["institution_type"]]
    if not new.get("institution_type"):
        name_low = (new.get("name") or "").lower()
        if "university" in name_low or "college" in name_low:
            new["institution_type"] = "university"
        elif "national lab" in name_low or "laboratory" in name_low:
            new["institution_type"] = "national_lab"
        else:
            new["institution_type"] = "research_centre"

    # Normalize directory.alumni from None -> []
    if isinstance(new.get("directory"), dict):
        d = new["directory"]
        for k in ("current_members", "alumni", "company_spinouts"):
            if d.get(k) is None:
                d[k] = []

    # If short_summary is present and short_description is not, promote.
    if not new.get("short_description") and new.get("short_summary"):
        new["short_description"] = new["short_summary"]

    # provenance
    new.setdefault("last_verified_at", None)
    new.setdefault("verification_source_count", None)

    new = _scrub(new, INSTITUTION_ALLOWED, fname, report)
    report.migrated.append((fname, "institution"))
    return new


# ── Driver ────────────────────────────────────────────────────────────────

def _process_dir(directory, migrate_fn, report, dry_run, force):
    if not directory.exists():
        return
    for path in sorted(directory.glob("*.md")):
        fname = path.name
        try:
            post = frontmatter.load(path)
        except Exception as e:
            report.errors.append((fname, f"parse: {e}"))
            continue
        meta = dict(post.metadata)
        new_meta = migrate_fn(meta, fname, report, force=force)
        if new_meta is None:
            report.skipped.append(fname)
            continue
        if dry_run:
            continue
        post.metadata = new_meta
        text = frontmatter.dumps(post)
        path.write_text(text + "\n", encoding="utf-8")


def _write_report(report, dry_run):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# Migration Report — content → v2 schemas")
    lines.append("")
    lines.append(f"Mode: **{'dry-run' if dry_run else 'applied'}**.")
    lines.append("")
    lines.append(f"- Migrated: **{len(report.migrated)}**")
    lines.append(f"- Skipped (already at target version): **{len(report.skipped)}**")
    lines.append(f"- Errors: **{len(report.errors)}**")
    lines.append("")

    if report.unmapped_platforms:
        lines.append("## Unmapped platform strings")
        lines.append("")
        lines.append("These free-form values were left out of the migrated `platforms`")
        lines.append("array. Add an entry to `PLATFORM_MAP` in the script if any of")
        lines.append("them should map to a controlled enum value.")
        lines.append("")
        for fname, val in sorted(set(report.unmapped_platforms)):
            lines.append(f"- `{fname}`: {val!r}")
        lines.append("")

    if report.defaulted_applications:
        lines.append("## Defaulted applications = ['computing']")
        lines.append("")
        lines.append("Experimental entries with no inferable application; defaulted")
        lines.append("conservatively. Stage 3 should review each and replace with the")
        lines.append("actual research-application axis.")
        lines.append("")
        for fname in sorted(report.defaulted_applications):
            lines.append(f"- {fname}")
        lines.append("")

    if report.defaulted_modality:
        lines.append("## Defaulted company modality = software")
        lines.append("")
        for fname in sorted(report.defaulted_modality):
            lines.append(f"- {fname}")
        lines.append("")

    if report.unmapped_status:
        lines.append("## Unmapped company operating_status")
        lines.append("")
        for fname, val in sorted(set(report.unmapped_status)):
            lines.append(f"- `{fname}`: {val!r} (defaulted to `private`)")
        lines.append("")

    if report.dropped_fields:
        lines.append("## Dropped fields")
        lines.append("")
        lines.append("Top-level keys that aren't part of the new schemas were removed.")
        lines.append("Mostly cross-template inheritance (e.g. an institution carrying")
        lines.append("a company-shaped `funding` or `status` block).")
        lines.append("")
        from collections import Counter
        counts = Counter(k for _, k in report.dropped_fields)
        for k, n in counts.most_common():
            lines.append(f"- `{k}` ({n} entries)")
        lines.append("")

    if report.errors:
        lines.append("## Errors")
        lines.append("")
        for fname, msg in report.errors:
            lines.append(f"- `{fname}`: {msg}")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="Print summary; do not modify files.")
    ap.add_argument("--force", action="store_true",
                    help="Re-process entries even if they already have target schema_version.")
    args = ap.parse_args()

    report = Report()
    _process_dir(PEOPLE_DIR,       migrate_person,      report, args.dry_run, args.force)
    _process_dir(COMPANIES_DIR,    migrate_company,     report, args.dry_run, args.force)
    _process_dir(INSTITUTIONS_DIR, migrate_institution, report, args.dry_run, args.force)
    _write_report(report, args.dry_run)

    print(f"Migrated: {len(report.migrated)}")
    print(f"Skipped:  {len(report.skipped)}")
    print(f"Errors:   {len(report.errors)}")
    if report.unmapped_platforms:
        print(f"Unmapped platform strings: {len(set(report.unmapped_platforms))} unique")
    if report.defaulted_applications:
        print(f"Defaulted applications: {len(report.defaulted_applications)} entries")
    print(f"Report: {REPORT_PATH}")
    if report.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
