from HAL import *


class Robot:
    def __init__(self):
        self.drive = Drive()
        self.bat = Bateria()

    def goTo(self):
        pass

    def exit(self):
        self.drive.exit()
        self.bat.exit()