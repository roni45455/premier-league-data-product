import json
from pathlib import Path

import requests


BASE_URL = "https://api.openligadb.de"
LEAGUE = "pl"
SEASON = 2026

RAW_DIR = Path("data/raw")
STATE_FILE = RAW_DIR / "matchweek_state.json"

def extract():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    current_group = requests.get(
        f"{BASE_URL}/getcurrentgroup/{LEAGUE}"
    ).json()

    current_matchweek = current_group["groupOrderID"]

    print(f"\nCurrent matchweek: {current_matchweek}")

    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {}

    all_matches = []

    for matchweek in range(1, current_matchweek + 1):

        matchweek_key = str(matchweek)

        is_complete = state.get(
            matchweek_key,
            {}
        ).get("complete", False)

        if is_complete and matchweek != current_matchweek:
            print(f"MW {matchweek}: complete -> skipped")
            continue

        print(f"MW {matchweek}: fetching...")

        url = (
            f"{BASE_URL}/getmatchdata/"
            f"{LEAGUE}/{SEASON}/{matchweek}"
        )

        matches = requests.get(url).json()

        print(f"MW {matchweek}: {len(matches)} matches received")

        output_file = RAW_DIR / f"matchweek_{matchweek}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)

        all_matches.extend(matches)

        complete = all(
            match["matchIsFinished"]
            for match in matches
        )

        print(f"MW {matchweek}: complete = {complete}")

        state[matchweek_key] = {
            "complete": complete
        }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"\nTotal matches returned: {len(all_matches)}")

    return all_matches