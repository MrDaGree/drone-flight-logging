import os
import glfw
import json
import pygame
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image

from flights import Flights
from flight import Flight

# In ImGui '##' means whats after will be hidden so I also add the flight id to ensure unique or
# it will cause issues with the GUI for most things like dropdowns etc.

flightSavesLocation = "S:\_Drone\Hobby"
addNewFlightData = {}
addNewFlightData["copyFromFolder"] = flightSavesLocation
addNewFlightData["location_name"] = ""
addNewFlightData["batteries_used"] = 0
addNewFlightData["flight_time"] = 0
addNewFlightData["date"] = ""

window_width = 1220
window_height = 700

currentViewingFlightData = {}
currentSelectedLocations = {}

def loadFlightData():
    # define a global variable called flights that will store the flights object containing all the flights
    global flights
    flights = Flights(flightSavesLocation)

    # fill the currentSelectedLocations to the default 'True' state
    for location in flights.getFlightLocations():
        if not location in currentSelectedLocations:
            currentSelectedLocations[location] = True

# loadImage function taken from https://github.com/swistakm/pyimgui/issues/82#issuecomment-637709585

def loadImage(imgPath):
    # load the image as a pygame image
    image = pygame.image.load(imgPath)
    # flip the image vertically so its not upside down
    imgSurface = pygame.transform.flip(image, False, True)

    # get the data from the image, ensuring in RGBA format for color
    imageData = pygame.image.tostring(imgSurface, "RGBA", 1)

    # get the height and width from the flipped image
    width = imgSurface.get_width()
    height = imgSurface.get_height()

    # to be honest, magic.
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                gl.GL_UNSIGNED_BYTE, imageData)

    # return the 'texture' image and the width and height to use later
    return texture, width, height

def mainMenuBar():
    if imgui.begin_menu_bar():
        # Create a menu bar button for locations
        if imgui.begin_menu('Locations'):
            # Loop through all the locations to then be sorted
            for location in flights.getFlightLocations():
                # create the menu item so we can check if clicked
                click, state = imgui.menu_item(location, selected=currentSelectedLocations[location])

                if click:
                    # if the button was clicked just toggle the boolean in the currentselected locations as this handles showing or hiding
                    # in the loop below in the main GUi panel
                    currentSelectedLocations[location] = not currentSelectedLocations[location]
            imgui.end_menu()

        imgui.end_menu_bar()


def handlePhotoPreviewButtonClick(path, photo):
    # Create a button for the preview dropdown with the photo name as a hidden text to ensure uniqueness
    if imgui.button("Preview##" + photo):
        # get the image as a texture from the function along with the width and height
        img, width, height = loadImage(os.path.join(path, "photos", photo))
        # store the image information in the viewing variable for the sidepane
        currentViewingFlightData["preview"] = {}
        currentViewingFlightData["preview"]['image'] = img
        currentViewingFlightData["preview"]['width'] = width
        currentViewingFlightData["preview"]['height'] = height

def mediaDropDown(flight):
    # create a drop down for raw
    if imgui.tree_node("Raw ##" + str(flight.id)):
        # loop through all the 'raw' media in the flight
        for raw in flight.getFlightMedia().raw:
            # display the media name in the dropdown
            imgui.text(raw)

        imgui.tree_pop()

    # create a drop down for photos
    if imgui.tree_node("Photos ##" + str(flight.id)):
        # loop through all the 'photo' aka non raw media in the flight
        for photo in flight.getFlightMedia().images:
            # display the media name in the dropdown
            imgui.text(photo)
            # on the same line create the preview button for photos
            imgui.same_line()
            handlePhotoPreviewButtonClick(flight.flight_directory, photo)
                
        imgui.tree_pop()

    # create a drop down for videos
    if imgui.tree_node("Videos ##" + str(flight.id)):
        # loop through all the 'video' media in the flight
        for video in flight.getFlightMedia().video:
            # display the media name in the dropdown
            imgui.text(video)

        imgui.tree_pop()

def flightDropDown(flight_name, flight):
    # create the drop down with the flight location and date
    expanded, _ = imgui.collapsing_header(flight.getLocationName() + " (" + flight.getFlightDate() + ")##" + str(flight.id))

    if expanded:
        #Display flight stats if the drop down is visible
        imgui.text("Flight Time: " + str(flight.getFlightTime()) + "h")
        imgui.same_line()
        imgui.text("| Batteries Used: " + str(flight.getBatteriesUsed()))
        imgui.text("Location: " + flight.getLocationName())
        imgui.text("Flight has Panorama: " + str(flight.media.flightHasPanoramas))
        imgui.separator()
        if imgui.button("Open in File Browser"):
            os.startfile(flight.flight_directory)
        imgui.spacing()
        # code for each media type drop down
        mediaDropDown(flight)
        imgui.spacing()

