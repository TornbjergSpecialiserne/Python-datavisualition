# Link to dataset
# https://www.kaggle.com/datasets/valakhorasani/electric-vehicle-charging-patterns

import matplotlib.pyplot as plt
import numpy as np
import re
import math
import pandas as pd
import csv

# Setup values
# Make timeslot for each hour
hourTimeSlots = {}    
for i in range(24):
    hourTimeSlots[i] = 0

# Car users
userTypes = {}


def RemoveDateFromString(input_string):
    # Regular expression pattern to match dates in YYYY-MM-DD format
    pattern = r'\d{4}-\d{2}-\d{2} '
    
    # Replace the matched date with an empty string
    return re.sub(pattern, '', input_string)

def TimeStringToTime(inputString):
    cleanString = RemoveDateFromString(inputString)
    hour = int(cleanString[0:2])
    minute = int(cleanString[3:5])

    return hour, minute

def TimeDiffentInMinuts(startTime, endTime):
    startHour, startMin = TimeStringToTime(startTime)
    endHour, endMin  = TimeStringToTime(endTime)
    # Hour calculation
    hourDiffent = endHour - startHour
    if(startHour > endHour):
        hourToMidnight = 24 - startHour
        hourDiffent = hourToMidnight + endHour

    # Hour overflow    
    if(endMin < startMin):
        endHour -= 1
        endMin += 60       
    
    minDiffent  = endMin - startMin    

    return (hourDiffent * 60) + minDiffent 

def GeneratorCSV():
    with open("ev_charging_patterns.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        
        for row in reader:
            yield row



try:
    first_row = True
    for row in GeneratorCSV():
        # How long do people charge there car
        reuslt = TimeDiffentInMinuts(row[5], row[6])
        targetHour = math.floor(reuslt / 60)
        if(targetHour in hourTimeSlots):
            hourTimeSlots[targetHour] += 1

        # what kind of travelor uses EVs
        driverType = row[19]
        if(driverType in userTypes):
            userTypes[driverType] += 1
        else:
            userTypes[driverType] = 1

        #Write placement
        with open("LocationData.csv", 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            if first_row:
                # Write header if it's the first row
                writer.writerow(["ID", "Location", "Cost"])
                first_row = False
            # Write the row
            writer.writerow([row[4], row[5], row[11]])

        
except FileNotFoundError:
    print("File not found")

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Make bar plot of hour charge
barCharingTime = list(hourTimeSlots.values())
barLabels = list(hourTimeSlots.keys())

# Plot the bar chart in the first subplot
ax1.bar(barLabels, barCharingTime, color='skyblue', edgecolor='black')
ax1.set_xlabel('Hours')
ax1.set_ylabel('Number of Uses')
ax1.set_title('Hourly Charging Patterns')
ax1.grid(True, linestyle='--', alpha=0.7)

# Make pie chart of user types
pieLavels = list(userTypes.keys())
pieHowManyUsers = list(userTypes.values())

# Plot the pie chart in the second subplot
ax2.pie(pieHowManyUsers, labels=pieLavels, autopct='%1.1f%%', startangle=90)

plt.tight_layout()
plt.show()