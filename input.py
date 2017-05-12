import pygame

class Gamepad:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count < 1:
            raise Exception("No gamepad detected my dude")

        if joystick_count > 1:
            print("More then one joystick detected, please select the one you want to use")
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                print("id: {}, name: {}".format(i, joystick.get_name()))
            self.joystick = pygame.joystick.Joystick(int(input("Joystick id: ")))
        else:
            self.joystick = pygame.joystick.Joystick(0)

        self.joystick.init()

    def update_data(self):
        pygame.event.pump()

    def get_steer(self):
        return self.joystick.get_axis(0)

    def get_acceleration(self):
        return self.joystick.get_axis(2)
