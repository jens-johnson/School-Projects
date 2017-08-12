"""
eqanalysis.py: analyze and plot earthquake data
Authors: Christopher Johnson
CIS 210 assignment 7, Fall 2016
"""

# a set of modules that we need to use in the code below
import math
import random
import argparse
from data import *
import turtle
import sys

# constants for the k-means clustering algorithm
# if you change these in your experimentation, you will need to look at 
# all parts of the code that refer to them, as there is some dependence
# on them (such as number of colors used in plotting clusters)
#
# IF YOU DO CHANGE THEM, YOU MUST PUT THEM BACK TO THE ORIGINAL VALUES
# BEFORE SUBMITTING YOUR WORK!!!!!
NO_OF_CLUSTERS = 6
NO_OF_ITERATIONS = 7

def euclid_distance(point1, point2):
    """
    computes the euclidean distance between two points
    Args:
        point1: list of floats, index 0 is longitude, index 1 is latitude
        point2: list of floats, index 0 is longitude, index 1 is latitude
    Returns:
        float, sqrt((x1-x2)**2 + (y1-y2)**2)
    """

    total = 0
    for index in range(2):
        diff = point1[index] - point2[index]
        total += diff * diff

    return math.sqrt(total)

def create_centroids(k, datadict):
    """
    randomly selects 'k' points from 'datadict' as the starting
        centroids for the k-means clustering algorithm
    Args:
        k: int, number of clusters desired
        datadict: list of lists, each contained list represents an EQ event
    Returns:
        list of lists, each contained list is an event to act as the centroid
    """
    centroids = []
    count = 0
    centroid_keys = []

    while count < k:
        rkey = random.randint(1, len(datadict))
        if rkey not in centroid_keys:
            centroids.append(datadict[rkey])
            centroid_keys.append(rkey)
            count += 1

    return centroids

def create_clusters(k, centroids, datadict, iterations):
    """
    k-means clustering algorithm - implementation taken from page 249 of
        ranum and miller text, with some modifications
    Args:
        k: integer, number of clusters
        centroids: list of events, each event is the centroid of its cluster
        datadict: dictionary of all EQ events
        iterations: int, number of clustering iterations to perform
    Returns:
        list of lists: each contained list is the set of indices into 'datadict'
           for events that belong to that cluster
    """
    for iteration in range(iterations):
        #print("****Iteration", iteration, "****")
        clusters = []
        for i in range(k):
            clusters.append([])

        for key in datadict:
            distances = []
            for cl_index in range(k):
                dist = euclid_distance(datadict[key], centroids[cl_index])
                distances.append(dist)
            min_dist = min(distances)
            index = distances.index(min_dist)
            clusters[index].append(key)

        dimensions = 2
        for cl_index in range(k):
            sums = [0]*dimensions
            for key in clusters[cl_index]:
                data_points = datadict[key]
                for ind in range(2):
                    sums[ind] = sums[ind] + data_points[ind]
            for ind in range(len(sums)):
                cl_len = len(clusters[cl_index])
                if cl_len != 0:
                    sums[ind] /= cl_len
            centroids[cl_index] = sums

        #for c in clusters:
            #print("CLUSTER")
            #for key in c:
                #print(datadict[key], end=" ")
            #print()

    return clusters

def read_file(filename):
    """
    read the EQ events from the csv file, 'filename'; any lines starting with
        # are skipped; the longitude, latitude, magnitude, and depth (in miles)
        is extracted from each event record, and stored as a list against its
        record number in a dictionary
    Args:
        filename: string, name of a CSV file containing the EQ data
    Returns:
        dictionary, indexed by integers, each value is a list of floats
            representing an EQ event
    """
    dict = {}
    key = 0

    fd = open(filename, "r")
    for line in fd:
        if line[0] == '#':
            continue		# causes the loop to grab another line
        key += 1
        values = line.rstrip('\n').split(',')
        lat = float(values[7])
        lon = float(values[8])
        mag = float(values[1])
        dep = float(values[10])
        dict[key] = [lon, lat, mag, dep]
    fd.close()
    return dict

# global data for map - if we had ;earmed about classes yet, this would have
# been hidden in a class instance, and the plot_*() functions would be methods
# on that class instance.  for now, these are global variables, and the
# plot functions access them

eq_turtle = None
eq_win = None
# these are the longitudes and latitudes for the Pacific NorthWest map that
# I have provided to you; do not change them!
left_lon = -128.608689
right_lon = -114.084764
top_lat = 51.248522
bot_lat = 38.584004
lon_diff = 0
lat_diff = 0
size_x = 0
size_y = 0
left_x = 0
bot_y = 0

