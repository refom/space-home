import pygame

pygame.mixer.init()


class Music:
    mixer_bgm = pygame.mixer.Sound('assets/bgm.wav')
    mixer_click = pygame.mixer.Sound('assets/click.wav')
    mixer_load_resource = pygame.mixer.Sound('assets/load_resource.mp3')
    mixer_thruster = pygame.mixer.Sound('assets/thruster.wav')
    mixer_lose = pygame.mixer.Sound('assets/lose.mp3')
    mixer_win = pygame.mixer.Sound('assets/win.wav')
    
    bgm_channel = pygame.mixer.Channel(0)
    bgm_channel.set_volume(0.4)

    sfx_channel = pygame.mixer.Channel(1)
    sfx_channel.set_volume(0.7)

    engine_channel = pygame.mixer.Channel(2)
    engine_channel.set_volume(0.3)

    engine_on = False
    engine_pause = False

    @classmethod
    def music(cls):
        cls.bgm_channel.play(cls.mixer_bgm, loops=-1)

    @classmethod
    def click_sound(cls):
        cls.sfx_channel.play(cls.mixer_click)

    @classmethod
    def load_resource_sound(cls):
        cls.sfx_channel.play(cls.mixer_load_resource)

    @classmethod
    def lose_sound(cls):
        cls.sfx_channel.play(cls.mixer_lose)

    @classmethod
    def win_sound(cls):
        cls.sfx_channel.play(cls.mixer_win)

    @classmethod
    def start_thruster(cls):
        if (cls.engine_on): return
        if (cls.engine_pause):
            print("unpause thruster")
            cls.engine_channel.unpause()
            cls.engine_pause = False
            cls.engine_on = True
            return

        print("start thruster")
        cls.engine_channel.play(cls.mixer_thruster, loops=-1)
        cls.engine_on = True
        cls.engine_pause = False

    @classmethod
    def stop_thruster(cls):
        if (not cls.engine_on): return
        print("stop thruster")
        cls.engine_channel.pause()
        cls.engine_on = False
        cls.engine_pause = True
    


