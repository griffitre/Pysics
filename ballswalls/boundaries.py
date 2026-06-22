import pygame
from listener.listenermanager import *
from ballswalls.classes import *
import math

class Boundaries(ListenerManager):
  def __init__(self, name):
    self.name = name
    self.white = (255,255,255)
    pass

  def generate(self, screen, body):
    self.body = body
    self.body.start(screen, self)
    pass


class FreeFallBox(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("FreeFallBox")
    self.listenerManager = listenerManager
    pass
    
  def generate(self, screen, body):
    self.body = body
    self.boxX1, self.boxX2 = 20, 480
    self.boxY1, self.boxY2 = 20, 480
    screen.fill((0,0,0))
    pygame.draw.line(screen,self.white,(self.boxX1,self.boxY1),(self.boxX1,self.boxY2))
    pygame.draw.line(screen,self.white,(self.boxX1,self.boxY1),(self.boxX2,self.boxY1))
    pygame.draw.line(screen,self.white,(self.boxX1,self.boxY2),(self.boxX2,self.boxY2))
    pygame.draw.line(screen,self.white,(self.boxX2,self.boxY1),(self.boxX2,self.boxY2))
    self.body.start(screen, self)

class FrictionRamp(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("FrictionRamp")
    self.listenerManager = listenerManager
    self.xPos = [20, 480]
    self.yPos = [300, 480]

  def generate(self, screen, body):
    self.body = body
    self.angle = math.degrees(math.atan((self.yPos[1]-self.yPos[0])/(self.xPos[1]-self.xPos[0])))
    screen.fill((0,0,0))
    pygame.draw.line(screen, self.white, (self.xPos[0],self.yPos[1]), (self.xPos[1],self.yPos[1]))
    pygame.draw.line(screen, self.white, (self.xPos[1],self.yPos[0]), (self.xPos[1], self.yPos[1]))
    pygame.draw.line(screen, self.white, (self.xPos[0], self.yPos[1]), (self.xPos[1], self.yPos[0]))
    pygame.draw.line(screen, self.white, (self.xPos[1], self.yPos[0]), (780, self.yPos[0]))
    self.body.start(screen, self)


class Momentum(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("Momentum")
    self.listenerManager = listenerManager
    self.groundPos = [(100, 300), (700, 300)]
    self.wall1 = [(100, 300), (100, 100)]
    self.wall2 = [(700, 300), (700, 100)]

  def generate(self, screen, body):
    self.body = body
    screen.fill((0,0,0))
    pygame.draw.line(screen, self.white, self.groundPos[0], self.groundPos[1])
    pygame.draw.line(screen, self.white, self.wall1[0], self.wall1[1])
    pygame.draw.line(screen, self.white, self.wall2[0], self.wall2[1])
    self.body.start(screen, self)


class Spring(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("Spring")
    self.listenerManager = listenerManager
    self.groundPos = [(100, 500), (700, 500)]
    self.wall1 = [(100, 500), (100, 100)]
    self.wall2 = [(700, 500), (700, 100)]

  def generate(self, screen, body):
    self.body = body
    screen.fill((0,0,0))
    pygame.draw.line(screen, self.white, self.groundPos[0], self.groundPos[1])
    pygame.draw.line(screen, self.white, self.wall1[0], self.wall1[1])
    pygame.draw.line(screen, self.white, self.wall2[0], self.wall2[1])
    self.body.start(screen, self)

class Circular(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("Circular")
    self.listenerManager = listenerManager
    self.center = [400, 200]

  def generate(self, screen, body):
    self.body = body
    screen.fill((0,0,0))
    pygame.draw.circle(screen, self.white, (self.center), 3)
    self.body.start(screen, self)

class Harmonic(Boundaries):
  def __init__(self, listenerManager):
    super().__init__("Harmonic")
    self.listenerManager = listenerManager
    self.groundPos = [(100, 300), (700, 300)]
    self.wallPos1, self.wallPos2 = [100, 300], [100, 100]
    self.xIn = 460
    self.angleADeg = 20
    self.angleBDeg = (180 - self.angleADeg) / 2
    self.angleARad = math.radians(self.angleADeg)
    self.angleBRad = math.radians(self.angleBDeg)
    self.springNodes = []
    self.distBetween = (math.sin(self.angleARad)*math.sqrt(20**2+60**2)) / math.sin(self.angleBRad)
    

  def generate(self, screen, body):
    self.body = body
    screen.fill((0,0,0))
    self.body.start(screen, self)
    pygame.draw.line(screen, self.white, self.groundPos[0], self.groundPos[1])
    pygame.draw.line(screen, self.white,(self.wallPos1), (self.wallPos2))
    self.springNodes = []
    self.sizePercent = self.body.x / self.xIn
    for i in range(0,16):
      if i == 0:
        self.springNodes.append((100, 250))
      elif i == 15:
        self.springNodes.append((self.body.x, 250))
      elif i % 2 != 0:
        self.springNodes.append(((110 + (self.distBetween*self.sizePercent)*i), 220))
      elif i % 2 == 0:
        self.springNodes.append(((130 + (self.distBetween*self.sizePercent)*i), 280))

    for coords in self.springNodes:
      self.index = self.springNodes.index(coords)
      if self.index != 0:
        pygame.draw.line(screen, self.white, self.springNodes[self.index - 1],self.springNodes[self.index])
    
    