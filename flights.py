import os

from flight import Flight

class Flights():

    flightsSaveLocation = "S:\_Drone\IL\Carpentersville, IL"

    flights = {}

    def __init__(self):
        for dir in os.listdir(self.flightsSaveLocation):
            if dir[:1] != ".":
                self.flights[dir] = Flight(os.path.join(self.flightsSaveLocation, dir))

    def getFlights(self):
        return self.flights