import os
import sys
from src.exception import CustomException
from src.logger import get_logger
logging = get_logger(__name__)
import pandas as pd


from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:                                         #this only stores path to file
    raw_data_path_delivery: str =os.path.join('artifacts',"deliveries.csv")
    raw_data_path_match: str =os.path.join('artifacts',"matches.csv")
    
    
class DataIngestion:     #creating files in artifacts folder & storing data in it
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()    #this ingestion_config has 3 variables data from above

    def initiate_data_ingestion(self):                 
        logging.info("Entered the data ingestion method or component") 
        try:
            delivery_df=pd.read_csv(r'C:\Users\abhi1\Desktop\ipl\notebook\deliveries.csv')  
            match_df=pd.read_csv(r'C:\Users\abhi1\Desktop\ipl\notebook\matches.csv')    
            logging.info('Read the dataset as dataframe')   

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path_delivery),exist_ok=True) #creating directory If the directory doesn’t exist

            delivery_df.to_csv(self.ingestion_config.raw_data_path_delivery,index=False,header=True)   #This line saves the entire dataset (df) as a CSV file at the location
            match_df.to_csv(self.ingestion_config.raw_data_path_match,index=False,header=True)  
 


            logging.info("Data ingestion completed successfully.")

            return(
                self.ingestion_config.raw_data_path_delivery, #returns path
                self.ingestion_config.raw_data_path_match

            )
        except Exception as e:
            logging.error("Exception occurred during data ingestion.")
            raise CustomException(e,sys)    
        
        
if __name__=="__main__": #It makes sure the code inside this runs only when you run this file directly, not when you import it somewhere else.
    obj=DataIngestion()                                  #initialising object
    delivery_data,match_data=obj.initiate_data_ingestion()   #storing path of train and test data

    data_transformation=DataTransformation()
    X_train, X_test, y_train, y_test,transformer=data_transformation.initiate_data_transformation(delivery_data,match_data) #passing these paths as parameter

    modeltrainer=ModelTrainer()
    print(modeltrainer.train_model(X_train, X_test, y_train, y_test,transformer)) #prints r2 score of best model after applying best parameters

        