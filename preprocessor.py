import pandas as pd

def preprocess(matches,ball):
    inning1 = ball[ball['inning'] == 1]
    firstinning_score = inning1.groupby('match_id')['total_runs'].sum().reset_index()
    firstinning_score.rename(columns={'match_id': 'id'}, inplace=True)
    matches = pd.merge(matches, firstinning_score, how='left', on='id')
    inning2 = ball[ball['inning'] == 2]
    secondinning_score = inning2.groupby('match_id')['total_runs'].sum().reset_index()
    secondinning_score.rename(columns={'match_id': 'id'}, inplace=True)
    matches = pd.merge(matches, secondinning_score, how='left', on='id')
    matches['team1'] = matches['team1'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['team2'] = matches['team2'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['team1'] = matches['team1'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['team2'] = matches['team2'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['winner'] = matches['winner'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['winner'] = matches['winner'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['toss_winner'] = matches['toss_winner'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['toss_winner'] = matches['toss_winner'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['team1'] = matches['team1'].replace(to_replace='Rising Pune Supergiant', value='Rising Pune Supergiants')
    matches['team2'] = matches['team2'].replace(to_replace='Rising Pune Supergiant', value='Rising Pune Supergiants')
    matches['toss_winner'] = matches['toss_winner'].replace(to_replace='Rising Pune Supergiant',
                                                            value='Rising Pune Supergiants')
    matches['winner'] = matches['winner'].replace(to_replace='Rising Pune Supergiant', value='Rising Pune Supergiants')
    return matches
def preprocess_ball(matches,ball):
    ball['batting_team'] = ball['batting_team'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    ball['bowling_team'] = ball['bowling_team'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    ball['batting_team']= ball['batting_team'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    ball['bowling_team']= ball['bowling_team'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    ball['batting_team'] = ball['batting_team'].replace(to_replace='Rising Pune Supergiant', value='Rising Pune Supergiants')
    ball['bowling_team']= ball['bowling_team'].replace(to_replace='Rising Pune Supergiant', value='Rising Pune Supergiants')
    matches.rename(columns={'id': 'match_id'}, inplace=True)
    season = matches[['match_id', 'Season']].reset_index()
    season.drop(columns=['index'], inplace=True)
    ball = pd.merge(ball, season, on='match_id', how='left')
    return ball