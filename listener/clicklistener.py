from listener.listenermanager import *
import pygame
import time

class ClickListener(Listener):
  def __init__(self, listenerManager):
    super().__init__(listenerManager, pygame.MOUSEBUTTONDOWN)
    self.prevClickCoords = []
    self.finClickCoords = []

  def onEvent(self, event):
    if self.listenerManager.body.x == None and self.listenerManager.body.y == None:
      pass
      
    else:
      self.clickX = event.pos[0]
      self.clickY = event.pos[1]
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.clickX >= self.listenerManager.body.x - 11 and self.clickX <= self.listenerManager.body.x + 11 and self.clickY >= self.listenerManager.body.y - 11 and self.clickY <= self.listenerManager.body.y + 11 and event.button == 1:
          self.listenerManager.body.grab = True
          if event.button == 1:
            self.prevClickCoords.append(self.clickX)
            self.prevClickCoords.append(self.clickY)

        if self.listenerManager.body.grab == True:
          if event.button == 3:
            self.rClickX = event.pos[0]
            self.rClickY = event.pos[1]
            self.finClickCoords.append(self.rClickX)
            self.finClickCoords.append(self.rClickY)
            self.listenerManager.body.velocityX = (self.rClickX - self.prevClickCoords[0]) / (self.listenerManager.body.makeshiftTimer)
            self.listenerManager.body.velocityY = ((self.rClickY - self.prevClickCoords[1])) / (self.listenerManager.body.makeshiftTimer)
            self.prevClickCoords = []
            self.listenerManager.body.grab = False
          
          
            
    