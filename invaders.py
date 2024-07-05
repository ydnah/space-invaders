import os

import pygame

pygame.init()
pygame.font.init()

# Game Varibles
WIDTH, HEIGHT = 500, 500
PLAYER_VEL = 5
ENEMY_VEL = 1

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
        pygame.display.set_caption("Space Invaders")
        self.running = True
        self.score = 0
        self.level = 1
        self.enemy_direction = 1
        self.crab_array = []
        self.populate_enemy()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.move()
        self.move_enemies()

    def move_enemies(self):
        move_down = False
        for enemy in self.crab_array:
            enemy.x += ENEMY_VEL * self.enemy_direction
            if enemy.x + enemy.get_width() >= WIDTH or enemy.x <= 0:
                move_down = True
        if move_down:
            self.enemy_direction *= -1
            for enemy in self.crab_array:
                enemy.y += enemy.get_height()

    def render(self):
        self.display.fill((0, 0, 0))
        self.main_font = pygame.font.SysFont("comicsans", 25)
        # draw text
        level_label = self.main_font.render(
            f"score< {self.score} >", 1, (255, 255, 255)
        )
        self.display.blit(level_label, (10, 10))

        self.player.draw(self.display)

        for enemy in self.crab_array:
            enemy.draw(self.display)

        pygame.display.flip()

    def populate_enemy(self, count=11, start_x=20, start_y=50, spacing=30):
        self.crab_array = []
        for i in range(count):
            x_position = start_x + i * spacing
            y_positon = start_y
            self.crab_array.append(Enemy(x_position, y_positon, CRAB))


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

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x - PLAYER_VEL > 0:
            self.x -= PLAYER_VEL

        if (
            keys[pygame.K_RIGHT]
            and self.x - PLAYER_VEL + self.ship_img.get_width() + 10 < WIDTH
        ):
            self.x += PLAYER_VEL


class Enemy(Ship):
    def __init__(self, x, y, enemy_type):
        super().__init__(x, y)
        self.ship_img = enemy_type
        self.mask = pygame.mask.from_surface(self.ship_img)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def move(self):
        if self.x - ENEMY_VEL + self.ship_img.get_width() + 10 < WIDTH:
            self.x += ENEMY_VEL

    def check_position(self):
        pass


def main():
    FPS = 60
    clock = pygame.time.Clock()

    game = Invaders()
    while game.running:
        clock.tick(FPS)
        game.check_event()
        game.update()
        game.render()


if __name__ == "__main__":
    main()
