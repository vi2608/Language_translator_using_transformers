import os
import sys
import tensorflow as tf
from trans.entity.config_entity import ModelTrainingConfig
from trans.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelTrainerArtifact
from trans.logger import logging
from trans.exception import transException
from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, AutoTokenizer, AdamWeightDecay
from trans.constant import MODEL_NAME, BATCH_SIZE, LEARNING_RATE, WEIGHT_DECAY

class ModelTrainer:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainingConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise transException(e, sys)
    
    def train_model(self, tokenized_train_dataset, tokenized_validation_dataset):
        try:
            logging.info("Starting model training phase")

            model = TFAutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

            data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf")

            train_dataset = model.prepare_tf_dataset(
                tokenized_train_dataset,
                batch_size=BATCH_SIZE,
                shuffle=True,
                collate_fn=data_collator
            )

            validation_dataset = model.prepare_tf_dataset(
                tokenized_validation_dataset,
                batch_size=BATCH_SIZE,
                shuffle=False,
                collate_fn=data_collator
            )

            optimizer = AdamWeightDecay(learning_rate=LEARNING_RATE, weight_decay_rate=WEIGHT_DECAY)
            model.compile(optimizer=optimizer)

            history = model.fit(train_dataset, validation_data=validation_dataset, epochs=1)
            
            return model, history
        except Exception as e:
            raise transException(e, sys) from e
    
    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            logging.info("Starting model training stage")

            tokenized_train_dataset = self.data_transformation_artifact.tokenized_train_dataset
            tokenized_validation_dataset = self.data_transformation_artifact.tokenized_validation_dataset
            tokenized_test_dataset = self.data_transformation_artifact.tokenized_test_dataset

            trained_model, history = self.train_model(tokenized_train_dataset=tokenized_train_dataset, 
                                                      tokenized_validation_dataset=tokenized_validation_dataset)
            
            model_save_dir = self.model_trainer_config.trained_model_dir_path
            os.makedirs(model_save_dir, exist_ok=True)
            trained_model.save_pretrained(model_save_dir)

            keras_native_test_data = self.test_keras_dataset(tokenized_test_dataset=tokenized_test_dataset)

            os.makedirs(self.model_trainer_config.keras_native_test_data_filepath, exist_ok=True)
            tf.data.Dataset.save(keras_native_test_data, path=self.model_trainer_config.keras_native_test_data_filepath)

            model_train_artifact = ModelTrainerArtifact(trained_model_dir_path=model_save_dir,
                                                        keras_native_test_data=keras_native_test_data)
            return model_train_artifact
        except Exception as e:
            raise transException(e, sys) from e

    def test_keras_dataset(self, tokenized_test_dataset):
        try:
            model = TFAutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf")

            logging.info("Converting tokenized test dataset into keras native format")

            keras_test_dataset = model.prepare_tf_dataset(
                tokenized_test_dataset,
                batch_size=BATCH_SIZE,
                shuffle=False,
                collate_fn=data_collator
            )
            return keras_test_dataset
        except Exception as e:
            raise transException(e, sys) from e