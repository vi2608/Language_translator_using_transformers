import os
from datetime import datetime
from trans import constant

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name : str = constant.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(constant.ARTIFACT_DIR, timestamp)


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, constant.DATA_INGESTION_DIR_NAME)
        self.data_ingestion_raw_file_path: str = os.path.join(self.data_ingestion_dir, constant.DATA_INGESTION_RAW_DIR_NAME)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, constant.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, constant.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, constant.TRAIN_FILE_NAME)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, constant.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, constant.TEST_FILE_NAME)
        self.tokenizer_file_path: str = os.path.join(self.data_transformation_dir, constant.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, constant.DATA_TRANSFORMERS_TOKENIZER_SAVE_DIR)
        self.tokenized_dataset_file_path: str = os.path.join(self.data_transformation_dir, constant.TOKENIZED_DATASET_DIR_NAME)
        self.tokenized_train_dataset_file_path: str = os.path.join(self.data_transformation_dir, constant.TOKENIZED_TRAIN_DATASET_DIR_NAME)
        self.tokenized_test_dataset_file_path: str = os.path.join(self.data_transformation_dir, constant.TOKENIZED_TEST_DATASET_DIR_NAME)
        self.tokenized_validation_dataset_file_path: str = os.path.join(self.data_transformation_dir, constant.TOKENIZED_VALIDATION_DATASET_DIR_NAME)

class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, constant.MODEL_TRAINER_DIR_NAME)
        self.trained_model_dir_path: str = os.path.join(self.model_trainer_dir, constant.MODEL_TRAINER_TRAINED_MODEL_DIR)
        self.expected_accuracy: float = constant.MODEL_TRAINER_EXPECTED_SCORE
        self.keras_native_test_data_filepath: str = os.path.join(self.model_trainer_dir, constant.KERAS_NATIVE_TEST_DATA)

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, constant.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path: str = os.path.join(self.model_evaluation_dir, constant.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = constant.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
    def __init__(self):
        self.BUCKET_NAME: str = constant.TRAINING_BUCKET_NAME