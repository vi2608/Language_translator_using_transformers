import os
import sys
from trans.exception import transException
from trans.logger import logging
from trans.constant import GCLOUD_MODEL, MODEL_NAME, TRAINING_BUCKET_NAME
from transformers import TFAutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from trans.cloud_storage.gcp_cloud import GCloudSync


class LangTranslator:
    def __init__(self):
        pass

    @staticmethod
    def fetch_model_from_gcloud():
        try:
            logging.info("Downloading Model from glcloud")
            os.makedirs(GCLOUD_MODEL, exist_ok=True)
            gcloud = GCloudSync()
            gcloud.sync_model_from_gcloud(gcp_bucket_url=TRAINING_BUCKET_NAME,
                                          folder="tf_model",
                                          destination=GCLOUD_MODEL)
            logging.info("Model Downlaoding COmpleted")
            print(os.path.join(os.getcwd(), "gcloud_model/gcloud_model"))
            #return os.path.join(os.getcwd(), GCLOUD_MODEL)
            return GCLOUD_MODEL
        except Exception as e:
            raise transException(e, sys) from e
        
    def prediction(self, text):
        try:
            logging.info("starting prediction")
            model = TFAutoModelForSeq2SeqLM.from_pretrained(self.fetch_model_from_gcloud())
            tokenizer =  AutoTokenizer.from_pretrained(MODEL_NAME)
            tokenized = tokenizer([text], return_tensors='np')
            out = model.generate(**tokenized, max_length=128)
            with tokenizer.as_target_tokenizer():
                prediction = tokenizer.decode(out[0], skip_special_tokens=True)
                logging.info("prediction completed")
                return prediction
        
        except Exception as e:
            raise transException(e, sys) from e