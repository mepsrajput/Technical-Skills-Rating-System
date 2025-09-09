# file: evaluate_skill.py
import pandas as pd

def evaluate_skill(csv_path):
    df = pd.read_csv(csv_path)
    
    # Calculate weighted score
    df["Weighted Score"] = df["Score (0-10)"] * df["Weight (%)"] / 100
    
    total = df["Weighted Score"].sum()
    final_rating = round(total, 0)
    
    print("Skill:", df["Skill"].iloc[0])
    print("Total Weighted Score:", round(total, 2))
    print("Final Rating (1–10):", int(final_rating))
    return df, final_rating

if __name__ == "__main__":
    # Example usage
    df, rating = evaluate_skill("templates/skills_rating_template.csv")
    print(df)
