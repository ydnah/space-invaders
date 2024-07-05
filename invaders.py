import os

import pygame

pygame.init()
pygame.font.init()

# Game Varibles
WIDTH, HEIGHT = 500, 500

# Enemies
CRAB = pygame.image.load(os.path.join("assets", "space__0002_B1.png"))
OCTOPUS = pygame.image.load(os.path.join("assets", "space__0000_A1.png"))
SQUID = pygame.image.load(os.path.join("assets", "space__0004_C1.png"))
UFO = pygame.image.load(os.path.join("assets", "space__0007_UFO.png"))
# Player ship
PLAYER = pygame.image.load(os.path.join("assets", "space__0006_Player.png"))
# Projectile
LASER = pygame.image.load(os.path.join("assets", "Projectile_Player.png"))


class Invaders:
    def __init__(self):
        self.player = Player((WIDTH // 2) - 15, HEIGHT - 100)
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.score = 0
        self.level = 1

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.display.fill((0, 0, 0))
        self.main_font = pygame.font.SysFont("comicsans", 25)
        # draw text
        level_label = self.main_font.render(
            f"score< {self.score} >", 1, (255, 255, 255)
        )
        self.display.blit(level_label, (10, 10))

        self.player.draw(self.display)

        pygame.display.flip()


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = type
        self.ship_img = None
        self.laser_img = None

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = PLAYER
        self.laser_img = LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.lives = 3


class Enemy(Ship):
    def __init__(self):
        super().__init__()


def main():
    FPS = 60
    clock = pygame.time.Clock()

    game = Invaders()
    while game.running:
        clock.tick(FPS)
        game.render()
        game.check_event()


if __name__ == "__main__":
    main()
