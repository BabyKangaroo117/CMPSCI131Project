import requests
import os
from dotenv import load_dotenv
import json
import math

load_dotenv()
API_KEY = os.getenv("API_KEY_RADAR")
HEADER = {"Authorization": API_KEY}


class FindDestination:
    def __init__(self):
        self._url_autocomplete = "https://api.radar.io/v1/search/autocomplete?"
        self._url_geocoding = "https://api.radar.io/v1/geocode/forward?"

    def get_latitude_longitude(self, addresses: list):
        """Takes a list of addresses as an input and returns a list of dictionaries
        with the keys as the addresses and the values as their longitude and latitude as tuples"""

        latitude_longitudes = []
        for address in addresses:
            dictionary = {}
            # Get the coordinates of each address
            response = requests.get(self._url_geocoding + "query=" + address + "&country=US", headers=HEADER)
            locations = json.loads(response.text)
            try:
                latitude = locations["addresses"][0]["latitude"]
                longitude = locations["addresses"][0]["longitude"]
                dictionary[address] = (latitude, longitude)
                latitude_longitudes.append(dictionary)
            except (IndexError, KeyError):
                pass

        return latitude_longitudes

    def average_latitude_longitude(self, coordinates: list):
        """Takes a list of dictionaries with values of tuples that contain longitude and latitude coordinates
         and returns the average latitude and longitude as a tuple"""

        latitude_sum = 0
        longitude_sum = 0

        for coordinate in coordinates:
            for key, value in coordinate.items():
                latitude_sum += value[0]
                longitude_sum += value[1]

        latitude_average = latitude_sum / len(coordinates)
        longitude_average = longitude_sum / len(coordinates)

        return latitude_average, longitude_average

    def find_locations(self, query: str, midpoint_coordinates: tuple):
        """Takes a tuple that contains a latitude and longitude and a destination query (such as italian restaurant),
         then returns a list of locations that are nearby"""

        # Find the query locations that are near the midpoint coordinates
        response = requests.get(self._url_autocomplete + "query=" + query + "&near=" +
                                str(midpoint_coordinates[0]) + "," + str(midpoint_coordinates[1]), headers=HEADER)
        locations = json.loads(response.text)['addresses']

        # Save the addresses in a list
        location_addresses = []
        for dictionary in locations:
            location_addresses.append(dictionary["formattedAddress"])
        #print(location_addresses)

        return location_addresses

    def calculate_distance(self, origins: list, destinations: list):
        """Takes a list of dictionaries with an address as the key and the value as a tuple with coordinates.
        Finds the distance between the origin addresses and destination addresses. Returns a list with the distance
        to each destination from each origin address."""

        location_distances = []

        for location in origins:
            distances = []
            for origin_address, origin_coordinates in location.items():
                for destination in destinations:
                    for dest_address, dest_coordinates in destination.items():
                        distance = math.sqrt((origin_coordinates[0] - dest_coordinates[0]) ** 2 +
                                (origin_coordinates[1] - dest_coordinates[1]) ** 2)
                        distance_tuple = (dest_address, distance)
                        distances.append(distance_tuple)
            location_distances.append(distances)
        #print(location_distances)
        return location_distances

    def sort_by_distance(self, location_distances: list):
        """Takes the output of calculate_distance and sorts the distances by increasing order"""
        def bubbleSort(locations_lst):
            n = len(locations_lst)
            swapped = False
            for i in range(n - 1):

                for j in range(0, n-i-1):
                    if locations_lst[j][1] > locations_lst[j + 1][1]:
                        swapped = True
                        locations_lst[j], locations_lst[j + 1] = locations_lst[j + 1], locations_lst[j]
                if not swapped:
                    return locations_lst
            return locations_lst

        sorted_list = []
        for distances in location_distances:
            sorted_list.append(bubbleSort(distances))

        return sorted_list

    def shortest_distance_destination(self, distances: list):
        """Finds the shortest average distance between each destination and the origin addresses"""
        def average_distance(distances: list):
            first_list = distances[0]
            average_distances = []
            for i in range(len(first_list)):     #0 to len of destinations
                for j in range(len(distances)):  #0 to len of origin addresses. Up to 4
                    average = (distances[j][i][1]) / len(first_list)
                    average_distances.append(average)

            return average_distances

        average_distances = average_distance(distances)
        print(average_distances)
        shortest_distance = average_distances[0]
        for distance in average_distances:
            if distance < shortest_distance:
                shortest_distance = distance
        index_shortest_distance = average_distances.index(shortest_distance)
        print(index_shortest_distance)
        shortest_distance_destination = distances[0][index_shortest_distance][0]

        return shortest_distance_destination




















