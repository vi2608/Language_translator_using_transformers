from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    ingested_data_raw_file_path: str

@dataclass
class DataTransformationArtifact:
    tokenized_datasets: str
    tokenized_train_dataset: 'Dataset'
    tokenized_test_dataset: 'Dataset'
    tokenized_validation_dataset: 'Dataset'

@dataclass
class ModelTrainerArtifact:
    trained_model_dir_path: str
    keras_native_test_data: 'tensorflow.python.data.ops.dataset_ops.PrefetchDataset'

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool

@dataclass
class ModelPusherArtifact:
    bucket_name: str
    gcloud_model_path: str