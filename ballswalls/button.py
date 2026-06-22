from ballswalls.boundaries import *
from listener.listenermanager import *
from listener.clicklistener import *
import pygame, sys


class Button(ListenerManager):
  def __init__(self, size, text, coords):
    self.size = size
    self.text = text
    self.coords = coords

  def onUpdate(self, screen):
    pass

