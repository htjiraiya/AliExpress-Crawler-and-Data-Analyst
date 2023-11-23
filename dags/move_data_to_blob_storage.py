from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv


def upload_to_blob(products_json_path, blob_name):
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    CONTAINER_NAME = os.getenv('CONTAINER_NAME')

    # Init BlobServiceClient with connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING)

    # Get BlobClient
    blob_client = blob_service_client.get_blob_client(
        CONTAINER_NAME, blob=blob_name)

    # open and read file
    with open(products_json_path, 'r') as file:
        data = file.read()

    # upload data
    blob_client.upload_blob(data)


def main():
    load_dotenv()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, 'data')
    file = os.listdir(data_dir)[-1]
    products_json_path = os.path.join(parent_dir, 'data', file)
    blob_name = 'products.json'
    upload_to_blob(products_json_path, blob_name)


if __name__ == '__main__':
    main()
