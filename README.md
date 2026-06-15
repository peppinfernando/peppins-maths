# The 3 Amigos Tuition Centre, Cork · Kildare · Limerick — Junior Cycle Mathematics Study App

## 🍀 Live Study App

**➡️ Open the app:** [https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/](https://your-username.github.io/your-repo-name/)

A complete, mobile-friendly Junior Cycle Maths study app for First Year students at The 3 Amigos Tuition Centre, Cork · Kildare · Limerick. Covers all 45 days of the tuition programme.

## Features

- 📖 **Concept pages** with tutor explanations, analogies, worked examples and common mistakes
- ✏️ **Practice questions** with hints and worked answers (6–10 per day)
- ⚡ **Quiz mode** — random questions across all topics with instant feedback
- 📈 **Progress tracker** — mark days complete, stored in your browser
- 📐 **Fully responsive** — works on mobile, tablet and desktop
- 🚫 **No server needed** — pure HTML/CSS/JS, works offline after first load

## Topics Covered (45 Days)

| Block | Days | Topics |
|-------|------|--------|
| Number | 1–7 | Place Value, BEMDAS, Factors, Integers, Fractions, Decimals, %, Sets, Ratio, Tax |
| Algebra | 8–17 | Expressions, Expanding, Factorising, Equations, Simultaneous, Quadratics, Functions |
| Geometry | 18–28 | Angles, Theorems, Constructions, Area, Volume, Coordinate Geometry, Trigonometry |
| Statistics | 29–38 | Data, Mean/Median, Charts, Scatter, Probability, Counting, Normal Distribution, CBA |
| Revision | 39–45 | Rapid-fire reviews + 3 full mock exam papers |

## Running Locally

```bash
python3 generate.py
cd docs
python3 -m http.server 8080
# Open http://localhost:8080
```

## Publishing to GitHub Pages

1. Push this repository to GitHub
2. Go to **Settings → Pages**
3. Under **Source**, select `Deploy from a branch`
4. Choose **Branch: main** and **Folder: /docs**
5. Click **Save**
6. Your app will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/` within a few minutes

## Regenerating the App

If you modify `generate.py`, regenerate the site:

```bash
python3 generate.py
```

All output goes into the `docs/` folder, ready to commit and push.

## Aligned To

- NCCA Junior Cycle Mathematics Specification 2018
- SEC Junior Cycle Exam Papers 2021–2025
- The 3 Amigos Tuition Centre, Cork · Kildare · Limerick teaching sequence

---
*Built for The 3 Amigos Tuition Centre Junior Cycle Maths Tuition Programme*
