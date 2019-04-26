#!/usr/bin/env python

import pygame
import time
import random as rd
import tkinter as tk
from tkinter import messagebox

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480   # set the window size


class Snake:

    HORIZONTAL_DIRECTION = ['left', 'right']    # define the four snake's moving direction
    VERTICAL_DIRECTION = ['up', 'down']
    WIDTH = 20

    def __init__(self):
        self.move_distance = 10                 # one step moving length
        self.food_color = (255, 0, 0)           # food color: red
        self.reset()

    def reset(self):
        self.head = [100, 100]  # the position of the first-time snake head
        self.body = []
        for i in range(5):
            self.body.insert(0, [self.head[0] - i * self.WIDTH, self.head[1]])
        
        self.generated_food = []
        self.current_direction = 'right'        # the first moving direction is always right
        self.speed = 10
        self.map = {}                           # generate the screen into a map
        for x in range(32):
            for y in range(24):
                self.map[(x, y)] = 0
        self.generate_food()
        self.game_status = "stop"

    def check_status(self):                     # check the game status
        if self.body.count(self.head) > 1:      # check if the snake eat itself
            return True
        if self.head[0] < 0 or self.head[0] > 620 or self.head[1] < 0 or self.head[1] > 460:
            return True                         # check the snake whether it hit the boundary od the screen
        return False

    def move(self):                             # move the snake head
        if self.current_direction in self.HORIZONTAL_DIRECTION:
            if self.current_direction == self.HORIZONTAL_DIRECTION[0]:
                self.head[0] -= self.move_distance
            else:
                self.head[0] += self.move_distance
        else:
            if self.current_direction == self.VERTICAL_DIRECTION[0]:
                self.head[1] -= self.move_distance
            else:
                self.head[1] += self.move_distance

    def calculate_taken_position(self):
        for x, y in self.body:
            self.map[(x // self.WIDTH, y // self.WIDTH)] = 1

    def generate_food(self):                          # when the snake head hit the food then generate a new food
        if len(self.body) // 16 > 4:
            self.speed = len(self.body) // 16
        self.calculate_taken_position()

        empty_position = []                           # find the empty position to generate new food (at random)
        for position in self.map.keys():
            if not self.map[position]:
                empty_position.append(position)

        random = rd.choice(empty_position)
        self.generated_food = [random[0] * self.WIDTH, random[1] * self.WIDTH]

    def check_direction(self, changed_direction):     # check the snake's moving direction
        if self.current_direction in self.HORIZONTAL_DIRECTION:
            if changed_direction in self.VERTICAL_DIRECTION:
                self.current_direction = changed_direction
        else:
            if changed_direction in self.HORIZONTAL_DIRECTION:
                self.current_direction = changed_direction

    def words_setting(self, pygame):                  # set the game screen word
        font_of_title = pygame.font.SysFont('arial', 60)
        self.welcome_words = font_of_title.render('Snake Game', True, (0, 0, 0))
        font_of_tips = pygame.font.SysFont('arial', 40)
        self.start_words = font_of_tips.render('Start', True, (0, 0, 0))
        self.close_game_words = font_of_tips.render('ESC to exit', True, (0, 0, 0))
        self.gameover_words = font_of_tips.render('Game Over', True, (255, 0, 0))
        self.restart_words = font_of_tips.render('Click Here To Restart', True, (255, 0, 0))

    def run(self, pygame, screen):
        if self.game_status == "run":
            self.move()
            self.body.append(self.head[:])
            if self.head == self.generated_food:
                self.generate_food()                  # check if the snake eat the food
            else:
                self.body.pop(0)
            for x, y in self.body:                    # draw the snake and food on the screen
                pygame.draw.rect(screen, [0, 0, 0], [x, y, self.WIDTH, self.WIDTH], 0)
            pygame.draw.rect(screen, self.food_color, [self.generated_food[0], self.generated_food[1], self.WIDTH, self.WIDTH], 0)
            if self.check_status():
                self.reset()
                screen.blit(self.gameover_words, ((WINDOW_WIDTH - self.gameover_words.get_width())/2, (WINDOW_HEIGHT - self.gameover_words.get_height())/2))
                screen.blit(self.restart_words, ((WINDOW_WIDTH - self.restart_words.get_width())/2, (WINDOW_HEIGHT - self.gameover_words.get_height())/2 + 50))
                pygame.display.update()
                self.game_status = "finish"
        elif self.game_status == "stop":
            screen.blit(self.welcome_words, ((WINDOW_WIDTH - self.welcome_words.get_width())/2, 100))
            screen.blit(self.start_words, ((WINDOW_WIDTH - self.start_words.get_width())/2, 310))
            screen.blit(self.close_game_words, ((WINDOW_WIDTH - self.close_game_words.get_width())/2, 350))
        else:
            return
        pygame.display.update()
        pygame.time.Clock().tick(self.speed)


def main():
    
    pygame.init()
    pygame.mixer.init()
    snake = Snake()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake')
    new_direction = snake.current_direction
    snake.words_setting(pygame)
    background_image = pygame.image.load("BackgroundIMG.jpg")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if snake.game_status == "run":
                    pressed_direction = ""
                    if event.key == pygame.K_LEFT:
                        pressed_direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        pressed_direction = "right"
                    elif event.key == pygame.K_UP:
                        pressed_direction = "up"
                    elif event.key == pygame.K_DOWN:
                        pressed_direction = "down"
                    if pressed_direction != "":
                        snake.check_direction(pressed_direction)
            elif (snake.game_status == "stop") and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ((WINDOW_WIDTH - snake.start_words.get_width())/2) <= x <= (((WINDOW_WIDTH - snake.start_words.get_width())/2) + snake.start_words.get_width()):
                    if (310) <= y <= (310 + snake.start_words.get_height()):
                        snake.game_status = "run"
            elif (snake.game_status == "finish") and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ((WINDOW_WIDTH - snake.restart_words.get_width())/2) <= x <= (((WINDOW_WIDTH - snake.restart_words.get_width())/2) + snake.restart_words.get_width()):
                    if ((WINDOW_HEIGHT - snake.restart_words.get_height())/2 + 50) <= y <= (((WINDOW_HEIGHT - snake.restart_words.get_height())/2 + 50) + snake.restart_words.get_height()):
                        snake.game_status = "run"
        
        screen.blit(background_image, [0, 0])
        snake.run(pygame, screen)

        
if __name__ == '__main__':
    main()
