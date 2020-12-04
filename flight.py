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

        with open(os.path.join(flightPath, "data.json")) as data:
            self.raw_flight_data = json.load(data)

        self.media = FlightMedia(flightPath)

        self.flight_directory = flightPath

        self.id = hashlib.md5(flightPath.encode())
        
        print("Loaded flight information for " + flightPath)

    def getFlightTime(self):
        return self.raw_flight_data["flight_time"]

    def getBatteriesUsed(self):
        return self.raw_flight_data["batteries_used"]

    def getLocationName(self):
        return self.raw_flight_data["location_name"]

    def getFlightMedia(self):
        return self.media
