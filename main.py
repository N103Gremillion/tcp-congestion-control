# Name: Jacob Pace, Nathan Gremillion
# Date: Sep 27, 2025
# CSC 450-001 Projec 1
# TCP Tahoe Simulation
import csv
import random
from utils import * 
from typing import Iterator, List, TextIO


# def simulateReno(starting_index : int):
    
#     ssthresh = CWND_BEFORE_CONGESTION // 2

#     index : int = starting_index
    
#     while index < MAX_ROW:
#         index+=1
        
#     return

def simulateTahoe(starting_index : int):
    
    ssthreshold : int = CWND_BEFORE_CONGESTION // 2
    cwnd : int = MSS # starts at 1 for Tahoe
    cur_rtt : float = 0.1 # default at start
    
    total_bytes_to_send : int = get_bytes_sent_in_range(ROWS, starting_index, MAX_ROW - 1)
    total_MSS_to_send : int = bytes_to_MSS(total_bytes_to_send)
    
    mss_sent : int = 0
    bytes_in_flight : int = 0    
    index : int = starting_index
    phase : str = "SS"
    
    # first implement slow start phase
    while index < MAX_ROW and mss_sent < total_MSS_to_send:
        row : List[str] = ROWS[index]
        source : str = row[SOURCE_INDEX]
        
        if cwnd >= ssthreshold:
            phase = "CA"
                
        if source == CLIENT_IP:
            seq : int = parse_seq_from_info(row[INFO_INDEX])
            
            new_row = [
            row[NO_INDEX],
            row[TIME_INDEX],
            row[TCP_DELTA_INDEX],
            row[SOURCE_INDEX],
            row[DESTINATION_INDEX],
            row[TCP_SEG_LEN_INDEX],
            row[BYTES_IN_FLIGHT_INDEX],
            cwnd,
            row[INFO_INDEX],
            phase
            ]

            TAHOE_WRITER.writerow(new_row)
        else:
            if phase == "SS":
                cwnd += MSS
            else:
                cwnd += (MSS * MSS) // cwnd
            
            TAHOE_WRITER.writerow(row)
        index+=1
        
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