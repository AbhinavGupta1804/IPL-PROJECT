#common fuctionalites
                 #A pickle file saves Python OBJECTS in binary format for efficient storage and faster loading
import os
import sys

import numpy as np 
import pandas as pd
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
                                               
def save_object(file_path, obj):                            ## Define a function to save an object to a file
    try:
        dir_path = os.path.dirname(file_path)               ## Get the directory path from the file path

        os.makedirs(dir_path, exist_ok=True) ## Create the directory if it doesn't exist (without raising an error)

        with open(file_path, "wb") as file_obj:   # Open the file at 'file_path' in write-binary mode
            pickle.dump(obj, file_obj)          #This takes the object obj and saves it into the file in binary form.

    except Exception as e:
        raise CustomException(e, sys)
    

    
def load_object(file_path):         #loading pickle file
    try:
        with open(file_path, "rb") as file_obj: #open the file path in read byte mode
            return pickle.load(file_obj)        #loading pickle file using dill

    except Exception as e:      #e represents the actual exception/error message that occurred during the execution of the code
        raise CustomException(e, sys)