def handleAddNewFlight():
    newFlightDir = os.path.join(flightSavesLocation, addNewFlightData["date"])
    os.mkdir(newFlightDir)

    photosPath = os.path.join(newFlightDir, "photos")
    rawPath = os.path.join(newFlightDir, "raw")
    videoPath = os.path.join(newFlightDir, "video")

    os.mkdir(photosPath)
    os.mkdir(rawPath)
    os.mkdir(videoPath)
    os.mkdir(os.path.join(newFlightDir, "panoramas"))
    os.mkdir(os.path.join(newFlightDir, "export"))

    for file in os.listdir(addNewFlightData["copyFromFolder"]):
        mediaExtension = file[-3:]
        if mediaExtension == "JPG":
            os.rename(os.path.join(addNewFlightData["copyFromFolder"], file), os.path.join(photosPath, file))

        if mediaExtension == "DNG":
            os.rename(os.path.join(addNewFlightData["copyFromFolder"], file), os.path.join(rawPath, file))

        if mediaExtension == "MP4":
            os.rename(os.path.join(addNewFlightData["copyFromFolder"], file), os.path.join(videoPath, file))

    del addNewFlightData["copyFromFolder"]

    with open(os.path.join(newFlightDir, "data.json"), "x") as flightData:
        json.dump(addNewFlightData, flightData, sort_keys=True, indent=4)

    
    addNewFlightData["copyFromFolder"] = flightSavesLocation
    addNewFlightData["location_name"] = ""
    addNewFlightData["batteries_used"] = 0
    addNewFlightData["flight_time"] = 0
    addNewFlightData["date"] = ""

    loadFlightData()

def main():
    loadFlightData()

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # get the style object and edit the object to make it look decent with GLFW
        style = imgui.get_style()
        style.window_rounding = 0
        style.frame_rounding = 0

        #create the main ImGuI frame to then use to display the actual GUI on
        imgui.new_frame()

        flags = imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_MENU_BAR

        imgui.set_next_window_size(window_width, window_height)
        imgui.set_next_window_position(0, 0)

        # Start the beginning of the ImGui window, drone flight logger being an ID
        imgui.begin("Drone Flight Logger", False, flags=flags)

        
        if imgui.button("Add new Flight"):
            imgui.open_popup("test")

        imgui.same_line()

        imgui.text("Total Flight Time: " + str(flights.getTotalFlightTime()) + "h")

        imgui.same_line()

        imgui.text("| Total Batteries Used: " + str(flights.getTotalBatteriesUsed()))

        # Main Menu Bar Code
        mainMenuBar()

        # create a child window in the inital window to divide the window up so there can be a preview on the left
        imgui.begin_child("flight_selector", width=window_width/5*2, border=True)

        # loop through all flights and assign flight as the key value
        for flight in flights.getFlights():
            # get the flight data based off the flight name
            flight_data = flights.getFlights()[flight]
            # if the flight location is in the List variable of currently selected locations show it
            if currentSelectedLocations[flight_data.getLocationName()]:
                # flight drop down code, passing in the flight name and flight data
                flightDropDown(flight, flight_data)

        imgui.end_child()

        imgui.same_line()

        # create the preview sidepane of the main window
        imgui.begin_child("flight_info", border=True)

        # if there is the key preview in currentviewingflightdata show the image. Done this way as I will eventually add in the flight location and other stats to the sidepane as well
        if "preview" in currentViewingFlightData:
            imgui.image(currentViewingFlightData["preview"]['image'], currentViewingFlightData["preview"]['width']/6, currentViewingFlightData["preview"]['height']/6)

        imgui.end_child()

        if imgui.begin_popup_modal("test")[0]:
            addNewFlightData["date"] = imgui.input_text("Flight date", addNewFlightData["date"], 2046)[1]
            addNewFlightData["batteries_used"] = imgui.input_int('Batteries used', addNewFlightData["batteries_used"])[1]
            addNewFlightData["flight_time"] = imgui.input_int('Flight time in minutes', addNewFlightData["flight_time"])[1]
            addNewFlightData["location_name"] = imgui.input_text("Flight location", addNewFlightData["location_name"], 2046)[1]
            addNewFlightData["copyFromFolder"] = imgui.input_text("Folder with new flight media", addNewFlightData["copyFromFolder"], 2046)[1]

            if imgui.button("test"):
                handleAddNewFlight()
                imgui.close_current_popup()

            # imgui.text("Select an option:")
            # imgui.separator()
            # imgui.selectable("One")
            # imgui.selectable("Two")
            # imgui.selectable("Three")
            imgui.end_popup()

        imgui.end()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


# Create the GLFW window with the window name and size defined at top of file
def impl_glfw_init():
    window_name = "Drone Flight Logger"

    if not glfw.init():
        printToLog("Could not initialize OpenGL context")
        exit(1)

    # get rid of the mouse 'hint' to resize the window to ensure the ImGui GUI stays on the whole screen
    glfw.window_hint(glfw.RESIZABLE, False)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(window_width), int(window_height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        printToLog("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()