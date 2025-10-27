import pygame
import time
import sys
import random
from typing import Tuple, Union

#roulette sim has been made with chat gp-eahs noder
# --- CONFIG ---
WHEEL_IMAGE_PATH = "istockphoto-495810122-612x612.jpg"
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60
SLOTS_ORDER = [
            0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
            5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
        ]

class Roulette:

    @staticmethod
    def start_roulette(winning_number, balance, has_won):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Roulette")

        # Load and scale the wheel image
        wheel = pygame.image.load(WHEEL_IMAGE_PATH).convert()
        wheel = pygame.transform.scale(wheel, (800, 800))
        wheel.set_colorkey((255, 255, 255))  # make white transparent

        wheel_rect = wheel.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Font for balance and result
        font = pygame.font.SysFont("arial", 48)

        # Spin variables
        angle = 0
        spin_speed = 25  # degrees per frame
        slowing_down = False
        clock = pygame.time.Clock()

        # Run the spin animation
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            background = pygame.image.load("6494b914-00b0-47d6-8a18-44d7824e7c54.jpg")
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(background, (0, 0))

            # Draw wheel
            rotated_wheel = pygame.transform.rotate(wheel, angle)
            new_rect = rotated_wheel.get_rect(center=wheel_rect.center)
            screen.blit(rotated_wheel, new_rect.topleft)

            # Draw arrow indicator at top
            pygame.draw.polygon(screen, (255, 0, 0), [
                (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 420),
                (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 420),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 380)
            ])

            # Draw balance
            balance_text = font.render(f"Balance: {balance}", True, (255, 255, 255))
            screen.blit(balance_text, (50, 50))

            pygame.display.flip()
            clock.tick(FPS)

            # Spin logic
            angle += spin_speed
            if not slowing_down and angle > 1080:  # after ~3 spins
                slowing_down = True
            if slowing_down:
                spin_speed *= 0.98  # gradually slow down
                if spin_speed < 0.3:
                    running = False  # stop spinning

        # Show final result
        print (has_won)
        if has_won == "True":
            won_text = "won"
        elif has_won == "False":
            won_text = "lost"
        else:
            won_text = "error"
        result_text = font.render(f"Roulette stopped on {winning_number} you {won_text}!"
                                  , True, Roulette.get_number_color_rgb(winning_number))
        screen.blit(result_text, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 + 400))
        pygame.display.flip()
        time.sleep(20)
        pygame.quit()


    def get_random_number_by_color(color_name: str) -> str:
        """
        Selects a random number corresponding to the specified color on
        a standard European Roulette wheel.

        :param color_name: The desired color ('RED', 'GREEN', or 'BLACK').
        :return: A string representation of a random number with that color.
        :raises ValueError: If the color_name is not valid.
        """
        # Define the sequence of the European Roulette wheel slots
        # (used only to derive color lists, not for angle calculation)


        # Calculate the number lists for each color based on the wheel sequence:
        # 0 is GREEN (Index 0)
        # RED starts at Index 1 and alternates (1, 3, 5, ...)
        # BLACK starts at Index 2 and alternates (2, 4, 6, ...)
        COLOR_NUMBERS = {
            'GREEN': [0],
            'RED': [n for i, n in enumerate(SLOTS_ORDER) if i % 2 == 1],
            'BLACK': [n for i, n in enumerate(SLOTS_ORDER) if i % 2 == 0 and i != 0]
        }

        # Normalize input and check for validity
        color = color_name.upper()

        if color not in COLOR_NUMBERS:
            raise ValueError("Invalid color name. Must be 'RED', 'GREEN', or 'BLACK'.")

        # Select a random number from the list of numbers for that color
        selected_number = random.choice(COLOR_NUMBERS[color])

        # Return the number as a string
        return str(selected_number)



    def get_number_color_rgb(number: Union[int, str]) -> Tuple[int, int, int]:
        """
        Returns the RGB color tuple for a given European Roulette number.

        :param number: The roulette number (0-36) as an integer or string.
        :return: An RGB tuple (R, G, B) representing the number's color.
        :raises ValueError: If the number is invalid or outside the 0-36 range.
        """

        # Define standard RGB values for the colors
        RGB_COLORS = {
            'GREEN': (0, 128, 0),  # Dark Green
            'RED': (255, 0, 0),  # Pure Red
            'BLACK': (0, 0, 0)  # Pure Black
        }

        try:
            # Convert input to integer
            num = int(number)
        except ValueError:
            raise ValueError("Input must be a valid integer number (0-36).")

        if num < 0 or num > 36:
            raise ValueError("Number must be between 0 and 36 for European Roulette.")

        # Handle Green (0) first
        if num == 0:
            return RGB_COLORS['GREEN']

        # Get the index of the number in the sequence
        try:
            # Get the index (position) of the number in the SLOTS_ORDER list
            index = SLOTS_ORDER.index(num)
        except ValueError:
            # This shouldn't happen if the number is 1-36, but it's a safety check
            raise ValueError(f"Number {num} not found in SLOTS_ORDER definition.")

        # Determine color based on the index parity:
        # RED numbers are at odd indices (1, 3, 5, ...)
        if index % 2 == 1:
            return RGB_COLORS['RED']
        # BLACK numbers are at even indices (2, 4, 6, ...)
        else:
            return RGB_COLORS['BLACK']

    @staticmethod
    def is_a_number(winning_sign):
        return winning_sign.isnumeric()

