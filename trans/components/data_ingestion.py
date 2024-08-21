import os
import sys
from trans.entity.config_entity import DataIngestionConfig
from trans.entity.artifact_entity import DataIngestionArtifact
from trans.logger import logging
from trans.exception import transException
from trans.cloud_storage.gcp_cloud import GCloudSync
from trans.constant import TRAINING_BUCKET_NAME, DATASET_FOLDER, TRAIN, TEST, VALIDATION, JSON_FILE

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise transException(e, sys) from e
        
    def sync_folder_from_gcloud(self) -> None:

        try:
            logging.info("Entered the get_data_from method of Data Ingestion Class")

            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)

            os.makedirs(self.data_ingestion_config.data_ingestion_raw_file_path, exist_ok=True)

            gcloud = GCloudSync()
            gcloud.sync_folder_from_gcloud(gcp_bucket_url=TRAINING_BUCKET_NAME,
                                           folder=DATASET_FOLDER,
                                           destination=self.data_ingestion_config.data_ingestion_raw_file_path,
                                           train=TRAIN, test=TEST, validation=VALIDATION, jsonfile=JSON_FILE)
            logging.info("Exiting the get_data_from method of Data Ingestion Class")
        except Exception as e:
            raise transException(e, sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("Starting data ingestion component")

            self.sync_folder_from_gcloud()

            data_ingestion_artifact = DataIngestionArtifact(
                ingested_data_raw_file_path=self.data_ingestion_config.data_ingestion_raw_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            raise transException(e, sys) from e
   