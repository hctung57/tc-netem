#!/bin/bash
for i in {1..500}; do
    echo "Speed test times: $i"
    ./speedtest.sh
    sleep 30
done
