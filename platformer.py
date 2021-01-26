# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# Twitter: @ScissorMarks

# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

import pygame
import engine
import utils
import level
import scene

# constant variables
SCREEN_SIZE = (700,500)
DARK_GREY = (50,50,50)
MUSTARD = (209,206,25)

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Rik\'s Platform Game')
clock = pygame.time.Clock()

# game states = playing // win // lose
game_state = 'playing'

entities = []

# player
player_speed = 0
player_acceleration = 0.2

coin1 = utils.makeCoin(100,200)
coin2 = utils.makeCoin(200,250)

enemy = utils.makeEnemy(150,274)
enemy.camera = engine.Camera(420,10,200,200)
enemy.camera.setWorldPos(150,250)

player = utils.makePlayer(300,0)
player.camera = engine.Camera(10,10,400,400)
player.camera.setWorldPos(300,0)
player.camera.trackEntity(player)
player.score = engine.Score()
player.battle = engine.Battle()

cameraSys = engine.CameraSystem()

# lose if no players have lives remaining
def lostLevel(level):
    # level isn't lost if any player has a life left
    for entity in level.entities:
        if entity.type == 'player':
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    # level is lost otherwise
    return True

# win if no collectable items left
def wonLevel(level):
    # level isn't won if any collectable exists
    for entity in level.entities:
        if entity.type == 'collectable':
            return False
    # level isn't won otherwise
    return True

level1 = level.Level(
    platforms=[
        # middle
        pygame.Rect(100,300,400,50),
        # left
        pygame.Rect(100,250,50,50),
        # right
        pygame.Rect(450,250,50,50)
    ],
    entities = [
        player, enemy, coin1, coin2
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

level2 = level.Level(
    platforms=[
        # middle
        pygame.Rect(100,300,400,50)
    ],
    entities = [
        player, coin1
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

# set the current level
world = level1

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

running = True
while running:
# game loop

    if sceneManager.isEmpty():
        running = False
    sceneManager.input()
    sceneManager.update()
    sceneManager.draw(screen) 

    # -----
    # INPUT
    # -----

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == 'playing':

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y
        
        # player input
        keys = pygame.key.get_pressed()
        # a=left
        if keys[pygame.K_a]:
            new_player_x -= 2
            player.direction = 'left'
            player.state = 'walking'
        # d=right
        if keys[pygame.K_d]:
            new_player_x += 2
            player.direction = 'right'
            player.state = 'walking'
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player.state = 'idle'
        # w=jump (if on the ground)
        if keys[pygame.K_w] and player_on_ground:
            player_speed = -5
        
        # control zoom level of the player camera
        # zoom out
        if keys[pygame.K_q]:
            player.camera.zoomLevel -= 0.01
        # zoom in
        if keys[pygame.K_e]:
            player.camera.zoomLevel += 0.01

    # ------
    # UPDATE
    # ------

    if game_state == 'playing':

        # update animations
        for entity in world.entities:
            entity.animations.animationList[entity.state].update()

        # horizontal movement

        new_player_rect = pygame.Rect(new_player_x,player.position.rect.y,player.position.rect.width,player.position.rect.height)
        x_collision = False

        #...check against every platform
        for p in world.platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x
        
        # vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(int(player.position.rect.x), int(new_player_y) ,player.position.rect.width,player.position.rect.height)
        y_collision = False
        player_on_ground = False

        #...check against every platform
        for p in world.platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                # if the platform is below the player
                if p[1] > new_player_y:
                    # stick the player to the platform
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = int(new_player_y)

        # see if any coins have been collected
        player_rect = pygame.Rect(int(player.position.rect.x), int(player.position.rect.y), player.position.rect.width, player.position.rect.height)

        # collection system
        for entity in world.entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    world.entities.remove(entity)
                    player.score.score += 1

        # enemy system
        for entity in world.entities:
            if entity.type == 'dangerous':
                if entity.position.rect.colliderect(player_rect):
                    player.battle.lives -= 1
                    # reset player position
                    player.position.rect.x = 300
                    player.position.rect.y = 0
                    player_speed = 0

    if world.isWon():
        game_state = 'win'
    if world.isLost():
        game_state = 'lose'

    # ----
    # DRAW
    # ----

    #cameraSys.update(screen, world)

    #if game_state == 'win':
    #    drawText('You win!', 50, 50)
        
    #if game_state == 'lose':
    #    drawText('You lose!', 50, 50)

    clock.tick(60)

# quit
pygame.quit()