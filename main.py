import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Asset Loading
try:
    background = pygame.image.load('bg.png')
    playerImg = pygame.image.load('player1.png')
    bulletImg = pygame.image.load('bullet.png')
    enemyImg = [pygame.image.load('enemy.png') for _ in range(6)]
    # These match your filenames exactly
    bullet_sound = pygame.mixer.Sound('Laser.mp3')
    explosion_sound = pygame.mixer.Sound('Explosion.mp3')
except Exception as e:
    print(f"Error loading files: {e}")
    bullet_sound = None
    explosion_sound = None

pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()

# Player
playerX = 370
playerY = 380
playerX_change = 0

# Enemies
enemyX = [random.randint(0, 736) for _ in range(6)]
enemyY = [random.randint(50, 150) for _ in range(6)]
enemyX_change = [4 for _ in range(6)]
enemyY_change = [40 for _ in range(6)]

# Bullet
bulletX = 0
bulletY = 380
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                if bullet_sound: bullet_sound.play()
                bulletX = playerX
                bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, 736))

    for i in range(6):
        if enemyY[i] > 340:
            for j in range(6):
                enemyY[j] = 2000
            game_over_text()
            break

        speed_multiplier = 1 + (score_value // 5) * 0.2
        enemyX[i] += enemyX_change[i] * speed_multiplier
        
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        distance = math.sqrt((math.pow(enemyX[i] - bulletX, 2)) + (math.pow(enemyY[i] - bulletY, 2)))
        if distance < 27:
            if explosion_sound: explosion_sound.play()
            bulletY = 380
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))

    if bulletY <= 0:
        bulletY = 380
        bullet_state = "ready"
    if bullet_state == "fire":
        screen.blit(bulletImg, (bulletX + 16, bulletY + 10))
        bulletY -= bulletY_change

    screen.blit(playerImg, (playerX, playerY))
    show_score(10, 10)
    pygame.display.update()

pygame.quit()