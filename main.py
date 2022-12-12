
from scripts.Window import Window
from scripts.Clock import Clock
from scripts.Font import Font
from scripts.Menu import Menu
from scripts.camera import Camera
from scripts.Background import Background
from scripts.PlanetManager import PlanetManager
from scripts.music import Music

Window.init()
Clock.init()
Font.init()
Music.music()

camera = Camera()
planet_manager = PlanetManager()

Background.init()
while True:
    Clock.update()
    events = Window.input()
    Menu.input(events)

    Menu.update()
    Window.update()


