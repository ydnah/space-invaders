import os
import random

import pygame

pygame.init()
pygame.font.init()

# Game Varibles
WIDTH, HEIGHT = 480, 540
PLAYER_VEL = 5

# End threshold
ENEMY_Y_THRESHOLD = HEIGHT - 110

# Enemy speed
ENEMY_VEL_BASE = 0.2
ENEMY_VEL_MAX = 2

FPS = 60

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
        self.enemy_array = []
        self.enemy_laser_array = []
        self.populate_enemy()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.controls()
        self.move_enemies()
        self.player.move_lasers(6, self.enemy_array, self)
        self.clean_dead_enemies()
        self.enemy_shoot()
        self.move_enemy_lasers()
        if self.player.lives == 0:
            self.running = False

        if not any(enemy for row in self.enemy_array for enemy in row):
            self.level += 1
            self.populate_enemy()

    def move_enemies(self):
        remaining_enemies = sum(
            sum(1 for enemy in row if not enemy.is_dead) for row in self.enemy_array
        )
        if remaining_enemies > 0:
            enemy_velocity = ENEMY_VEL_BASE + (
                (ENEMY_VEL_MAX + self.level * 0.5) - ENEMY_VEL_BASE
            ) * (1 - remaining_enemies / self.total_enemies)
        else:
            enemy_velocity = ENEMY_VEL_BASE

        move_down = False
        for row in self.enemy_array:
            for enemy in row:
                enemy.x += enemy_velocity * self.enemy_direction
                if enemy.x + enemy.get_width() >= WIDTH or enemy.x <= 0:
                    move_down = True
                elif enemy.y + enemy.get_height() >= ENEMY_Y_THRESHOLD:
                    self.running = False

        if move_down:
            self.enemy_direction *= -1
            for row in self.enemy_array:
                for enemy in row:
                    enemy.y += enemy.get_height()

    def render(self):
        self.display.fill((0, 0, 0))
        self.main_font = pygame.font.SysFont("comicsans", 25)
        # draw text
        level_label = self.main_font.render(
            f"score< {self.score} >", 1, (255, 255, 255)
        )
        self.display.blit(level_label, (10, 10))

        pygame.draw.line(
            self.display, (255, 255, 255), (0, HEIGHT - 70), (WIDTH, HEIGHT - 70), 2
        )

        lives_label = self.main_font.render(f"{self.player.lives}", 1, (255, 255, 255))
        self.display.blit(lives_label, (10, HEIGHT - 70))

        self.player.draw(self.display)

        for row in self.enemy_array:
            for enemy in row:
                enemy.draw(self.display)

        for laser in self.enemy_laser_array:
            laser.draw(self.display)

        pygame.display.flip()

    def populate_enemy(self, count=11, start_x=20, start_y=80, spacing=30):
        self.enemy_array = []
        row = 0

        enemy_rows = [
            (OCTOPUS, 1, 40),
            (CRAB, 2, 20),
            (SQUID, 2, 10),
        ]

        for enemy, rows, score_value in enemy_rows:
            for _ in range(rows):
                inner_list = []
                for i in range(count):
                    x_position = start_x + i * spacing
                    y_position = start_y + row * spacing
                    inner_list.append(Enemy(x_position, y_position, enemy, score_value))
                self.enemy_array.append(inner_list)
                row += 1

        self.total_enemies = sum(len(row) for row in self.enemy_array)

    def clean_dead_enemies(self):
        self.enemy_array = [
            row for row in self.enemy_array if any(not enemy.is_dead for enemy in row)
        ]
        for row in self.enemy_array:
            row[:] = [enemy for enemy in row if not enemy.is_dead]

    def enemy_shoot(self):
        for row in self.enemy_array:
            for enemy in row:
                if enemy.shoot_chance(self):
                    laser = Laser(
                        enemy.x + enemy.get_width(), enemy.y + enemy.get_height(), LASER
                    )
                    self.enemy_laser_array.append(laser)

    def move_enemy_lasers(self):
        for laser in self.enemy_laser_array:
            laser.move(-2)
            if laser.off_screen(HEIGHT - 80):
                self.enemy_laser_array.remove(laser)
            elif laser.is_collision(self.player):
                self.player.lives -= 1
                self.enemy_laser_array.remove(laser)


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y -= vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collide(self, obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def is_collision(self, obj):
        return self.collide(self, obj)


class Ship:
    COOLDOWN = FPS // 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.is_dead = False

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.is_collision(obj):
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(
                self.x + 12,
                self.y,
                self.laser_img,
            )
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = PLAYER
        self.laser_img = LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.lives = 3

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x - PLAYER_VEL > 0:
            self.x -= PLAYER_VEL

        if (
            keys[pygame.K_RIGHT]
            and self.x - PLAYER_VEL + self.ship_img.get_width() + 10 < WIDTH
        ):
            self.x += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move_lasers(self, vel, objs, game):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for row in objs:
                    for obj in row:
                        if laser.is_collision(obj):
                            obj.is_dead = True
                            game.score += obj.score_value
                            if laser in self.lasers:
                                self.lasers.remove(laser)
                            break


class Enemy(Ship):
    def __init__(self, x, y, enemy_type, score_value):
        super().__init__(x, y)
        self.ship_img = enemy_type
        self.score_value = score_value
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self):
        if self.x - ENEMY_VEL_BASE + self.ship_img.get_width() + 10 < WIDTH:
            self.x += ENEMY_VEL_BASE

    def shoot_chance(self, game):
        if random.randrange(0, 110 * FPS * game.level) == 1:
            return True
        return False


def main():
    clock = pygame.time.Clock()

    game = Invaders()
    while game.running:
        clock.tick(FPS)
        game.check_event()
        game.update()
        game.render()


if __name__ == "__main__":
    main()
