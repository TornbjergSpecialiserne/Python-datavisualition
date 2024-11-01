# Link to dataset
# https://www.kaggle.com/datasets/valakhorasani/electric-vehicle-charging-patterns

import matplotlib.pyplot as plt
import numpy as np
import csv
import re
import logging
import math

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

def ConvertToMinuts(hour, minute):
    return (hour * 60) + minute

def TimeDiffentInMinuts(startTime, endTime):
    cal_start_hour, cal_start_min = TimeStringToTime(startTime)
    cal_end_hour, cal_end_min  = TimeStringToTime(endTime)
    # Hour calculation
    cal_dif_hour = cal_end_hour - cal_start_hour
    if(cal_start_hour > cal_end_hour):
        hourToMidnight = 24 - cal_start_hour
        cal_dif_hour = hourToMidnight + cal_end_hour

    # Hour overflow    
    if(cal_end_min < cal_start_min):
        cal_end_hour -= 1
        cal_end_min += 60       
    
    cal_dif_min  = cal_end_min - cal_start_min
    

    return ConvertToMinuts(cal_dif_hour, cal_dif_min)    

# Make timeslot for each hour
hourTimeSlots = {}    
for i in range(24):
    hourTimeSlots[i] = 0


#Open data file
with open("ev_charging_patterns.csv", "r") as csv_file:
    #Skip header line
    next(csv_file)

    csv_reader = csv.reader(csv_file)
    

    # See what languages 
    for line in csv_reader:
        charingTime = TimeDiffentInMinuts(line[5], line[6])

        # Check for worng calculation / input
        if(charingTime < 0):
            logging.debug(f"Input was {line[5]} & {line[6]} with result {charingTime}")
            continue
        
        # Distribute results
        targetHour = math.floor(charingTime / 60)
        if(targetHour in hourTimeSlots):
            hourTimeSlots[targetHour] += 1
        

# Make bar plot of hour charge
# Data
labels = list(hourTimeSlots.keys())
values = list(hourTimeSlots.values())

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color='skyblue', edgecolor='black')

# Customize the chart
plt.xlabel('Hours')
plt.ylabel('Uses')
plt.title('Hour charges')
plt.grid(True, linestyle='--', alpha=0.7)

# Show the chart
plt.tight_layout()
plt.show()