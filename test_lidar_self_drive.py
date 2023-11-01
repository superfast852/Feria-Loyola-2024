# pip install opencv-python numpy rplidar-roboticia

from rplidar import RPLidar
import numpy as np
import cv2

lidar = RPLidar(None, "COM3", timeout=3)  # Busca el puerto com apropiado
lidar.start()
iterator = lidar.iter_scans(1000)
print(lidar.get_info(), lidar.get_health())
next(iterator)
map = [0]*360

def plotMap(mapa):
    xy = np.array([(distance*np.cos(np.deg2rad(angle)), distance*np.sin(np.deg2rad(angle))) for angle, distance in enumerate(mapa)])
    blank = np.zeros((max(xy.flatten()), max(xy.flatten()), 3))
    for x, y in xy:
        blank[y, x] = (255, 255, 255)
    cv2.imshow("Test Map", blank)
    cv2.waitKey(1)

try:
    for _, angle, distance in next(iterator):
        map[int(angle)] = distance
        plotMap(map)
except KeyboardInterrupt:
    lidar.stop()


