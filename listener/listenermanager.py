import pygame, sys

class ListenerManager:
  def __init__(self, body):
    self.activeMenu = None
    self.listeners = []
    self.screen = pygame.display.set_mode((800, 800))
    self.clock = pygame.time.Clock()
    self.body = body

  def listen(self):
    while True:
      self.clock.tick(30)
      self.mouseX = pygame.mouse.get_pos()[0]
      self.mouseY = pygame.mouse.get_pos()[1]
      
      if self.activeMenu != None:
        self.activeMenu.generate(self.screen, self.body)
        
      for event in pygame.event.get():
        for listener in self.listeners:
          if event.type == listener.eventType:
            listener.onEvent(event)

      pygame.display.update()

  
  def compareMenu(self, menu):
    if self.activeMenu == None:
      pass
    else:
      return self.activeMenu.name == menu
      
class Listener:
  def __init__(self, listenerManager, eventType):
    self.listenerManager = listenerManager
    self.eventType = eventType
    self.listenerManager.listeners.append(self)

  def onEvent(self, event):
    pass
