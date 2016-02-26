# Graph GCInspector

A simple how to for graphing the GCInspector pause times from Cassandra logs. The output of iostat is useful but its also nice if you can get it into a graph. The idea of this small repository is to show how this is done.

## Overview

This repository is simply two scripts; one that parses a set of logs and outputs some data in a given format and one that parses the resulting data and draws some nice graphs. As most of my other repos, this one could probably be very easily improved.

There's a few things that will need to be setup beforehand though, see below for details on this. Note this was all tested on MacOS. It _should_ work just fine on Linux, it's probably not going to work on MS Windows, sorry!

Its best to use this to run against a set of logs *one node at a time* since the output will not distinguish which node the GC pause times are from

## Setup

You'll need to install the following:

gnuplot

## MacOS users

If you're running this on a MAC you'll need to install homebrew first:

### Install brew

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Install GNU Plot

brew install gnuplot

## Creating the data

Gather your logs into seperate directories if you can (this will make things easier). Theres no need to run any "greps" to parse stuff out. The script should pull out all the info it needs.

Run the script with the base directory your logs are in and the file name (the name uses a simple regex match) for example:

```
./parse_GCs.py ~/Unwell_Cluster1/logs/node1 system.log
```

You'll generate 3 files like so:

```
-rw-r--r--   1 mark  staff       0 26 Feb 13:45 parnew.out
-rw-r--r--   1 mark  staff    6328 26 Feb 13:45 g1.out
-rw-r--r--   1 mark  staff       0 26 Feb 13:45 cms.out
```

In this example the logs only had G1 events so we only have output in the `g1.out` file. (Note the output names are set in the script but you cna change them eaisly if you like)

The content of the file should look something like this:

```
2015-08-11 17:21:35,996 329
2015-08-11 22:56:14,478 230
2015-08-11 22:28:20,205 201
```

It won't necessarily be in order depending on what files you have but this will not matter. when it's plotted the order will naturally sort on the graph

## Creating the graphs

This is done by running the next script. Simply give the input data file name and the output file name:

```
$ ./graph-gcs.sh g1.out JVM_g1.png
procesing g1.out for GCs, plotting JVM_g1.png
```

![alt example](https://github.com/markcurtis1970/graph-gcinspector/blob/master/example.png)
