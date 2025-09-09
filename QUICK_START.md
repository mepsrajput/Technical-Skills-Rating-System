# 🚀 Skill Evaluation — Quick Start

Evaluate **any skill** (SQL, Python, Docker, etc.) using this framework. You can use existing templates in `templates/` or create your own.

---

## 1. Clone & setup

```bash
git clone https://github.com/mepsrajput/Technical-Skills-Rating-System.git
cd Technical-Skills-Rating-System
```

(Optional) create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install pandas pyyaml
```

---

## 2. Choose or create a template

- Use an existing file in `templates/` (e.g., `sql_template.json`, `skill_template.csv`), **or**  
- Create a new JSON / CSV / YAML file describing the skill you want to evaluate.

**Example JSON (`templates/my_skill.json`):**

```json
{
  "skill": "SkillName",
  "categories": [
    {"name": "Category A", "weight": 30, "score": 7},
    {"name": "Category B", "weight": 30, "score": 8},
    {"name": "Category C", "weight": 40, "score": 6}
  ]
}
```

**Example CSV (`templates/my_skill.csv`):**

```csv
Skill,Category,Weight (%),Score (0-10)
MySkill,Core Knowledge,40,7
MySkill,Tooling,30,8
MySkill,Practice,30,6
```

> If you create a new template, put it in `templates/` so it’s easy to find and version.

---

## 3. Run the evaluator

The script supports `.json`, `.csv`, `.yml` / `.yaml`.

```bash
# Basic run
python code/evaluate.py templates/my_skill.json

# Save result to file
python code/evaluate.py templates/my_skill.json --output results/my_skill_result.json

# Normalize weights if they don’t sum to 100
python code/evaluate.py templates/my_skill.csv --normalize --output results/my_skill_result.csv
```

---

## 4. Review your results

- Console shows:
  - Weighted total (0–10)  
  - Final rating (1–10, rounded)  
  - Category breakdown (weight, score, weighted score)  
- If `--output` used, a detailed JSON/CSV is saved in `results/`.

---

## 5. Add evidence (recommended)

For scores **≥ 7 (Expert)**, attach proof files in a results folder:

```
results/<skillname>/
├─ queries/         # .sql, .py, or other code samples
├─ explain/         # EXPLAIN / ANALYZE outputs or logs
├─ benchmarks/      # timing CSVs or markdown
└─ evidence.md      # short description + links
```

---

## 6. If no template exists

1. Copy the generic template:
   ```bash
   cp templates/skill_template.csv templates/<your_skill>.csv
   ```
2. Edit categories, weights, and scores.  
3. Run the evaluator as above.

---

## 🏅 Rating legend

- **1–3 → Beginner**  
- **4–6 → Practitioner (independent work)**  
- **7–8 → Expert (scales & optimizes)**  
- **9–10 → Authority (leads, contributes publicly)**
