# Define the text
text = """[Your multiline text here]""" * 10  # Replace [Your multiline text here] with your actual text

# Split the text into lines
lines = text.split('\n')

# Function to split text into chunks of a specified number of lines
def split_text_into_chunks(lines, chunk_size):
    for i in range(0, len(lines), chunk_size):
        yield '\n'.join(lines[i:i+chunk_size])

# Splitting the text every 30 lines
chunk_size = 30
chunks = list(split_text_into_chunks(lines, chunk_size))

# Print the first chunk as a sample
print(chunks[0])

#def run_model_on_chunk(chunk):
    """
    Placeholder function for running the DeBERTa model on a text chunk.
    Replace this with your actual model function and return the percentage.
    """
    # Replace this with your model code
    # For demonstration, it returns a random percentage between 0 and 100
    import random
    return random.uniform(0, 100)

# Assuming 'chunks_dict' is your dictionary with the text chunks

relevant_chunks = {}

for key, chunk in chunks_dict.items():
    percentage = run_model_on_chunk(chunk)
    if percentage > 20:
        relevant_chunks[key] = chunk

# Now, let's save the relevant chunks to a Python file
with open('extraction.py', 'w') as file:
    file.write("extracted_chunks = {}\n".format(relevant_chunks))

