import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20 
GAP = 15
letters = [] 
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13)/ 2)
starty = 600
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
BUTTON_FONT = pygame.font.SysFont('comicsans', 50)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
word = random.choice(words)
guessed = []
hint_available = 0
hangman_status = 0
incorrect_guesses = 0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
HINT_COLOR = (100, 255, 100)  # Light green
HINT_HOVER = (70, 220, 70)    # Slightly darker green
HINT_TEXT = (240, 255, 240)   # Very light green text
RED = (255, 0, 0)             # For revealed hint letters

def reset_game():
    global hangman_status, word, guessed, letters, hint_available, incorrect_guesses
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    hint_available = 0
    incorrect_guesses = 0
    # Reset all letters to visible
    for letter in letters:
        letter[3] = True

def draw():
    win.fill(WHITE)
    # draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 30))

    # draw word with letters in red if they were hinted
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (500, 300))

    # draw letter buttons (skip letters that were guessed)
    for letter in letters:
        x, y, ltr, visible = letter 
        if visible and ltr not in guessed:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    
    # draw hint button if hints are available
    if hint_available > 0:
        draw_hint_button()
        
    # draw hint counter
    hint_text = LETTER_FONT.render(f"Hints: {hint_available}", 1, BLACK)
    win.blit(hint_text, (WIDTH - 150, 50))
        
    win.blit(images[hangman_status], (200, 150))
    pygame.display.update()

def draw_hint_button():
    button_width, button_height = 200, 60
    button_x = WIDTH - button_width - 30
    button_y = HEIGHT - button_height - 30
    
    # Check mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    hint_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    if hint_rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, HINT_HOVER, hint_rect, border_radius=10)
    else:
        pygame.draw.rect(win, HINT_COLOR, hint_rect, border_radius=10)
    
    pygame.draw.rect(win, BLACK, hint_rect, 2, border_radius=10)  # Border
    
    text = BUTTON_FONT.render("Use Hint", 1, HINT_TEXT)
    win.blit(text, (button_x + button_width//2 - text.get_width()//2, 
                   button_y + button_height//2 - text.get_height()//2))
    
    return hint_rect

def draw_end_buttons():
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    retry_y = HEIGHT // 2 + 50
    quit_y = HEIGHT // 2 + 130
    
    # Check mouse position for hover effects
    mouse_pos = pygame.mouse.get_pos()
    
    # Retry button
    retry_rect = pygame.Rect(button_x, retry_y, button_width, button_height)
    if retry_rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, DARK_GRAY, retry_rect, border_radius=10)
    else:
        pygame.draw.rect(win, GRAY, retry_rect, border_radius=10)
    pygame.draw.rect(win, BLACK, retry_rect, 2, border_radius=10)
    retry_text = BUTTON_FONT.render("Retry", 1, BLACK)
    win.blit(retry_text, (button_x + button_width//2 - retry_text.get_width()//2, 
                        retry_y + button_height//2 - retry_text.get_height()//2))
    
    # Quit button
    quit_rect = pygame.Rect(button_x, quit_y, button_width, button_height)
    if quit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, DARK_GRAY, quit_rect, border_radius=10)
    else:
        pygame.draw.rect(win, GRAY, quit_rect, border_radius=10)
    pygame.draw.rect(win, BLACK, quit_rect, 2, border_radius=10)
    quit_text = BUTTON_FONT.render("Quit", 1, BLACK)
    win.blit(quit_text, (button_x + button_width//2 - quit_text.get_width()//2, 
                        quit_y + button_height//2 - quit_text.get_height()//2))
    
    return retry_rect, quit_rect

def use_hint():
    global hint_available
    # Find letters in word that haven't been guessed yet
    available_letters = [letter for letter in word if letter not in guessed]
    if available_letters:
        # Choose a random letter to reveal
        hint_letter = random.choice(available_letters)
        guessed.append(hint_letter)  # Add directly to guessed list
        hint_available -= 1
        # Disable the corresponding letter button
        for letter in letters:
            if letter[2] == hint_letter:
                letter[3] = False

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = BUTTON_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 - 50))
    
    # Draw buttons
    retry_button, quit_button = draw_end_buttons()
    pygame.display.update()
    
    # Wait for user to click retry, quit, or close window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    waiting = False
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False
        pygame.time.delay(100)
    
    return True

def main():
    global hangman_status, word, guessed, hint_available, incorrect_guesses
    
    reset_game()  # Initialize game state
    
    FPS = 60 
    clock = pygame.time.Clock()
    run = True

    while run: 
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                
                # Check if hint button was clicked
                if hint_available > 0:
                    hint_rect = draw_hint_button()
                    if hint_rect.collidepoint((m_x, m_y)):
                        use_hint()
                        continue
                
                # Check letter buttons
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible and ltr not in guessed:  # Only interact with visible, non-guessed letters
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                                incorrect_guesses += 1
                                # Grant a hint for every 2 incorrect guesses
                                if incorrect_guesses % 2 == 0:
                                    hint_available += 1
        
        draw()

        won = True             
        for letter in word:
            if letter not in guessed:
                won = False
                break
    
        if won:
            if display_message("You WON!"):
                reset_game()
            else:
                run = False
            continue

        if hangman_status == 6:
            if display_message("You LOST!"):
                reset_game()
            else:
                run = False
            continue

while True:
    if not main():
        break
pygame.quit()