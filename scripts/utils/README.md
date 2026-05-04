Serp + trafilatura helper

Usage

1. Install requirements (from `scripts/requirements.txt`).
2. Set `SERPAPI_API_KEY` environment variable.
3. Run:

```
python scripts/utils/serp_extract.py "Full Name PhD advisor" --num 5
```

This returns a compact JSON with candidate evidence sentences (token-efficient). Use the output to populate evidence maps and `education[].advisor` fields.

Notes

- Prefer site-limited queries (site:orcid.org, site:.edu, site:.ac.uk) to improve precision.
- If SerpAPI is not available, replace `search_serpapi` with another SERP provider wrapper (Bing, Google CSE).

AcademicTree helper

- Use `scripts/utils/academictree_lookup.py` to query AcademicTree entries via SerpAPI and extract advisor relationships.
- Example:

```
export SERPAPI_API_KEY=...
python scripts/utils/academictree_lookup.py "Rainer Blatt" --num 3
```

The script prints compact JSON with `candidates[*].parsed.advisors` when found.

DuckDuckGo helper (no API key)

- Use `scripts/utils/ddg_extract.py` for free searches via DuckDuckGo and token-efficient extraction. This avoids paid APIs.
- Example:

```
python scripts/utils/ddg_extract.py "Christopher Monroe PhD advisor" --num 5
```

The script prints compact JSON with `results[*].candidates` when found.
