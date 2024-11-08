import os
import sys
from ..exception import CustomException
from ..logger import logging
import pandas as pd 

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv') # (folder,file_name)
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def inititate_data_ingestion(self):
        logging.info("entered the data ingestion method or component")
        try:
            # reading data from the source --> it can be MongoDB or SQL or or APIs or anything else
            df = pd.read_csv('notebook/data/student.csv')
            logging.info('read the dataset as dataframe')
            
            # making the components of artifacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok = True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index= False, header = True)
            
            logging.info('train test split inititated')
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)
            
            # saving the splitted train and test set in artifacts folder
            train_set.to_csv(self.ingestion_config.train_data_path,index= False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path,index= False, header = True)
            
            logging.info('ingestion of the data is completed')
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    
    obj = DataIngestion()
    train_data, test_data = obj.inititate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)
    
    model_trainer = ModelTrainer()
    print(f"R-square score of the model is: {model_trainer.initiate_model_trainer(train_arr,test_arr)*100}")