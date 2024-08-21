# Language Translator Using Transformers

This project implements a language translation system using FastAPI and Hugging Face's Transformers library. It provides an API for training a translation model and making predictions.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Train a language translation model
- Make predictions using the trained model
- Fallback to pre-trained model if custom model is unavailable
- Google Cloud Storage integration for model storage

## Prerequisites

- Python 3.9+
- Google Cloud SDK (for GCloud integration)
- FastAPI
- Uvicorn
- Transformers
- TensorFlow

## Installation

1. Clone the repository:
git clone https://github.com/vi2608/Language_translator_using_transformers.git
cd Language_translator_using_transformers

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install the required packages:
pip install -r requirements.txt

4. Set up Google Cloud SDK and authenticate (if using GCloud features).

## Project Structure
Language_translator_using_transformers/
├── trans/
│   ├── cloud_storage/
│   │   └── gcp_cloud.py
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_evaluation.py
│   │   ├── model_pusher.py
│   │   └── model_trainer.py
│   ├── constant/
│   │   └── init.py
│   ├── entity/
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   ├── exception/
│   │   └── init.py
│   ├── logger/
│   │   └── init.py
│   ├── ml/
│   │   └── models/
│   │       └── prediction.py
│   └── pipeline/
│       └── train_pipeline.py
├── config/
│   └── schema.yaml
├── main.py
├── requirements.txt
└── README.md

## Usage

1. Start the FastAPI server:
python main.py

2. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `GET /`: Redirects to the API documentation
- `GET /train`: Initiates the model training pipeline
- `POST /predict`: Makes a translation prediction

## Configuration

The project uses various configuration constants defined in `trans/constant/__init__.py`. Modify these as needed for your specific use case.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

