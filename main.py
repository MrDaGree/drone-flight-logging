import os
import glfw
import pygame
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image

from flights import Flights
from flight import Flight

window_width = 1220
window_height = 700

currentViewingFlightData = {}

def loadFlightData():
    global flights
    flights = Flights()

def loadImage(imgPath):
    image = pygame.image.load(imgPath)
    imgSurface = pygame.transform.flip(image, False, True)

    imageData = pygame.image.tostring(imgSurface, "RGBA", 1)

    width = imgSurface.get_width()
    height = imgSurface.get_height()

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                gl.GL_UNSIGNED_BYTE, imageData)

    return texture, width, height

def mainMenuBar():
    if imgui.begin_menu_bar():
        if imgui.begin_menu('File'):
            imgui.menu_item('Close')
            imgui.end_menu()

        imgui.end_menu_bar()

def handlePhotoPreviewButtonClick(path, photo):
    if imgui.button("Preview (" + photo + ")"):
        
        print(photo)
        img, width, height = loadImage(os.path.join(path, "photos", photo))
        currentViewingFlightData["preview"] = {}
        currentViewingFlightData["preview"]['image'] = img
        currentViewingFlightData["preview"]['width'] = width
        currentViewingFlightData["preview"]['height'] = height

def photosDropDown(flight):
    if imgui.tree_node("Photos ##" + str(flight.id)):
        for photo in flight.getFlightMedia().images:
            imgui.text(photo)
            imgui.same_line()
            handlePhotoPreviewButtonClick(flight.flight_directory, photo)
                
        imgui.tree_pop()

def flightDropDown(flight_name, flight):
    expanded, _ = imgui.collapsing_header(flight_name + "##" + str(flight.id))

    if expanded:
        imgui.text("Flight Time: " + flight.getFlightTime())
        imgui.same_line()
        imgui.text(" | Batteries Used: " + flight.getBatteriesUsed())
        imgui.text("Location: " + flight.getLocationName())
        imgui.spacing()
        photosDropDown(flight)

def main():
    loadFlightData()

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        style = imgui.get_style()

        style.window_rounding = 0

        imgui.new_frame()

        style.frame_rounding = 0

        flags = imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_MENU_BAR

        imgui.set_next_window_size(window_width, window_height)
        imgui.set_next_window_position(0, 0)
        imgui.begin("Drone Flight Logger", False, flags=flags)

        # Main Menu Bar Code
        mainMenuBar()

        imgui.begin_child("flight_selector", width=window_width/5*2, border=True)

        for flight in flights.getFlights():
            flightDropDown(flight, flights.getFlights()[flight])

        imgui.end_child()

        imgui.same_line()

        imgui.begin_child("flight_info", border=True)

        if "preview" in currentViewingFlightData:
            imgui.image(currentViewingFlightData["preview"]['image'], currentViewingFlightData["preview"]['width']/6, currentViewingFlightData["preview"]['height']/6)

        imgui.end_child()


        imgui.end()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    window_name = "Drone Flight Logger"

    if not glfw.init():
        printToLog("Could not initialize OpenGL context")
        exit(1)


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