def prepare_turtle():
    """
    Prepares the turtle and the window to plot magnitudes, depths, or clusters
    Args:
        None
    Outputs:
        creates turtle, sets window size, defines remainder of global
        data needed for plot_routines
    """
    global eq_turtle, eq_win
    global left_lon, right_lon, top_lat, bot_lat
    global lon_diff, lat_diff
    global size_x, size_y, left_x, bot_y

    eq_turtle = turtle.Turtle()
    eq_turtle.speed(10)
    eq_win = turtle.Screen()
    eq_win.screensize(655,808)	# number of pixels in the map I have provided
    lon_diff = right_lon - left_lon
    lat_diff = top_lat - bot_lat
    size_x = eq_win.screensize()[0]
    left_x = -size_x/2
    size_y = eq_win.screensize()[1]
    bot_y = -size_y/2
    eq_win.bgpic("PacificNW.gif")	# the map I have provided
    eq_turtle.hideturtle()
    eq_turtle.up()

def xy_calculate(lon, lat):
    """
    compute (x, y) given lon[gitude] and lat[itude]
    Args:
        lon: float, longitude value for point on map
        lat: float, latitude value for point on map
    Returns:
        tuple, corresponding pixel x and y values for use in turtle methods
    """
    global left_lon, right_lon, top_lat, bot_lat
    global lon_diff, lat_diff
    global size_x, size_y, left_x, bot_y

    x = left_x + (lon - left_lon) / lon_diff * size_x
    y = bot_y + (lat - bot_lat) / lat_diff * size_y
    return (x, y)

def plot_clusters(eq_clusters, eq_dict):
    """
    plot the clusters - use turtle.dot() at the appropriate location on the
        map for each event; use a different color for the events in each
        cluster - e.g. for cluster 0, use 'red', for 1, use 'violet' ...
    Args:
        eq_clusters: list of lists, each contained list has the indices for
                     events in that cluster in eq_dict
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        plots all events in a particular cluster as dots on the map
    """
    global eq_turtle
    ct = 0  #CJ 11/8: Initialize count to be iterated to change color for clusters
    my_colors = ["violet","blue","green","yellow","orange","red"] #CJ 11/8: List of colors for each of the different clusters
    for i in eq_clusters:
        tcolor = my_colors[ct] #CJ 11/8: Change color for dots for each of the different clusters
        ct += 1 #CJ 11/8: Iterate count for different clusters
        for j in i:
            val = eq_dict[j] #CJ 11/8: Grab the EQ data line containing [lon,lat,mag,dep]
            (lon,lat) = val[:2] #CJ 11/8: Grab the longitude and latitude from the EQ data for plotting
            (a,b) = xy_calculate(lon,lat) #CJ 11/8: Translate lon,lat data into turtle coordinates
            eq_turtle.goto(a,b) #CJ 11/8: Go to the lon,lat turtle positions
            eq_turtle.dot(tcolor) #CJ 11/8: Draw a dot at the position with the cluster color

def bin_value(value, bounds):
    """
    'bounds' defines a set of bins; this function returns the index of the
        first bin that contains 'value'
    Args:
        value: float, value to place in bin
        bounds: list of floats, bounds[i] is the top value of the bin
                code assumes that bounds is an increasing set of values
    Returns:
        integer, index of smallest value of bounds[] that is >= value
            if value > bounds[-1], returns len(bounds)
    """
    for i in range(len(bounds)):
        if value <= bounds[i]:
            return i
    return len(bounds)

def plot_magnitudes(eq_dict):
    """
    plot the magnitudes - use turtle.dot() at the appropriate location on the
        map for each event; use a different color and size for magnitude
        equivalence classes - e.g. if magnitude of event is <=1, use small dot
        that is 'violet', if between 1 and 2, use slightly larger dot that is
        'blue', ..., if between 9-10, use very large dot that is 'red'
    Args:
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        plots magnitude of all events as dots on the map
    """
    global eq_turtle
    mag_colors = ["violet","purple","DarkBlue","powder blue","light green","dark green","yellow","orange","red"] #CJ 11/9: List of colors for increasing magnitudes
    mag_sizes = [4,7,9,12,15,18,20,23,26,29,33] #CJ 11/9: List of dot sizes for increasing magnitudes
    mag_bounds = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0] #CJ 11/9: List of bounds for EQ magnitudes, upper-values for bin function
    for i in eq_dict:
        magset = eq_dict[i] #CJ 11/9: Grab the EQ line containing [lon,lat,mag,dep]
        magnitude = magset[2] #CJ 11/9: Grab the magnitude from EQ line data
        (lon,lat) = magset[:2] #CJ 11/9: Grab the longitude and latitude from EQ line data
        (a,b) = xy_calculate(lon,lat) #CJ 11/9: Translate lon,lat data into turtle coordinates
        eq_turtle.goto(a,b) #CJ 11/9: Go to the lon,lat turtle positions
        m_color = mag_colors[bin_value(magnitude,mag_bounds)] #CJ 11/9: Assigns appropriate magnitude color using bin_value function
        m_size = mag_sizes[bin_value(magnitude,mag_bounds)] #CJ 11/9: Assigns appropriate magnitude size using bin_value function
        eq_turtle.dot(m_size, m_color) #CJ 11/9: Plot a turtle dot of the appropriate color and size at the given lon,lat

