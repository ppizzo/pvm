#!/bin/sh

#PORT=/dev/ttyUSB0
PORT=/dev/ttyACM0
DELAY=10

stty -F ${PORT} 1:0:cbd:0:3:1c:7f:8:4:5:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0
#stty -F ${PORT} 85:0:8bd:0:3:1c:7f:0:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0
#stty -F ${PORT} 1:0:8bd:0:0:0:0:0:0:3:1:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0

while :
do
    echo -e "#010\r" >${PORT}
    sleep $DELAY
done

#       1  2     3      4    5     6      7    8     9       10
#*010   4 389.7 10.48  4085 236.5 16.58  3922  46  20704 � SP4600
# 1 status
# 2 gen volt (generatore solare)
# 3 gen curr (generatore solare)
# 4 gen power (generatore solare)
# 5 grid voltage (rete)
# 6 grid current (rete)
# 7 delivered power (rete)
# 8 temp
# 9 daily yeld
# 10 inverter type

#      max od prod od  cont. prod*10  ore es. od  ore es. tot 
# *013  4117  20705   3848   3848      8:15    186:52    186:52
