import pygame
import sys
import random
import os
import math

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game Variables
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = -4
PIPE_SPAWN_TIME = 1500  # milliseconds

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rotation = 0
        self.bird_img = pygame.image.load('flapp-removebg-preview.png')
        # Scale down the bird image
        self.bird_img = pygame.transform.scale(self.bird_img, (34, 24))
        self.rect = self.bird_img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def jump(self):
        self.velocity = BIRD_JUMP
        self.rotation = 45

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        # Rotate bird based on velocity with smoother transitions
        if self.velocity < 0:
            self.rotation = min(self.rotation + 3, 30)
        else:
            self.rotation = max(self.rotation - 3, -45)

    def draw(self, screen):
        # Rotate bird image
        rotated_bird = pygame.transform.rotate(self.bird_img, self.rotation)
        # Get new rect for rotated image
        rotated_rect = rotated_bird.get_rect(center=self.rect.center)
        screen.blit(rotated_bird, rotated_rect)  # Temporary rectangle for bird

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, 350)
        self.top_height = self.gap_y - 100
        self.bottom_y = self.gap_y + 100
        self.width = 80  # Increased from 52 to 80 for thicker pipes
        # Load and scale pipe image
        self.pipe_img = pygame.image.load('pipe-removebg-preview.png')
        self.pipe_img = pygame.transform.scale(self.pipe_img, (self.width, 320))
        # Create flipped version for top pipe
        self.pipe_img_flipped = pygame.transform.flip(self.pipe_img, False, True)
        # Create collision rectangles with proper dimensions
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, self.bottom_y, self.width, WINDOW_HEIGHT - self.bottom_y)
        self.scored = False  # Initialize scored attribute to prevent AttributeError

    def update(self):
        self.x += PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        # Draw top pipe (flipped)
        screen.blit(self.pipe_img_flipped, (self.x, self.top_height - 320))
        # Draw bottom pipe
        screen.blit(self.pipe_img, (self.x, self.bottom_y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.background_img = pygame.image.load('images.png')
        self.background_img = pygame.transform.scale(self.background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(50, WINDOW_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.last_pipe = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.bird.jump()

    def spawn_pipe(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > PIPE_SPAWN_TIME:
            self.pipes.append(Pipe(WINDOW_WIDTH))
            self.last_pipe = current_time

    def check_collisions(self):
        # Ground collision
        if self.bird.y >= WINDOW_HEIGHT - self.bird.rect.height:
            self.bird.y = WINDOW_HEIGHT - self.bird.rect.height
            self.game_over = True
        # Ceiling collision
        elif self.bird.y <= 0:
            self.bird.y = 0
            self.game_over = True

        # Pipe collisions with adjusted hitbox
        bird_hitbox = self.bird.rect.inflate(-10, -10)  # Smaller hitbox for more forgiving collisions
        for pipe in self.pipes:
            if pipe.top_rect.colliderect(bird_hitbox) or \
               pipe.bottom_rect.colliderect(bird_hitbox):
                self.game_over = True

    def update(self):
        if not self.game_over:
            self.bird.update()
            self.spawn_pipe()
            
            # Update pipes and remove off-screen pipes
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -52]
            for pipe in self.pipes:
                pipe.update()
                # Score when passing pipes - check if bird has passed the middle of the pipe
                if not pipe.scored and self.bird.x > pipe.x + (pipe.width / 2):
                    self.score += 1
                    pipe.scored = True

            self.check_collisions()

    def draw(self):
        # Draw background image
        self.screen.blit(self.background_img, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(self.score), True, BLACK)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2, 50))

        if self.game_over:
            game_over_text = font.render('Game Over! Press SPACE', True, BLACK)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()