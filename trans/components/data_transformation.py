import sys
from trans.entity.config_entity import DataTransformationConfig
from trans.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from trans.exception import transException
from trans.logger import logging
from trans.constant import MODEL_NAME, MAX_INPUT_LENGTH, MAX_TARGET_LENGTH, SOURCE_LANG, TARGET_LANG
from transformers import AutoTokenizer
from datasets import load_from_disk

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
            :param data_ingestion_artifact: Output reference of data ingestion artifact stage
            :param data_transformation_config: configuration for data transformation
        """

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise transException(e, sys) from e

    @staticmethod
    def dataset_preprocess(dataset):
        logging.info("start data preprocessing")
        inputs = [row.get(SOURCE_LANG, '') for row in dataset['translation']]
        targets = [row.get(TARGET_LANG, '') for row in dataset['translation']]

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model_inputs = tokenizer(inputs, max_length=MAX_INPUT_LENGTH, truncation=True)

        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, max_length=MAX_TARGET_LENGTH, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs  
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Start data transformation stage")

            datasets = load_from_disk(self.data_ingestion_artifact.ingested_data_raw_file_path)

            tokenized_datasets = datasets.map(self.dataset_preprocess, batched=True)

            tokenized_datasets.save_to_disk(self.data_transformation_config.tokenized_dataset_file_path)

            tokenized_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
            tokenized_train_dataset.save_to_disk(self.data_transformation_config.tokenized_train_dataset_file_path)

            tokenized_validation_dataset = tokenized_datasets["validation"].shuffle(seed=42).select(range(1000))
            tokenized_validation_dataset.save_to_disk(self.data_transformation_config.tokenized_validation_dataset_file_path)

            tokenized_test_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))
            tokenized_test_dataset.save_to_disk(self.data_transformation_config.tokenized_test_dataset_file_path)

            data_transformation_artifact = DataTransformationArtifact(tokenized_datasets=tokenized_datasets,
                                                                      tokenized_train_dataset=tokenized_train_dataset,
                                                                      tokenized_validation_dataset=tokenized_validation_dataset,
                                                                      tokenized_test_dataset=tokenized_test_dataset)
            return data_transformation_artifact
        except Exception as e:
            raise transException(e, sys) from e
