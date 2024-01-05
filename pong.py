import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')


# Paddle Class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


# Ball Class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy = -self.dy

        # Reset ball if it goes past paddles
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.rect.x, self.rect.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            self.dx = random.choice([-4, 4])
            self.dy = random.choice([-4, 4])

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def collision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.dx = -self.dx


# Create paddles and ball
player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Game loop
running = True
paused = False
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    if not paused:
        # Move player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move(-5)
        if keys[pygame.K_DOWN]:
            player_paddle.move(5)

    # Move player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.move(-5)
    if keys[pygame.K_DOWN]:
        player_paddle.move(5)

    # Simple AI Movement
    if ai_paddle.rect.centery < ball.rect.y:
        ai_paddle.move(4)
    elif ai_paddle.rect.centery > ball.rect.y:
        ai_paddle.move(-4)

    # Drawing
    screen.fill(BLACK)
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    if paused:
        # Display a pause message
        font = pygame.font.Font(None, 74)
        text = font.render('Paused', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    # Move ball and check for collisions
    ball.move()
    ball.collision_with_paddle(player_paddle)
    ball.collision_with_paddle(ai_paddle)

    # Drawing
    screen.fill(BLACK)
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
