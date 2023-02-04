import cv2
import numpy as np
import random
import time

def myRange(x, A, B):
    if x >= A and x <= B:
        return True
    return False

class FirstSlit():
    def __init__(self, x, y, slit_width, slit_height):
        self.x = int(x)
        self.y = int(y)
        self.slit_width = int(slit_width)
        self.slit_height = int(slit_height)
    
    def check(self, x, y):
        if myRange(x, self.x, self.x + self.slit_width) and (y, self.y, self.slit_height):
            return True
        return False

class SecondSlit():
    def __init__(self, x, y, slit_width, slit_height):
        self.x = int(x)
        self.y = int(y)
        self.slit_width = int(slit_width)
        self.slit_height = int(slit_height)
    
    def check(self, x, y):
        if myRange(x, self.x, self.x + self.slit_width) and (y, self.y, self.slit_height):
            return True
        return False

class theBoard():
    def __init__(self, x, y, z, width, height, depth):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.width = int(width)
        self.height = int(height)
        self.depth = int(depth)
        self.holeA = FirstSlit(x + 0.3 * width, y + 0.2 * height, 0.01 * width, 0.7 * height)
        self.holeB = SecondSlit(x + 0.7 * width, y + 0.2 * height, 0.01 * width, 0.7 * height)
    
    def checkHit(self, x, y, z):
        if myRange(z, self.z, self.z + self.depth):
            if myRange(x, self.x, self.x + self.width):
                if myRange(y, self.y, self.y + self.height):
                    if self.holeA.check(x, y) or self.holeB.check(x, y):
                        return False
                    return True
        return False

    def draw(self):
        area = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.rectangle(area, (0, 0), (self.width, self.height), (255, 255, 255), -1)
        cv2.rectangle(area, (self.holeA.x - self.x, self.holeA.y - self.y), (self.holeA.x - self.x + self.holeA.slit_width, self.holeA.y - self.y + self.holeA.slit_height), (0, 0, 0), -1)
        cv2.rectangle(area, (self.holeB.x - self.x, self.holeB.y - self.y), (self.holeB.x - self.x + self.holeB.slit_width, self.holeB.y - self.y + self.holeB.slit_height), (0, 0, 0), -1)
        cv2.imshow("theBoard", area)
        cv2.waitKey(1)

class theScreen():
    def __init__(self, x, y, z, width, height, deepth):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.width = int(width)
        self.height = int(height)
        self.deepth = int(deepth)
        self.paintBuf = np.zeros((height, width, 3), np.uint8)
    
    def checkHit(self, x, y, z):
        if myRange(z, self.z, self.z + self.deepth):
            if myRange(x, self.x, self.x + self.width):
                if myRange(y, self.y, self.y + self.height):
                    cv2.circle(self.paintBuf, (int(x) - self.x, int(y) - self.y), 1, (0, 255, 0), -1)
                    return True
        return False
    
    def draw(self):
        cv2.imshow("theScreen", self.paintBuf)
        cv2.waitKey(1)


class theBall():
    def __init__(self, x, y, z, scalr, maxStep, brd, scr):
        self.x = x
        self.y = y
        self.z = z
        self.brd = brd
        self.scr = scr
        self.x_v = (random.random() * 2 - 1) * scalr
        self.y_v = (random.random() * 2 - 1) * scalr
        self.z_v = (random.random() * 2 - 1) * scalr
        self.maxStep = maxStep
    
    def forward(self):
        for _ in range(self.maxStep):
            #print('Now at %f %f %f' % (self.x, self.y, self.z));
            if self.brd.checkHit(self.x, self.y, self.z) or self.scr.checkHit(self.x, self.y, self.z):
                #print('Hit!\n')
                break
            self.x += self.x_v
            self.y += self.y_v
            self.z += self.z_v
            #time.sleep(0.01)
    
brd = theBoard(-256, -256, 200, 512, 512, 10)
scr = theScreen(-960, -540, 400, 1920, 1080, 10)
brd.draw()

for i in range(8192):
    ball = theBall(0, 0, 0, 1, 2048, brd, scr)
    ball.forward()
    scr.draw()

print('Done!')
time.sleep(30)