# Evidence Map — Template

A field-by-field mapping from each non-trivial value in a profile's YAML
frontmatter to the source it was drawn from, including a quote when possible.
The point is reproducibility: a future maintainer (or LLM agent) should be able
to re-verify any claim without redoing the original research.

## How to use

For every populated field that isn't self-evident (i.e. not just a name or an
internal id), add a bullet of the form:

```
*   **`field.path`**: "value as recorded"
    *   *Source*: <URL> (location within page, e.g. section/header)
    *   *Quote*: "verbatim sentence from the source" (when the source is text)
```

Group cross-references (e.g. confirmation from another profile in this repo)
as additional `*Source*` lines.

---

## Worked example — Quantum Art

*   **`short_summary`**: "Developer of scalable, multi-core quantum computers using trapped-ion qubits."
    *   *Source*: https://quantum-art.tech (Header: "Scalable Quantum Computing Solutions")
*   **`approach.elevator_pitch`**: "We employ multi-qubit gates, implementing up to 1,000 standard two-qubit gates in a single operation... Made possible by multi-tone, multi-mode coherent control."
    *   *Source*: https://quantum-art.tech (Section: "Inspiring Quantum Computing")
*   **`approach.differentiators`**: "Dynamically reconfigurable multi-core architecture"
    *   *Source*: https://quantum-art.tech (Section: "technology")
*   **`people.founders`**: "Tal David (CEO & Co-Founder), Amit Ben Kish (CTO & Co-Founder), Roee Ozeri (Co-Founder & Chief Scientist)"
    *   *Source*: https://tracxn.com/d/companies/quantum-art (and confirmed by `001-roee-ozeri.md` affiliation)
*   **`funding.rounds[0]`**: "$100 million Series A"
    *   *Source*: https://www.prnewswire.com/news-releases/quantum-art-raises-100-million-in-series-a-funding-302328222.html
    *   *Quote*: "Quantum Art ... today announced it has raised $100 million in Series A funding."
*   **`location`**: "Ness Ziona, Israel"
    *   *Source*: https://tracxn.com/d/companies/quantum-art
