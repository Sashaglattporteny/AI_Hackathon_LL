import time
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from pathlib import Path
from typing import Dict

'''
Authenticate
'''


key = os.getenv('Azure_Computer_Vision_key')
endpoint = os.getenv('Azure_End_point')

# Set credentials
credentials = CognitiveServicesCredentials(key)
# Create client
client = ComputerVisionClient(endpoint, credentials)


def pdf_text(file_path):
    # Images PDF with text
    filepath = open(
        file_path, 'rb')

    # Async SDK call that "reads" the image
    response = client.read_in_stream(filepath, raw=True)

    # Don't forget to close the file
    filepath.close()

    # Get ID from returned headers
    operation_location = response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # SDK call that gets what is read
    while True:
        result = client.get_read_result(operation_id)
        if result.status.lower() not in ['notstarted', 'running']:
            break
        print('Waiting for result...')
        time.sleep(10)
    return result


def texts_from_pdf(data_directory: Path) -> Dict[str, str]:
    texts = {}
    for file in os.listdir(data_directory):
        if file.lower().endswith('.pdf'):
            file_path = os.path.join(data_directory, file)

            # logging
            print(f"Processing file: {file}")
            extracted_text = pdf_text(file_path)
            # add the extracted text to the dictionary
            texts[file] = extracted_text
            print(f"Extraction completed for {file}")

    print("All files processed.")
    return texts
