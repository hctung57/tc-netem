import os
import time
import csv
import sys



########## CONFIG HERE ##########
SLEEP = 1
MASTER_INF="vnet3"
CLOUD_INF="vnet0"
EDGE_INF="vnet1"
#################################

os.system(f'tc qdisc del dev {MASTER_INF} root')
os.system(f'tc qdisc del dev {CLOUD_INF} root')
os.system(f'tc qdisc del dev {EDGE_INF} root')



os.system(f"tc qdisc add dev {EDGE_INF} root handle 1: htb default 10")
os.system(f"tc class add dev {EDGE_INF} parent 1: classid 1:1 htb rate 1mbit")
os.system(f"tc qdisc add dev {EDGE_INF} parent 1:1 handle 10: netem delay 138ms 5ms distribution normal")
os.system(f"tc filter add dev {EDGE_INF} parent 1: protocol all prio 1 u32 match u32 0 0 flowid 1:1")

os.system(f"tc qdisc add dev {MASTER_INF} root handle 1: htb default 10")
os.system(f"tc class add dev {MASTER_INF} parent 1: classid 1:1 htb rate 1mbit")
os.system(f"tc filter add dev {MASTER_INF} protocol ip parent 1:0 prio 2 u32 match ip src 192.168.122.59/32 flowid 1:1")

os.system(f"tc qdisc add dev {CLOUD_INF} root handle 1: htb default 10")
os.system(f"tc class add dev {CLOUD_INF} parent 1: classid 1:1 htb rate 1mbit")
os.system(f"tc filter add dev {CLOUD_INF} protocol ip parent 1:0 prio 2 u32 match ip src 192.168.122.59/32 flowid 1:1")


while True:
    with open('result.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count +=1
                time.sleep(SLEEP)
                continue
            download = float(row[3])
            upload = float(row[4])
            print(f"Simulated network parameter: {line_count}, download: {download}mbit, upload:{upload}mbit")
            
            os.system(f"tc class change dev {EDGE_INF} parent 1: classid 1:1 htb rate {upload}mbit")

            os.system(f"tc class change dev {CLOUD_INF} parent 1: classid 1:1 htb rate {download}mbit")

            os.system(f"tc class change dev {MASTER_INF} parent 1: classid 1:1 htb rate {download}mbit")

            line_count += 1
            time.sleep(SLEEP)
