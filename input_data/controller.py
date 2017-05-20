import pygame_sdl2 as pygame

class Gamepad:
    def __init__(self, provider):
        self.provider = provider
        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count < 1:
            raise Exception("No gamepad detected my dude")

        if joystick_count > 1:
            print("More then one joystick detected, please select the one you want to use")
            for i in range(joystick_count):
                self.joystick = pygame.joystick.Joystick(i)
                print("id: {}, name: {}".format(i, self.joystick.get_name()))
            self.joystick = pygame.joystick.Joystick(int(input("Joystick id: ")))
        else:
            self.joystick = pygame.joystick.Joystick(0)

        self.joystick.init()

    def update_data(self):
        pygame.event.pump()

    def get_steer(self):
        return self.joystick.get_axis(0)

    def get_acceleration(self):
        if self.provider == "xinput":
            return self.joystick.get_axis(2)
        elif self.provider == "dinput":
            acceleration = (self.joystick.get_axis(4) / 2) - 0.5  # Scale from -1-1 range to -1-0, 0 = no accel -1 = max accel
            breaking = ((self.joystick.get_axis(3) / 2) * -1) + 0.5  # Scale from -1-1 range to 0-1, 0 = no break 1 = max break
            return acceleration + breaking # Max break no accel = 1, max accel no break = -1

