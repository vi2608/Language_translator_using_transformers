import uvicorn
import sys
from trans.pipeline.train_pipeline import TrainPipeline
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from trans.ml.models.prediction import LangTranslator
from trans.exception import transException
from trans.logger import logging

text: str = "Translate the language to Hindi"

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        logging.info("Training pipeline is starting")
        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training Pipeline is already running")
        train_pipeline.run_pipeline()
        logging.info("Training pipeline completed")
        return Response("Training Successful")
    except Exception as e:
        raise transException(e, sys) from e
    
@app.post("/predict")
async def predict_route(text):
    try:
        logging.info("Prediction starting")
        obj = LangTranslator()
        generated_text = obj.prediction(text)
        logging.info("Prediction completed")
        return generated_text
    except Exception as e:
        raise transException(e, sys) from e
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)