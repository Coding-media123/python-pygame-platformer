from .ui_action_listener import *
from .ui_text import *
from .colours import *

import pygame

class ButtonUI:

    def __init__(self, text, actionListener=None):

        self.actionListener = actionListener

        self.activeCurrent = False
        self.activePrevious = False
        
        self.pressedCurrent = False
        self.pressedPrevious = False

        self.activeLength = 15
        self.pressedTimer = 0

        self.execNextFrame = False

        self.normalColour = LIGHT_GREY
        self.activeColour = WHITE
        self.pressedColour = GREEN

        self.colour = self.normalColour

        self.width = 100
        self.height = 45
        self.text = text

    def update(self, active, pressed):

        self.activePrevious = self.activeCurrent
        self.activeCurrent = active
        activatedThisFrame = self.activeCurrent and not self.activePrevious
        deactivatedThisFrame = self.activePrevious and not self.activeCurrent

        self.pressedPrevious = self.pressedCurrent
        self.pressedCurrent = pressed
        pressedThisFrame = self.pressedCurrent and not self.pressedPrevious
        releasedThisFrame = self.pressedPrevious and not self.pressedCurrent

        if self.execNextFrame:
            self.execNextFrame = False
            self.actionListener.execute()

        if pressed:
            self.pressedTimer = self.activeLength
        
        if pressedThisFrame:
            self.execNextFrame = True

        if self.pressedTimer > 0:
            self.colour = self.pressedColour
            self.pressedTimer = max(0, self.pressedTimer - 1)
            if self.pressedTimer == 0:
                self.colour = self.activeColour

        if activatedThisFrame:
            self.colour = self.activeColour
        
        if deactivatedThisFrame:
            self.colour = self.normalColour
        
    def draw(self, screen, x, y):
        drawText(screen, self.text, x, y, self.colour, 255, align='center')