#!/bin/sh
#
# Plot daily details graph
#
# 2012, Pietro Pizzo <pietro.pizzo@gmail.com>
######################################################################

cd `dirname $0`

# Read configuration file
eval $(cat config |grep output_dir)
eval $(cat config |grep daily_details_plot_file)
data_file=$daily_details_plot_file

# Parameters check
if [ $# -eq 1 ]; then
    date_ref=$1
elif [ $# -eq 0 ]; then
    date_ref=$(date +"%Y-%m-%d")
else
    echo "Usage: `basename $0` [yyyy-mm-dd]" >&2
    exit 1
fi

# Other checks
if [ ! -d $output_dir ]; then
    echo "Output directory not found. Exiting." >&2
    exit 2
fi

# Create plot data file
rm -f $data_file
python3 <<EOF
import plot
plot.plot_daily_details("${date_ref}")
EOF

cd $output_dir

# Check if the datafile has been created
if [ ! -r $data_file ]; then
    echo "Datafile not found. Exiting." >&2
    exit 2
fi
if [ ! -s $data_file ]; then
    echo "Empty datafile. Exiting." >&2
    rm -f $data_file
    exit 3
fi

# Plot data
gnuplot <<EOF
set title "${date_ref}"
set autoscale
set xdata time
set timefmt "%H:%M:%S"
set yrange [0:5000]
set y2range [0:90]
set xrange ["05:00:00":"22:00:00"]
set xtics 3600 nomirror rotate by -45
set ytics 500 nomirror
set y2tics 5
set grid xtics ytics

set bmargin 3
set rmargin 5
set pointsize 0.1

set terminal png size 1400, 600
set output "pvm-${date_ref}-daily_details.png"

plot "${data_file}" using 2:9 title "Grid power" with lines axis x1y1, \
"${data_file}" using 2:10 title "Temperature" with lines axis x1y2
EOF

# Clean up
rm -f $data_file
