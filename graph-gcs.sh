#!/bin/bash
#
# gc puase time grapher
# points will start at field $3 for ms
# the micro seconds are ignored
#
# 2015-08-11 22:20:18,399 203
# 2015-08-11 22:39:07,316 221
# 2015-08-11 18:53:40,785 212
# 2015-08-11 15:31:42,993 207
# 2015-08-11 23:51:02,186 206

if [ $# -ne 2 ];then
	echo "Plot graphs for GC values"
	echo ""
	echo "Useage: $0 <gc_values_file> <output_file>"
	echo ""
	echo "The output file will be a .png format showing"
	echo "a graph of the GC pause times for the data"
	exit 1
fi

echo "procesing $1 for GCs, plotting $2"

cat $1 > dat.dat

gnuplot <<_EOF_
set boxwidth 500 # use fixed width bars
set style fill solid 1.0 # solid fill
set key off # in this case we dont need the legend
set terminal png
set output "$2"
set title "jvm GC pauses from file: $1"
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H:%M\n%d/%m"
set xtics nomirror scale 3,2
set ylabel "miliseconds"
set samples 10
# the plot values are arranged like 1:2:3
# where each represent a solumn 
# 1. col1 for date and time
# 2. col2 for the data
# 3. col3 for the colour
plot "dat.dat" using 1:3:3 with boxes palette title "jvm GC pauses in ms" 
_EOF_

rm dat.dat
