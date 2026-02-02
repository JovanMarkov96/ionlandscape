# Cleanup Verification Checklist

After running the deprecation commands, perform the following checks:

## 1. Startup Check
- [ ] Run `python scripts/build_index.py`. **Expectation**: Success (0 exit code). The build should not depend on any deprecated scripts.
- [ ] Run `cd website && npm run start`. **Expectation**: Docusaurus starts on port 3000.

## 2. Smoke Test (Manual)
- [ ] **Home Page**: Map loads. Markers appear.
- [ ] **Interaction**: Click a marker. Profile panel opens.
- [ ] **Directory**: Go to `/ionlandscape/groups`. Filters work.
- [ ] **Mobile**: Resize browser to mobile width. Check sidebar overlay.

## 3. Pipeline Check
- [ ] Run `python scripts/verify_profile_data.py --all`. **Expectation**: Success.
- [ ] Run `python scripts/ingest_profiles.py --dry-run`. **Expectation**: Runs without import errors.

## 4. CI Check
- [ ] (Optional) Push to a branch and verify GitHub Actions pass. Since `build_index.py` and `npm run build` are the only CI steps, they must pass.
