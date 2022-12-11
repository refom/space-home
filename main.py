
from scripts.Window import Window
from scripts.Clock import Clock
from scripts.Font import Font
from scripts.Menu import Menu
from scripts.camera import Camera
from scripts.PlanetManager import PlanetManager

Window.init()
Clock.init()
Font.init()
camera = Camera()
planet_manager = PlanetManager()

while True:
    Clock.update()
    events = Window.input()
    Menu.input(events)

    Menu.update()
    Window.update()


