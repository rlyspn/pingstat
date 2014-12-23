#!/usr/bin/python

from collections import Counter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys


def create_time_fig(in_file, out_file, title):
    x_arr = []
    min_y = []
    avg_y = []
    max_y = []
    with open(in_file ,'r') as dat:
        for line in dat:
            if len(line) > 0:
                line = line.rstrip()
                sp = line.split(' ')
                if len(sp) < 4:
                    continue
                x = int(sp[0])
                x_arr.append(x)
                min_y.append(float(sp[1]))
                avg_y.append(float(sp[2]))
                max_y.append(float(sp[3]))

    plt.xlabel("Time")
    plt.ylabel("RTT (ms)")
    plt.title(title)
    #plt.plot(x_arr, min_y, label="Min")
    plt.plot(x_arr, avg_y, label="Avg")
    #plt.plot(x_arr, max_y, label="Max")
    plt.legend(loc='upper left')
    plt.savefig(out_file)
    plt.clf()


def get_cdf(dat):
    x = []
    y = []
    curr = 0
    total = len(dat)
    counter = Counter(dat)

    for c in iter(sorted(counter.iteritems())):
        if c is None:
            continue
        curr += c[1]
        x.append(float(curr)/total)
        y.append(c[0])
    return (x, y)
        


def create_cdf_fig(in_file, out_file, title):
    min_y = []
    avg_y = []
    max_y = []
    with open(in_file ,'r') as dat:
        for line in dat:
            if len(line) > 0:
                sp = line.split(' ')
                if len(sp) < 4:
                    continue
                min_y.append(float(sp[1]))
                avg_y.append(float(sp[2]))
                max_y.append(float(sp[3]))
    min_x, min__y = get_cdf(min_y)
    avg_x, avg__y = get_cdf(avg_y)
    max_x, max__y = get_cdf(max_y)

    ax = plt.subplot(1, 1, 1)
    plt.plot(min_x, min__y, label="Min")
    plt.plot(avg_x, avg__y, label="Avg")
    plt.plot(max_x, max__y, label="Max")

    matplotlib.use('Agg')
    plt.legend(loc='upper left')

    plt.xlabel("Fraction")
    plt.ylabel("RTT (ms)")
    plt.title(title)
    plt.savefig(out_file)
    plt.clf()

def get_out_file(in_file):
    return in_file.split('.')[0] + ".png"


def get_title(in_file):
    return in_file.split('.')[0]

if len(sys.argv) != 3:
    print "Expected: ./generate_figures <in_file> <out_dir>"
    sys.exit(1)

in_file = sys.argv[1]
out_dir = sys.argv[2]
title = get_title(in_file)
time_file = "time_" + get_out_file(in_file)
cdf_file = "cdf_" + get_out_file(in_file)

create_time_fig(in_file, os.path.join(out_dir, time_file), title + " Average Ping Time")
create_cdf_fig(in_file, os.path.join(out_dir, cdf_file), title + " CDF")
