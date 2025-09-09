# 🧑‍💻 Technical Skills Rating System (1–10)

This repository provides a **universal, evidence-based system** to rate technical skills
(programming languages, libraries, tools, platforms) on a **1–10 scale**.

# Technical Skills Rating System (1–10)

A unified, evidence-based system to rate technical skills (programming languages, libraries, tools, platforms) on a 1–10 scale.

This repository includes:
- `RATING_SYSTEM.md` — full rubric and guidance.
- `templates/skill_template.csv` — CSV template for manual scoring.
- `templates/*.json` — example JSON inputs.
- `code/evaluate.py` — single evaluator script that auto-detects CSV / JSON / YAML.
- `notebooks/SkillRatingDemo.ipynb` — demo notebook (optional).
- `examples/` — sample human-readable outputs.

## Quick start

1. Clone & prepare
git clone https://github.com/mepsrajput/Technical-Skills-Rating-System.git
cd Technical-Skills-Rating-System


(Optional) create a virtual environment and install recommended deps:

python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install pandas pyyaml

2. Choose or create a template

Use an existing file in templates/ (e.g. sql_template.json, skill_template.csv), or

Create a new JSON / CSV / YAML file for the skill you want to evaluate.

Example JSON structure (templates/my_skill.json):

{
  "skill": "SkillName",
  "categories": [
    {"name": "Category A", "weight": 30, "score": 7},
    {"name": "Category B", "weight": 30, "score": 8},
    {"name": "Category C", "weight": 40, "score": 6}
  ]
}


Example CSV header (templates/skill_template.csv):

Skill,Category,Weight (%),Score (0-10)
MySkill,Core Knowledge,40,7
MySkill,Tooling,30,8
MySkill,Practice,30,6


If you create a new template, put it in templates/ so it’s easy to find and version.

3. Run the evaluator

Supported input types: .json, .csv, .yml / .yaml.

# basic run
python code/evaluate.py templates/my_skill.json

# save the detailed result
python code/evaluate.py templates/my_skill.json --output results/my_skill_result.json

# normalize weights to sum to 100 if needed
python code/evaluate.py templates/my_skill.csv --normalize --output results/my_skill_result.csv

4. Read the output

Console shows:

Weighted total (0–10)

Final rating (1–10, rounded)

Category breakdown (weight, score, weighted score)

If --output used, a detailed JSON/CSV is saved to results/.

5. Attach evidence (recommended)

Place proof files for high-confidence scores (especially scores ≥ 7) in a results subfolder:

results/<skillname>/
├─ queries/         # .sql or .py or code samples
├─ explain/         # explain/analyze outputs or logs
├─ benchmarks/      # timing CSVs or markdown
└─ evidence.md      # short description + links

6. If a template does not exist

Copy an existing template as a starting point:

cp templates/skill_template.csv templates/<your_skill>.csv


Edit categories/weights/scores to match the skill.

Run the evaluator as above.

Rating Legend (quick)

1–3 — Beginner

4–6 — Practitioner (working/independent)

7–8 — Expert (scales & optimizes)

9–10 — Authority (public contributions, leadership)
