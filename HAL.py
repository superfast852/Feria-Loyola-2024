# In here, the HAL team will work. Check README for implementations.
from adafruit_ina219 import INA219
import board
from threading import Thread
from _thread import interrupt_main
from time import sleep
from extensions.tools import getAngle, math


class Drive:
    def __init__(self):
        self.lf = 0
        self.rf = 0
        self.lb = 0
        self.rb = 0
        self.stop = False
        self.thread = Thread(target=self.comms, daemon=True)
        self.thread.start()

    def cartesian(self, x, y, w, vel=1):
        theta = math.radians(getAngle(x, y))

        sin = math.sin(theta + math.pi / 4)
        cos = math.cos(theta + math.pi / 4)
        lim = max(abs(sin), abs(cos))

        lf = vel * cos / lim + w
        rf = vel * sin / lim - w
        lb = vel * sin / lim + w
        rb = vel * cos / lim - w

        clip = vel+abs(w)

        if clip > 1:
            lf /= clip
            rf /= clip
            lb /= clip
            rb /= clip

        self.lf = lf
        self.lb = lb
        self.rf = rf
        self.rb = rb
        return lf, lb, rf, rb

    def diferencial(self, V, w):
        der = V + w / 2
        izq = V - w / 2

        clip = max(abs(izq), abs(der))
        if clip > 1:
            der /= clip
            izq /= clip

        self.lf = izq
        self.lb = izq
        self.rf = der
        self.rb = der

        return izq, der

    def comms(self):
        while not self.stop:
            pass
            sleep(0.1)

    def exit(self):
        self.stop = True
        self.thread.join()

class Bateria:
    def __init__(self, minimo=10):
        self.i2c_bus = board.I2C()
        self.lector = INA219(self.i2c_bus)
        self.thread = Thread(target=self._monitor, daemon=True)
        self.thread.start()
        self.stop = False
        self.minimo = minimo

    def _monitor(self):
        while not self.stop:
            voltaje = self.lector.bus_voltage + self.lector.shunt_voltage
            if voltaje < self.minimo:
                interrupt_main()
            sleep(1)

    def exit(self):
        self.stop = True
        self.thread.join()

class MotorKinematics:
    pass


if __name__ == '__main__':
    bat = Bateria(11)

