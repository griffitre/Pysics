import sys, pygame, time, math
from pygame.locals import QUIT
from ballswalls.boundaries import *
from ballswalls.classes import *
from listener.listenermanager import *
from listener.inputlistener import *
from listener.clicklistener import *

pygame.init()
pygame.display.set_caption('Physics Simulator')

screen = pygame.display.set_mode((500, 500))

bodyGeneral = BodyGeneral()
body = Body(bodyGeneral)
listenerManager = ListenerManager(body)
inputListener = InputListener(listenerManager)
clickListener = ClickListener(listenerManager)



listenerManager.listen()