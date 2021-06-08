import engine
import scene_win
import scene_lose
import gamesystems
import scene_fade_transition
import globals

class GameScene(engine.Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = gamesystems.CollectionSystem()
        self.battleSystem = gamesystems.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()
        self.powerupSystem = gamesystems.PowerupSystem()
        self.traumaSystem = engine.TraumaSystem()
        self.particleSystem = engine.ParticleSystem()
        self.emoteSystem = engine.EmoteSystem()
        self.textSystem = engine.TextSystem()
        self.triggerSystem = engine.TriggerSystem()
    def onEnter(self):
        engine.soundManager.playMusicFade('dawn')
    def input(self, sm):
        if engine.inputManager.isPressed(engine.keys.esc):
            sm.pop()
            sm.push(scene_fade_transition.FadeTransitionScene([self], []))
        if globals.world.isWon():
            # update the level select map accessible levels
            nextLevel = min(globals.curentLevel+1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
            sm.push(scene_win.WinScene())
        if globals.world.isLost():
            sm.push(scene_lose.LoseScene())
    def update(self, sm):
        self.inputSystem.update()
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()
        self.powerupSystem.update()
        self.traumaSystem.update()
        self.emoteSystem.update()
        self.textSystem.update()
        self.triggerSystem.update()
    def draw(self, sm, screen):
        # background
        screen.fill(engine.BLACK)
        self.cameraSystem.update(screen)
        self.particleSystem.update(screen)