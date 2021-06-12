import pygame
import globals
import utils
from .system import *
from .colours import *
import random

class InputSystem(System):

    def setRequirements(self):
        self.requiredComponents = ['input', 'intention']
    
    def updateEntity(self, entity):
        #if entity.input.inputFunc is not None:
        #    entity.input.inputFunc(inputStream, entity)
        if entity.getComponent('input').inputFunc is not None:
            entity.getComponent('input').inputFunc(entity)
        
