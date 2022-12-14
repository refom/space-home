
from scripts.Window import Window
from scripts.Menu import Menu

from scripts.manager.camera import Camera
from scripts.manager.PlanetManager import PlanetManager

from scripts.components.Clock import Clock
from scripts.components.Font import Font
from scripts.components.Background import Background
from scripts.components.music import Music

Window.init()
Clock.init()
Font.init()
Background.init()
Music.music()

camera = Camera()
planet_manager = PlanetManager()

Menu.init()
while True:
    Clock.update()
    events = Window.input()
    Menu.input(events)

    Menu.update()
    Window.update()


