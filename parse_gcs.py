#!/usr/bin/python

import sys
import os
import json
import re
import collections
import operator

# Check arguments
# (note 2 includes arg 0 which is this script!)
if len(sys.argv) != 3:
    print "\n***",sys.argv[0], "***\n"
    print 'Incorrect number of arguments, please run script as follows:'
    print '\n'+str(sys.argv[0])+' <directory> <file>'
    sys.exit(0)

# Setup local variables
path = sys.argv[1]
pattern = sys.argv[2]
result = collections.OrderedDict()
gc_cms_raw = { }
gc_cms = { }
gc_parnew = { }
gc_g1 = { }

# Change your output file names here
g1_out = 'g1.out'
parnew_out = 'parnew.out'
cms_out = 'cms.out'

# parse for CMS
def parse_cms(filename):
    keyspace = 'none'
    table = 'none'
    property = 'none'
    propertyval = 'none'
    file = open(filename, 'r')
    for line in file:
       message = ".*GCInspector.*ConcurrentMarkSweep.*"
       matched = re.match ( message, line, re.M)
       if matched:
           split1 = line.replace(' ms','ms').split(']')
           split2 = split1[1].split('ms')
           split3 = split2[0].split(' ')
           gc_date = split3[1]
           gc_time = split3[2]
           gc_ms = split3[len(split3)-1]
           gc_datetime = gc_date + ' ' + gc_time
           gc_cms[gc_datetime] = gc_ms

# parse for ParNew
def parse_parnew(filename):
    keyspace = 'none'
    table = 'none'
    property = 'none'
    propertyval = 'none'
    file = open(filename, 'r')
    for line in file:
       message = ".*GCInspector.*ParNew.*"
       matched = re.match ( message, line, re.M)
       if matched:
           split1 = line.replace(' ms','ms').split(']')
           split2 = split1[1].split('ms')
           split3 = split2[0].split(' ')
           gc_date = split3[1]
           gc_time = split3[2]
           gc_ms = split3[len(split3)-1]
           gc_datetime = gc_date + ' ' + gc_time
           gc_parnew[gc_datetime] = gc_ms

# parse for G1
def parse_g1(filename):
    keyspace = 'none'
    table = 'none'
    property = 'none'
    propertyval = 'none'
    file = open(filename, 'r')
    for line in file:
       message = ".*GCInspector.*G1.*"
       matched = re.match ( message, line, re.M)
       if matched:
           split1 = line.replace(' ms','ms').split(']')
           split2 = split1[1].split('ms')
           split3 = split2[0].split(' ')
           gc_date = split3[1]
           gc_time = split3[2]
           gc_ms = split3[len(split3)-1]
           gc_datetime = gc_date + ' ' + gc_time
           gc_g1[gc_datetime] = gc_ms

# write out files
def writeOutput(outfile, gc_values):
    with open(outfile, 'w') as out_file:
        for datetime, gc in gc_values.iteritems():
            line = datetime + ' ' +gc + '\n'
            out_file.write(line)
    out_file.close

# Use os.walk to find all the directories under the path
# if the files match the search pattern, then perform the parse
for dirname, dirnames, filenames in os.walk(path):
    for file in filenames:
        matched = re.match( pattern, file, re.M)
        if matched:
            # carry out parse
            parse_cms(dirname + '/' + file)
            parse_parnew(dirname + '/' +file)
            parse_g1(dirname + '/' + file)

# Once all files have been parsed then write
# all the values out into data files ready for
# graph plotting
writeOutput(g1_out, gc_g1)
writeOutput(parnew_out, gc_parnew)
writeOutput(cms_out, gc_cms)

