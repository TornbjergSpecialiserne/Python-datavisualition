import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
import csv

codeLanguage = {}
dataPoints = 0

#Open data file
with open("Task Catagories.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    # Get number of lines
    dataPoints = csv_reader.line_num

    # See what languages 
    for line in csv_reader:
        if(line[2] in codeLanguage):
            codeLanguage[line[2]] += 1
        else:
            codeLanguage[line[2]] = 1


# Test for seeing results
# for key, value in codeLanguage.items():
#     print(f"{key}: {value}")

# Remove langues only few people use 
userThreshold = 4
# Add other categori
codeLanguage["Other"] = 0
for index, (key, value) in enumerate(reversed(list(codeLanguage.items()))):
    if(key == "Other"):
        continue

    if value < userThreshold:
        codeLanguage["Other"] += value
        del codeLanguage[key]
        
pieLabels = list(codeLanguage.keys())
pieSize = list(codeLanguage.values())        



# # Load CSV file
# df = pd.read_csv('Task Catagories.csv')

# # Display the first few rows
# print(df.head())

# plt.pie(pieSize, labels=pieLabels, autopct='%1.1f%%')
# plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.title('Language Distribution')
# plt.show()

# Extract keys and values from the dictionary
languages = list(codeLanguage.keys())
counts = list(codeLanguage.values())

# Create scatter plot
plt.figure(figsize=(12, 8))
for i, (lang, count) in enumerate(zip(languages, counts)):
    plt.scatter(i, count, s=200, alpha=0.8, label=lang)

plt.xlabel('Language Index')
plt.ylabel('Count')
plt.title('Language Distribution')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()