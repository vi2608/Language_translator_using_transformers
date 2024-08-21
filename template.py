import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files = [
    "components/data_ingestion.py",
    "components/data_transformation.py",
    "components/model_evaluation.py",
    "components/model_trainer.py",
    "components/model_pusher.py",
    "components/__init__.py",
    "constant/__init__.py",
    "cloud_storage/gcp_cloud.py",
    "entity/artifact_entity.py",
    "entity/__init__.py",
    "entity/config_entity.py",
    "pipeline/__init__.py",
    "pipeline/train_pipeline.py",
    "pipeline/__init__.py",
    "utils/main_utils.py",
    "exception/__init__.py",
    "logger/__init__.py",
    "ml/__init__.py",
    "setup.py",
    "test.py",
    "main.py",
    "requirements.txt",
    "research/trails.ipynb"
    ]

for filepath in list_of_files:
    filepath = Path(filepath)
    print(f"Filepath: {filepath}")
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating Director {filedir} for the file {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating file {filename}")
        
    else:
        logging.info(f"{filename} is already exists")
