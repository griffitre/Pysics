import pygame, sys
import random
import time
import math
import os
from ballswalls.boundaries import *
from listener.listenermanager import *
from images import *



class BodyGeneral(ListenerManager):
  def __init__(self):
    self.g = 9.8
    self.bodyList = []

class Body:
  def __init__(self, bodyGeneral):
    super().__init__()
    self.frictionBodyRectangle = pygame.image.load("images/rectbody.jpg").convert_alpha()
    self.frictionBodyBox = pygame.image.load("images/square.png").convert_alpha()
    self.bodyGeneral = bodyGeneral
    self.bodyGeneral.bodyList.append(self)
    self.lineList = []
    self.mass = 5
    self.muS = 0.5
    self.muK = 0.45
    self.bodyType = 1
    self.prevX = 0
    self.prevY = 0
    self.makeshiftTimer = 0
    self.firstRun = True
    self.x = None
    self.y = None
    self.grab = False
    self.vector = False


  def start(self, screen, box):
    self.box = box


    if self.box.listenerManager.activeMenu == None:
      pass

    elif self.box.listenerManager.compareMenu("FreeFallBox"):

      self.Fg = self.mass*self.bodyGeneral.g
      self.Ffk = self.muK*self.mass*self.bodyGeneral.g
      self.Fnetx = self.Ffk
      self.Fnety = self.Fg
      self.Fnet = self.Fg + self.Ffk

      if self.firstRun == True:
        self.x = random.randint(30,470)
        self.y = random.randint(50,150)
        self.velocityInitialY = 0
        self.velocityY = 0
        self.velocityXDirIn = random.randint(-1,0)
        if self.velocityXDirIn == 0:
          self.velocityX = 10
        else:
          self.velocityX = 10*self.velocityXDirIn
        self.firstRun = False

      else:
        self.coordinates = [self.x, self.y]
        if self.y + 11 < self.box.boxY2 or self.velocityX > -1 and self.velocityX < 1 :
          self.Ffk = 0
          self.accelerationX = 0

        if self.grab == True:
          self.makeshiftTimer += 1
          self.velocityX = 0
          self.velocityY = 0
          self.x = self.box.listenerManager.mouseX
          self.y = self.box.listenerManager.mouseY

          self.lineList.append(self.coordinates)
          pygame.draw.circle(screen,(255,0,0),(self.coordinates[0], self.coordinates[1]),10)

          if len(self.lineList) == 15:
            self.lineList.pop(0)
          for line in self.lineList:
            pygame.draw.line(screen, (255,255,255), (line[0], line[1]), (line[0], line[1]))

        else:
          self.velocityY = self.velocityY+self.bodyGeneral.g/30

          self.prevX = self.x

          self.x += self.velocityX
          self.y += self.velocityY

          if self.y + 11 >= self.box.boxY2:
            self.velocityY = (self.velocityY * -1) * 0.8
            self.y = self.box.boxY2 - 11

            self.accelerationX = self.Fnetx/self.mass
            if self.x - self.prevX < 0:
              self.velocityX += self.accelerationX / 30

            elif self.x - self.prevX > 0:
              self.velocityX -= self.accelerationX / 30

            elif self.x - self.prevX < 20:
              self.velocityX = self.velocityX

            if self.velocityY > -0.3 and self.velocityY < 0:
              self.velocityY = 0


          if self.y - 11 <= self.box.boxY1:
            self.velocityY = self.velocityY * -1
            self.y = self.box.boxY1 + 11

          if self.x + 11 >= self.box.boxX2:
            self.velocityX = (self.velocityX * -1) * 0.9
            self.x = self.box.boxX2 - 11

          if self.x - 11 <= self.box.boxX1:
            self.velocityX = (self.velocityX * -1) * 0.9
            self.x = self.box.boxX1 + 11

          if self.velocityX < 1 and self.velocityX > -1:
            self.velocityX = 0
            self.accelerationX = 0

          self.lineList.append(self.coordinates)

          if len(self.lineList) == 15:
            self.lineList.pop(0)
          for line in self.lineList:
            pygame.draw.line(screen, (255,255,255), (line[0], line[1]), (line[0], line[1]))
          pygame.draw.circle(screen, (255,0,0 ), (self.coordinates[0], self.coordinates[1]),10)

          self.Ek = (0.5*self.mass*(self.velocityX**2))+(0.5*self.mass*(self.velocityY**2))
          self.Eg = self.mass*self.bodyGeneral.g*(self.box.boxY2 - 11 - self.y)
          self.Et = self.Eg + self.Ek

          self.makeshiftTimer = 0

    elif self.box.listenerManager.compareMenu("FrictionRamp"):
      if self.firstRun == True:
        self.x = 600
        self.y = 150
        self.prevX = 600
        self.prevY = 150
        self.accelerationX = 0
        self.accelerationY = 0
        self.velocityX = 0
        self.velocityY = 0
        self.Fn = 0
        self.Ffs = 0
        self.Ffk = 0
        self.Fg = self.mass*self.bodyGeneral.g
        self.firstRun = False

      self.frictionBodyRotated = pygame.transform.rotate(self.frictionBodyBox, (-(360-self.box.angle)))

      self.velocityX += self.accelerationX / 30
      self.velocityY += self.accelerationY / 30


      self.prevX = self.x
      self.prevY = self.y


      self.x += self.velocityX
      self.y += self.velocityY


      if self.x + 1 > self.box.xPos[1]:
        self.Fn = 0
        if self.y + 11 >= self.box.yPos[0]:
          self.y = self.box.yPos[0] - 11
          self.velocityY = 0
          self.Fn = self.bodyGeneral.g * self.mass * -1

        if self.velocityX > -0.15 and self.velocityX < 0.15:
          self.velocityX = 0

        if self.velocityX == 0:  
          self.Ff = 0

        elif self.velocityX > 0:
          self.Ff = self.Fn*self.muK

        else:
          self.Ff = self.Fn*self.muK * -1

        self.FnetX = self.Ff
        self.FnetY = self.Fn + self.Fg

      elif self.x - 1 < self.box.xPos[1]:

        if self.y + 11 >= ((self.box.yPos[1]-self.box.yPos[0])/(self.box.xPos[1]-self.box.xPos[0]))*(self.box.xPos[1] - (self.x - 20)) + self.box.yPos[0]:

          self.Fn = self.bodyGeneral.g*self.mass
          self.FnY = self.Fn*((self.box.xPos[1]-self.box.xPos[0])/(math.sqrt((self.box.xPos[1]-self.box.xPos[0])**2 + (self.box.yPos[1]-self.box.yPos[0])**2))) * -1

          self.FgX = self.Fg*((self.box.yPos[1]-self.box.yPos[0])/(math.sqrt((self.box.xPos[1]-self.box.xPos[0])**2 + (self.box.yPos[1]-self.box.yPos[0])**2))) * -1
          self.FgY = self.Fg*((self.box.xPos[1]-self.box.xPos[0])/(math.sqrt(((self.box.xPos[1]-self.box.xPos[0])**2 + (self.box.yPos[1]-self.box.yPos[0])**2))))


          if self.velocityX > -0.15 and self.velocityX < 0.15:
            self.velocityX = 0


          if self.velocityX == 0:
            self.velocityY = 0

          if self.velocityX < 0:
            self.Ff = self.FnY*self.muK * -1

          elif self.velocityX > 0:
            self.Ff = self.FnY * self.muK

          elif self.velocityX == 0:
            if self.FgX >= self.FnY*self.muS:
              self.Ff = -self.FgX

            else:
              self.Ff = self.FnY * self.muK

          self.FnetY = self.Fg + self.FnY
          self.FnetX = self.FgX + self.Ff

        else:
          self.FnetX = 0
          self.FnetY = self.Fg

        if self.y >= ((self.box.yPos[1]-self.box.yPos[0])/(self.box.xPos[1]-self.box.xPos[0]))*(self.box.xPos[1] - (self.x - 20)) + self.box.yPos[0] - 11:
          self.y = ((self.box.yPos[1]-self.box.yPos[0])/(self.box.xPos[1]-self.box.xPos[0]))*(self.box.xPos[1] - (self.x - 20)) + self.box.yPos[0] - 11

      self.accelerationX = self.FnetX/self.mass
      self.accelerationY = self.FnetY/self.mass

      self.rectBody = self.frictionBodyBox.get_rect(center = (self.x,self.y))
      self.rotatedRectBody = self.frictionBodyRotated.get_rect(center = (self.x,self.y))

      if self.x < self.box.xPos[1]:
        screen.blit(self.frictionBodyRotated, self.rotatedRectBody)
      else:
        screen.blit(self.frictionBodyBox, self.rectBody)
      self.Ek = 0.5*self.mass*self.velocityX**2
      self.Eg = self.mass*9.8*(self.box.yPos[1]-self.box.yPos[0])/10

    elif self.box.listenerManager.compareMenu("Momentum"):
      if self.firstRun == True:
        self.sameMassCollide = False
        self.ball1Coords = [150, 290]
        self.ball2Coords = [650, 290]
        self.ball1M = 3
        self.ball2M = 4
        self.ball1VelIn = 5
        self.ball2VelIn = -3
        self.collisionDet = 11
        self.ball1VelFin = self.ball1VelIn
        self.ball2VelFin = self.ball2VelIn
        self.pTotIn = (self.ball1M*self.ball1VelIn) + (self.ball2M*self.ball2VelIn)
        self.eTotIn = (0.5*self.ball1M*self.ball1VelIn**2) + (0.5*self.ball2M*self.ball2VelIn**2)
        self.pTotFin = self.pTotIn
        self.eTotFin = self.eTotIn
        self.firstRun = False
        self.sameMassCollide = False


      self.ball1PrevX = self.ball1Coords[0]
      self.ball2PrevX = self.ball2Coords[0]
      self.ball1Coords[0] += self.ball1VelIn
      self.ball2Coords[0] += self.ball2VelIn

      if self.ball1Coords[0] + 11 >= 700:
        self.ball1Coords[0] = 112

      elif self.ball1Coords[0] - 11 <= 100:
        self.ball1Coords[0] = 688

      if self.ball2Coords[0] - 11 <= 100:
        self.ball2Coords[0] = 688

      elif self.ball2Coords[0] + 11 >= 700:
        self.ball2Coords[0] = 112
      if abs(self.ball1VelIn) >= 11 or abs(self.ball2VelIn) >=11:
        if abs(self.ball1VelIn) >= 11:
          self.collisionDet = abs(self.ball1VelIn)

        elif abs(self.ball2VelIn) >= 11:
          self.collisionDet = abs(self.ball2VelIn)

        else:
          self.collisionDet = 11

      if self.ball1Coords[0] + self.collisionDet >= self.ball2Coords[0] - 11 and self.ball1Coords[0] < self.ball2Coords[0] or self.ball1Coords[0] - self.collisionDet <= self.ball2Coords[0] + 11 and self.ball1Coords[0] > self.ball2Coords[0] or self.ball2Coords[0] - self.collisionDet <= self.ball1Coords[0] + 11 and self.ball2Coords[0] > self.ball1Coords[0] or self.ball2Coords[0] + self.collisionDet >= self.ball1Coords[0] - 11 and self.ball2Coords[0] < self.ball1Coords[0]:

        if self.ball1M == self.ball2M:
          if self.sameMassCollide == False:
            if abs(self.ball1VelIn) == abs(self.ball2VelIn):
              self.ball1VelFin, self.ball2VelFin = 0, 0
            else:
              self.ball1VelFin = (self.ball1VelIn + self.ball2VelIn) / 2
              self.ball2VelFin = self.ball1VelFin
              if -0.0000001 <= self.eTotFin - self.eTotIn and self.eTotFin - self.eTotIn <= 0.0000001:
                self.eTotFin = self.eTotIn
            self.ball1VelIn = self.ball1VelFin
            self.ball2VelIn = self.ball2VelFin
            self.sameMassCollide = True
          self.pTotFin = (self.ball1M*self.ball1VelFin) + (self.ball2M*self.ball2VelFin)
          self.eTotFin = (0.5*self.ball1M*self.ball1VelFin**2) + (0.5*self.ball2M*self.ball2VelFin**2)

        else:
          self.a = (self.ball1M*self.ball2M) + self.ball1M**2
          self.b = -((2*self.ball1M*self.ball2M*self.ball2VelIn)+(2*(self.ball1M**2)*self.ball1VelIn))
          self.c = ((self.ball1M**2)*(self.ball1VelIn**2)) + (2*self.ball1M*self.ball1VelIn*self.ball2M*self.ball2VelIn) - (self.ball1M*self.ball2M*(self.ball1VelIn**2))

          if 2*self.a == 0 or self.b**2-(4*self.a*self.c) < 0:
            self.ball1VelFin = (((-self.b))-math.sqrt((self.b**2)-(4*self.a*self.c)))/(2*self.a)
            self.ball2VelFin = (self.ball1M*self.ball1VelIn + self.ball2M*self.ball2VelIn - self.ball1M*self.ball1VelFin) / self.ball2M

          else:
            self.quadFormPlus = (((-self.b))+math.sqrt((self.b**2)-(4*self.a*self.c)))/(2*self.a)
            self.quadFormMinus = (((-self.b))-math.sqrt((self.b**2)-(4*self.a*self.c)))/(2*self.a)

            if self.ball2Coords[0] <= self.ball1Coords[0]:
              if self.ball2Coords[0] - 11 <= self.ball1Coords[0] <= self.ball2Coords[0]+11:
                self.ball1VelFin = self.quadFormMinus
                self.ball2VelFin = (self.ball1M*self.ball1VelIn+self.ball2M*self.ball2VelIn-self.ball1M*self.quadFormMinus)/self.ball2M
              else:
                self.ball1VelFin = self.quadFormPlus
                self.ball2VelFin = (self.ball1M*self.ball1VelIn+self.ball2M*self.ball2VelIn-self.ball1M*self.quadFormPlus)/self.ball2M

            else:
              self.ball1VelFin = self.quadFormMinus
              self.ball2VelFin = (self.ball1M*self.ball1VelIn+self.ball2M*self.ball2VelIn-self.ball1M*self.quadFormMinus)/self.ball2M
          self.pTotFin = (self.ball1M*self.ball1VelFin) + (self.ball2M*self.ball2VelFin)
          self.eTotFin = (0.5*self.ball1M*self.ball1VelFin**2) + (0.5*self.ball2M*self.ball2VelFin**2)
          self.ball1VelIn = self.ball1VelFin
          self.ball2VelIn = self.ball2VelFin
          if -0.0000001 <= self.eTotFin - self.eTotIn and self.eTotFin - self.eTotIn <= 0.0000001:
            self.eTotFin = self.eTotIn
      pygame.draw.circle(screen, (255,0,0), self.ball1Coords, 10)
      pygame.draw.circle(screen, (0,255,0), self.ball2Coords, 10)

    elif self.box.listenerManager.compareMenu("Spring"):
      if self.firstRun == True:
        self.x = 400
        self.y = 200
        self.k = 1.5
        self.springIn = [[100, 300], [700, 300]]
        self.springFin = [[100, 300], [700, 300]]
        self.Fg = self.bodyGeneral.g * self.mass
        self.Fs = 0
        self.Fn = 0
        self.velocityY = 0
        self.velocityX = 0
        self.accelerationY = 0
        self.firstRun = False

      self.y += self.velocityY

      if self.y + 14 >= self.springFin[0][1]:
        self.y = self.springFin[0][1] - 11
        self.Fn = self.mass* self.bodyGeneral.g * -1
        if self.Fg > abs(self.Fs):
          self.springFin[0][1] += 3
          self.springFin[1][1] += 3

      if self.y + 14 < self.springIn[0][1]:
        self.Fn = 0

      if self.springFin[0][1] > 300 and self.y + 14 < self.springFin[0][1]:
        self.springFin[0][1] -= 3
        self.springFin[1][1] -= 3

      elif abs(self.Fs) > self.Fg and self.springFin[0][1] > 300:
        self.springFin[0][1] -= 3
        self.springFin[1][1] -= 3
        self.velocityY = -3

      if self.springFin[0][1] >= 500:
        self.springFin[0][1] = 500

      self.Fs = -self.k*(self.springFin[0][1] - self.springIn[0][1])

      if self.y + 14 >= self.springFin[0][1]:
        self.FnetY = self.Fg + self.Fn + self.Fs
      else:
        self.FnetY = self.Fg

      self.accelerationY = self.FnetY / self.mass
      self.velocityY += self.accelerationY / 30

      pygame.draw.line(screen, (255,255,255), (self.springFin[0]), (self.springFin[1]))
      pygame.draw.circle(screen, (255,0,0), (self.x, self.y), 10)

    elif self.box.listenerManager.compareMenu("Circular"):
      if self.firstRun == True:
        self.period = 20
        self.radius = 100
        self.x = self.box.center[0] + self.radius
        self.y = self.box.center[1]
        self.arcLen = 0
        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.makeshiftTimer = 0
        self.radians = 0
        self.firstRun = False
      
      self.speed = math.sqrt((4*(math.pi**2)*(self.radius**2))/self.period**2)

      self.x = self.box.center[0] + self.radius * math.cos(self.radians)
      self.y = self.box.center[1] + self.radius * math.sin(self.radians)

      self.arcLen = self.speed*(self.makeshiftTimer/30)
      self.makeshiftTimer += 1
      if self.arcLen > 2*math.pi*100:
        self.arcLen = 0
        self.makeshiftTimer = 0

      self.radians = self.arcLen/self.radius

      pygame.draw.line(screen, (255,255,255), (self.box.center), (self.x, self.y))
      pygame.draw.line(screen, (255,255,255), (self.box.center), (self.box.center[0]+self.radius, self.box.center[1]))
      pygame.draw.circle(screen, (255,0,0), (self.x, self.y), 10)

    elif self.box.listenerManager.compareMenu('Harmonic'):
      if self.firstRun == True:
        self.k = 1.5
        self.massTot = self.mass
        self.period = 2*math.pi*(math.sqrt(self.massTot/self.k))
        self.amplitude = 100
        self.x = 460
        self.y = self.box.wallPos1[1] - 61
        self.firstRun = False

      self.xNew = self.amplitude*math.sin((2*math.pi)*((self.makeshiftTimer/30)/self.period) - 460)
      self.makeshiftTimer += 1
      self.x = 460 + self.xNew
      if self.xNew > 0:
        self.box.angleADeg += 1 / (self.makeshiftTimer/30)
      elif self.xNew < 0:
        self.box.angleADeg -= 1 / (self.makeshiftTimer/30)
        
      pygame.draw.rect(screen, (255,0,0), (self.x, self.y, 60, 60))
                                   

    if self.vector == True:
      if self.box.listenerManager.compareMenu("Momentum"):
        pygame.draw.aaline(screen, (100,100,100), (self.ball1Coords[0], self.ball1Coords[1]), ((self.ball1Coords[0]+self.ball1VelIn*3), self.ball1Coords[1]), 4)
        pygame.draw.aaline(screen, (100,100,100), (self.ball2Coords[0], self.ball2Coords[1]), ((self.ball2Coords[0]+self.ball2VelIn*3), self.ball2Coords[1]), 4)

      else:
        pygame.draw.aaline(screen, (100,100,100), (self.x, self.y), ((self.x+self.velocityX*3), (self.y+self.velocityY*3)), 4)
