# Name: Jacob Pace
# Date: Sep 27, 2025
# CSC 450-001 Projec 1
# TCP Tahoe Simulation

import csv
import random

def simulate():
    # Defining used variables
    num = 3503
    time = 4.417981

    sender = "192.168.10.184"
    reciever = "192.168.10.196"

    # Used when sending the ACK packet from the reciever
    sending = True

    # TCP Algorithm State: SS = Slow Start, CA = Collision Avoidance
    state = ""

    # Variables to track ammount of sent packets to "force" an ACK packet
    transmits = 0
    ackThresh = 0

    # Slow Start Threshold
    ssthresh = 262144//2

    # Used when formatting output for respective packets
    senPacket = "52343  >  5201[BoundErrorUnreassembled Packet]"
    ackPacket = "5201  >  52343 [ACK] Seq=1 Ack=10766642 Win=212992 Len=0"

    # Tracker variables for segment length
    tcpSegLen = 1460
    currLen = 1460

    # track the packets that are in flight 
    rtt = 0.105 # secondes
    # these are {"size" : , "send_time" : }
    packets_in_flight = [] 

    newRow = ["--No.--", "--Time--","--Src--","--Dest--", "--Length--", "--Protocol--", "--Sequence Num--", "--TCP Seg Len--", "--ACK--", "--Window Size--", "--Bytes in Flight--", "--Info--", "--State--"]   

    while num < 8848:
        
        packets_to_ack = []

        bytes_in_flight = 0
        for packet in packets_in_flight:
            bytes_in_flight += packet["size"]

        if currLen >= ssthresh:
            # State = Collision Avoidance "CA"
            state = "CA"
            currLen = currLen + tcpSegLen

            if transmits == 0:
                ackThresh = currLen//tcpSegLen
                sending = True
                transmits+=1
            elif transmits < ackThresh:
                sending = True
                transmits+=1
            elif transmits == ackThresh:
                sending = False
                transmits = 0
                
        ### Both the Slow Start and Collision Avoidance logic is the same, they just utilize different incremental
        ### methods for the ACK packet simulation
        ###
        ### If there have been no transmits or the transmit tracker just reset, make a new ACK Threshold
        ### so that an ACK packet has to be sent after so many transmit packets defined by the ACK Threshold,
        ### and simulate a sender packet
        ###
        ### If the number of transmits is less than the ACK Threshold, increment transmit and simulate a sender packet
        ###
        ### If the ACK Threshold is met, simulate an ACK packet and reset the transmit tracker
        else:
            #State = Slow Start "SS"
            state = "SS"

            if transmits == 0:
                ackThresh = currLen//tcpSegLen
                sending = True
                transmits+=1
            elif transmits < ackThresh:
                sending = True
                transmits+=1
            elif transmits == ackThresh:
                sending = False
                transmits = 0
                currLen*=2

        # Increment num and time
        num+=1
        time+= random.uniform(0.0, 0.001)
        
        # check if any of the packets in flight have been in flight for longer than an RTT
        for packet in packets_in_flight:
            if (time - packet["send_time"] >= rtt):
                packets_to_ack.append(packet)

        # Remove acked packets from flight
        for packet in packets_to_ack:
            packets_in_flight.remove(packet)
            bytes_in_flight -= packet["size"]

        # Format output here
        if sending == True and bytes_in_flight + tcpSegLen <= currLen:
            packets_in_flight.append({"size": tcpSegLen, "send_time": time})
            newRow = [str(num), str(time), sender, reciever, "--Length--", "iPerf3", "--TCP Delta--", "--Seqence Number--",  "1460", "--ACK--", str(currLen), str(bytes_in_flight), senPacket, state]  
        elif sending == False: 
            newRow = [str(num), str(time), reciever, sender, "--Length--", "TCP", "--TCP Delta--", "--Seqence Number--",  "0", "--ACK--", str(currLen), str(bytes_in_flight), ackPacket, state]
        formatRow = [newRow]
        writer.writerows(formatRow)

    # Final Packet
    num+=1
    time+= random.uniform(0.0, 0.001)
    newRow = [str(num), str(time), reciever, sender, "--Length--", "TCP", "--TCP Delta--", "--Seqence Number--",  "--Tcp Segment Length--", "--ACK--", str(currLen), "--Bytes in Flight--", "5201  >  52343 [RST, ACK] Seq=1 Ack=11671842 Win=0 Len=0", "CA"]
    formatRow = [newRow]
    writer.writerows(formatRow)
    
### Open csv file, extract all rows, create new csv file and edit all rows from 3503 on ###
output = open("Tahoe.csv", "w", newline='')
writer = csv.writer(output)
with open("Project1DataV2.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == "3503":
            simulate()
            break # INTEGERAL LINE, DO NOT REMOVE!!!
        else:
            rowOfRows = [row]
            writer.writerows(rowOfRows)