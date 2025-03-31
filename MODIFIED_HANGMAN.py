
# =====Developer Hangman Game=====

# A Python implementation of Hangman using Pygame featuring:
# - Interactive letter buttons
# - Visual hangman progression
# - Hint system (earned after incorrect guesses)
# - Win/lose detection with restart options


import math
import random
import pygame


# Initialize pygame and set up the game window
pygame.init()
WIDTH, HEIGHT = 1200, 800  # Window dimensions
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Developer Hangman")


# ========== GAME CONSTANTS ==========
RADIUS = 20      # Radius of letter buttons
GAP = 15         # Gap between letter buttons
A = 65           # ASCII value for 'A' (used to generate letters)
# Word bank
WORDS = ["IDE", "PIP", "IPO", "CODE", "JADE", "RAIL", "REPLIT", "PYTHON", "PYGAME", "SOFTWARE", "CONUNDRUM", "DEVELOPER", "INTERFACE", "COMPILER", "PROTOCOL"] 


# Colour definitions (RGB values)
WHITE = (255, 255, 255)       # Background
BLACK = (0, 0, 0)             # Text and outlines
GRAY = (200, 200, 200)        # Quit & Retry buttons colour
GREEN = (100, 255, 100)  # Hint button colour



def initialize_letter_buttons():
    
    # Creates and positions all letter buttons in two rows.

    buttons = []
    # Calculate starting x position to center the buttons horizontally
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 600  # Vertical position of first button row
    
    # Create buttons for A-Z (26 letters)
    for i in range(26):
        # Position calculation:
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        buttons.append([x, y, chr(A + i), True])  # [x, y, letter, visible]
    
    return buttons


# ========== GAME INITIALIZATION ==========
letters = initialize_letter_buttons()  # Create all letter buttons

# Font setup for different text elements
LETTER_FONT = pygame.font.SysFont('comicsans', 40)   # Letter buttons
WORD_FONT = pygame.font.SysFont('comicsans', 60)     # Word display
TITLE_FONT = pygame.font.SysFont('comicsans', 70)    # Game title
BUTTON_FONT = pygame.font.SysFont('comicsans', 50)   # Action buttons

# Load hangman images (states 0-6)
images = []
for i in range(7):
    try:
        image = pygame.image.load(f"hangman{i}.png")
        images.append(image)
    except FileNotFoundError:
        # Fallback if images not found - create blank surface
        blank_image = pygame.Surface((200, 400))
        blank_image.fill(WHITE)
        images.append(blank_image)


def reset_game():
    
    # Resets all game variables to their initial state for a new game.
    # Global variables affected:
       # - hangman_status: Reset to starting image
       # - word: New random word selected
       # - guessed: Empty list for new guesses
       # - hint_available: Reset hint counter
       # - incorrect_guesses: Reset mistake counter
    # Also reactivates all letter buttons.
   
    global hangman_status, word, guessed, hint_available, incorrect_guesses
    
    hangman_status = 0          # Reset hangman image to first state
    word = random.choice(WORDS) # Select new random word
    guessed = []                # Clear guessed letters
    hint_available = 0          # Reset hint counter
    incorrect_guesses = 0       # Reset mistake counter
    
    # Reactivate all letter buttons
    for letter in letters:
        letter[3] = True


