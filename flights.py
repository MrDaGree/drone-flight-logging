import os

from flight import Flight

class Flights():

    flightsSaveLocation = ""

    flights = {}

    def __init__(self, flightsLocation):
        self.flightsSaveLocation = flightsLocation

        # when the flights object is init'd, get all the directories in the flightsSaveLocation variable above
        for dir in os.listdir(self.flightsSaveLocation):
            # if the directory or file starts with a '.' ignore it or continue if not. This is from MacOS hidden files being
            # something I had to jump around.
            if dir[:1] != ".":
                # create a new 'Flight' object in a dictionary under the directory name as the key, these are date names for 
                # file explorer viewing ease so these should always be unique.
                self.flights[dir] = Flight(os.path.join(self.flightsSaveLocation, dir))

    # below is just a few getters to simplify code that is used a lot

    # get the flights dictionary and return it
    def getFlights(self):
        return self.flights

    def getTotalFlightTime(self):
        time = 0.0
        for flight in self.flights:
            time += self.flights[flight].getFlightTime()

        return time

    def getTotalBatteriesUsed(self):
        batteries = 0.0
        for flight in self.flights:
            batteries += self.flights[flight].getBatteriesUsed()

        return batteries

    # return a list of flight locations
    def getFlightLocations(self):
        locations = []
        for flight in self.getFlights():
            flight_location = self.getFlights()[flight].getLocationName()
            if flight_location not in locations:
                locations.append(flight_location)

        return locations