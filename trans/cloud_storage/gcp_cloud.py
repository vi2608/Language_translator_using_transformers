import os
import subprocess
from trans.logger import logging
from trans.exception import transException

class GCloudSync:
    @staticmethod
    def sync_folder_to_gcloud(gcp_bucket_url, filepath, filename):
        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        subprocess.run(command, shell=True, check=True)

    @staticmethod
    def sync_folder_from_gcloud(gcp_bucket_url, filename, destination):
        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        subprocess.run(command, shell=True, check=True)

    @staticmethod
    def sync_folder_from_gcloud_recursive(gcp_bucket_url, folder, destination, train, test, validation, jsonfile):
        dirs = [train, test, validation, jsonfile]
        for i in dirs:
            command = f"gsutil -m cp -r gs://{gcp_bucket_url}/{folder}/{i} {destination}"
            subprocess.run(command, shell=True, check=True)

    @staticmethod
    def sync_model_from_gcloud(gcp_bucket_url, folder, destination):
        os.makedirs(destination, exist_ok=True)
        files_to_download = ['config.json', 'tf_model.h5']
        
        for file in files_to_download:
            source = f"gs://{gcp_bucket_url}/{folder}/{file}"
            target = os.path.join(destination, file)
            command = f"gsutil cp {source} {target}"
            
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                logging.info(f"Successfully downloaded {file}: {result.stdout}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error downloading {file}: {e.stderr}")
                raise Exception(f"Error downloading {file}: {e.stderr}")
        
        logging.info(f"All files successfully downloaded to {destination}")
        
        # List the contents of the destination directory for verification
        logging.info(f"Contents of {destination}:")
        for file in os.listdir(destination):
            logging.info(f"- {file}")