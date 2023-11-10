from openai import OpenAI
import os

#API key stored locally -> aiming to push it into the dotenv soon...
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

print("environement is build")


# Getting text files from pdf previously created with OCR

# for pre-production purposes, upload from local file without going through OCR process
with open("/Users/lucazosso/Desktop/IE_Course/Hackathon/Looping_Legends/extracted/XS2021832634_extracted.txt", "r") as file:
    term_sheet_test = file.read()

# Fields to target


financial_product_terms = {
    "ISIN": "International Securities Identification Number",
    "Issuer": "The entity or organization that issues the financial product",
    "Ccy": "The currency in which the financial product is denominated or traded",
    "Underlying(s)": "The assets, indices, or securities on which the financial product's performance is based, for example: GLE, RNO FP,VOW3 GY, DAI GY. it is sometimes called bloomberg code/identifier",
    "Strike": "The strike price of the underlying and not the barrier. It must be a number and must not contain any letters. It is a financial number so it will have decimals. You can also calculate it by taking the knock-in barrier price divided by barrier level, and it cannot be 100% of Initial Level ",
    "Launch Date": "The date when the financial product is officially issued and made available for investment or trading",
    "Final Valuation Day": "The date on which the final valuation of the financial product is made",
    "Maturity": "The date on which the financial product is set to expire or mature",
    "Cap": "An upper limit on potential returns for the financial product",
    "Barrier": "A specific level or threshold that, if reached, can trigger certain events or determine the product's performance"
}

# There is a unique value for each Underlying so if there are multiple underlyings there will be multiple strike prices.
elements_to_extract_value_from = financial_product_terms.keys()

# Prompting


prompt = f'''
I want you to act as a data extraction specialist in the finance industry with special knowledge in financial term sheet.
Your task is to go through this text file {term_sheet_test} and extract the value of the corresponding key elements listed here {elements_to_extract_value_from}.
I have also included in this file {financial_product_terms} the meaning of each element to help you in your extraction.
Please keep in mind that if multiple underlyings are present then each underlying has its unique strick price.
As a result please provide a dictionary as an output format (key: value(s)).

'''

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {
            "role": "user",
            "content": f"{prompt}",
        },
    ],
)
print(completion.choices[0].message.content)

-- Version 2 

prompt= f''''
You are the best financial data analyst in the world with special expertise on term sheets. 
Your task is to go through this text file {term_sheet_test} and extract the value of the corresponding key elements listed here {elements_to_extract_value_from}. You can use {prompting_category} as context to find the values. You need to deliver a dictionary as an output format (key: value(s)). 
You must always follow the Rule and avoid what is stated in the Restriction.
'''

prompting_category = {
    "ISIN": {
        "Rule": "International Securities Identification Number from the term sheet. The ISIN is a 12-character alphanumeric code that uniquely identifies the bond for accurate tracking and trading. Look for the word 'ISIN' in close proximity, and ensure that the extracted string is exactly 12 characters. It can also be a CUSIP number of 9 characters.",
        "Restriction": "It can't be a float."
    },
    "Issuer": {
        "Rule": "The entity or organization that issues the financial product. Identify and extract the issuer's name (both full name and initials) from the term sheet. In the provided data, examples include RBC, BNP, Citi, MS, and GS.",
        "Restriction": "It can't be a number."
    },
    "Ccy": {
        "Rule": "Extract the currency mentioned in the term sheet. The currency in which the financial product is denominated or traded. Check that the currency exists in a specified list; currency can look like: EUR, USD in the provided data. They can be multiple.",
        "Restriction": "It can't be a number."
    },
    "Underlying(s)": {
        "Rule": "The assets, indices, or securities on which the financial product's performance is based, for example: GLE, RNO FP, VOW3 GY, DAI GY. It can also be called bloomberg code/identifier. Keep in mind that if multiple underlyings are present then each underlying has its unique strike price.",
        "Restriction": "It can't be a number"
    },
    "Strike": {
        "Rule": "The strike price of the underlying and not the barrier. It comes as a percentaje attached to automatic early redemption. You can also calculate it by taking the (knock-in barrier price / by barrier level). It can also be called ETI Initial.",
        "Restriction": "It can't be 100%, It can't contain letters."
    },
    "Launch Date": {
        "Rule": "Find and extract the launch date (Trade Date) from the term sheet. The launch date marks the initiation of the bond. Provide it in the format dd/mm/yyyy and verify its accuracy.",
        "Restriction": "It can't be in another format that is not dd/mm/yyyy "
    },
    "Final Valuation Day": {
        "Rule": "Identify and extract the final valuation day from the term sheet. The final valuation day is crucial for determining the bond's concluding value. Provide it in the format dd/mm/yyyy and ensure precision.",
        "Restriction": "It can't be in another format that is not dd/mm/yyyy "
    },
    "Maturity": {
        "Rule": "Extract the maturity date from the term sheet. The maturity date signifies when the bond reaches maturity. Provide it in the format dd/mm/yyyy and verify its accuracy.",
        "Restriction": "It can't be in another format that is not dd/mm/yyyy"
    },
    "Cap": {
        "Rule": "Find and extract the cap value mentioned in the term sheet. The cap value influences the maximum value of a variable and impacts the bond's potential returns. Confirm the accuracy of the cap values and check for associated conditions.",
        "Restriction": "It can't be a number or a letter"
    },
    "Barrier": {
        "Rule": "The barrier is a percentage. It is a specific level or threshold that, if reached, can trigger certain events or determine the product's performance. Look for the word 'Barrier' in close proximity.",
        "Restriction": "It can't be a number that is not a percentage."
    }
}

