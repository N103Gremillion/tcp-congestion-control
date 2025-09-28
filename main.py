# Name: Jacob Pace, Nathan Gremillion
# Date: Sep 27, 2025
# CSC 450-001 Projec 1
# TCP Tahoe Simulation
import csv
import random

# indexes of each value when reading from the input csv
NO_INDEX = 0
TIME_INDEX = 1
SOURCE_INDEX = 2
DESTINATION_INDEX = 3
BYTES_IN_FLIGHT_INDEX = 6
TCP_DELTA_INDEX = 7
TCP_SEG_LEN_INDEX = 8
CALCED_WINDOW_SIZE_INDEX = 9
INFO_INDEX = 10

# file constants
READ_FILE_NAME = "project1_data.csv"
READ_FILE = open(READ_FILE_NAME, "r") 
FILE_READER = csv.reader(READ_FILE)

RENO_FILE = open("Reno.csv", "w", newline='')
RENO_WRITER = csv.writer(RENO_FILE)

TAHOE_FILE = open("Tahoe.csv", "w", newline='')
TAHOE_WRITER = csv.writer(TAHOE_FILE)

# ips
CLIENT_IP = "192.168.10.184"
SERVER_IP = "192.168.10.196"

# others
ROWS = list(FILE_READER)
MAX_ROW = len(ROWS)

def simulateReno(starting_index):
    index = starting_index
    
    while index < MAX_ROW:
        index+=1
        
    return

def simulateTahoe(starting_index):
    index = starting_index

    while index < MAX_ROW:
        index+=1
    return 

    
### Open csv file, extract all rows, create new csv file and edit all rows from 3503 on ###
for i, row in enumerate(ROWS):
    if row[0] == "3503":
        simulateTahoe(i)
        simulateReno(i)
        break # INTEGERAL LINE, DO NOT REMOVE!!!
    else:
        RENO_WRITER.writerows(row)
        TAHOE_WRITER.writerows(row)
            
READ_FILE.close()
RENO_FILE.close()
TAHOE_FILE.close()