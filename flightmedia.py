import os

class FlightMedia():

    def __init__(self, flightPath):
        self. images = []
        self.raw = []
        self.video = []
        self.flightHasPanoramas = False

        for photo in os.listdir(os.path.join(flightPath, "photos")):
            self.images.append(photo)

        for raw in os.listdir(os.path.join(flightPath, "raw")):
            self.raw.append(raw)

        for video in os.listdir(os.path.join(flightPath, "video")):
            self.video.append(video)

        if len(os.listdir(os.path.join(flightPath, "panoramas"))) > 0:
            self.flightHasPanoramas = True
