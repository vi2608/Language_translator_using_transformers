"""
application constants
""" 

import os 

APP_HOST = "0.0.0.0"
APP_PORT = 8080

"""
Google cloud storage constants
"""

TRAINING_BUCKET_NAME = "lang-translation-bucket"
GCLOUD_MODEL = "gcloud_model"

"""
----Training Pipeline Contants----
"""

PIPELINE_NAME: str = "lang-translation-egenie"
ARTIFACT_DIR: str = "artifacts"
MODEL_NAME: str = "Helsinki-NLP/opus-mt-en-hi"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: str = os.path.join('config', 'schema.yaml')
BLOCK_SIZE: int = 128
DATASET_FOLDER: str = "dataset"
TRAIN: str = "train"
TEST: str = "test"
VALIDATION: str = "validation"
JSON_FILE: str = "dataset_dict.json"

"""
Data ingestion constants
"""

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_RAW_DIR_NAME: str = "raw_dataset"

"""
Data Transformation Constants
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMERS_TOKENIZER_SAVE_DIR: str = "tokenizer"
TOKENIZED_DATASET_DIR_NAME: str = "tokenized_dataset"
TOKENIZED_TRAIN_DATASET_DIR_NAME: str = "tokenized_train_dataset"
TOKENIZED_TEST_DATASET_DIR_NAME: str = "tokenized_test_dataset"
TOKENIZED_VALIDATION_DATASET_DIR_NAME: str = "tokenized_validation_dataset"

MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128
SOURCE_LANG = "en"
TARGET_LANG = "hin"

"""
Model Trainer constant
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "saved_models"
KERAS_NATIVE_TEST_DATA: str = "kerasNativeTestData"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.3


BATCH_SIZE = 16
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
NUM_TRAIN_EPOCHS = 1


"""
Model Evalaution Constant
"""
MODEL_EVALUATION_REPORT_NAME: str = "evaluation_report"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float =  0.02
MODEL_EVALUATION_DIR_NAME : str = "model_evaluation"
