from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "matches.csv"


def load(new_matches):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_data = pd.DataFrame(new_matches)

    if OUTPUT_FILE.exists():
        existing_data = pd.read_csv(OUTPUT_FILE)

        combined = pd.concat(
            [existing_data, new_data],
            ignore_index=True
        )

        combined = (
            combined
            .sort_values("last_update")
            .drop_duplicates(
                subset="match_id",
                keep="last"
            )
        )

    else:
        combined = new_data

    combined.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Saved {len(combined)} matches to {OUTPUT_FILE}")

    return combined