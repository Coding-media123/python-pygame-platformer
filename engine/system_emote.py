from .system import System

class EmoteSystem(System):

    def setRequirements(self):
        self.requiredComponents = ['emote']
    
    def updateEntity(self, entity):
        em = entity.getComponent('emote')
        em.update()
        if em.destroy:
            em = None