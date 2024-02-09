import pygame
import os
import random
import time
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
MENU_FONT = pygame.font.SysFont('comicsans', 60)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
MAX_BULLETS_bot = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_home_screen():
    WIN.blit(SPACE, (0, 0))
    
    # Draw 1-player button
    pygame.draw.rect(WIN, WHITE, (300, 350, 400, 80))
    start_text = MENU_FONT.render("Single player", True, BLACK)
    WIN.blit(start_text, (320, 345))

    # Draw 2-player button
    pygame.draw.rect(WIN, WHITE, (300, 150, 400, 80))
    start_text = MENU_FONT.render("2 player", True, BLACK)
    WIN.blit(start_text, (320, 145))

    pygame.display.update()


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def bot_yellow_handle_movement(direction, yellow):

    if direction == 'left' and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if direction == 'right' and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if direction == 'up' and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if direction == 'down' and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL
    

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()

    run = False
    game_mode = "1P"
    while (not run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # single player:
                if 300 <= mouse_x <= 700 and 350 <= mouse_y <= 430:
                    run = True
                # 2 player:
                elif 300 <= mouse_x <= 700 and 150 <= mouse_y <= 230:
                    game_mode = "2P"
                    run = True

        draw_home_screen()

    last_time = time.time()
    last_bot_bullet = time.time()
    bot_move_time = random.uniform(0.2, 0.5)
    direction = "none"
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS    and game_mode == "2P":
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()
        
        if abs(yellow.y - red.y) <= 50 and len(yellow_bullets) < MAX_BULLETS_bot and time.time() - last_bot_bullet >= 0.3    and game_mode == "1P":
            bullet = pygame.Rect(
                yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
            yellow_bullets.append(bullet)
            last_bot_bullet = time.time()
            #BULLET_FIRE_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        if game_mode == "2P":
            yellow_handle_movement(keys_pressed, yellow)
        else:
            bot_yellow_handle_movement(direction, yellow)
            if time.time() - last_time >= bot_move_time:
                last_time = time.time()
                direction = random.choice(["left", "right", "up", "down"])
                bot_move_time = random.uniform(0.2, 0.8)

        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
