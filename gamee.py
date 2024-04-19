import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
game_font = pygame.font.SysFont('arial', 25)

class Movement(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Coordinates = namedtuple('Coordinates', 'x, y')

# Color definitions for the display
WHITE = (255, 255, 255)
RED = (200, 0, 0)
NAVY_BLUE = (0, 0, 255)
SKY_BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

block_size = 20  # Size of each square block
GAME_SPEED = 40  # Speed of the game

class AutomatedSnakeGame: # Class for controlling the Snake game logic for AI implementation.  

    def __init__(self, width=640, height=480): # Setup the game with specified width and height.
        self.width = width
        self.height = height
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Automated Snake Game')
        self.game_timer = pygame.time.Clock()
        self.restart_game()

    def restart_game(self): # Resets the game environment to start a new game.
        self.current_direction = Movement.RIGHT
        self.snake_head = Coordinates(self.width / 2, self.height / 2)
        self.snake_body = [self.snake_head,Coordinates(self.snake_head.x - block_size, self.snake_head.y),
            Coordinates(self.snake_head.x - (2 * block_size), self.snake_head.y)
        ]
        self.current_score = 0
        self.food_position = None
        self.set_food_location()
        self.iteration_number = 0

    def set_food_location(self): # Randomly places food item on the game board.
        x = random.randint(0, (self.width - block_size) // block_size) * block_size
        y = random.randint(0, (self.height - block_size) // block_size) * block_size
        self.food_position = Coordinates(x, y)
        if self.food_position in self.snake_body:
            self.set_food_location()

    def execute_game_step(self, action): # Updates the game state based on AI's action choice.
        self.iteration_number += 1
        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.update_snake_direction(action)
        self.update_positions()
        self.draw_game_elements()
        self.game_timer.tick(GAME_SPEED)
        return self.evaluate_action()

    def update_snake_direction(self, action): # Change snake's direction based on provided action.
        directions = [Movement.RIGHT, Movement.DOWN, Movement.LEFT, Movement.UP]
        current_index = directions.index(self.current_direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = directions[current_index]  # No change
        elif np.array_equal(action, [0, 1, 0]):
            new_direction = directions[(current_index + 1) % 4]  # Right turn
        else:  # Turn left
            new_direction = directions[(current_index - 1) % 4]

        self.current_direction = new_direction
        x, y = self.snake_head.x, self.snake_head.y
        if self.current_direction == Movement.RIGHT:
            x += block_size
        elif self.current_direction == Movement.LEFT:
            x -= block_size
        elif self.current_direction == Movement.DOWN:
            y += block_size
        elif self.current_direction == Movement.UP:
            y -= block_size

        self.snake_head = Coordinates(x, y)

    def draw_game_elements(self):  # Redraws the game window with updated snake and food positions.
        self.game_display.fill(BLACK)
        for coord in self.snake_body:
            pygame.draw.rect(self.game_display, NAVY_BLUE, pygame.Rect(coord.x, coord.y, block_size, block_size))
            pygame.draw.rect(self.game_display, SKY_BLUE, pygame.Rect(coord.x + 4, coord.y + 4, 12, 12))

        pygame.draw.rect(self.game_display, RED, pygame.Rect(self.food_position.x, self.food_position.y, block_size, block_size))
        score_text = game_font.render("Score: " + str(self.current_score), True, WHITE)
        self.game_display.blit(score_text, [0, 0])
        pygame.display.flip()
