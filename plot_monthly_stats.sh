#!/bin/sh
#
# Plot monthly stats graph
#
# 2012, Pietro Pizzo <pietro.pizzo@gmail.com>
######################################################################

cd `dirname $0`

# Read configuration file
eval $(cat config |grep output_dir)
eval $(cat config |grep monthly_stats_plot_file)
data_file=$monthly_stats_plot_file

# Parameters check
if [ $# -eq 1 ]; then
    date_ref=$1
elif [ $# -eq 0 ]; then
    date_ref=$(date +"%Y-%m")
else
    echo "Usage: `basename $0` [yyyy-mm]" >&2
    exit 1
fi

# Other checks
if [ ! -d $output_dir ]; then
    echo "Output directory not found. Exiting." >&2
    exit 2
fi

# Calculate xrange
date_start=$(date +"%Y-%m-%d" -d "${date_ref}-01 -1 day")
date_end=$(date +"%Y-%m-%d" -d "${date_ref}-01 +1 month")

# Create plot data file
rm -f $data_file
python3 <<EOF
import plot
import db
db.clean_daily_totals()
plot.plot_monthly_stats("${date_ref}")
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
set timefmt "%Y-%m-%d"
set format x "%d"
set yrange [0:35000]
set xrange ["${date_start}":"${date_end}"]
#set xtics 86400 nomirror rotate by -45
set xtics 86400 nomirror
unset mxtics
set ytics 5000 nomirror
set grid xtics ytics

set bmargin 3
set rmargin 5
set pointsize 0.1

set terminal png size 1400, 600
set output "pvm-${date_ref}-monthly_stats.png"

set style fill solid
set boxwidth 0.5 relative
set style line 1 lw 4 lc 3

plot "${data_file}" using 2:3 title "Daily production" with boxes, \
"${data_file}" using 2:4 title "Reference production" with lines linestyle 1

EOF

# Clean up
rm -f $data_file
