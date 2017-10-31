# Lots of this code is based off of the sprite animation answer from https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images

#todo bitedown animation. Score display, health bar-display, link to val of health, create game gui- newgame,exit,

import os
import pygame
import random
pygame.init()

SIZE = WIDTH, HEIGHT = 1200, 800
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
soldierList = []
difficulty = 1


def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        size = (225, 133)  # This should match the size of the images.

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index].convert_alpha()  # 'image' is the current image of the animation.

        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt, player):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

        for i in soldierList:
            if player.rect.x >= i.rect.x:
                i.images = i.images_right
            elif player.rect.x < i.rect.x:
                i.images = i.images_left

    def update(self, dt, player):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt, player)
        




    def eat(self, player):
        deadSoldiers=[]
        playerX = player.rect.x
        global soldierList
        for i in soldierList:
            if player.images == player.images_right:
                print(player.images == player.images_right)
                if abs(i.rect.x-225 - playerX) < 50 :
                    deadSoldiers.append(i)
                   
            else:
                print(player.images == player.images_right)
                if abs(i.rect.x - playerX) < 50 :
                    deadSoldiers.append(i)
                    
                
        return deadSoldiers

def main():
    global soldierList
    global difficulty
    images = load_images(path='img/dino')  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(100, 575), images=images)
    playerEatImg = load_images(path='img/eat')
    bgImg = load_images(path='img/bg')
    bg = AnimatedSprite(position=(0, 0), images=bgImg)
    soldierImg = load_images(path='img/soldier')
    def addSoldier():
        for i in range(difficulty):
            soldierX = random.randint(50, 1150)
            soldier = AnimatedSprite(position=(soldierX, 650), images=soldierImg)
            soldierList.append(soldier)
    addSoldier()
    
    all_sprites = pygame.sprite.Group(bg, player,soldierList)  # Creates a sprite group and adds 'player' to it.

    def dinoEatAnim(player):
       
        playerEat = AnimatedSprite(position=(player.rect.x, 575), images=playerEatImg)
        if player.images == player.images_right:
             playerEat.images = playerEat.images_right
        else:
            playerEat.images = playerEat.images_left
        return playerEat


    running = True
    SCORE = 0
    health = 100
    myCounter = 0
    eatTimer = 50
    eating = False
    while running:
       # print('x=', player.rect.x)
        if player.rect.x<=0 or player.rect.x>=975:
            player.velocity.x =0

        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 4
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -4
                elif event.key == pygame.K_SPACE:
                    deadSoldiers = player.eat(player)
                    newList = []
                    for e in soldierList:
                        if e not in deadSoldiers:
                            newList.append(e)
                    playerEat = dinoEatAnim(player)
                    soldierList = newList
                    all_sprites = pygame.sprite.Group(bg, playerEat,soldierList)
                    eating = True
                    SCORE += len(deadSoldiers)
                    #print(SCORE)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
        
        if eating == True:
            
            eatTimer -= 1
            print('eatin = true:  ', eatTimer)
            if eatTimer == 0:
                all_sprites = pygame.sprite.Group(bg, player,soldierList)
                eatTimer =50
                eating = False
        myCounter += 1
        if (myCounter % 100 == 0):
            addSoldier()
            #shoot
            #all_sprites = pygame.sprite.Group(bg, player,soldierList)
            if myCounter == 2000:
                difficulty += 1
                myCounter = 0
        all_sprites.update(dt, player)  # Calls the 'update' method on all sprites in the list (currently just the player).

        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
