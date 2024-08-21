import sys
from trans.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataTransformationConfig, ModelTrainingConfig, ModelEvaluationConfig, ModelPusherConfig
from trans.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from trans.cloud_storage.gcp_cloud import GCloudSync
from trans.components.data_ingestion import DataIngestion
from trans.components.model_evaluation import ModelEvaluation
from trans.components.data_transformation import DataTransformation
from trans.components.model_trainer import ModelTrainer
from trans.components.model_pusher import ModelPusher
from trans.logger import logging
from trans.exception import transException

class TrainPipeline:
    is_pipeline_running = False
    
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = GCloudSync()

    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingesiton completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise transException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("starting data transformation")
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise transException(e, sys) from e
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact,
                             data_ingestion_artifact: DataIngestionArtifact) -> ModelTrainerArtifact:
        try:
            model_train_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("starting model training")
            model_training = ModelTrainer(
                model_trainer_config=model_train_config,
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_artifact=data_transformation_artifact
            )
            model_train_artifact = model_training.initiate_model_training()
            logging.info(f"Model training completed and artifact: {model_train_artifact}")
            return model_train_artifact
        except Exception as e:
            raise transException(e, sys) from e

    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               data_transformation_artifact: DataTransformationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact):
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config=model_eval_config,
                                         data_ingestion_artifact=data_ingestion_artifact,
                                         model_trainer_artifact=model_trainer_artifact,
                                         data_transformation_artifact=data_transformation_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except Exception as e:
            raise transException(e, sys) from e
    
    @staticmethod
    def start_model_pusher(model_trainer_artifact:ModelTrainingConfig):
        try:
            model_pusher_config = ModelPusherConfig()
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                       model_trainer_artifact=model_trainer_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise transException(e, sys) from e
        
        
    def run_pipeline(self):
        
        try:
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            model_trainer_artifact = self.start_model_training(data_ingestion_artifact=data_ingestion_artifact,
                                                               data_transformation_artifact=data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                              data_transformation_artifact=data_transformation_artifact,
                                                              model_trainer_artifact=model_trainer_artifact)
            if not model_eval_artifact.is_model_accepted:
                print("Trained Model is not better than the best model")
            else:
                model_pusher_artifact = self.start_model_pusher(model_trainer_artifact=model_trainer_artifact)
                print("Best model pushed to cloud")
                
        except Exception as e:
            raise transException(e, sys) from e