def plot_depths(eq_dict):
    """
    plot the depths - use turtle.dot() at the appropriate location on the
        map for each event; use a different color and size for depth
        equivalence classes - e.g. if depth of event is <=1 mile, use a very
        large dot that is 'red', if between 1 and 5, use slightly smaller dot
        that is 'orange', ..., if between 50-100, use a small dot that is
        'violet'
    Args:
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        plots depth of all events as dots on the map
    """
    global eq_turtle
    mile_colors = ["red","dark orange","orange","yellow","green yellow","green","light green","powder blue","dark blue","purple","violet"] #CJ 11/9: List of colors for decreasing depths
    mile_sizes = [30,26,22,20,18,16,13,10,7,5,3] #CJ 11/9: List of dot sizes for decreasing depths
    mile_bounds = [1.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0] #CJ 11/9: List of bounds for EQ depths, upper-values for bin function
    for i in eq_dict:
        depset = eq_dict[i] #CJ 11/9: Grab the EQ line containing [lon,lat,mag,dep]
        depth = depset[3] #CJ 11/9: Grab the depth from EQ line data
        (lon,lat) = depset[:2] #CJ 11/9: Grab the longitude and latitude from EQ line data
        (a,b) = xy_calculate(lon,lat) #CJ 11/9: Translate lon,lat data into turtle coordinates
        eq_turtle.goto(a,b) #CJ 11/9: Go to the lon,lat turtle positions
        d_color = mile_colors[bin_value(depth,mile_bounds)] #CJ 11/9: Assigns appropriate depth color using bin_value function
        d_size = mile_sizes[bin_value(depth,mile_bounds)] #CJ 11/9: Assigns appropriate depth size using bin_value function
        eq_turtle.dot(d_size,d_color) #CJ 11/9: Plot a turtle dot of the appropriate color and size at the given lon,lat
    

def analyze_depths(eq_dict):
    """
    Perform statistical analysis on the depth information in the dictionary
    Args:
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        mean, median, and standard deviation of depth data
        frequency table for the depth data
    """
    depth_list = [] #CJ 11/10: Generate empty list of depths to be analyzed
    for i in eq_dict:
        adep = eq_dict[i]
        depth = adep[3]      #CJ 11/10: Add each depth value into the depth_list for statistical analysis
        depth_list.append(depth)
    depth_median = data_median(depth_list) #CJ 11/10: Calculate the median of all the depths
    (depth_mean, depth_variance) = data_mean_variance(depth_list) #CJ 11/10: Use data module to calculate the mean and variance of the depths
    depth_standdev = math.sqrt(depth_variance) #CJ 11/10: Calculate standard deviation by using the math module to take the square root of variance 
    print("Mean depth = {:.1f} miles".format(depth_mean)) 
    print("Median depth = {:.1f} miles".format(depth_median))
    print("Standard deviation = {:.2f} miles".format(depth_standdev))
    data_freq_table(depth_list) 

def analyze_magnitudes(eq_dict):
    """
    Perform statistical analysis on the magnitude information in the dictionary
    Args:
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        mean, median, and standard deviation of magnitude data
        frequency table for the magnitude data
    """
    mag_list = [] #CJ 11/10: Generate empty list of magnitudes to be analyzed
    for i in eq_dict:
        amag = eq_dict[i] 
        mag = amag[2]          #CJ 11/10: Add each magnitude value into the mag_list for statistical analysis
        mag_list.append(mag)
    mag_median = data_median(mag_list) #CJ 11/10: Calculate the median of all the magnitudes
    (mag_mean, mag_variance) = data_mean_variance(mag_list) #CJ 11/10: Use data module to calculate the mean and variance of the magnitudes
    mag_standdev = math.sqrt(mag_variance) #CJ 11/10: Calculate standard deviation by using the math module to take the square root of variance
    print("Mean magnitude = {:.1f}".format(mag_mean))
    print("Median magnitude = {:.1f}".format(mag_median))
    print("Standard deviation = {:.2f}".format(mag_standdev))
    data_freq_table(mag_list)
    

