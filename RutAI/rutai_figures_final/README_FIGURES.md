# RutAI manuscript — figures

Eight figures selected for the JCR Q1 manuscript, each in PNG (300 dpi) and PDF (vector) format.

## Editorial criteria for selection

The original thesis document contains 67 figures (consistent with a TFG-style document). For a journal manuscript targeting *Pervasive and Mobile Computing* or similar JCR Q1 venue, the editorial standard is **6–10 figures**, each carrying distinct scientific value and not replaceable by text or tables. The selection below applies that filter.

**Figures included (8 total):**

| # | File | Section | Purpose |
|---|------|---------|---------|
| 1 | `Figure_01_architecture` | §3 — System overview | System architecture; client–server layered design |
| 2 | `Figure_02_geofence_method` | §4.1 — Methods | Geofence experimental method; TP/FP/TN/FN definitions; pseudoreplication collapse |
| 3 | `Figure_03_pois_map` | §4.1 — Methods | Geographic distribution of the 20 POIs in Quevedo |
| 4 | `Figure_04_geofence_results` | §5.1 — Results | Precision and recall by radius (Wilson 95% CIs); confusion matrix counts |
| 5 | `Figure_05_fp_analysis` | §5.1 — Results | False-positive analysis: overshoot vs radius; GPS error explanation |
| 6 | `Figure_06_bandit_regret` | §5.2 — Results | Cumulative regret of bandit policies over T = 500 |
| 7 | `Figure_07_ui_mockups` | §3 — System overview | Schematic mockups of the three core UI screens |
| 8 | `Figure_08_tam_summary` | §5.3 — Results | TAM construct means with CIs; correlation heatmap with discriminant validity flags |

**Figures from the thesis intentionally excluded:**

- 7 UML class diagrams (Figs. 11–17 in thesis): too granular for Q1; replaced by the higher-level architecture in Figure 1.
- 24 individual UI screenshots showing every wizard step: replaced by 3 representative mockups in Figure 7.
- 4 use-case UML diagrams (Figs. 3–6): typical of a TFG, not appropriate for a journal manuscript.
- 5 separate TAM figures (Figs. 37–41): consolidated into Figure 8 since the TAM is now a complementary section, not a primary contribution.
- Login/registration/profile screenshots: not relevant to the scientific content.

## English captions (LaTeX-ready)

Each caption follows Elsevier's CAS-DC convention and contains the figure number, a bold short title, and a one-paragraph description of what is shown and how to read it.

### Figure 1
> **Figure 1.** System architecture of RutAI — three-layer client-server design. The Android mobile client (left) implements presentation (Jetpack Compose UI, ViewModels), business logic (geofence service, route generator, foreground GPS service, WebSocket client), and data layers (Room, Retrofit, OkHttp WebSocket, osmdroid). The cloud backend (right) implements router, service, and repository layers using FastAPI, with PostgreSQL and Redis (Upstash) for storage. Communication uses HTTPS / REST for synchronous operations and WSS / WebSocket for real-time collaborative tracking. External services include OpenRouteService, OpenStreetMap, and Firebase Cloud Messaging.

### Figure 2
> **Figure 2.** Geofence experiment method. (a) A geofence is a circular region of radius R around a POI centroid; a trigger event from the application is labeled TP if the user is inside R, FP if outside, TN if no trigger fires while outside, FN if no trigger fires while inside. (b) Multiple raw triggers within the same physical crossing of a (POI × radius × session) tuple are collapsed to one independent observation labeled by the dominant outcome, reducing the raw count of 139 trigger events to 78 statistically independent observations. All Wilson 95% CIs and McNemar tests are computed on the collapsed dataset.

### Figure 3
> **Figure 3.** Twenty points of interest used in the geofence experiment, Quevedo, Ecuador. POIs span parks, monuments, university campuses (UTEQ, UTB), commercial centers, and the Quevedo Riverside Trail, distributed across the urban perimeter. Sample geofence radii (50, 100, 200 m) are illustrated around the UTEQ campus (POI 19) for scale. Coordinates are in WGS84.

