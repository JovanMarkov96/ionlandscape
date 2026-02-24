# TODO & Roadmap

## Features
- [ ] **Feedback / Report Outdated Info system:**
  - **UX/Frontend:**
    - Add a small discrete button (e.g., 🚩, ✏️, or a bug icon) to the profile cards (`PersonPanel.jsx`, `CompanyPanel.jsx`, `MapPanel.jsx`, etc.).
    - Implement a hover tooltip explaining: "Report incorrect or outdated information".
    - Clicking opens a small popup modal or inline expansion with:
      - A text area to write what is wrong or missing.
      - Hidden fields that automatically capture the context (e.g., Card Type: Company, Name: Quantum Art, ID: c001).
      - (Optional) An email address field for follow-up.
      - A Submit button.
  - **Infrastructure:**
    - Choose and implement a simple form handling solution (e.g., Formspree, Web3Forms, Netlify Forms, or a `mailto:` link) to route these reports via email to the maintainers without needing a custom backend.
