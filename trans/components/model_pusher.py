import os
import sys
from trans.exception import transException
from trans.logger import logging
from trans.entity.config_entity import ModelPusherConfig
from trans.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact
from trans.cloud_storage.gcp_cloud import GCloudSync
from trans.constant import TRAINING_BUCKET_NAME

class ModelPusher:

    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_trainer_artifact: ModelTrainerArtifact):
        """
         :param model_pusher_config: configuration for model_pusher
        """

        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifact = model_trainer_artifact

        self.gcloud = GCloudSync()

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
            Method Name: initiate_model_pusher
            Description: this method initiates model pusher
            Output:  Model Pusher artifact
        """
        logging.info("Entered Initiate_model_pusher method of ModelTrainier Class")
        try:
            self.gcloud.sync_folder_to_gcloud(gcp_bucket_url=TRAINING_BUCKET_NAME,
                                              filepath=self.model_trainer_artifact.trained_model_dir_path)
            
            logging.info("Uploaded best Model to google cloud")

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.BUCKET_NAME,
                gcloud_model_path=self.model_trainer_artifact.trained_model_dir_path
            )
            logging.info("Exited the initiate_model_pusher method of Modeltrainer Class")
            return model_pusher_artifact
        except Exception as e:
            raise transException(e, sys) from e