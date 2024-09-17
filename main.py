import pygame
import sys
import os

#text for screen s
def textscreens(text,x,y):
    FONT_SIZE = 22
    FONT = pygame.font.Font(None, FONT_SIZE)
    text_render = FONT.render(text, True, (0, 0, 0) )
    text_rect = text_render.get_rect(center = (x,y))
    screen.blit(text_render, text_rect)
    
    pygame.display.flip()

#startscreen
def startscreen():
    screen.fill((155,155,155))
    textscreens("Welcome to Spelling Bee", SCREEN_WIDTH //2, SCREEN_HEIGHT // 4 )
    pygame.display.flip()   
    clicked_key()   
    
#endscreen
def endscreen():
    screen.fill((155,155,155))
    textscreens(f"You guessed {len(correct_guesses)} out of {max_guesses} words correctly.", SCREEN_WIDTH //2, SCREEN_HEIGHT // 4 )
    textscreens(f"Words you missed:{missed_words}", SCREEN_WIDTH //2, SCREEN_HEIGHT // 2 )
    pygame.display.flip()
    clicked_key()

#move the bee closer to the honeycomb
def move_bee(bee_pos, target_pos, step):
    if bee_pos[1] > target_pos[1]:
        bee_pos[1] -= step
    return bee_pos
def clicked_key():
    pressed = True
    while pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pressed = False

# Initialize Pygame
pygame.init()


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spelling Bee Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT_SIZE = 32
FONT = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        
# Defining valid words
VALID_WORDS = {"flip","flop", "glop", "lipo", "pill", "ping", "loop", "poll", "polo", "poop", "poof", "goon", "long","ill"}

    
 #Game variables
letters = "PFGILNO"
user_input = ''
correct_guesses = set()
correct_guess_count = 0
max_guesses = len(VALID_WORDS)

#images
bee_image = pygame.image.load(os.path.join('images', 'bee.png')).convert_alpha()
honeycomb_image = pygame.image.load(os.path.join('images', 'honeycomb.png')).convert_alpha()

#sounds
ding_sound = pygame.mixer.Sound("sound/ding.mp3")

#positions of bee and honeycomb on screen
honeycomb_position = (SCREEN_WIDTH // 2     - honeycomb_image.get_width() // 2, 50)
bee_start_position = (SCREEN_WIDTH // 2 - bee_image.get_width() // 2, SCREEN_HEIGHT - 100)
bee_position = list(bee_start_position)

startscreen()
#game loop
running = True
while running:
    screen.fill(WHITE)

     # Draw the honeycomb image
    screen.blit(honeycomb_image, honeycomb_position)
    # Draw the bee image
    screen.blit(bee_image, bee_position)

    # Drawing the letters and user input
    letters_text = FONT.render(f"Letters: {letters}", True, BLACK)
    screen.blit(letters_text, (20, 20))

    input_text = FONT.render(f"Input: {user_input}", True, BLACK)
    screen.blit(input_text, (20, 80))


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input in VALID_WORDS and user_input not in correct_guesses:
                    correct_guesses.add(user_input)
                    correct_guess_count += 1
                    bee_position = move_bee(bee_position, honeycomb_position, SCREEN_HEIGHT // max_guesses)
                user_input = ''
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                running = False 
            else:
                user_input += event.unicode.lower()

    if bee_position[1] <= honeycomb_position[1]:
        ding_sound.play()
        missed_words = VALID_WORDS - correct_guesses
        endscreen()
        
        running = False
   
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()