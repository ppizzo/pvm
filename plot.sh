#!/bin/sh

gnuplot <<EOF
set title "FV 2012/07/14"
set autoscale
set xdata time
set timefmt "%H:%M:%S"
set yrange [0:5000]
set y2range [0:90]
set xrange ["06:00:00":"22:00:00"]
set xtics 3600 nomirror rotate by -45
set ytics 500 nomirror
set y2tics 5
set grid xtics, ytics

set bmargin 3
set rmargin 5

set terminal png size 1000, 500
set output "fv-2012-07-14.png"

plot "fv-2012-07-14.plot" using 1:7 title "Grid power" with lines axis x1y1, \
"fv-2012-07-14.plot" using 1:8 title "Temperature" with lines axis x1y2
EOF