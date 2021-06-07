from .system import *
from .engine import *

class TriggerSystem(System):

    def check(self, entity):
        return entity.hasComponent('position') and entity.hasComponent('triggers') # position is not None and entity.triggers is not None
    
    def updateEntity(self, screen, inputStream, entity):

        trg = entity.getComponent('triggers')
        pos = entity.getComponent('position')

        for trigger in trg.triggerList:

            trigger.last = trigger.current
            trigger.current = []

            if trigger.boundingBox is not None:

                adjustedRect = pygame.rect.Rect(
                    pos.rect.x + trigger.boundingBox.x,
                    pos.rect.y + trigger.boundingBox.y,
                    trigger.boundingBox.w,
                    trigger.boundingBox.h
                )

                for otherEntity in engine.world.entities:

                    if otherEntity.hasComponent('position') and otherEntity.hasComponent('collider'): #position is not None and otherEntity.collider is not None:
                        op = otherEntity.getComponent('position')
                        oc = otherEntity.getComponent('collider')
                        otherRect = pygame.rect.Rect(
                            op.rect.x + oc.rect.x,
                            op.rect.y + oc.rect.y,
                            oc.rect.w,
                            oc.rect.h
                        )

                        if adjustedRect.colliderect(otherRect):
                            trigger.current.append(otherEntity.ID)

                #print(trigger.current)
                
            if trigger.current and not trigger.last:
                trigger.onEnter(entity)
            elif not trigger.current and trigger.last:
                trigger.onExit(entity)
            elif trigger.current:
                trigger.onStay(entity)
            
                #print(world.getEntitiesByTagList(['player1'])[0].ID)
                            #trigger.onCollide(otherEntity)