import os

from flight import Flight

class Flights():

    flightsSaveLocation = "S:\_Drone\Hobby"

    flights = {}

    def __init__(self):
        for dir in os.listdir(self.flightsSaveLocation):
            if dir[:1] != ".":
                self.flights[dir] = Flight(os.path.join(self.flightsSaveLocation, dir))

    def getFlights(self):
        return self.flights

    def getFlightLocations(self):
        locations = []
        for flight in self.getFlights():
            flight_location = self.getFlights()[flight].getLocationName()
            if flight_location not in locations:
                locations.append(flight_location)

        return locations