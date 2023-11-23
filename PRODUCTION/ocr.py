from dotenv import load_dotenv
import os
import re
from pathlib import Path
from typing import Dict
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from nltk.tokenize import word_tokenize

# Ensure nltk 'punkt' package is downloaded
# import nltk
# nltk.download('punkt', quiet=True)

# Load the environment variables from the .env file

env_path = Path(
    '/Users/lucazosso/Desktop/IE_Course/Hackathon/production/ATT85165.env')
load_dotenv(dotenv_path=env_path)

# Normalization and tokenization functions


def normalize_text(text: str) -> str:
    text = text.lower()  # Convert to lower case
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text


def tokenize_text(text: str) -> list:
    tokens = word_tokenize(text)
    return tokens


# Azure Form Recognizer Client Setup
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
endpoint = "https://ocr-ie-hackathon.cognitiveservices.azure.com/"
azure_client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))


def pdf_text(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        poller = azure_client.begin_analyze_document(
            model_id="prebuilt-read", document=f, pages="1-5")
        result = poller.result()
        print('Waiting for result...')

        extracted_text = " ".join(
            [line.content for page in result.pages for line in page.lines])
        normalized_text = normalize_text(extracted_text)
        tokens = tokenize_text(normalized_text)
        return ' '.join(tokens)


def texts_from_pdf(data_directory: Path) -> Dict[str, str]:
    texts = {}
    for file in os.listdir(data_directory):
        if file.lower().endswith('.pdf'):
            file_path = os.path.join(data_directory, file)
            print(f"Processing file: {file}")
            extracted_text = pdf_text(file_path)
            texts[file] = extracted_text
            print(f"Extraction completed for {file}")

    print("All files processed.")
    return texts
