import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
display_font = pygame.font.SysFont('arial', 25)

class Movement(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Position = namedtuple('Position', 'x, y')

WHITE = (255, 255, 255)
DARK_RED = (200, 0, 0)
DEEP_BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

SEGMENT_SIZE = 20
GAME_PACE = 20

class HumanControlledSnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Challenge')
        self.timer = pygame.time.Clock()
        self.start_new_game()

    def start_new_game(self):
        self.current_direction = Movement.RIGHT
        self.snake_head = Position(self.width / 2, self.height / 2)
        self.snake_body = [self.snake_head,Position(self.snake_head.x - SEGMENT_SIZE, self.snake_head.y),
            Position(self.snake_head.x - (2 * SEGMENT_SIZE), self.snake_head.y)
        ]
        self.score = 0
        self.food_position = None
        self.set_food_location()

    def set_food_location(self):
        x = random.randint(0, (self.width - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
        y = random.randint(0, (self.height - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
        self.food_position = Position(x, y)
        if self.food_position in self.snake_body:
            self.set_food_location()

    def game_iteration(self):
        self.handle_events()
        self.move_snake()
        self.render_game()
        self.timer.tick(GAME_PACE)
        return self.check_game_over(), self.score

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def move_snake(self):
        x, y = self.snake_head.x, self.snake_head.y
        if self.current_direction == Movement.RIGHT:
            x += SEGMENT_SIZE
        elif self.current_direction == Movement.LEFT:
            x -= SEGMENT_SIZE
        elif self.current_direction == Movement.DOWN:
            y += SEGMENT_SIZE
        elif self.current_direction == Movement.UP:
            y -= SEGMENT_SIZE
        self.snake_head = Position(x, y)

    def render_game(self):
        self.screen.fill(BLACK)
        for segment in self.snake_body:
            pygame.draw.rect(self.screen, DEEP_BLUE, pygame.Rect(segment.x, segment.y, SEGMENT_SIZE, SEGMENT_SIZE))
            pygame.draw.rect(self.screen, LIGHT_BLUE, pygame.Rect(segment.x + 4, segment.y + 4, 12, 12))
        pygame.draw.rect(self.screen, DARK_RED, pygame.Rect(self.food_position.x, self.food_position.y, SEGMENT_SIZE, SEGMENT_SIZE))
        score_text = display_font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, [0, 0])
        pygame.display.update()

if __name__ == '__main__':
    game = HumanControlledSnakeGame()
    while True:
        game_over, score = game.game_iteration()
        if game_over:
            break
    print('Final Score:', score)
    pygame.quit()
