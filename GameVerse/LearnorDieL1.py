import pygame
import sys
import io
import contextlib
from code import InteractiveInterpreter
import mysql.connector
from tkinter import messagebox
global level
level=1
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2424",
        database="gameverse"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")

gameid=3

if len(sys.argv) > 1:
        userid = sys.argv[1]
else:
        userid = ""
# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1250, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn or Die")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
HOVER_BLUE = (100, 149, 237)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Character attributes
char_x, char_y = 50, 350
char_width, char_height = 50, 50
char_velocity = 70
wrong_attempts = 0

# Font setup
font = pygame.font.Font(None, 36)
fontgameover= pygame.font.Font(None,50)
fontlevelcompleted= pygame.font.Font(None,43)
input_font = pygame.font.Font(None, 28)

# Interpreter desired output
DESIRED_OUTPUT = "Hello"

# User input storage
user_input = ""
cursor_position = 0  # Cursor position in the input string

# Interpreter dimensions
interpreter_x, interpreter_y = 780, 50
interpreter_width, interpreter_height = 450, 500
interpreter_padding = 10

# Button dimensions
button_width, button_height = 115, 55
button_x, button_y = interpreter_x + (interpreter_width - button_width) // 2, interpreter_y + interpreter_height - button_height - 27

# Python interactive interpreter setup
interpreter = InteractiveInterpreter()

# Background image and character image
background_image = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/backgroundgame.png')
background_image = pygame.transform.scale(background_image, (750, 500))
Rabbit = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/rabbit2.jpg')
Rabbit = pygame.transform.scale(Rabbit, (70, 70))
Bridge = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/bridge.png')
Bridge = pygame.transform.scale(Bridge, (150, 10))

wronganswer_sound = pygame.mixer.Sound('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/wronganswersound.mp3')
gameover_sound = pygame.mixer.Sound('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/Gameover.mp3')
gamewin_sound = pygame.mixer.Sound('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/Gamewinsound.mp3')


# Load background images
full_background_image = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/backgroundlod.jpg')
full_background_image = pygame.transform.scale(full_background_image, (WIDTH, HEIGHT))

interpreter_background_image = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/backgroundinterpreter.png')
interpreter_background_image = pygame.transform.scale(interpreter_background_image, (interpreter_width, interpreter_height))
# Define text area properties
text_start_x = interpreter_x + interpreter_padding + 35
text_start_y = interpreter_y + interpreter_padding + 30
# Adjust max width and max lines
max_width = interpreter_width - (text_start_x - interpreter_x) - interpreter_padding-20
max_lines = (interpreter_height - (text_start_y - interpreter_y)) // input_font.get_height()
# Load button background image
button_bg = pygame.image.load('C:/Users/SHIVAM JANI/Desktop/GameVerse/GameVerse/assets/runbuttonbackground.png')
button_bg = pygame.transform.scale(button_bg, (button_width, button_height))


def draw_game(cursor_visible, hover=False, click=False):
    """Draws the game screen with separate background images."""
    screen.blit(full_background_image, (0, 0))  # Full window background

    # Draw interpreter area background
    interpreter_background_image.set_colorkey((255, 255, 255))
    screen.blit(interpreter_background_image, (interpreter_x, interpreter_y))

    # Draw label on top of the interpreter
    label_text = font.render("Write Code Here", True, BLACK)
    label_x = interpreter_x + (interpreter_width - label_text.get_width()) // 2
    label_y = interpreter_y - 20  # Adjust the y position above the interpreter
    screen.blit(label_text, (label_x, label_y))

    # Draw rabbit area
    screen.blit(background_image, (1, 130))

    # Draw character
    Rabbit.set_colorkey((255, 255, 255))
    screen.blit(Rabbit, (char_x, char_y))

    # Adjust button size based on state
    adjusted_width, adjusted_height = button_width, button_height

    if hover:
        adjusted_width += 5  # Slightly increase on hover
        adjusted_height += 5
    if click:
        adjusted_width -= 5
        adjusted_height-= 5 # Slightly shrink on click

    button_bg_resized = pygame.transform.scale(button_bg, (adjusted_width, adjusted_height))
    button_bg_resized.set_colorkey((255, 255, 255))

    # Center adjusted button
    adjusted_x = button_x - (adjusted_width - button_width) // 2
    adjusted_y = button_y - (adjusted_height - button_height) // 2
    screen.blit(button_bg_resized, (adjusted_x, adjusted_y))

    # Render and center the button text
    button_text = font.render("Run", True, GRAY)
    text_x = adjusted_x + (adjusted_width - button_text.get_width()) // 2
    text_y = adjusted_y + (adjusted_height - button_text.get_height()) // 2
    screen.blit(button_text, (text_x, text_y))

    # Display instructions and attempts left
    instructions = font.render(f"Write Python code to print '{DESIRED_OUTPUT}'", True, BLACK)
    attempts_left = font.render(f"Attempts left: {3 - wrong_attempts}", True, BLACK)

    # Wrap text within interpreter
    wrapped_lines = []
    for line in user_input.split("\n"):
        while input_font.size(line)[0] > max_width:  # Check if line exceeds width
            split_index = len(line) - 1
            while input_font.size(line[:split_index])[0] > max_width:
                split_index -= 1
            wrapped_lines.append(line[:split_index])
            line = line[split_index:]
        wrapped_lines.append(line)

    # Limit lines to fit inside interpreter
    wrapped_lines = wrapped_lines[:max_lines]

    # Draw text and determine cursor position
    cursor_x, cursor_y = text_start_x, text_start_y
    cursor_pos_in_line = 0
    current_char_count = 0

    for i, line in enumerate(wrapped_lines):
        text_surface = input_font.render(line, True, BLACK)
        screen.blit(text_surface, (text_start_x, text_start_y + i * input_font.get_height()))

        # Find cursor position in wrapped text
        if cursor_position >= current_char_count and cursor_position <= current_char_count + len(line):
            cursor_pos_in_line = cursor_position - current_char_count
            cursor_x = text_start_x + input_font.size(line[:cursor_pos_in_line])[0]
            cursor_y = text_start_y + i * input_font.get_height()

        current_char_count += len(line) + 1  # +1 for newline

    # Draw cursor
    if cursor_visible:
        pygame.draw.line(screen, BLACK, (cursor_x, cursor_y),
                         (cursor_x, cursor_y + input_font.get_height()))

    screen.blit(instructions, (20, 20))
    screen.blit(attempts_left, (20, 60))
    pygame.display.flip()


