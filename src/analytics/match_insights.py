import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
matches_df = pd.read_csv('artifacts/matches.csv')      # Update path if needed
deliveries_df = pd.read_csv('artifacts/deliveries.csv')

def get_city_win_percentage(city, team):
    matches_in_city = matches_df[matches_df['city'] == city]
    played = matches_in_city[(matches_in_city['team1'] == team) | (matches_in_city['team2'] == team)]
    wins = played[played['winner'] == team]

    if len(played) == 0:
        return None  # Return None if no data available

    win_percent = (len(wins) / len(played)) * 100
    # return win_percent  # Return win percentage as a float
    return f"{team} has a win rate of {win_percent:.2f}% when playing in {city}."




def get_toss_decision_outcome(city, team, decision):
    filtered = matches_df[ 
        (matches_df['city'] == city) &
        (matches_df['toss_winner'] == team) &
        (matches_df['toss_decision'] == decision)
    ]
    won = filtered[filtered['winner'] == team]

    if len(filtered) == 0:
        return {"No data": 100}  # Return a dictionary if no matches found

    win_percentage = (len(won) / len(filtered)) * 100
    lose_percentage = 100 - win_percentage

    # Return a dictionary with toss decision outcomes
    # return win_percentage
    return f"Teams choosing to {decision} in {city} win {win_percentage:.2f}% of the time."



def get_avg_first_innings_score(city):
    city_matches = matches_df[matches_df['city'] == city]

    if city_matches.empty:
        return f"No matches played in {city}."

    match_ids = city_matches['id'].unique()

    first_innings = deliveries_df[
        (deliveries_df['match_id'].isin(match_ids)) &
        (deliveries_df['inning'] == 1)
    ]

    if first_innings.empty:
        return f"No first innings data for {city}."

    # Calculate total runs per match
    runs_per_match = first_innings.groupby('match_id')['total_runs'].sum()
    avg_score = runs_per_match.mean()

    return f"Average 1st innings score in {city}: {int(avg_score)} runs."


# === LOCAL TESTING ===
# if __name__ == '__main__':
#     test_city = 'Mumbai'
#     test_team = 'Mumbai Indians'
#     test_decision = 'bat'

#     print("=== Testing Venue Win % ===")
#     print(get_city_win_percentage(test_city, test_team))

#     print("\n=== Testing Toss Decision Outcome ===")
#     toss_decision_outcome = get_toss_decision_outcome(test_city, test_team, test_decision)
#     print(toss_decision_outcome)  # This will print the toss decision outcome as a dictionary

#     print("\n=== Testing Average First Innings Score ===")
#     print(get_avg_first_innings_score(test_city))

    