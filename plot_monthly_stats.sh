#!/bin/sh
#
# PVM PhotoVoltaic Monitor
#
# Plot monthly stats graph.
#
# Copyright (C) 2012 Pietro Pizzo <pietro.pizzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

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

# Create dirs
dest_dir=$(echo $date_ref |cut -c 1-7 |tr '-' '/')
mkdir -p ${output_dir}/$dest_dir

# Calculate xrange
date_start=$(date +"%Y-%m-%d" -d "${date_ref}-01 -1 day")
date_end=$(date +"%Y-%m-%d" -d "${date_ref}-01 +1 month")

# Create plot data file
rm -f $data_file
python3 <<EOF
import plot
plot.plot_monthly_stats("${date_ref}")
EOF

cd $output_dir

# Check if the datafile has been created
if [ ! -r $data_file ]; then
    echo "Datafile not found. Exiting." >&2
    exit 3
fi
if [ ! -s $data_file ]; then
    echo "Empty datafile. Exiting."
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
set output "${dest_dir}/pvm-${date_ref}-monthly_stats.png"

set style fill solid
set boxwidth 0.5 relative
set style line 1 lw 4

plot "${data_file}" using 2:3 title "Daily production (W)" with boxes lt rgb "red", \
"${data_file}" using 2:4 title "Reference production (W)" with lines linestyle 1 lt rgb "blue"

EOF

# Clean up
rm -f $data_file
