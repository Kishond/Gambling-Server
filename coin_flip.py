import pygame
import sys
#coinb flip sim has been made with chat gp-eahs noder nederr

# === SETTINGS ===
WIN_WIDTH, WIN_HEIGHT = 600, 400
FPS = 60

class CoinFlip:
    @staticmethod
    def coin_flip_animation(win_coin, balance, has_won):
        pygame.init()
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Coin Flip")

        font = pygame.font.Font(None, 50)
        clock = pygame.time.Clock()

        # Colors
        BG = (30, 30, 30)
        GOLD = (255, 215, 0)
        WHITE = (255, 255, 255)
        RED = (200, 50, 50)
        GREEN = (50, 200, 50)

        # Create a simple circle as the coin
        coin_radius = 70
        coin_x, coin_y = WIN_WIDTH // 2, WIN_HEIGHT // 2

        # Animation variables
        flip_time = 2  # seconds
        frames = flip_time * FPS
        angle = 0

        for frame in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BG)

            # Flip animation (scaling height)
            scale = abs((frame % (FPS // 2)) / (FPS // 2) - 0.5) * 2
            coin_height = int(coin_radius * scale + 5)
            pygame.draw.ellipse(screen, GOLD, (coin_x - coin_radius, coin_y - coin_height, coin_radius * 2, coin_height * 2))

            text = font.render("Flipping...", True, WHITE)
            screen.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, 50))

            pygame.display.flip()
            clock.tick(FPS)

        # Final result
        result_text = font.render(f"{'You Won!' if has_won == "True" else 'You Lost!'}", True, GREEN if has_won == "True" else RED)
        coin_text = font.render(f"Result: {win_coin}", True, GOLD)
        balance_text = font.render(f"Balance: {balance}", True, WHITE)

        screen.fill(BG)
        screen.blit(result_text, (WIN_WIDTH // 2 - result_text.get_width() // 2, 80))
        screen.blit(coin_text, (WIN_WIDTH // 2 - coin_text.get_width() // 2, 150))
        screen.blit(balance_text, (WIN_WIDTH // 2 - balance_text.get_width() // 2, 220))
        pygame.display.flip()

        pygame.time.wait(2500)
        pygame.quit()


