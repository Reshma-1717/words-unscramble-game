import pygame
import random
import nltk
from nltk.corpus import words

# Initialize Pygame and NLTK
pygame.init()
nltk.download('words')

# Screen setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" WORDS UNSCRAMBLE GAME")

# Fonts and colors
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
RED = (220, 20, 60)  # Crimson red for scrambled word
BLUE = (0, 0, 205)  # Medium blue for scores
GREEN = (34, 139, 34)  # Forest green for messages
ORANGE = (255, 140, 0)  # Dark orange for user input
PURPLE = (75, 0, 130)  # Indigo for hints
GOLD = (255, 215, 0)  # Gold for the timer

# Game settings
TIME_LIMIT = 60  # seconds per turn
word_list = [word.lower() for word in words.words() if len(word) == 5]  # Filter words to length of 5
player_score = 0

# Utility functions
def scramble_word(word):
    scrambled = ''.join(random.sample(word, len(word)))
    return scrambled if scrambled != word else scramble_word(word)  # Ensure it's actually scrambled

def get_random_word():
    return random.choice(word_list)

def get_hint(word):
    return f"Hint: Starts with '{word[0]}' and ends with '{word[-1]}'"

# Main game loop
def game_loop():
    global player_score
    clock = pygame.time.Clock()
    run = True

    # Game variables
    current_word = get_random_word()
    scrambled_word = scramble_word(current_word)
    user_input = ""
    message = "Guess the word!"
    hint_message = get_hint(current_word)
    timer = TIME_LIMIT  # Set timer for each round

    while run:
        screen.fill(WHITE)

        # Timer countdown
        timer -= 1 / 30  # Decrease by 1 second every 30 frames
        if timer <= 0:
            message = f"Time's up! The correct word was '{current_word}'."
            timer = TIME_LIMIT  # Reset timer
            current_word = get_random_word()
            scrambled_word = scramble_word(current_word)
            user_input = ""
            hint_message = get_hint(current_word)

        # Render game elements with colors
        word_text = FONT.render(f"Scrambled: {scrambled_word}", True, RED)
        score_text = FONT.render(f"Player Score: {player_score}", True, BLUE)
        input_text = FONT.render(f"Your Guess: {user_input}", True, ORANGE)
        message_text = FONT.render(message, True, GREEN)
        hint_text = FONT.render(hint_message, True, PURPLE)
        timer_text = FONT.render(f"Time left: {int(timer)}s", True, GOLD)

        # Blit to screen
        screen.blit(word_text, (50, 50))
        screen.blit(score_text, (50, 100))
        screen.blit(input_text, (50, 150))
        screen.blit(message_text, (50, 200))
        screen.blit(hint_text, (50, 250))
        screen.blit(timer_text, (600, 50))  # Display timer in the top-right corner

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Submit guess
                    if user_input.lower() == current_word:
                        message = "Correct! You guessed it."
                        player_score += 1
                    else:
                        message = f"Wrong! The correct word was {current_word}."
                    # Reset for next round
                    current_word = get_random_word()
                    scrambled_word = scramble_word(current_word)
                    user_input = ""
                    hint_message = get_hint(current_word)
                    timer = TIME_LIMIT  # Reset timer
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        clock.tick(30)

    pygame.quit()

# Run the game
game_loop()
