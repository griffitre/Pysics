from listener.listenermanager import *
from ballswalls.classes import *
from ballswalls.boundaries import *
import pygame, sys

class InputListener(Listener):
  def __init__(self, listenerManager):
    super().__init__(listenerManager, pygame.KEYDOWN)

  def onEvent(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_1:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = FreeFallBox(self.listenerManager)
        self.listenerManager.body.lineList = []
      elif event.key == pygame.K_2:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = FrictionRamp(self.listenerManager)
      elif event.key == pygame.K_3:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = Momentum(self.listenerManager)
      elif event.key == pygame.K_4:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = Spring(self.listenerManager)
      elif event.key == pygame.K_5:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = Circular(self.listenerManager)
      elif event.key == pygame.K_6:
        self.listenerManager.body.firstRun = True
        self.listenerManager.activeMenu = Harmonic(self.listenerManager)
      elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()



      if self.listenerManager.compareMenu("FrictionRamp"):
        if event.key == pygame.K_EQUALS:
          self.listenerManager.activeMenu.yPos[0] -= 5
        elif event.key == pygame.K_MINUS:
          self.listenerManager.activeMenu.yPos[0] += 5

        if event.key == pygame.K_LEFT:
          self.listenerManager.body.velocityX -= 5
        
        if event.key == pygame.K_RIGHT:
          self.listenerManager.body.velocityX += 5

      if event.key == pygame.K_v:
        self.listenerManager.body.vector = True
        
    