def custom_interpreter(user_code):
    """Executes user code and checks if it generates the desired output."""
    try:
        fake_output = io.StringIO()  # Redirect stdout
        with contextlib.redirect_stdout(fake_output):
            interpreter.runsource(user_code, "<stdin>", "exec")
        result = fake_output.getvalue()
        return result.strip() == DESIRED_OUTPUT.strip()
    except Exception as e:
        print(f"Error executing user code: {e}")
        return False


def game_over():
    """Displays the game over screen with character animation."""
    global char_y
    while char_y < HEIGHT:
        screen.fill(WHITE)
        screen.blit(full_background_image, (0, 0))
        screen.blit(background_image, (1, 130))
        Rabbit.set_colorkey((255, 255, 255))
        screen.blit(Rabbit, (char_x, char_y))
        char_y += 10
        pygame.display.flip()
        clock.tick(30)
    screen.blit(full_background_image, (0, 0))
    game_over_text = fontgameover.render("Game Over!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 -100, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(3000)


def level_completed():
    """Displays the level completed screen and updates the database."""
    global level

    # Fetch the current level from the database
    cursor.execute("SELECT level FROM scores WHERE user_id = %s AND game_id = %s", (userid, gameid))
    fetched_level = cursor.fetchone()

    if fetched_level and fetched_level[0]==1:
        current_level = fetched_level[0]
        new_level = current_level + 1  # Increment the level
        # Update the database with the new level
        cursor.execute("UPDATE scores SET level = %s WHERE user_id = %s AND game_id = %s", (new_level, userid, gameid))
        db.commit()
    else:
        pass
        #new_level = 1   Default to level 1 if no record is found



    # Display the level completed message
    # screen.fill(WHITE)
    screen.blit(full_background_image, (0, 0))
    level_completed_text = fontlevelcompleted.render(f"Level 1 Completed!", True, DARK_BLUE)
    screen.blit(level_completed_text, (WIDTH // 2 - 130, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(6000)

    # Update the global level variable
    level = new_level



# Main game loop
running = True
cursor_visible = True
cursor_timer = 0
button_hover = False
button_click = False
pygame.key.set_repeat(200, 50)  # Set key repeat delay and interval
# max_width = interpreter_width - 2 * interpreter_padding - 10
# max_lines = (interpreter_height - 2 * interpreter_padding) // input_font.get_height()
while running:
    cursor_timer += clock.get_time()
    if cursor_timer >= 500:  # Toggle cursor visibility every 500ms
        cursor_visible = not cursor_visible
        cursor_timer = 0

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    draw_game(cursor_visible, hover=button_hover, click=button_click)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_position > 0:
                    user_input = user_input[:cursor_position - 1] + user_input[cursor_position:]
                    cursor_position -= 1
            elif event.key == pygame.K_RETURN:
                if user_input.count("\n") < max_lines - 1:  # Prevent exceeding max lines
                    user_input = user_input[:cursor_position] + "\n" + user_input[cursor_position:]
                    cursor_position += 1
            elif event.key == pygame.K_LEFT and cursor_position > 0:
                cursor_position -= 1
            elif event.key == pygame.K_RIGHT and cursor_position < len(user_input):
                cursor_position += 1
            elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                # Ignore Shift key presses
                pass
            else:
                current_line_index = user_input[:cursor_position].count("\n")
                wrapped_lines = user_input.split("\n")
                current_line = wrapped_lines[current_line_index] if current_line_index < len(wrapped_lines) else ""
                text_width = input_font.size(current_line + event.unicode)[0]

                if text_width < max_width:  # Allow only if within width
                    user_input = user_input[:cursor_position] + event.unicode + user_input[cursor_position:]
                    cursor_position += 1

        if event.type == pygame.MOUSEBUTTONDOWN and button_hover:
            button_click = True

        if event.type == pygame.MOUSEBUTTONUP:
            button_click = False
            if button_hover:
                if not custom_interpreter(user_input):
                    wrong_attempts += 1
                    if wrong_attempts < 3:
                        wronganswer_sound.play()
                    char_x += char_velocity
                    if wrong_attempts >= 3:
                        gameover_sound.play()
                        draw_game(cursor_visible)
                        game_over()
                        running = False
                else:
                    Bridge.set_colorkey((255, 255, 255))
                    screen.blit(Bridge, (276, 413))
                    gamewin_sound.play()
                    pygame.time.wait(1000)
                    level_completed()
                    running = False

                user_input = ""
                cursor_position = 0

    clock.tick(30)

pygame.quit()
sys.exit()