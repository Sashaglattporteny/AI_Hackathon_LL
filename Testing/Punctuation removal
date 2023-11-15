#remove punctuation signs
for sign in [".",",",":",";","-"]:
    lines = lines.replace(sign, "")
#Remove en of line
lines = lines.replace("\n"," ")
#Lowercase 
lines = lines.lower()
#Tokenize text
words = lines.split(" ")
#Get vocab
vocab =set(words)

#Count number of words in the text
result = []
for word in vocab:
    wcount = words.count(word)
    result.append((wcount,word))
print(result)
