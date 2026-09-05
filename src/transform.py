def transform(matches):

    transformed_matches = []

    for match in matches:

        # Keep only finished matches
        if not match["matchIsFinished"]:
            continue

        # Find the final score
        final_result = next(
            (
                result
                for result in match["matchResults"]
                if result["resultTypeKind"] == "After90Minutes"
            ),
            None
        )

        # Skip finished matches without a valid final result
        if final_result is None:
            continue

        transformed_match = {
            "match_date": match["matchDateTimeUTC"],
            "matchweek": match["group"]["groupOrderID"],
            "home_team": match["team1"]["teamName"],
            "away_team": match["team2"]["teamName"],
            "home_goals": final_result["pointsTeam1"],
            "away_goals": final_result["pointsTeam2"],
            "last_update": match["lastUpdateDateTime"]
        }

        transformed_matches.append(transformed_match)

    print(f"Transformed {len(transformed_matches)} finished matches")

    return transformed_matches