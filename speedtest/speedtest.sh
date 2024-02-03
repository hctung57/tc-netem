#!/bin/bash
iperf3 -c 3.26.150.18 -f m > upload.log
uploadBW=$(cat upload.log | head -n 16 | tail -n 1| awk '{print $7}')
iperf3 -c 3.26.150.18 -f m -R > download.log
downloadBW=$(cat download.log | head -n 17 | tail -n 1| awk '{print $7}')
last_two_lines=$(echo "$result" | tail -n 2)
ping -c 10 3.26.150.18 > ping.log
pingData=$(cat ping.log | tail -n 1| awk '{print $4}')
IFS='/' read -r _ rtt_avg _ rtt_mdev <<< "$pingData"
echo $(date "+%Y-%m-%d %H:%M:%S"),$rtt_avg,$rtt_mdev,$downloadBW,$uploadBW >> result.csv
