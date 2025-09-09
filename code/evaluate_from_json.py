import json
import sys

def evaluate_from_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    
    total = 0
    for cat in data["categories"]:
        weighted = cat["score"] * cat["weight"] / 100
        total += weighted
    
    final_rating = round(total, 0)
    
    print(f"\nSkill: {data['skill']}")
    print(f"Weighted Total: {round(total,2)}")
    print(f"Final Rating (1–10): {int(final_rating)}")
    
    return final_rating

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluate_from_json.py path/to/file.json")
    else:
        evaluate_from_json(sys.argv[1])
