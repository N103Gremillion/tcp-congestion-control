# indexes of each value when reading from the input csv
import csv
import math
from typing import Iterator, List, TextIO


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

# Note: RTT is only known when the server sends an ACK for a client segment.
# RTTS maps TCP sequence number -> RTT for that segment.
RTTS : dict[str, int] = {} 

def get_bytes_sent_in_range(rows : List[List[str]], start_row_index : int, end_row_index : int) -> int:
  start_row : List[str] = rows[start_row_index]
  end_row : List[str] = rows[end_row_index]
  
  # these should both be from the server but just in case
  if (start_row[SOURCE_INDEX] == SERVER_IP and end_row[SOURCE_INDEX] == SERVER_IP):
    start_ACK : int = parse_ack_from_info(start_row[INFO_INDEX])
    end_ACK : int = parse_ack_from_info(end_row[INFO_INDEX])
    return end_ACK - start_ACK
  
  return -1

def parse_seq_from_info(info : str) -> int:
  info_list : List[str] = info.split(" ")
  res : int = 0

  for entry in info_list:
    if entry[0:3] == "Seq":
      seq_info : List[str] = entry.split("=")
      res = int(seq_info[-1])

  return res

def parse_ack_from_info(info : str) -> int:
  info_list : List[str] = info.split(" ")
  res : int = 0
  
  for entry in info_list:
    if entry[0:3] == "Ack":
      ack_info : List[str] = entry.split("=")
      res = int(ack_info[-1])
  
  return res

def bytes_to_MSS(bytes : int) -> int:
  return math.ceil(bytes / MSS)

def MSS_to_bytes(mss : int) -> int:
  return mss * MSS
  
def compute_RTTS(rows : List[List[str]]) -> dict[str, int]:
  times_sent = {} # seq no. -> time sent
  rtts : dict[str, int] = {}
  
  for row in rows:
    source : str = row[SOURCE_INDEX]
    time_sent : float = float(row[TIME_INDEX])
    info : str = row[INFO_INDEX]
    
    if source == CLIENT_IP:
      seq = parse_seq_from_info(info)
      times_sent[seq] = time_sent
    elif source == SERVER_IP:
      ack = parse_ack_from_info(info)
      if ack in times_sent:
        rtts[ack] = time_sent - times_sent[ack]
          
  return rtts

RTTS = compute_RTTS(ROWS[1:]) # skip the header row
