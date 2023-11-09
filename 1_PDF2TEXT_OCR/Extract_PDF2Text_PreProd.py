import time
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

'''
Authenticate
'''
key = '296addcde7bb4b7f904fc731b6dd8dd1'
endpoint = 'https://llocrpdftextextraction.cognitiveservices.azure.com/'

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

# pdf directory setup


pdf_directory = '/Users/lucazosso/Desktop/IE_Course/Hackathon/Looping_Legends/pdf_folders'
parent_directory = os.path.dirname(pdf_directory)
extracted_directory = os.path.join(parent_directory, "extracted")

# Create the 'extracted' directory if it does not exist
if not os.path.exists(extracted_directory):
    os.makedirs(extracted_directory)

for file in os.listdir(pdf_directory):
    if file.lower().endswith('.pdf'):
        file_path = os.path.join(pdf_directory, file)

        # logging
        print(f"Processing file: {file}")

        result = pdf_text(file_path)
        # Write the results to a file
        result_file_name = f"{os.path.splitext(file)[0]}_extracted.txt"
        result_file_path = os.path.join(extracted_directory, result_file_name)

        with open(result_file_path, 'w') as result_file:
            if result.status == OperationStatusCodes.succeeded:
                for readResult in result.analyze_result.read_results:
                    for line in readResult.lines:
                        result_file.write(line.text + "\n")
                    result_file.write("\n")

        print(f"Extraction completed for {
              file} and text has been written to {result_file_path}")

print("All files processed.")
