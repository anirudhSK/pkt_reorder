#! /usr/bin/python3
import random
import sys
from longest_increasing_subsequence import longest_increasing_subsequence

# constants
NUM_RECEIVERS = 2
NUM_PACKETS = 100000
MEAN_INTERSEND_TIME = float(sys.argv[1])
MEAN_DELAY = float(sys.argv[2])

# generate a Poisson process
pkt_send_times = []
current_time = 0
for j in range(0, NUM_PACKETS):
    current_time += random.expovariate(1.0/MEAN_INTERSEND_TIME)
    pkt_send_times += [current_time]

# Receive times for each receiver
pkt_receive_times = []
for i in range(0, NUM_RECEIVERS):
    # map from sequence number to its receive time
    pkt_receive_times += [dict()]

# Simulate random sender-receiver delays
for i in range(0, NUM_RECEIVERS):
    for j in range(0, NUM_PACKETS):
        pkt_receive_times[i][j] = pkt_send_times[j] + random.expovariate(1/MEAN_DELAY)

# Determine receive order at first receiver
receive_order_0 = [k for k, v in sorted(pkt_receive_times[0].items(), key = lambda item: item[1])]
receive_order_1 = [k for k, v in sorted(pkt_receive_times[1].items(), key = lambda item: item[1])]
## print("Receive order at rx 0")
## print(receive_order_0)
## print()
## 
## print("Receive order at rx 1")
## print(receive_order_1)
## print()

# Now, find order at second receiver, relative to the order at the first receiver.
# --> for every entry in receive_order,
# --> use the sequence number associated with the entry,
# --> to find when it was received at the other receiver.
# --> then sort by these receive times to determine order
seq_num_by_arrival_at_rx0=0
receive_times_1 = []
for seq_num in receive_order_0:
    receive_times_1 += [(seq_num_by_arrival_at_rx0, pkt_receive_times[1][seq_num])]
    seq_num_by_arrival_at_rx0+=1
inter_receiver_order = [seq_num_by_arrival_at_rx0 for seq_num_by_arrival_at_rx0, receive_time in sorted(receive_times_1, key = lambda item: item[1])]

## print("Receive order at rx1 based on seq numbers from rx at rx 0")
## print(inter_receiver_order)
## print()
## 

print("Reordering rate: ", 1 - len(longest_increasing_subsequence(inter_receiver_order))/NUM_PACKETS)
