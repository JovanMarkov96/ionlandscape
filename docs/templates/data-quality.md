# Data Quality Notes — Template

A short companion document used during profile ingestion to record fields that
were intentionally left empty, and any non-authoritative sources that were
consulted. One per profile (person / company / institution) when the data is
non-trivial enough to warrant documentation.

## How to use

For each empty or partial field, add a bullet stating *which* field and *why*
nothing better was recorded (e.g. no source found, source was off-topic,
fact was not verifiable). For each non-authoritative source consulted, note
how it was used so a reviewer can judge the trust level.

---

## Worked example — Quantum Art

*   **`milestones`**: `[]` (Empty) — No relevant quotes found for specific dated milestones beyond funding.
*   **`media`**: `logo_path` and `hero_image_path` are empty strings. No external binaries were added to the repository.
*   **`linkedin`**: Empty. No relevant quotes found for specific LinkedIn URL in the checked sources (focused on Tech/Funding).
*   **`status.acquired`**: False. Company is active and recently raised Series A.

### Non-professional Sources
*   **Wikipedia**: Not used.
*   **Tracxn**: Used for location and founder confirmation (secondary source).
*   **PR Newswire**: Used for Series A funding details.
