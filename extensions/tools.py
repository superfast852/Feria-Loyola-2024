import math


def getAngle(x, y):
    if x == 0 and y == 0:
        return 0.0

    angulo = math.degrees(math.atan2(y, x) - math.pi/2)

    if angulo < 0:
        angulo += 360

    return angulo



class XboxController:
    pass


# Lapse determines the range of steps you will take.
# If lapse == 100, the smoothing will apply from 0 to 100.
def smoothSpeed(start, stop, lapse=100):
    def smooth(stamp):
        t = stamp/lapse
        if t < 0.5:
            res = 4 * t * t * t
        else:
            p = 2 * t - 2
            res = 0.5 * p * p * p + 1
        return stop*res + start*(1-res)

    return smooth


# Usage:
if __name__ == '__main__':
    from matplotlib import pyplot as plt
    start = 0
    stop = 100
    smoothHandle = smoothSpeed(start, stop)
    x = range(101)
    y = [smoothHandle(i) for i in x]
    plt.plot(x, y)
    plt.show()
