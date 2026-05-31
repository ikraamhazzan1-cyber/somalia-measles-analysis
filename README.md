# 💉 Somalia Measles Vaccination Coverage Analysis — 2019–2023

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Complete](https://img.shields.io/badge/Status-Complete-brightgreen)]()
[![Field: Immunization](https://img.shields.io/badge/Field-Immunization-teal)]()
[![WHO Target: 95%](https://img.shields.io/badge/WHO%20Target-95%25-red)]()

> **Regional analysis of measles vaccination coverage gaps, zero-dose children, and structural determinants of immunization failure across seven Somali regions — 2019 to 2023.**

---

## 📋 Overview

This project investigates why measles vaccination coverage in Somalia remains critically below the WHO 95% herd immunity threshold — and which structural factors drive coverage failure. The analysis uses district-level immunization data to identify priority regions, quantify unvaccinated child burden, and model determinants of low coverage.

---

## 🔑 Key Findings

| Metric | Value |
|--------|-------|
| Unvaccinated Children (2023) | **125,025** |
| Regions reaching WHO 95% target | **0 out of 7** |
| Lowest MCV1 coverage | **Southwest State — 46%** |
| Highest MCV1 coverage | **Somaliland — 83%** |
| IDP–coverage correlation | **r = −0.939** (p<0.001) |
| Conflict–coverage correlation | **r = −0.928** (p<0.001) |

---

## 📊 Figures

| Figure | Description |
|--------|-------------|
| `fig1_regional_coverage.png` | MCV1/MCV2 vs WHO target by region |
| `fig2_coverage_trends.png` | 5-year trend lines by region |
| `fig3_unvaccinated_heatmap.png` | Zero-dose children heatmap |
| `fig4_determinants.png` | Structural drivers correlation plots |
| `fig5_geographic_map.png` | GIS-style bubble map of Somalia |

---

## 🗂️ Project Structure

```
measles_project/
├── data/
│   └── somalia_measles_data.csv
├── scripts/
│   └── measles_analysis.py
├── outputs/
│   ├── fig1_regional_coverage.png
│   ├── fig2_coverage_trends.png
│   ├── fig3_unvaccinated_heatmap.png
│   ├── fig4_determinants.png
│   └── fig5_geographic_map.png
└── report/
    └── Somalia_Measles_Report_2019_2023.html
```

---

## 🛠️ Methods

- **Design:** Retrospective cross-sectional analysis
- **Outcomes:** MCV1/MCV2 coverage (%), zero-dose children
- **Determinants:** Distance to clinic, IDP %, conflict score
- **Statistics:** Pearson correlation, descriptive analysis
- **Visualization:** Trend lines, heatmaps, GIS bubble map
- **Tools:** Python 3.12 — pandas, matplotlib, seaborn, scipy, numpy

---

## ▶️ How to Run

```bash
git clone https://github.com/ikraamhazzan1-cyber/somalia-measles-analysis.git
cd somalia-measles-analysis
pip install pandas matplotlib seaborn scipy numpy
python3 scripts/measles_analysis.py
```

---

## 👤 Author

**Ikraam Hassan Abdullahi**
MSc Epidemiology | BSc Public Health
Somalia 🇸🇴

🔗 LinkedIn: https://www.linkedin.com/in/ikraam-yar
💻 GitHub: https://github.com/ikraamhazzan1-cyber

---

MIT License — free to use with attribution.

*Part of an independent epidemiological portfolio targeting global health and humanitarian response positions.*
