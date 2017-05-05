import pygame

class Gamepad:
    def __init__(self, joystick_id):
        self.joystick_id = joystick_id
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() < 1:
            raise Exception("No gamepad detected my dude")
        self.joystick = pygame.joystick.Joystick(self.joystick_id)
        self.joystick.init()

    def update_data(self):
        pygame.event.pump()

    def get_steer(self):
        return self.joystick.get_axis(0)

    def get_acceleration(self):
        return self.joystick.get_axis(2)