import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import helper
import preprocessor
matches = pd.read_csv('matches.csv')
ball = pd.read_csv('deliveries.csv')
matches = preprocessor.preprocess(matches,ball)
ball = preprocessor.preprocess_ball(matches,ball)
st.sidebar.title('IPL 2008-2019')
menu = st.sidebar.radio(
    'Select an Option' ,
    ('Overall','Team wise analysis','Player wise analysis')
)


if menu == 'Overall':
    st.title("Overall Analysis of IPL from 2008-2019")
    unique = matches['team1'].nunique()
    seasons = matches['Season'].nunique()
    match = matches.shape[0]
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.subheader("Teams")
        st.title(unique)
    with col2:
        st.subheader("No of Seasons")
        st.title(seasons)
    with col3:
        st.subheader("No of matches played")
        st.title(match)
    total_runs = helper.runs(matches)
    st.subheader("The total runs scored by each team is")
    st.dataframe(total_runs)
    st.subheader("The winner of each season is:")
    winner = helper.winner(matches)
    st.dataframe(winner)
    st.subheader("The orange cap holder of each season")
    orange = helper.orange(matches,ball)
    st.dataframe(orange)
    st.subheader("The purple cap holder of each season")
    purple = helper.purple(matches,ball)
    st.dataframe(purple)
    st.subheader("The maximum sixes in each Season")
    sixes = helper.sixes(matches,ball)
    st.dataframe(sixes)
    st.subheader("The maximum fours in each Season")
    fours = helper.fours(matches,ball)
    st.dataframe(fours)
    st.subheader("The fielder who has taken most no of catches:")
    catches = helper.catches(matches,ball)
    st.dataframe(catches)
    st.subheader("The fielder who has done most run outs till now:")
    runout = helper.runout(ball)
    st.dataframe(runout)

if menu == 'Team wise analysis':
    team = helper.teams(matches)
    selected_team = st.sidebar.selectbox("Select Team",team)
    st.title("Analysis of " + str(selected_team))
    no_of_times_won = helper.won(matches, selected_team)
    st.subheader("No of Title Won by " + str(selected_team))
    st.title(no_of_times_won)
    most_runs = helper.most_runs_team(matches,ball,selected_team)
    st.subheader("Player who has scored most runs for" + str(selected_team))
    st.dataframe(most_runs)
    most_wickets = helper.most_wickets_team(matches,ball,selected_team)
    st.subheader("Player who had taken most wickets for the team  " + str(selected_team))
    st.dataframe(most_wickets)
    most_sixes = helper.most_sixes_team(matches,ball,selected_team)
    st.subheader("Player who had hit most no of sixes for the team  " + str(selected_team))
    st.dataframe(most_sixes)
    most_fours = helper.most_fours_team(matches,ball,selected_team)
    st.subheader("Player who had hit most no of fours for the team  " + str(selected_team))
    opponent_team = helper.opponentteam(matches,selected_team)
    opponent_team = st.selectbox("Select Opponent",opponent_team)
    matches_played , matches_won = helper.oppo(matches,selected_team,opponent_team)
    st.header(str(selected_team) + " VS " + str(opponent_team))
    st.subheader("Total no of matches played")
    st.title(matches_played)
    st.subheader("Matches won by " + str(selected_team))
    st.title(matches_won)
    try:
        win_percentage = ((matches_won / matches_played) * 100)
        st.subheader("Win percentage of " + str(selected_team) + " against " + str(opponent_team))
        st.title(win_percentage)
    except ZeroDivisionError:
        st.subheader("No Matches played against each other")
    st.subheader("Most successful batsman of " + str(selected_team) + " against " + str(opponent_team))
    top10batsman = helper.top10batsman(ball,selected_team,opponent_team)
    st.dataframe(top10batsman)
    st.subheader("Most successful bowlers of " + str(selected_team) + " against " + str(opponent_team))
    top10bowler = helper.top10bowlers(ball, selected_team, opponent_team)
    st.dataframe(top10bowler)

if menu == 'Player wise analysis':
    menu2 = st.sidebar.radio(
        'Select player',
        ('Batsman','Bowler','Batsman VS Bowler')
    )
    if menu2 == 'Batsman':
        batsman = helper.batsman(ball)
        selected_batsman = st.sidebar.selectbox("Select Batsman",batsman)
        st.title(str(selected_batsman))
        T_runs_scored , matches_played_batsman , fours , sixes , ball_played , teams_played = helper.batsmanruns(ball,selected_batsman)
        avg =(T_runs_scored/matches_played_batsman)
        strikerate = ((T_runs_scored/ball_played)*100)
        st.subheader("Total Runs Scored")
        st.subheader(T_runs_scored)
        st.subheader("Total Matches Played:")
        st.subheader(matches_played_batsman)
        st.subheader("Fours:")
        st.subheader(fours)
        st.subheader("Sixes:")
        st.subheader(sixes)
        st.subheader("AVG")
        st.subheader(avg)
        st.subheader("Strike rate:")
        st.subheader(strikerate)
        st.subheader("Played for teams:")
        for i in range(len(teams_played)):
            st.subheader(teams_played[i])
    if menu2 == 'Bowler':
        bowler = helper.bowler(ball)
        selected_bowler = st.sidebar.selectbox("Select Bowler" , bowler)
        st.title(str(selected_bowler))
        no_wickets , no_wickets_season , matches , teamss_played , teamwise_wicket = helper.bowler_wickets(ball,selected_bowler)
        st.subheader("Total Wickets taken")
        st.subheader(no_wickets)
        st.subheader("Total Matches Played")
        st.subheader(matches)
        st.subheader("Wickets VS Season")
        st.dataframe(no_wickets_season)
        st.subheader("Played for teams:")
        for i in range(len(teamss_played)):
            st.subheader(teamss_played[i])
        st.subheader("Wickets for the teams")
        st.dataframe(teamwise_wicket)
    if menu2 == 'Batsman VS Bowler' :
        batsman = helper.batsman(ball)
        bowler = helper.bowler(ball)
        selected_batsman = st.sidebar.selectbox("Select Batsman", batsman)
        selected_bowler = st.sidebar.selectbox("Select Bowler", bowler)
        st.title(str(selected_batsman) +  " VS " + str(selected_bowler))
        ballsfaced, runsscored, strike_rate, wicket, six, four = helper.batsmanvsbowler(ball,selected_batsman,selected_bowler)
        st.subheader("Balls Faced")
        st.subheader(ballsfaced)
        st.subheader("Total Runs Scored")
        st.subheader(runsscored)
        st.subheader("Strike Rate")
        st.subheader(strike_rate)
        st.subheader("No of time " + str(selected_bowler) + " out " + str(selected_batsman))
        st.subheader(wicket)
        st.subheader("Sixes")
        st.subheader(six)
        st.subheader("Four")
        st.subheader(four)
