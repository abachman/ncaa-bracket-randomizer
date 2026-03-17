#!/usr/bin/env python3
"""Generate women's bracket JSON from Torvik CSV, and ESPN IDs.

To obtain the women's Torvik CSV, download it via browser from:
  https://barttorvik.com/ncaaw/
and export/save the team results CSV, then pass it as the argument:
  python3 generate_bracket_women.py [path_to_csv]

The CSV is expected to have the same column layout as the men's:
  col 2 (index 1) = team name, col 9 (index 8) = barthag
"""

import csv
import json
import sys

csv_path = sys.argv[1] if len(sys.argv) > 1 else "2026_team_results_ncaaw.csv"

# Load barthag data
barthag = {}
with open(csv_path) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        team = row[1]
        b = float(row[7])
        barthag[team] = b

# Load ESPN IDs (same file as men's — school IDs are gender-neutral on ESPN)
with open("espn_ids.json") as f:
    espn_ids = json.load(f)

# Name mappings: bracket name -> Torvik/ESPN name
# Women's Torvik uses the same naming conventions as men's for most teams.
# Add entries here as needed when mismatches are found.
name_map = {
    "UConn": "Connecticut",
    "Ohio State": "Ohio St.",
    "Iowa State": "Iowa St.",
    "Ole Miss": "Mississippi",
    "NC State": "N.C. State",
    "Murray State": "Murray St.",
    "South Dakota State": "South Dakota St.",
    "Colorado State": "Colorado St.",
    "Cal Baptist": "Cal Baptist",
    "Missouri State": "Missouri St.",
    "Michigan State": "Michigan St.",
    "Miami (OH)": "Miami OH",
    "Oklahoma State": "Oklahoma St.",
}


def get_team(name, seed):
    lookup = name_map.get(name, name)
    b = barthag[lookup]
    eid = espn_ids[lookup]
    return {"name": name, "seed": seed, "barthag": round(b, 6), "espn_id": eid}


# Layout: Fort Worth 1 and Fort Worth 3 on left, Sacramento 2 and 4 on right.
# Mirrors how men's bracket is structured (1-seed regions on left).
bracket = {
    "title": "2026 NCAA Women's Tournament",
    "layout": {
        "topLeft": "fw1",
        "bottomLeft": "fw3",
        "topRight": "sac2",
        "bottomRight": "sac4",
    },
}

# --- Fort Worth 1 (top left) — UConn region ---
bracket["fw1"] = {
    "1": get_team("UConn", 1),
    "16": get_team("UTSA", 16),
    "8": get_team("Iowa State", 8),
    "9": get_team("Syracuse", 9),
    "5": get_team("Maryland", 5),
    "12": get_team("Murray State", 12),
    "4": get_team("North Carolina", 4),
    "13": get_team("Western Illinois", 13),
    "6": get_team("Notre Dame", 6),
    "11": get_team("Fairfield", 11),
    "3": get_team("Ohio State", 3),
    "14": get_team("Howard", 14),
    "7": get_team("Illinois", 7),
    "10": get_team("Colorado", 10),
    "2": get_team("Vanderbilt", 2),
    "15": get_team("High Point", 15),
}

# --- Sacramento 2 (top right) — UCLA region ---
# 11 seed play-in: Nebraska vs Richmond — Nebraska used as default
bracket["sac2"] = {
    "1": get_team("UCLA", 1),
    "16": get_team("Cal Baptist", 16),
    "8": get_team("Oklahoma State", 8),
    "9": get_team("Princeton", 9),
    "5": get_team("Ole Miss", 5),
    "12": get_team("Gonzaga", 12),
    "4": get_team("Minnesota", 4),
    "13": get_team("Green Bay", 13),
    "6": get_team("Baylor", 6),
    "11": get_team("Nebraska", 11),  # Play-in: Nebraska vs Richmond
    "3": get_team("Duke", 3),
    "14": get_team("Charleston", 14),
    "7": get_team("Texas Tech", 7),
    "10": get_team("Villanova", 10),
    "2": get_team("LSU", 2),
    "15": get_team("Jacksonville", 15),
}

# --- Fort Worth 3 (bottom left) — Texas region ---
# 16 seed play-in: Missouri State vs Stephen F. Austin — Missouri State used as default
bracket["fw3"] = {
    "1": get_team("Texas", 1),
    "16": get_team("Missouri State", 16),  # Play-in: Missouri State vs Stephen F. Austin
    "8": get_team("Oregon", 8),
    "9": get_team("Virginia Tech", 9),
    "5": get_team("Kentucky", 5),
    "12": get_team("James Madison", 12),
    "4": get_team("West Virginia", 4),
    "13": get_team("Miami (OH)", 13),
    "6": get_team("Alabama", 6),
    "11": get_team("Rhode Island", 11),
    "3": get_team("Louisville", 3),
    "14": get_team("Vermont", 14),
    "7": get_team("NC State", 7),
    "10": get_team("Tennessee", 10),
    "2": get_team("Michigan", 2),
    "15": get_team("Holy Cross", 15),
}

# --- Sacramento 4 (bottom right) — South Carolina region ---
# 10 seed play-in: Virginia vs Arizona State — Virginia used as default
# 16 seed play-in: Southern vs Samford — Southern used as default
bracket["sac4"] = {
    "1": get_team("South Carolina", 1),
    "16": get_team("Southern", 16),  # Play-in: Southern vs Samford
    "8": get_team("Clemson", 8),
    "9": get_team("USC", 9),
    "5": get_team("Michigan State", 5),
    "12": get_team("Colorado State", 12),
    "4": get_team("Oklahoma", 4),
    "13": get_team("Idaho", 13),
    "6": get_team("Washington", 6),
    "11": get_team("South Dakota State", 11),
    "3": get_team("TCU", 3),
    "14": get_team("UC San Diego", 14),
    "7": get_team("Georgia", 7),
    "10": get_team("Virginia", 10),  # Play-in: Virginia vs Arizona State
    "2": get_team("Iowa", 2),
    "15": get_team("Fairleigh Dickinson", 15),
}

with open("2026.bracket.women.json", "w") as f:
    json.dump(bracket, f, indent=2)
    f.write("\n")

print("Wrote 2026.bracket.women.json")
