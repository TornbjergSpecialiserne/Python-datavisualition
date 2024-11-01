# Link to dataset
# https://www.kaggle.com/datasets/valakhorasani/electric-vehicle-charging-patterns

import matplotlib.pyplot as plt
import numpy as np
import re
import math
import pandas as pd

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



# Setup values
# Make timeslot for each hour
hourTimeSlots = {}    
for i in range(24):
    hourTimeSlots[i] = 0

try:
    # Open data file
    df = pd.read_csv("ev_charging_patterns.csv")

    # Skip header row
    df = df.iloc[1:]

    # Calculate charging time in minutes
    myHourCal = df.apply(lambda row: TimeDiffentInMinuts(row['Charging Start Time'], row['Charging End Time']), axis=1).tolist()

    

    for val in myHourCal:
        # Distribute results
        targetHour = math.floor(val / 60)
        if(targetHour in hourTimeSlots):
            hourTimeSlots[targetHour] += 1
except FileNotFoundError:
    print("File not found")



charingTime = list(hourTimeSlots.values())
labels = list(hourTimeSlots.keys())

# Make bar plot of hour charge
plt.figure(figsize=(12, 8))
plt.bar(labels, charingTime, color='skyblue', edgecolor='black')
plt.xlabel('Hours')
plt.ylabel('Number of Uses')
plt.title('Hourly Charging Patterns')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()