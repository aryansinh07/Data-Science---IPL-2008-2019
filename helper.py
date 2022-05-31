import pandas as pd
import preprocessor

def runs(matches):
    temp1 = matches.groupby('team1')['total_runs_x'].sum().reset_index()
    temp2 = matches.groupby('team2')['total_runs_y'].sum().reset_index()
    temp2.rename(columns={'team2': 'team1'}, inplace=True)
    total_runs = pd.merge(temp1, temp2, how='left', on='team1')
    total_runs['Total_runs_scored'] = total_runs['total_runs_x'] + total_runs['total_runs_y']
    total_runs = total_runs.sort_values(by='Total_runs_scored', ascending=False)
    total_runs.rename(columns={'total_runs_x':'total_runs_first_batting','total_runs_y':'total_runs_second_batting'}, inplace=True)
    total_runs['total_runs_first_batting']=total_runs['total_runs_first_batting'].astype('int')
    total_runs['total_runs_second_batting'] = total_runs['total_runs_second_batting'].astype('int')
    total_runs['Total_runs_scored'] = total_runs['Total_runs_scored'].astype('int')

    return total_runs
def winner(matches):
    winner = matches.drop_duplicates(subset=['Season'], keep='last').sort_values(by='Season', ascending=True)[
        ['Season', 'winner']].reset_index()
    winner.drop(columns=['index'], inplace=True)
    return winner

def orange(matches,ball):
    orange = ball.groupby(['Season', 'batsman'])['batsman_runs'].sum().reset_index()
    orange = orange.sort_values(by=['Season', 'batsman_runs'], ascending=[True, False]).drop_duplicates(subset=['Season'],
                                                                                               keep='first')
    return orange

def purple(matches , ball):
    ballpurple = ball[(ball['dismissal_kind'] != 'run out') & (ball['dismissal_kind'] != 'retired hurt') & (
                ball['dismissal_kind'] != 'obstructing the field')]
    purple = ballpurple.groupby(['Season', 'bowler'])['player_dismissed'].count().sort_index(
        ascending=False).reset_index()
    purple = purple.sort_values(by=['Season', 'player_dismissed'], ascending=[True, False]).drop_duplicates(subset=['Season'],
                                                                                                   keep='first')
    return purple

def sixes(matches,ball):
    sixes = ball[ball['batsman_runs'] == 6]
    sixes = sixes.groupby(['Season', 'batsman'])['batsman_runs'].count().reset_index()
    sixes = sixes.sort_values(by=['batsman_runs', 'Season'], ascending=[False, True]).drop_duplicates(subset=['Season'],
                                                                                                      keep='first')
    sixes = sixes.sort_values(by='Season' , ascending=True)
    sixes.rename(columns={'batsman_runs':'No of Sixes'},inplace=True)
    return sixes

def fours(matches,ball):
    fours = ball[ball['batsman_runs'] == 4]
    fours = fours.groupby(['Season', 'batsman'])['batsman_runs'].count().reset_index().sort_values(
        by=['Season', 'batsman_runs'], ascending=[True, False]).drop_duplicates(subset='Season', keep='first')
    fours.rename(columns={'batsman_runs':'No of Fours'},inplace=True)
    return fours

def catches(matches,ball):
    catches = ball[ball['dismissal_kind'] == 'caught']
    catches = catches.groupby('fielder')['dismissal_kind'].count().sort_values(ascending=False).reset_index()
    catchestop10 = catches.head(10)
    catchestop10.rename(columns={'dismissal_kind':'No of Catches'},inplace=True)
    return catchestop10

def runout(ball):
    runout = ball[(ball['dismissal_kind'] == 'run out')]
    top10runout = runout.groupby('fielder')['dismissal_kind'].count().sort_values(ascending=False).reset_index()
    top10runout.rename(columns={'dismissal_kind': 'No of Run Outs'}, inplace=True)
    return top10runout

def teams(matches):
    team = matches['team1'].unique().tolist()

    team.sort()
    return team

def opponentteam(matches,selected_team):
    opponentteam = matches['team1'].unique().tolist()
    opponentteam.remove(selected_team)
    opponentteam.sort()
    return opponentteam

def most_runs_team(matches,ball,selected_team):
    team = ball[(ball['batting_team'] == selected_team)]
    most_runs = team.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
    return most_runs

def most_wickets_team(matches,ball,selected_team):
    team = ball[(ball['bowling_team'] == selected_team)]
    mostwickets = team[(team['dismissal_kind'] != 'run out') & (team['dismissal_kind'] != 'retired hurt') & (
                team['dismissal_kind'] != 'obstructing the field')]
    mostwickets = mostwickets.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).reset_index()
    return mostwickets
def most_sixes_team(matches,ball,selected_team):
    team = ball[(ball['batting_team'] == selected_team)]
    sixes = team[team['batsman_runs'] == 6]
    sixes = sixes.groupby('batsman')['batsman_runs'].count().sort_values(ascending=False).reset_index().head(10)
    sixes.rename(columns={'batsman_runs': 'No of Sixes'}, inplace=True)
    return sixes
