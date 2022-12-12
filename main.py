
from scripts.Window import Window
from scripts.components.Clock import Clock
from scripts.components.Font import Font
from scripts.Menu import Menu
from scripts.manager.camera import Camera
from scripts.components.Background import Background
from scripts.manager.PlanetManager import PlanetManager
from scripts.components.music import Music

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


