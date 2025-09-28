# Name: Jacob Pace, Nathan Gremillion
# Date: Sep 27, 2025
# CSC 450-001 Projec 1
# TCP Tahoe Simulation
import csv
import random
from typing import Iterator, List, TextIO

# indexes of each value when reading from the input csv
NO_INDEX : int = 0
TIME_INDEX : int = 1
SOURCE_INDEX : int = 2
DESTINATION_INDEX : int = 3
BYTES_IN_FLIGHT_INDEX : int = 6
TCP_DELTA_INDEX : int = 7
TCP_SEG_LEN_INDEX : int = 8
CALCED_WINDOW_SIZE_INDEX : int = 9
INFO_INDEX : int = 10
PHASE_INDEX : int = 11

# file constants
READ_FILE_NAME : str = "input-data.csv"
READ_FILE : TextIO = open(READ_FILE_NAME, "r") 
FILE_READER : Iterator[List[str]] = csv.reader(READ_FILE)

RENO_FILE : TextIO = open("reno.csv", "w", newline='')
RENO_WRITER : csv.writer = csv.writer(RENO_FILE)

TAHOE_FILE : TextIO = open("tahoe.csv", "w", newline='')
TAHOE_WRITER : csv.writer = csv.writer(TAHOE_FILE)

# ips
CLIENT_IP : str = "192.168.10.184"
SERVER_IP : str = "192.168.10.196"

# others
ROWS : List[List[str]] = list(FILE_READER)
MAX_ROW : int = len(ROWS)

MSS : int = 1460
CWND_BEFORE_CONGESTION : int = 262144 # I pulled this off the trace file

# def simulateReno(starting_index : int):
    
#     ssthresh = CWND_BEFORE_CONGESTION // 2

#     index : int = starting_index
    
#     while index < MAX_ROW:
#         index+=1
        
#     return

def simulateTahoe(starting_index : int):
    ssthreshold : int = CWND_BEFORE_CONGESTION // 2
    cwnd : int = MSS # starts at 1 for Tahoe
    time: float = float(ROWS[starting_index][TIME_INDEX])
    index : int = starting_index
    phase : str = "SS"
    
    # first implement slow start phase
    while index < MAX_ROW:
        row : List[str] = ROWS[index]
        
        # Decide phase
        if cwnd >= ssthreshold:
            phase = "CA"
        index+=1
        
        if phase == "SS":
            cwnd += MSS
        else:
            cwnd += MSS * MSS // cwnd
        
        new_row = [
        row[NO_INDEX],
        row[TIME_INDEX],
        row[TCP_DELTA_INDEX],
        row[SOURCE_INDEX],
        row[DESTINATION_INDEX],
        row[TCP_SEG_LEN_INDEX],
        row[BYTES_IN_FLIGHT_INDEX],
        row[CALCED_WINDOW_SIZE_INDEX],
        row[INFO_INDEX],
        phase
        ]
        
        TAHOE_WRITER.writerow(new_row)
            
    return 

# add the phase column
ROWS[0].append("Phase") 
for row in ROWS[1:]:
    row.append("---")
    
### Open csv file, extract all rows, create new csv file and edit all rows from 3503 on ###
for i, row in enumerate(ROWS):
    
    new_row : List[str] = [
        row[NO_INDEX],
        row[TIME_INDEX],
        row[TCP_DELTA_INDEX],
        row[SOURCE_INDEX],
        row[DESTINATION_INDEX],
        row[TCP_SEG_LEN_INDEX],
        row[BYTES_IN_FLIGHT_INDEX],
        row[CALCED_WINDOW_SIZE_INDEX],
        row[INFO_INDEX],
        row[PHASE_INDEX]
    ]
    
    if row[0] == "3503":
        simulateTahoe(i)
        # simulateReno(i)
        break # INTEGERAL LINE, DO NOT REMOVE!!!
    else:
        RENO_WRITER.writerow(new_row)
        TAHOE_WRITER.writerow(new_row)
            
READ_FILE.close()
RENO_FILE.close()
TAHOE_FILE.close()