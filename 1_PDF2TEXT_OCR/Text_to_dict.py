def create_line_dictionary(file_path):
    line_dictionary = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file, start=1):
            line_dictionary[idx] = line.strip()

    return line_dictionary

# Replace 'your_text_file.txt' with the actual path to your .txt file.
text_file_path = 'XS2021832634_extracted.txt'

# Create the dictionary
line_dict = create_line_dictionary(text_file_path)

# Example: Print the first 10 lines
for idx in line_dict:
    print(f"Line {idx}: {line_dict.get(idx, 'Not available')}")



