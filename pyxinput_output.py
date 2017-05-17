from pyxinput import vController


class PYXInputController:
    def __init__(self):
        self.controller = vController()

    def update(self, prediction):
        self.controller.set_value("AxisLx", prediction[0])
        self.controller.set_value("TriggerR", prediction[1])