def analyze_clusters(eq_clusters, eq_dict):
    """
    Perform statistical analysis on the depth and magnitude information
        for each cluster
    Args:
        eq_clusters: list of lists, each contained list has the indices into
                     eq_dict for events in that cluster
        eq_dict: list of lists, each contained list represents an EQ event
    Outputs:
        for each cluster:
            mean, median, and standard deviation of magnitude data
            mean, median, and standard deviation of depth data
    """
    ct = 0   #CJ 11/10: Initialize count to indicate cluster names
    for i in eq_clusters:
        cluster_list_mag = []  #CJ 11/10: Create empty lists for each cluster to perform statistical analysis on magnitude and depth
        cluster_list_dep = []
        for j in i:
            cval = eq_dict[j]
            (mag, dep) = cval[2:]
            cluster_list_mag.append(mag)  #CJ 11/10: Append magnitude and depth data from each cluster to
            cluster_list_dep.append(dep)  #          their appropriate lists
        mag_median = data_median(cluster_list_mag) #CJ 11/10: Calculate magnitude median
        (mag_mean, mag_variance) = data_mean_variance(cluster_list_mag) #CJ 11/10: Calculate magnitude mean and variance
        mag_standdev = math.sqrt(mag_variance) #CJ 11/10: Calculate magnitude standard deviation by using the math module to take the square root of variance
        depth_median = data_median(cluster_list_dep) #CJ 11/10: Calculate depth median
        (depth_mean, depth_variance) = data_mean_variance(cluster_list_dep) #CJ 11/10: Calculate depth standard deviation by using the math module to take the square root of variance
        depth_standdev = math.sqrt(depth_variance) #CJ 11/10: Calculate depth standard deviation by using the math module to take the square root of variance
        print("Analysis of cluster {}".format(ct))
        print("  Analysis of magnitude data")
        print("    Mean magnitude = {:.1f}".format(mag_mean))
        print("    Median magnitude = {:.1f}".format(mag_median))
        print("    Standard deviation = {:.2f}".format(mag_standdev))
        print("  Analysis of depth data")
        print("    Mean depth = {:.1f} miles".format(depth_mean))
        print("    Median depth = {:.1f} miles".format(depth_median))
        print("    Standard deviation = {:.2f} miles".format(depth_standdev))
        print() #CJ 11/10: Added an extra print line to give space for readability
        ct += 1 #CJ 11/10: Iterate cluster count

def main():
    """
    Interaction if run from the command line.
    Usage:  python3 eqanalysis.py eq_data_file.csv command
    """
    parser = argparse.ArgumentParser(description="Earthquake event file stats")
    parser.add_argument('eq_file', type=str,
                 help='A csv file containing earthquake events, one per line.')
    parser.add_argument('command', type=str,
                 help='One of the following strings: plot analyze')
    parser.add_argument('what', type=str,
                 help='One of the following strings: clusters depths magnitudes')
    args = parser.parse_args()
    eq_file = args.eq_file
    cmd = args.command
    what = args.what
    if cmd != 'plot' and cmd != 'analyze':
        print('Illegal command: {}; must be "plot" or "analyze"'.format(cmd))
        sys.exit(1)
    if what != 'clusters' and what != 'magnitudes' and what != 'depths':
        print('Can only process clusters, magnitudes, or depths')
        sys.exit(1)
    eq_dict = read_file(eq_file)
    prepare_turtle()
    if what == 'clusters':
        eq_centroids = create_centroids(NO_OF_CLUSTERS, eq_dict)
        eq_clusters = create_clusters(NO_OF_CLUSTERS, eq_centroids, eq_dict, NO_OF_ITERATIONS)
    if cmd == 'plot':
        if what == 'clusters':
            plot_clusters(eq_clusters, eq_dict)
        elif what == 'magnitudes':
            plot_magnitudes(eq_dict)
        elif what == 'depths':
            plot_depths(eq_dict)
        print("ALL EVENTS HAVE BEEN PLOTTED")
        eq_win.exitonclick()
    else:
        if what == 'clusters':
            analyze_clusters(eq_clusters, eq_dict)
        elif what == 'magnitudes':
            analyze_magnitudes(eq_dict)
        elif what == 'depths':
            analyze_depths(eq_dict)

if __name__ == "__main__":
    main()
