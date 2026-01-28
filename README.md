# Ion Landscape

Interactive map & academic family tree for trapped-ion and neutral-atom quantum computing.

## Local dev

1. Install Python deps:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt
```

2. Build data artifacts:
```bash
python scripts/build_index.py
```

3. Install website deps and run:
```bash
cd website
npm ci
npm start
```

Visit [http://localhost:3000/](http://localhost:3000/)

## Deploy

Push to `main`. GitHub Actions will build and deploy the site to the `gh-pages` branch. The site will be available at:

`https://JovanMarkov96.github.io/ionlandscape/`

## Project Structure

```
ionlandscape/
├─ content/
│  └─ people/           # Markdown files for each person
├─ scripts/
│  ├─ build_index.py    # Generates JSON/GeoJSON from Markdown
│  └─ requirements.txt  # Python dependencies
├─ website/
│  ├─ src/
│  │  ├─ pages/         # React pages
│  │  └─ components/    # React components (MapPanel, PersonPanel)
│  └─ static/data/      # Generated data files (by CI)
├─ .github/workflows/   # GitHub Actions deployment
└─ README.md
```

## Adding a new person

### Quick Method
Use the interactive profile creator:
```bash
python scripts/create_profile_template.py
```

This will guide you through creating a profile with verified data only.

### Manual Method
1. Create a new Markdown file in `content/people/` following the existing format
2. Include YAML frontmatter with required fields (id, name, location, etc.)
3. Only add information you can verify from authoritative sources
4. Push to `main` - the build will automatically regenerate the data files

See [INGESTION_GUIDE.md](INGESTION_GUIDE.md) for detailed instructions on data curation and verification.

## Data Curation & Verification

This repository includes automated tools for systematic profile ingestion and verification:

- **`ingest_profiles.py`** - Automated ingestion from authoritative ion-trapping website
- **`verify_profile_data.py`** - Validate existing profiles against schema
- **`create_profile_template.py`** - Interactive tool for creating new profiles
- **`batch_enrich_profiles.py`** - Bulk update profiles from JSON data

### Quick Verification
```bash
# Verify a single profile
python scripts/verify_profile_data.py 001-roee-ozeri

# Verify all profiles
python scripts/verify_profile_data.py --all
```

**Important:** All facts must be backed by authoritative sources. Never guess or hallucinate data.

See [INGESTION_GUIDE.md](INGESTION_GUIDE.md) for complete documentation.
