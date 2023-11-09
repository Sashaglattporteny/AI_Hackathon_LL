# Load the environment variables from the .env file
from dotenv import load_dotenv
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from pathlib import Path
from typing import Dict

env_path = Path('path to ATT85165.env')
load_dotenv(dotenv_path=env_path)

key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"
client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))


def pdf_text(file_path: str) -> str:
    # Images PDF with text
    with open(file_path, 'rb') as f:
        # Async SDK call that "reads" the image
        poller = client.begin_analyze_document(
            model_id="prebuilt-read", document=f)
        result = poller.result()
        print('Waiting for result...')

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
