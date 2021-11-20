import time

import pygame
import os
import sys
import random

pygame.init()
# Global Constants
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # the_screan where we gonna display

# import the images
RUNNING = [pygame.image.load(os.path.join("Assets/Dinos", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dinos", "DinoRun2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dinos", "DinoJump.png"))

BG = pygame.image.load(os.path.join("Assets/other", "Track.png"))

FONT = pygame.font.SysFont("inkfree", 20)


class Dinosaure:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.img = img  # we want the dino to  be running by default and not jumpin' so!! we need to set dino run to true and jump to false
        self.dino_run = True
        self.dino_jup = False
        self.jump_vel = self.JUMP_VEL  # we need jumping coordinations we need a fct called rect
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(),
                                img.get_height())  # this function will put a rectangle arround our dino image
        # self.X_Pos and self.Y_pos refers to the top left corner
        self.step_index = 0  # it will help us loop through the image of dinno if it's running

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jup:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.img = JUMPING
        if self.dino_jup:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jup = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.img = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1  # when we count from 0 to 4 it will show the first dino image with the left leg raised then from 5 to  9 the second img which shows the right leg raised
        # when it's at 10 it resets

    def draw(self, SCREEN):
        SCREEN.blit(self.img, (self.rect.x, self.rect.y))


class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):

        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300


def remove(index):
    dinosaurs.pop(index)


def main():
    global game_speed, x_pos_bg, dinosaurs, obstacles, y_pos_bg, points, text2

    clock = pygame.time.Clock()
    points = 0
    dinosaures = [Dinosaure()]
    obstacles=[]
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score(text2):
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1  # to this rate we calculate the points
        text = FONT.render(f'Your Points =   {str(points)}', True, (255, 0, 0))

        SCREEN.blit(text, (950, 50))  # 81 and 82 to show the points on the screen

        SCREEN.blit(text2, (550, 00))

    def background():  # it makes the background looks like it's movin'
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width+2+ x_pos_bg,2+y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg =100
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))
        for dinos in dinosaures:
            dinos.update()
            dinos.draw(SCREEN)
        if len(dinosaures) == 0 :
            break
        #generate the cactus on our screen randomly
        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
        for obs in obstacles :
            obs.draw(SCREEN)
            obs.update()
            #if the dinos hits one of the cactus then he'll be removed from dinos list
            for i ,dinos in enumerate(dinosaures) :
                if dinos.rect.colliderect(obs.rect):

                    remove(i)

                else :
                    text2 = FONT.render(' !!  keep going  !!', True, (0, 0, 0))



        user_input = pygame.key.get_pressed()
        for i, dinos in enumerate(dinosaures):
            if user_input[pygame.K_SPACE]:
                dinos.dino_jup = True
                dinos.dino_run = False
        score(text2)
        background()
        clock.tick(25)
        pygame.display.update()


main()  # here we are calling the main methode at this rate if i run my code we'll get a blank screen so we will add the class DINOSAUR
