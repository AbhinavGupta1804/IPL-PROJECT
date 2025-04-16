
import sys
import pandas as pd
import os
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
     try:
        transformer_path = os.path.join("artifacts", "transformer.pkl")
        model_path = os.path.join("artifacts", "model.pkl")

        model = load_object(model_path)

        # Predict using the transformed features
        prediction = model.predict_proba(features)
        return prediction

     except Exception as e:
        raise CustomException(e, sys)



class CustomData:
    def __init__(self, batting_team, bowling_team, city, score, overs, wickets, target, toss_winner, toss_decision):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.city = city
        self.score = score
        self.overs = overs
        self.wickets = wickets
        self.target = target
        self.toss_winner = toss_winner
        self.toss_decision = toss_decision

    def get_data_as_data_frame(self):
        try:
            runs_left = self.target - self.score
            balls_left = 120 - (self.overs * 6)
            wickets_left = 10 - self.wickets
            crr = self.score / self.overs
            rrr = (runs_left * 6) / balls_left
            momentum = crr - rrr

            data = {
                "batting_team": [self.batting_team],
                "bowling_team": [self.bowling_team],
                "city": [self.city],
                "runs_left": [runs_left],
                "balls_left": [balls_left],
                "wickets_left": [wickets_left],
                "total_runs_x": [self.target],
                "crr": [crr],
                "rrr": [rrr],
                "momentum": [momentum],
                "toss_winner": [self.toss_winner],
                "toss_decision": [self.toss_decision],
            }

            return pd.DataFrame(data)

        except Exception as e:
            raise CustomException(e, sys)
