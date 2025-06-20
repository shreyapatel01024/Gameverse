import pygame
import random
import sys
import mysql.connector

# Initialize Pygame
pygame.init()

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@2424",
    database="gameverse"
)
cursor = conn.cursor()
if len(sys.argv) > 1:
    userid = sys.argv[1]
else:
    userid = ""


# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

#game id

global gameid
gameid=2
# Load Assets
forest_bg = pygame.image.load("assets/tressurehuntassets/Background.jpeg")
forest_bg = pygame.transform.scale(forest_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

tree_img = pygame.image.load("assets/tressurehuntassets/Tree.png")
tree_img = pygame.transform.scale(tree_img, (90, 120))

rock_img = pygame.image.load("assets/tressurehuntassets/stone.png")
rock_img = pygame.transform.scale(rock_img, (50, 50))

player_img = pygame.image.load("assets/tressurehuntassets/dog.jpeg")
player_img = pygame.transform.scale(player_img, (60, 60))

enemy_img = pygame.image.load("assets/tressurehuntassets/skeleton.jpeg")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

treasure_img = pygame.image.load("assets/tressurehuntassets/diamond.jpeg")
treasure_img = pygame.transform.scale(treasure_img, (30, 30))

player_img.set_colorkey((255, 255, 255))
enemy_img.set_colorkey((255, 255, 255))
treasure_img.set_colorkey((255, 255, 255))
tree_img.set_colorkey((255, 255, 255))
rock_img.set_colorkey((255, 255, 255))

# Load Sounds
pygame.mixer.init()
background_music = "assets/tressurehuntassets/backgroundmusic.mp3"
treasure_sound = pygame.mixer.Sound("assets/tressurehuntassets/tresure.mp3")
collision_sound = pygame.mixer.Sound("assets/tressurehuntassets/colision.mp3")
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loop infinitely

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forest Treasure Hunt")

# Player settings
player_pos = [100, 100]
player_vel = [0, 0]
player_acceleration = 0.5
player_max_speed = 15
player_friction = 0.1
score = 0

# Enemy settings
enemy_pos = [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]
enemy_speed = 1

# Collision Detection
def detect_collision(pos1, size1, pos2, size2):
    return (pos1[0] < pos2[0] + size2 and pos1[0] + size1 > pos2[0] and
            pos1[1] < pos2[1] + size2 and pos1[1] + size1 > pos2[1])

# Obstacle settings
obstacles = []

# Generate obstacles without overlap
def generate_obstacles():
    global obstacles
    obstacles = []
    while len(obstacles) < 5:
        new_obstacle = [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]
        if not any(detect_collision(new_obstacle, 50, obs, 50) for obs in obstacles):
            obstacles.append(new_obstacle)

# Generate treasure without spawning on an obstacle
def generate_treasure():
    while True:
        pos = [random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)]
        if not any(detect_collision(pos, 30, obs, 50) for obs in obstacles):
            return pos

treasure_pos = generate_treasure()

# Draw game elements
def draw_game():
    screen.blit(forest_bg, (0, 0))

    for i, obs in enumerate(obstacles):
        if i % 2 == 0:
            screen.blit(tree_img, obs)
        else:
            screen.blit(rock_img, obs)

    screen.blit(enemy_img, enemy_pos)
    screen.blit(player_img, player_pos)
    screen.blit(treasure_img, treasure_pos)

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Show game over screen
def show_game_over():
    font = pygame.font.SysFont(None, 72)
    cursor.execute(f"SELECT score FROM scores where user_id={userid} and game_id={gameid}")
    result = cursor.fetchone()
    if result:
        highest_score = result[0] or 0
    else:
        highest_score = 0

    if score > highest_score:
        cursor.execute(f"UPDATE scores SET score={score} WHERE user_id={userid} and game_id={gameid}")
        conn.commit()  # Don't forget to commit the changes to the database
        highest_score=score
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 1.5))

    pygame.display.flip()
    pygame.time.delay(3000)

# Main game loop
running = True
obstacle_spawned = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not obstacle_spawned:
        generate_obstacles()
        obstacle_spawned = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_vel[0] -= player_acceleration
    if keys[pygame.K_RIGHT]:
        player_vel[0] += player_acceleration
    if keys[pygame.K_UP]:
        player_vel[1] -= player_acceleration
    if keys[pygame.K_DOWN]:
        player_vel[1] += player_acceleration

    player_vel[0] *= (1 - player_friction)
    player_vel[1] *= (1 - player_friction)

    player_vel[0] = max(-player_max_speed, min(player_vel[0], player_max_speed))
    player_vel[1] = max(-player_max_speed, min(player_vel[1], player_max_speed))

    new_pos = [player_pos[0] + player_vel[0], player_pos[1] + player_vel[1]]

    if not any(detect_collision(new_pos, 40, obs, 50) for obs in obstacles):
        player_pos = new_pos

    if detect_collision(player_pos, 40, treasure_pos, 30):
        treasure_sound.play()
        treasure_pos = generate_treasure()
        score += 1

    enemy_pos[0] += (1 if enemy_pos[0] < player_pos[0] else -1) * enemy_speed
    enemy_pos[1] += (1 if enemy_pos[1] < player_pos[1] else -1) * enemy_speed

    if detect_collision(player_pos, 40, enemy_pos, 40):
        collision_sound.play()
        show_game_over()
        break

    draw_game()
    clock.tick(FPS)

pygame.quit()
cursor.close()
conn.close()
sys.exit()
