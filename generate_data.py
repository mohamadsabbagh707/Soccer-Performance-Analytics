import csv
import random

CSV_FILE = "soccer_match_data.csv"

def generate_match(match_id):

    difficulty = random.choice(["Easy", "Normal", "Hard"])
    shots = 10

    if difficulty == "Easy":
        goals = random.randint(4, 8)
        power = random.randint(0, 3)

    elif difficulty == "Normal":
        goals = random.randint(2, 6)
        power = random.randint(1, 5)

    else:  # Hard
        goals = random.randint(0, 4)
        power = random.randint(2, 6)

    saves = shots - goals

    return [match_id, difficulty, shots, goals, saves, power]


def generate_dataset(n=150):

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "match_id",
            "difficulty_level",
            "shots",
            "goals",
            "saves",
            "power_shot_count"
        ])

        for i in range(1, n + 1):
            writer.writerow(generate_match(i))


if __name__ == "__main__":
    generate_dataset(150)
    print("150 rows generated successfully!")