### Figure 4
> **Figure 4.** Geofence detection performance by radius — RutAI evaluation in Quevedo, Ecuador. (a) Precision and recall with Wilson 95% confidence intervals for each radius. Recall remains at 1.000 across all radii; precision improves monotonically from 0.818 [0.615, 0.927] at R = 50 m to 1.000 [0.839, 1.000] at R = 200 m. (b) Confusion matrix counts on n = 78 collapsed observations. F1 score increases from 0.900 to 1.000 with radius. Sample sizes per radius are reported below the x-axis.

### Figure 5
> **Figure 5.** False positives are explained by GPS positioning error, not application logic. (a) All seven false positives detected across the experiment occurred within 1.2–6.0 m beyond the configured radius (mean overshoot 3.4 m at R = 50 m, 3.8 m at R = 100 m, no FPs at R = 200 m). The shaded band marks the reported GPS accuracy at trigger time (3.0–3.2 m). (b) Geometric explanation: a true position just outside the boundary is measured inside the geofence with non-trivial probability when the overshoot is comparable to the GPS uncertainty radius, producing the observed FP pattern.

### Figure 6
> **Figure 6.** Bandit policy comparison for route-type recommendation in RutAI (T = 500, 100 seeds). Mean cumulative regret with 95% bootstrap confidence intervals. Thompson Sampling (deployed as the production policy) achieves the lowest final regret (13.41, [11.61, 15.38]); ε-greedy(0.1) is the closest competitor (16.58, [13.27, 20.50]) with overlapping confidence intervals. The entropy-regularized UCB1 variant initially considered (32.82, [31.54, 34.07]) underperforms simpler alternatives in this stationary setting and is reported as a transparent negative result. Reward probabilities: fastest = 0.40, shortest = 0.50, recommended (optimal) = 0.65.

### Figure 7
> **Figure 7.** RutAI user interface — schematic mockups of the three core modules. (a) Route recommendation screen: three alternative routes (Recommended in green, Fastest in blue, Shortest in orange) overlaid on the map, with safety badges marking intersections with user-reported danger zones; the bottom panel shows route-type cards with the Thompson Sampling recommendation highlighted. (b) Geofence reminder setup: step 3 of a 4-step wizard, with trigger type selector, radius slider, and entry/exit/both options. (c) Collaborative tracking: real-time map showing live positions of the four members of a trust group, fed by a WebSocket fan-out from the backend.

### Figure 8
> **Figure 8.** TAM acceptance pilot — complementary evidence with documented limitations. (a) Construct means (n = 25) with 95% CIs; all five constructs exceed the 3.5 acceptance threshold. Cronbach's α is reported below each bar. (b) Pearson correlations between constructs. Triangle markers flag correlations r > 0.95, indicating that ATU, ITU, and PS are not statistically discriminated in this small pilot. The data are reported as exploratory complementary evidence, not as confirmatory validation; sample size and acquiescence bias limitations are discussed in §6.3.

## Notes on the application name

The thesis source document refers to the application as "RememberGo." For this manuscript, the application is consistently named **RutAI** — all figures use this name and all in-figure text is in English.

## File naming

PNG files are at 300 dpi for screen and online viewing. PDF files are vector versions for high-quality print and publication.

## Source code

Each figure is generated by the corresponding Python script in `figures_source/`:
- `fig01_architecture.py`
- `fig02_geofence_method.py`
- `fig03_pois_map.py`
- `fig04_geofence_results.py`
- `fig05_fp_analysis.py`
- `fig06_bandit_regret.py`
- `fig07_ui_mockups.py`
- `fig08_tam_summary.py`

All scripts use matplotlib only, with no external dependencies beyond the standard scientific Python stack (matplotlib, numpy, pandas, scipy).
