sudo tc qdisc del dev vnet1 root
#sudo tc qdisc add dev vnet0 root  netem delay $1ms  $2ms  distribution normal
sudo tc qdisc add dev vnet1 root  netem delay $1ms 
