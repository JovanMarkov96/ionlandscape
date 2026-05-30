---
last_verified_at: '2026-05-30'
media: {}
verification_source_count: 10
---

# Evidence Map: PsiQuantum (c030-psiquantum)

## Verification
- **Last Verified:** 2026-05-30
- **Completeness:** High

## Sources
1. [PsiQuantum Wikipedia](https://en.wikipedia.org/wiki/PsiQuantum) — Founding year, founders (O'Brien, Rudolph, Shadbolt, Thompson), technology overview, early funding history.
2. [PsiQuantum Technology Page](https://www.psiquantum.com/technology) — Omega chipset architecture, FBQC error correction, silicon photonics approach, operating temperature, manufacturing node.
3. [PsiQuantum Omega Announcement](https://www.psiquantum.com/news-import/omega) — Omega chipset announcement (Feb 26, 2025); 99.98% SPAM fidelity, 99.72% chip-to-chip interconnect fidelity; Nature paper s41586-025-08820-7.
4. [PsiQuantum $1B Series E](https://www.psiquantum.com/news-import/psiquantum-1b-fundraise) — Series E: $1B, September 10, 2025, $7B valuation; BlackRock/Temasek/Baillie Gifford leading; full investor list; NVIDIA partnership; Brisbane/Chicago deployment plans.
5. [Australian Government Investment – The Quantum Insider](https://thequantuminsider.com/2024/04/29/psiquantum-receives-940-million-aud-from-australian-government/) — A$940M (~US$617M) from Australian Commonwealth and Queensland governments; structure (equity + grants + loans); A$470M each; Brisbane computer by end 2027; announced April 30, 2024.
6. [DARPA US2QC Final Phase – BusinessWire](https://www.businesswire.com/news/home/20250205568029/en/DARPA-Selects-PsiQuantum-to-Advance-to-Final-Phase-of-Quantum-Computing-Program) — DARPA selects PsiQuantum for final (validation) phase of US2QC, February 5, 2025; multi-institutional evaluation (AFRL, Johns Hopkins APL, LANL, ORNL, NASA Ames).
7. [DARPA Phase 2 Advancement – BusinessWire](https://www.businesswire.com/news/home/20240109741595/en/DARPA-Advances-PsiQuantum-to-Second-Phase-of-Utility-Scale-Quantum-Computing-Program) — DARPA Phase 1 → Phase 2 advancement, January 9, 2024; program details (US2QC).
8. [Victor Peng CEO Appointment](https://www.psiquantum.com/news-import/psiquantum-appoints-victor-peng) — Victor Peng as Interim CEO (Feb 10, 2026); Jeremy O'Brien to Executive Chairman; Peng's background (Xilinx CEO, AMD President).
9. [Chicago Groundbreaking](https://www.psiquantum.com/news-import/psiquantum-breaks-ground-chicago) — Groundbreaking at IQMP South Works, Chicago, September 30, 2025; America's largest quantum computing project; DARPA QBI final-phase evaluation at Chicago site.
10. [CHIPS Act $100M LOI](https://www.psiquantum.com/news-import/us-department-of-commerce) — $100M Letter of Intent with U.S. Department of Commerce under CHIPS and Science Act, May 21, 2026; targets BTO switches, high-temperature SPDs, advanced packaging.
11. [GlobalFoundries Partnership](https://gf.com/dresden-press-release/psiquantum-and-globalfoundries-build-worlds-first-full-scale-quantum-computer/) — Partnership to manufacture at GlobalFoundries Fab 8, Malta NY (300mm, 45nm); announced 2021.
12. [BlackRock Series D – The Quantum Insider](https://thequantuminsider.com/2021/07/27/investors-see-the-light-as-blackrock-leads-450-million-series-d-investment-into-psiquantum/) — Series D: $450M, July 27, 2021, $3.15B valuation, BlackRock-led; other investors including Baillie Gifford, M12, Blackbird, Temasek, Founders Fund.
13. [Illinois Quantum Park Announcement](https://thequantuminsider.com/2024/07/25/psiquantum-announces-it-will-anchor-governor-j-b-pritzkers-illinois-quantum-and-microelectronics-park-in-chicago/) — Illinois Quantum and Microelectronics Park (IQMP) partnership; anchor tenant; July 25, 2024.

## Field Map
- `founded_year`, `founders`, `spun_out_of`: Source 1
- `approach.architecture_tags`, `approach.elevator_pitch`: Sources 2, 3
- `approach.differentiators`: Sources 2, 3, 6
- `products.Omega`: Source 3
- `products.Construct`: psiquantum.com homepage (fetched May 2026)
- `funding.series_a`, `funding.series_b`, `funding.series_c`: Crunchbase (search-verified May 2026)
- `funding.series_d`: Source 12
- `funding.grant (Australian)`: Source 5
- `funding.series_e_plus`: Source 4
- `milestones (GlobalFoundries)`: Source 11
- `milestones (DARPA Phase 2)`: Source 7
- `milestones (Australian investment)`: Source 5
- `milestones (Illinois)`: Source 13
- `milestones (DARPA final phase)`: Source 6
- `milestones (Omega)`: Source 3
- `milestones (Series E + NVIDIA)`: Source 4
- `milestones (Chicago groundbreaking)`: Source 9
- `milestones (Victor Peng CEO)`: Source 8
- `milestones (CHIPS Act LOI)`: Source 10
- `people.founders.person_id (190-jeremy-obrien)`: DB record; Source 1, 8
- `people.founders.person_id (191-terry-rudolph)`: DB record; Source 1
- `people.leadership (Victor Peng)`: Source 8
- `roadmap`: Sources 5, 9
- `partnerships`: Sources 4, 6, 11
- `offices (manufacturing, Malta NY)`: Source 11
- `offices (Brisbane)`: Source 5
- `offices (Chicago)`: Source 9
- `status.operating_status = private`: No IPO; confirmed private as of verification date

## Notes
- Total raised (~$2.32B) excludes the A$940M Australian government funding from the private venture sum; the Australian investment is recorded as a `grant` round with amount_usd = ~$617M (USD equivalent at time of announcement). Combined total including government funding exceeds $2.3B USD.
- Series B date (2017-09-05) from Crunchbase; Series C date approximate (Q4 2019 / early 2020 per various sources; 2020-01-01 used as conservative estimate).
- Victor Peng's role is "Interim CEO" as of Feb 10, 2026; a permanent CEO search was underway at verification date.
- `headcount: 280` per Wikipedia, reflecting 2024 data; likely higher by verification date but no updated figure sourced.
- The `government_contract` partnership type is not in the schema enum; replaced with `research` for the DARPA entry and left as `null` implicitly via the CHIPS Act entry using type `research` where appropriate — the CHIPS Act LOI is recorded as a milestone.
