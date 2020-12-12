import json
import os

from flightmedia import FlightMedia
import hashlib

class Flight():

    def __init__(self, flightPath):
        self.raw_flight_data = {}
        self.media = {}
        self.flight_directory = ""
        self.id = ""

        # open the data.json file to load the flight stats
        with open(os.path.join(flightPath, "data.json")) as data:
            self.raw_flight_data = json.load(data)

        # create a media object of FlightMedia given the directory path.
        self.media = FlightMedia(flightPath)

        # save a variable of the flight directory as it is used a bit later
        self.flight_directory = flightPath

        # create a md5 hash from the path as a way to ensure uniqueness in the GUI
        self.id = hashlib.md5(flightPath.encode())
        
        print("Loaded flight information for " + flightPath)

    # below is getters to make it easier to get data from flights later on

    def getFlightTime(self):
        return self.raw_flight_data["flight_time"]

    def getBatteriesUsed(self):
        return self.raw_flight_data["batteries_used"]

    def getLocationName(self):
        return self.raw_flight_data["location_name"]

    def getFlightDate(self):
        return self.raw_flight_data["date"]

    def getFlightMedia(self):
        return self.media
