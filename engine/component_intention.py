class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False
    def reset(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False