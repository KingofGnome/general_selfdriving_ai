from pyvjoy import VJoyDevice


class PyVjoyController:
    def __init__(self):
        self.controller = VJoyDevice(1)
        center = 0x7FFF // 2
        self.controller.data.wAxisX = center
        self.controller.data.wAxisY = center
        self.controller.data.wAxisZ = center
        self.controller.data.wAxisXRot = center
        self.controller.data.wAxisYRot = center
        self.controller.data.wAxisZRot = center
        self.controller.data.lButtons = 0
        self.controller.update()

    def update(self, prediction):
        self.controller.data.wAxisX = int(((prediction[0] / 2) + 0.5) * 32767)  # Evil floating point bit level hacking
        self.controller.data.wAxisZRot = int(((((prediction[1] * -1) / 2) + 0.5) * 32767))  # What the fuck
        self.controller.update()
