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

1. Create a new Markdown file in `content/people/` following the existing format
2. Include YAML frontmatter with required fields (id, name, location, etc.)
3. Push to `main` - the build will automatically regenerate the data files
