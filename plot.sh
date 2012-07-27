#!/bin/sh

gnuplot <<EOF
set title "FV 2012/07/26"
set autoscale
set xdata time
set timefmt "%H:%M:%S"
set yrange [0:5000]
set y2range [0:90]
set xrange ["05:00:00":"22:00:00"]
set xtics 3600 nomirror rotate by -45
set ytics 500 nomirror
set y2tics 5
set grid xtics, ytics

set bmargin 3
set rmargin 5

set terminal png size 1400, 600
set output "fv-2012-07-26.png"

plot "data.plot" using 2:9 title "Grid power" with lines axis x1y1, \
"data.plot" using 2:10 title "Temperature" with lines axis x1y2
EOF
