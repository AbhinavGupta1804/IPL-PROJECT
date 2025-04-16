from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.analytics.match_insights import (
    get_city_win_percentage,
    get_toss_decision_outcome,
    get_avg_first_innings_score
)

app = Flask(__name__)

teams = [
    'Royal Challengers Bengaluru', 'Mumbai Indians', 'Kolkata Knight Riders',
    'Rajasthan Royals', 'Chennai Super Kings', 'Sunrisers Hyderabad',
    'Delhi Capitals', 'Punjab Kings', 'Lucknow Super Giants', 'Gujarat Titans'
]

cities = [
    'Mumbai', 'Jaipur', 'Hyderabad', 'Kolkata', 'Abu Dhabi', 'Delhi',
    'Chennai', 'Chandigarh', 'Pune', 'Lucknow', 'Bengaluru', 'Dubai',
    'Raipur', 'Ahmedabad', 'Centurion', 'Navi Mumbai', 'Ranchi',
    'Indore', 'Cape Town', 'Durban', 'Johannesburg', 'Sharjah',
    'Cuttack', 'Bloemfontein', 'Dharamsala', 'Visakhapatnam',
    'Kimberley', 'Guwahati', 'East London', 'Nagpur', 'Port Elizabeth',
    'Mohali', 'Bangalore'
]

@app.route('/')
def home():
    return render_template('index.html', teams=teams, cities=cities)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get data from the form and convert to proper types
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        score = int(request.form['score'])  # Convert score to int
        overs = float(request.form['overs'])  # Convert overs to float
        wickets = int(request.form['wickets'])  # Convert wickets to int
        target = int(request.form['target'])  # Convert target to int
        toss_winner = request.form['toss_winner']
        toss_decision = request.form['toss_decision'].lower()

        # Create custom data object and get data as DataFrame
        custom_data = CustomData(
            batting_team, bowling_team, city, score, overs, wickets, target, toss_winner, toss_decision
        )
        input_df = custom_data.get_data_as_data_frame()

        # Predict using pipeline
        pipeline = PredictPipeline()
        prediction = pipeline.predict(input_df)

        win_prob = round(prediction[0][1] * 100, 2)
        lose_prob = round(prediction[0][0] * 100, 2)

        # Get insights
        venue_stat = get_city_win_percentage(city, batting_team)
        toss_stat = get_toss_decision_outcome(city, batting_team, toss_decision)
        avg_score_stat = get_avg_first_innings_score(city)

        
        # Strategic Recommendations
        suggestions = []

        if win_prob < 30 and overs < 10:
            suggestions.append("You're falling behind early. Introduce a power-hitter or accelerate scoring.")
        if wickets >= 6 and overs < 15:
            suggestions.append("Too many wickets lost. Stabilize the innings with defensive play.")
        if (score / overs) < (target / 20):
            suggestions.append("Run rate is below required. Increase aggression to keep up with the target.")
        if overs > 16 and win_prob > 70:
            suggestions.append("You’re in control. Rotate strike and avoid unnecessary risks.")
        if overs > 17 and (10 - wickets) >= 4:
            suggestions.append("Launch an all-out attack in the death overs!")

        if win_prob < 35 and overs < 10:
            suggestions.append("Try introducing slower bowlers or spinners to break momentum.")
        if overs < 6:
            suggestions.append("Powerplay in progress. Set attacking fields to take early wickets.")
        if wickets <= 2 and overs > 10:
            suggestions.append("Struggling to take wickets. Bring back your main bowler.")
        if wickets >= 6 and overs > 15:
            suggestions.append("Opponent is collapsing. Go aggressive and finish the innings early.")
        # if venue_stat < 40:
        #     suggestions.append("Your team has a weak record here. Consider adapting a different game plan.")

        if toss_winner == batting_team and toss_decision.lower() == 'field' and win_prob < 50:
            suggestions.append("Fielding after winning the toss might be risky. Consider revisiting toss strategy.")
        # if venue_stat > 60:
        #     suggestions.append("Great venue performance! Leverage home ground advantage.")
        # if avg_score_stat < 140 and score < 140 and overs >= 15:
        #     suggestions.append("This is a low-scoring pitch. Focus on building a defendable total.")
        # if avg_score_stat > 170 and target >= 170 and overs < 10 and score < 80:
        #     suggestions.append("High-scoring pitch. Boost your scoring rate to avoid pressure.")

        if win_prob > 70 and wickets <= 3 and overs > 16:
            suggestions.append("You're dominating! Try to boost Net Run Rate now.")
        if win_prob < 40 and target - score < 30 and wickets <= 2:
            suggestions.append("You're close to the target. Rotate strike, avoid risks.")
        if toss_winner == batting_team and city == batting_team and venue_stat > 65:
            suggestions.append("Perfect conditions today. Make this opportunity count!")

        return render_template(
            'index.html',
            win=win_prob,
            lose=lose_prob,
            teams=teams,
            cities=cities,
            batting_team=batting_team,
            bowling_team=bowling_team,
            city=city,
            score=score,
            overs=overs,
            wickets=wickets,
            target=target,
            toss_winner=toss_winner,
            toss_decision=toss_decision,
            venue_stat=venue_stat,
            toss_stat=toss_stat,
            avg_score_stat=avg_score_stat,
            suggestions=suggestions,
            
        )

if __name__ == '__main__':
    app.run(debug=True)
