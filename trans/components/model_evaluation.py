import os
import sys
from trans.exception import transException
from trans.logger import logging
from trans.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact, DataTransformationArtifact, DataIngestionArtifact
from trans.entity.config_entity import ModelEvaluationConfig
from trans.constant import GCLOUD_MODEL, TRAINING_BUCKET_NAME, LEARNING_RATE, WEIGHT_DECAY
from transformers import TFAutoModelForSeq2SeqLM, AdamWeightDecay
from trans.cloud_storage.gcp_cloud import GCloudSync

class ModelEvaluation:
    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_artifact: DataTransformationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact = data_transformation_artifact 
        except Exception as e:
            raise transException(e, sys) from e
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            model = TFAutoModelForSeq2SeqLM.from_pretrained(
                self.model_trainer_artifact.trained_model_dir_path
            )
            test_data = self.model_trainer_artifact.keras_native_test_data
            print(test_data)
            optimizer = AdamWeightDecay(learning_rate=LEARNING_RATE, weight_decay_rate=WEIGHT_DECAY)
            model.compile(optimizer=optimizer)
            loss = model.evaluate(test_data)
            print(loss)

            gcloud = GCloudSync()
            gcloud.sync_model_from_gcloud(gcp_bucket_url=TRAINING_BUCKET_NAME,
                                          folder=GCLOUD_MODEL,
                                          destination=GCLOUD_MODEL)
            cloud_model = TFAutoModelForSeq2SeqLM.from_pretrained(os.path.join(os.getcwd(), "trained_model"))
            cloud_optimizer = AdamWeightDecay(learning_rate=LEARNING_RATE, weight_decay_rate=WEIGHT_DECAY)
            cloud_model.compile(optimizer=cloud_optimizer)

            is_model_accepted = False
            cloud_loss = None

            if cloud_model is False:
                is_model_accepted = True
                print("Cloud model is false and model accepted is true")
                cloud_loss = None
            else:
                print("Entered inside the else condition")

                cloud_model = cloud_model.evaluate(test_data)

                print("model leaded from s3")
                cloud_loss - model.evaluate(test_data)

                if cloud_loss > loss:
                    print(f"printing the loss inside the if condition {cloud_loss} and {loss}")
                    is_model_accepted = True
                    print(f"{is_model_accepted}")

            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=is_model_accepted)
            print(f"{model_evaluation_artifact}")

            logging.info("exited the initiate_model_evaluation method of Model Evaluation Class")
            return model_evaluation_artifact
        except Exception as e:
            raise transException from e
