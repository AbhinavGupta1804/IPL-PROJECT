import streamlit as st
import pickle
import pandas as pd

teams = ['Royal Challengers Bengaluru',
 'Mumbai Indians',
 'Kolkata Knight Riders',
 'Rajasthan Royals',
 'Chennai Super Kings',
 'Sunrisers Hyderabad',
 'Delhi Capitals',
 'Punjab Kings',
 'Lucknow Super Giants',
 'Gujarat Titans']

cities = ['Mumbai', 'Jaipur', 'Hyderabad', 'Kolkata', 'Abu Dhabi', 'Delhi',
       'Chennai', 'Chandigarh', 'Pune', 'Lucknow', 'Bengaluru', 'Dubai',
       'Raipur', 'Ahmedabad', 'Centurion', 'Navi Mumbai', 'Ranchi',
       'Indore', 'Cape Town', 'Durban', 'Johannesburg', 'Sharjah',
       'Cuttack', 'Bloemfontein', 'Dharamsala', 'Visakhapatnam',
       'Kimberley', 'Guwahati', 'East London', 'Nagpur', 'Port Elizabeth',
       'Mohali', 'Bangalore']

pipe = pickle.load(open('ipl_win_predictor.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)                   #It creates two side-by-side columns in your Streamlit app.

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))
    

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')
    
col6, col7 = st.columns(2)
with col6:
    toss_winner = st.selectbox('Toss Winner', sorted(teams))
with col7:
    toss_decision = st.selectbox('Toss Decision', ['bat', 'field'])
    

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left
                             #'these are column names of our trained dataset'
    momentum = crr -rrr                         
    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],
                             'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets_left],
                             'total_runs_x':[target],'crr':[crr],'rrr':[rrr],'momentum':[momentum],'toss_winner': [toss_winner],
                             'toss_decision': [toss_decision],
})

    result = pipe.predict_proba(input_df)   #it returns  a array
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")