import pandas as pd
import numpy as np

from timeit import default_timer as timer

from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """ Calculate the great-circle distance between two points on the Earth surface.
    Takes 4 numbers, containing the latitude and longitude of each point in decimal degrees.

    The default returned unit is kilometers.
    """
    # mean earth radius - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
    avg_earth_radius = 6371.0 # 6371.0088

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    # calculate haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    d = sin(dlat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(dlon * 0.5) ** 2
    c = 2.0 * avg_earth_radius
    return c  * asin(sqrt(d))

# Idea 3: Convert this function into a function that takes a single array of
# lat and a single vector of lon (length N) and returns a matrix N x N with all
# pairwise distances.
def haversine_np(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between paired arrays representing
    points on the earth (specified in decimal degrees)

    All args must be numpy arrays of equal length.

    Returns an array of distances for each pair of input points.

    """
    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    # calculate haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    d = np.sin(dlat * 0.5)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon * 0.5)**2
    c = 2.0 * 6371.0
    return c * np.arcsin(np.sqrt(d))

def weighted_trip_length(stops_latitude, stops_longitud, weights):
    north_pole = (90,0)
    sleigh_weight = 10
    dist = 0.0
    # Start at the north pole with the sleigh full of gifts.
    prev_lat, prev_lon = north_pole
    prev_weight = np.sum(weights) + sleigh_weight
    for lat, lon, weight in zip(stops_latitude, stops_longitud, weights):
        # Idea 1: Calculating the distances between the points repeatedly is
        # slow. Calculate all distances once into a matrix, then use that
        # matrix here.
        dist += haversine(lat, lon, prev_lat, prev_lon) * prev_weight
        prev_lat, prev_lon = lat, lon
        prev_weight -= weight

    # Last trip back to north pole, with just the sleigh weight
    dist += haversine(north_pole[0], north_pole[1], prev_lat, prev_lon) * sleigh_weight
        
    return dist

def weighted_reindeer_weariness(all_trips, weight_limit = 1000):
    uniq_trips = all_trips.TripId.unique()
    
    if any(all_trips.groupby('TripId').Weight.sum() > weight_limit):
        raise Exception("One of the sleighs over weight limit!")
 
    dist = 0.0
    for t in uniq_trips:
        # Idea 2: There may be better/faster/simpler ways to represent a solution.
        this_trip = all_trips[all_trips.TripId==t]
        dist += weighted_trip_length(this_trip.Latitude, this_trip.Longitude, this_trip.Weight)
    
    return dist    


start_time = timer()

gifts = pd.read_csv('gifts.csv.zip')
sample_sub = pd.read_csv('sample_solution.csv.zip')
all_trips = sample_sub.merge(gifts, on='GiftId')

wrw = weighted_reindeer_weariness(all_trips)
end_time = timer()

# It should be close to 144525525772
print("WRW = {:.0f}  (Time: {:.2f} seconds)".format(wrw, end_time - start_time))