def most_fours_team(matches,ball,selected_team):
    team = ball[(ball['batting_team'] == selected_team)]
    fourss = team[team['batsman_runs'] == 4]
    fourss = fourss.groupby('batsman')['batsman_runs'].count().sort_values(ascending=False).reset_index().head(10)
    fourss.rename(columns={'batsman_runs': 'No of Sixes'}, inplace=True)
    return fourss

def oppo(matches,selected_team,opponent_team):
    matches_won = matches[((matches['team1'] == selected_team) & (matches['team2'] == opponent_team) & (
                matches['winner'] == selected_team)) | ((matches['team2'] == selected_team) & (
                matches['team1'] == opponent_team) & (matches['winner'] == selected_team))]
    matches_played = matches[((matches['team1'] == selected_team) & (matches['team2'] == opponent_team)) | (
                (matches['team2'] == selected_team) & (matches['team1'] == opponent_team))]
    matches_won = matches_won.shape[0]
    matches_played = matches_played.shape[0]
    return matches_played , matches_won

def top10batsman(ball,selected_team,opponent_team):
    top10batsman = ball[
        (ball['batting_team'] == selected_team) & (ball['bowling_team'] == opponent_team)]
    top10batsman = top10batsman.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
    return top10batsman

def top10bowlers(ball,selected_team,opponent_team):
    top10bowler = ball[((ball['dismissal_kind'] != 'run out') & (ball['dismissal_kind'] != 'retired hurt') & (
                ball['dismissal_kind'] != 'obstructing the field')) & (
                                   (ball['batting_team'] == opponent_team) & (
                                       ball['bowling_team'] == selected_team))]
    top10bowler = top10bowler.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).reset_index()
    return top10bowler
def won(matches,selected_team):
    iplwinners = matches.drop_duplicates(subset='Season', keep='last').sort_values(by='Season', ascending=True)[
        'winner'].tolist()
    count = 0
    for i in iplwinners:
        if i == selected_team:
            count = count + 1
    return count
def batsman(ball):
    batsman = ball['batsman'].unique().tolist()
    batsman.sort()
    return batsman

def batsmanruns(ball,selected_batsman):
    batsmanruns = ball[ball['batsman']==selected_batsman]['batsman_runs'].sum()
    matches_played_batsman = ball[ball['batsman'] ==selected_batsman]
    matches_played_batsman = matches_played_batsman.drop_duplicates(subset='match_id', keep='last').shape[0]
    fours = ball[(ball['batsman']==selected_batsman) & (ball['batsman_runs']==4)]['batsman_runs'].count()
    sixes = ball[(ball['batsman']==selected_batsman) & (ball['batsman_runs']==6)]['batsman_runs'].count()
    ball_played = ball[ball['batsman']==selected_batsman].shape[0]
    teams_played = ball[ball['batsman']==selected_batsman]
    teams_played = teams_played['batting_team'].unique().tolist()
    return batsmanruns , matches_played_batsman , fours , sixes , ball_played , teams_played

def bowler(ball):
    bowler = ball['bowler'].unique().tolist()
    bowler.sort()
    return bowler

def bowler_wickets(ball,selected_bowler):
    bowler = ball[((ball['dismissal_kind'] != 'run out') & (ball['dismissal_kind'] != 'retired hurt') & (
                ball['dismissal_kind'] != 'obstructing the field') & (ball['bowler'] == selected_bowler))]
    no_wickets = bowler['player_dismissed'].count()
    no_wickets_season = bowler.groupby(['Season'])['player_dismissed'].count().reset_index().sort_values(by='Season', ascending=True)
    matches = bowler.drop_duplicates(subset=['match_id'] , keep='first').shape[0]
    teams_played = bowler['bowling_team'].unique().tolist()
    teamswise_wicket = bowler.groupby('bowling_team')['player_dismissed'].count().reset_index()
    return no_wickets,no_wickets_season,matches,teams_played,teamswise_wicket

def batsmanvsbowler(ball,selected_batsman , selected_bowler):
    ballsfaced = ball[(ball['bowler'] == selected_bowler) & (ball['batsman'] == selected_batsman)]['batsman_runs'].count()
    runsscored = ball[(ball['bowler'] == selected_bowler) & (ball['batsman'] == selected_batsman)]['batsman_runs'].sum()
    strike_rate = (runsscored/ballsfaced)*100
    wicket= ball[(ball['bowler'] == selected_bowler) & (ball['batsman'] == selected_batsman)]['player_dismissed'].count()
    six = ball[(ball['bowler'] == selected_bowler) & (ball['batsman'] == selected_batsman) & (ball['batsman_runs'] == 6)].shape[0]
    four = ball[(ball['bowler'] == selected_bowler) & (ball['batsman'] == selected_batsman) & (ball['batsman_runs'] == 4)].shape[0]
    return ballsfaced , runsscored , strike_rate , wicket , six , four
