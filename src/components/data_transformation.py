import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from src.exception import CustomException
from src.logger import get_logger
from src.utils import save_object
import pickle

logging = get_logger(__name__)

@dataclass
class DataTransformationConfig:
    transformer_obj_file_path: str = os.path.join("artifacts", "transformer.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self, delivery_path: str, match_path: str):
        try:
            logging.info("Reading input CSV files")
            delivery_df = pd.read_csv(delivery_path)
            match_df = pd.read_csv(match_path)

            logging.info("Starting data transformation process")

            total_score_df = delivery_df.groupby(["match_id", "inning"]).sum()['total_runs'].reset_index()
            total_score_df = total_score_df[total_score_df['inning'] == 1].reset_index(drop=True)

            match_df = match_df.merge(total_score_df[['match_id','total_runs']], left_on='id', right_on='match_id')

            teams = [
                'Royal Challengers Bengaluru','Mumbai Indians','Kolkata Knight Riders',
                'Rajasthan Royals','Chennai Super Kings','Sunrisers Hyderabad',
                'Delhi Capitals','Punjab Kings','Lucknow Super Giants','Gujarat Titans']

            match_df['team1'] = match_df['team1'].replace({
                'Delhi Daredevils': 'Delhi Capitals',
                'Deccan Chargers': 'Sunrisers Hyderabad',
                'Kings XI Punjab': 'Punjab Kings',
                'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
            })
            match_df['team2'] = match_df['team2'].replace({
                'Delhi Daredevils': 'Delhi Capitals',
                'Deccan Chargers': 'Sunrisers Hyderabad',
                'Kings XI Punjab': 'Punjab Kings',
                'Royal Challengers Bangalore': 'Royal Challengers Bengaluru'
            })

            match_df = match_df[(match_df['team1'].isin(teams)) & (match_df['team2'].isin(teams))]
            match_df = match_df[match_df['method'] != 'D/L']

            match_df = match_df[['match_id','city','winner','total_runs','toss_winner','toss_decision']]
            delivery_df = match_df.merge(delivery_df, on='match_id')
            delivery_df = delivery_df[delivery_df['inning'] == 2]

            delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()
            delivery_df['runs_left'] = delivery_df['total_runs_x'] - delivery_df['current_score']
            delivery_df['balls_left'] = 126 - (delivery_df['over'] * 6 + delivery_df['ball'])

            delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna("0")
            delivery_df['player_dismissed'] = delivery_df['player_dismissed'].apply(lambda x: x if x == '0' else "1")
            delivery_df['player_dismissed'] = delivery_df['player_dismissed'].astype(int)
            delivery_df['wickets_left'] = 10 - delivery_df.groupby("match_id")['player_dismissed'].cumsum().values

            delivery_df['crr'] = (delivery_df['current_score'] * 6) / (120 - delivery_df['balls_left'])
            delivery_df['rrr'] = (delivery_df['runs_left'] * 6) / delivery_df['balls_left']
            delivery_df['momentum'] = delivery_df['crr'] - delivery_df['rrr']

            delivery_df['result'] = delivery_df.apply(lambda row: 1 if row['batting_team'] == row['winner'] else 0, axis=1)

            final_df = delivery_df[['batting_team','bowling_team','city','runs_left','balls_left','wickets_left','total_runs_x',
                                    'crr','rrr','momentum','toss_winner','toss_decision','result']]
            final_df = final_df.sample(frac=1).reset_index(drop=True)

            final_df.replace([np.inf, -np.inf], np.nan, inplace=True)
            final_df.dropna(inplace=True)
            final_df = final_df[final_df['balls_left'] != 0]

            X = final_df.drop('result', axis=1)
            y = final_df['result']

            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=40)

            ct = ColumnTransformer([
                ('categorical', OneHotEncoder(sparse_output=False, drop='first'),
                 ['batting_team','bowling_team','city','toss_winner','toss_decision'])
            ], remainder='passthrough')

            # X_train = ct.fit_transform(X_train)
            # X_test = ct.transform(X_test)
            ct.fit(X_train)  
            save_object(self.data_transformation_config.transformer_obj_file_path, ct)   #path to save , object to save

            logging.info("Data transformation completed successfully")
            logging.info(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")

            return X_train, X_test, y_train, y_test,ct

        except Exception as e:
            logging.error("Error during data transformation")
            raise CustomException(e, sys)