def draw_end_buttons():
    
    # Draws the end game buttons (Retry and Quit) 
   
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2  # Center horizontally
    retry_y = HEIGHT // 2 + 50   # Retry button vertical position
    quit_y = HEIGHT // 2 + 130   # Quit button vertical position
    
    # ===== RETRY BUTTON =====
    retry_rect = pygame.Rect(button_x, retry_y, button_width, button_height)

    # Colour the Retry Button Gray
    pygame.draw.rect(win, GRAY, retry_rect, border_radius=10)
    
    # Button border
    pygame.draw.rect(win, BLACK, retry_rect, 2, border_radius=10)
    
    # Button text 
    retry_text = BUTTON_FONT.render("Retry", 1, BLACK)
    win.blit(retry_text, (button_x + button_width // 2 - retry_text.get_width() // 2,
                          retry_y + button_height // 2 - retry_text.get_height() // 2))
    
    # ===== QUIT BUTTON =====
    quit_rect = pygame.Rect(button_x, quit_y, button_width, button_height)

    # Colour the Quit Button Gray
    pygame.draw.rect(win, GRAY, quit_rect, border_radius=10)
    
    # Button border
    pygame.draw.rect(win, BLACK, quit_rect, 2, border_radius=10)
    
    # Button text 
    quit_text = BUTTON_FONT.render("Quit", 1, BLACK)
    win.blit(quit_text, (button_x + button_width // 2 - quit_text.get_width() // 2,
                         quit_y + button_height // 2 - quit_text.get_height() // 2))
    
    return retry_rect, quit_rect


def draw():
    
    # Handles all rendering to the game window including:
    # - Title display
    # - Word display with blanks/guessed letters
    # - Letter buttons
    # - Hint system
    # - Hangman image

    win.fill(WHITE)  # Clear screen with white background
    
    # ===== TITLE =====
    title_text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 30))

    # ===== WORD DISPLAY =====
    display_word = ""
    for letter in word:
        # Show letter if guessed, underscore if not
        display_word += letter + " " if letter in guessed else "_ "
    
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (500, 300))  # Center the word display

    # ===== LETTER BUTTONS =====
    for letter in letters:
        x, y, ltr, visible = letter 
        # Only draw visible, unguessed letters
        if visible and ltr not in guessed:
            # Draw button outline
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            # Draw letter centered in button
            letter_text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(letter_text, (x - letter_text.get_width() / 2, 
                                  y - letter_text.get_height() / 2))
    
    # ===== HINT SYSTEM =====
    if hint_available > 0:
        draw_hint_button()  # Show hint button if hints available
        
    # Display remaining hint count
    hint_text = LETTER_FONT.render(f"Hints: {hint_available}", 1, BLACK)
    win.blit(hint_text, (WIDTH - 150, 50))
        
    # ===== HANGMAN IMAGE =====
    # Show current hangman state (0-6)
    win.blit(images[hangman_status], (200, 150))
    
    pygame.display.update()  # Refresh the display


def draw_hint_button():
    
    # Draws the hint button at bottom right of screen.
    
    button_width, button_height = 200, 60
    button_x = WIDTH - button_width - 30  # Right side position
    button_y = HEIGHT - button_height - 30  # Bottom position
    
    # Create button rectangle for collision detection
    hint_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Colour the Hint Button Green
    pygame.draw.rect(win, GREEN, hint_rect, border_radius=10)
    
    # Button border
    pygame.draw.rect(win, BLACK, hint_rect, 2, border_radius=10)
    
    # Button text 
    text = BUTTON_FONT.render("Use Hint", 1, BLACK)
    win.blit(text, (button_x + button_width // 2 - text.get_width() // 2,
                   button_y + button_height // 2 - text.get_height() // 2))
    
    return hint_rect


def use_hint():
    
    # Reveals a random unguessed letter from the word.
    # Effects:
        # - Decrements hint counter
        # - Adds letter to guessed list
        # - Disables corresponding letter button
    # Only works if there are available hints and letters left to reveal.
  
    global hint_available
    
    # Get letters in word that haven't been guessed
    available_letters = [letter for letter in word if letter not in guessed]
    
    if available_letters:
        # Randomly select one letter to reveal
        hint_letter = random.choice(available_letters)
        guessed.append(hint_letter)  # Mark as guessed
        hint_available -= 1          # Use one hint
        
        # Disable the button for the revealed letter
        for letter in letters:
            if letter[2] == hint_letter:
                letter[3] = False


def display_message(message):
    
    # Shows endgame message (win/lose) with retry/quit options.

    pygame.time.delay(1000)  # Pause briefly before showing message
    
    win.fill(WHITE)  # Clear screen
    text = BUTTON_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2,
                    HEIGHT / 2 - text.get_height() / 2 - 50))
    
    # Draw action buttons and get their click areas
    retry_button, quit_button = draw_end_buttons()
    pygame.display.update()
    
    # Wait for player decision
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
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False
        pygame.time.delay(100)
    
    return True


def main():
    # Main game loop controlling the game flow and state. 
    global hangman_status, word, guessed, hint_available, incorrect_guesses
    
    reset_game()  # Initialize game state
    clock = pygame.time.Clock()
    run = True

    while run: 
        clock.tick(60)  # Cap at 60 FPS

        # ===== EVENT HANDLING =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                
                # Hint button click check
                if hint_available > 0:
                    hint_rect = draw_hint_button()
                    if hint_rect.collidepoint((m_x, m_y)):
                        use_hint()
                        continue
                
                # Letter button click check
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible and ltr not in guessed:
                        # Calculate distance from click to button center
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:  # Click was inside button
                            letter[3] = False  # Disable button
                            guessed.append(ltr)
                            
                            if ltr not in word:  # Incorrect guess
                                hangman_status += 1
                                incorrect_guesses += 1
                                # Grant hint after every 2 incorrect guesses
                                if incorrect_guesses % 2 == 0:
                                    hint_available += 1
        
        draw()  # Update display

        # ===== WIN/LOSE CHECK =====
        # Check if all letters in word have been guessed
        won = all(letter in guessed for letter in word)
    
        if won:
            if display_message("You WON!"):
                reset_game()  # Restart if player chooses retry
            else:
                run = False  # Quit if player chooses quit
            continue

        # Check if hangman is complete (6 incorrect guesses)
        if hangman_status == 6:
            if display_message("You LOST!"):
                reset_game()
            else:
                run = False
            continue


if __name__ == "__main__":
    # Game launch and restart loop
    while True:
        if not main():  # Run game until player quits
            break
    pygame.quit()