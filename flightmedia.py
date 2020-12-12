import os

class FlightMedia():

    def __init__(self, flightPath):
        self. images = []
        self.raw = []
        self.video = []
        self.flightHasPanoramas = False

        # Append to the images list any photos in the photos directory's full complete path.
        for photo in os.listdir(os.path.join(flightPath, "photos")):
            self.images.append(photo)

        # Append to the raw list any raw photos in the raw directory's full complete path.
        for raw in os.listdir(os.path.join(flightPath, "raw")):
            self.raw.append(raw)

        # Append to the video list any video in the video directory's full complete path.
        for video in os.listdir(os.path.join(flightPath, "video")):
            self.video.append(video)

        # Panoramas from my drone are stored in a folder, these folders are then dropped in the panoramas folder
        # this just checks that there are at least a folder in the directory and assumes its a panorama and sets
        # the variable to true.
        if len(os.listdir(os.path.join(flightPath, "panoramas"))) > 0:
            self.flightHasPanoramas = True
