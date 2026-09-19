import pygame
import math
import random

from Game.journal import Journal


# ============================================================
# COLOURS
# ============================================================

ENEMY_GREEN = (55, 235, 105)
ENEMY_DARK = (18, 75, 42)
ENEMY_GLOW = (40, 220, 100)

BLUE = (55, 145, 255)
BLUE_LIGHT = (110, 200, 255)
BLUE_DARK = (20, 65, 130)

YELLOW = (255, 210, 65)
YELLOW_LIGHT = (255, 235, 120)
YELLOW_DARK = (105, 75, 15)

WHITE = (245, 248, 255)
BLACK = (3, 4, 6)


# ============================================================
# ENEMY
# ============================================================

class Enemy:

    SIZE = 6
    SPEED = 1.2
    DAMAGE = 10
    MAX_HP = 10
    COIN_DROP_CHANCE = 0.35

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.hp = self.MAX_HP
        self.alive = True

        self.journal_id = "normal"

        self.hit_flash = 0

        self.spawn_time = pygame.time.get_ticks()

        self.animation_offset = random.uniform(
            0,
            math.pi * 2
        )

    # =========================================================
    # RECT
    # =========================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.SIZE,
            self.SIZE
        )

    # =========================================================
    # MOVE
    # =========================================================

    def move_towards_player(self, player_x, player_y):

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance > 0:

            dx /= distance
            dy /= distance

            self.x += dx * self.SPEED
            self.y += dy * self.SPEED

    # =========================================================
    # DRAW GLOW
    # =========================================================

    def draw_glow(self, screen, center):

        glow = pygame.Surface(
            (44, 44),
            pygame.SRCALPHA
        )

        pulse = (
            math.sin(
                pygame.time.get_ticks() * 0.008
                +
                self.animation_offset
            )
            + 1
        ) / 2

        alpha = int(
            12 +
            pulse * 10
        )

        pygame.draw.circle(
            glow,
            (
                40,
                230,
                100,
                alpha
            ),
            (22, 22),
            15
        )

        screen.blit(
            glow,
            (
                int(center[0] - 22),
                int(center[1] - 22)
            )
        )

    # =========================================================
    # DRAW HEALTH BAR
    # =========================================================

    def draw_health_bar(self, screen):

        if self.hp >= self.MAX_HP:
            return

        width = 22
        height = 4

        x = int(
            self.x -
            width // 2
        )

        y = int(
            self.y -
            12
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (
                x - 1,
                y - 1,
                width + 2,
                height + 2
            )
        )

        pygame.draw.rect(
            screen,
            (65, 20, 25),
            (
                x,
                y,
                width,
                height
            )
        )

        health_width = int(
            width *
            max(
                0,
                self.hp / self.MAX_HP
            )
        )

        if health_width > 0:

            pygame.draw.rect(
                screen,
                ENEMY_GREEN,
                (
                    x,
                    y,
                    health_width,
                    height
                )
            )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        if not self.alive:
            return

        time = pygame.time.get_ticks()

        pulse = (
            math.sin(
                time * 0.009
                +
                self.animation_offset
            )
            + 1
        ) / 2

        center = (
            int(self.x),
            int(self.y)
        )

        # ====================================================
        # GLOW
        # ====================================================

        self.draw_glow(
            screen,
            center
        )

        # ====================================================
        # BODY SIZE
        # ====================================================

        size = 7 + int(pulse)

        # ====================================================
        # SHADOW
        # ====================================================

        pygame.draw.rect(
            screen,
            BLACK,
            (
                center[0] - size // 2 + 2,
                center[1] - size // 2 + 2,
                size,
                size
            )
        )

        # ====================================================
        # OUTLINE
        # ====================================================

        pygame.draw.rect(
            screen,
            (
                10,
                40,
                22
            ),
            (
                center[0] - size // 2 - 2,
                center[1] - size // 2 - 2,
                size + 4,
                size + 4
            )
        )

        # ====================================================
        # BODY
        # ====================================================

        if self.hit_flash > 0:

            body_color = WHITE

            self.hit_flash -= 1

        else:

            body_color = ENEMY_GREEN

        pygame.draw.rect(
            screen,
            body_color,
            (
                center[0] - size // 2,
                center[1] - size // 2,
                size,
                size
            )
        )

        # ====================================================
        # INNER CORE
        # ====================================================

        pygame.draw.rect(
            screen,
            ENEMY_DARK,
            (
                center[0] - 2,
                center[1] - 2,
                5,
                5
            )
        )

        pygame.draw.rect(
            screen,
            ENEMY_GLOW,
            (
                center[0] - 1,
                center[1] - 1,
                3,
                3
            )
        )

        # ====================================================
        # ENERGY SPIKES
        # ====================================================

        pygame.draw.line(
            screen,
            ENEMY_GREEN,
            (
                center[0],
                center[1] - size // 2 - 3
            ),
            (
                center[0],
                center[1] - size // 2
            ),
            1
        )

        pygame.draw.line(
            screen,
            ENEMY_GREEN,
            (
                center[0] - size // 2 - 3,
                center[1]
            ),
            (
                center[0] - size // 2,
                center[1]
            ),
            1
        )

        pygame.draw.line(
            screen,
            ENEMY_GREEN,
            (
                center[0] + size // 2,
                center[1]
            ),
            (
                center[0] + size // 2 + 3,
                center[1]
            ),
            1
        )

        # ====================================================
        # HEALTH
        # ====================================================

        self.draw_health_bar(screen)

    # =========================================================
    # HIT
    # =========================================================

    def hit(self, damage=10):

        self.hp -= damage
        self.hit_flash = 5

        if self.hp <= 0:

            self.hp = 0
            self.alive = False


# ============================================================
# EXP ORB
# ============================================================

class ExpOrb:

    SIZE = 6
    ATTRACTION_SPEED = 6
    EXP_VALUE = 1

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.x += random.uniform(-3, 3)
        self.y += random.uniform(-3, 3)

        self.animation_offset = random.uniform(
            0,
            math.pi * 2
        )

    # =========================================================
    # RECT
    # =========================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.SIZE,
            self.SIZE
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        player_x,
        player_y,
        attraction_radius
    ):

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= attraction_radius:

            if distance > 0:

                dx /= distance
                dy /= distance

                self.x += dx * self.ATTRACTION_SPEED
                self.y += dy * self.ATTRACTION_SPEED

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        return distance <= 10

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        time = pygame.time.get_ticks()

        pulse = (
            math.sin(
                time * 0.01 +
                self.animation_offset
            )
            + 1
        ) / 2

        center = (
            int(self.x),
            int(self.y)
        )

        glow = pygame.Surface(
            (30, 30),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (
                50,
                150,
                255,
                int(25 + pulse * 15)
            ),
            (15, 15),
            9 + int(pulse * 2)
        )

        screen.blit(
            glow,
            (
                center[0] - 15,
                center[1] - 15
            )
        )

        size = 4 + int(pulse)

        points = [
            (
                center[0],
                center[1] - size
            ),
            (
                center[0] + size,
                center[1]
            ),
            (
                center[0],
                center[1] + size
            ),
            (
                center[0] - size,
                center[1]
            )
        ]

        pygame.draw.polygon(
            screen,
            BLUE,
            points
        )

        pygame.draw.polygon(
            screen,
            BLUE_LIGHT,
            points,
            1
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                center[0] - 1,
                center[1] - 1,
                2,
                2
            )
        )


# ============================================================
# COIN
# ============================================================

class Coin:

    SIZE = 9
    ATTRACTION_SPEED = 6
    VALUE = 5

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.x += random.uniform(-5, 5)
        self.y += random.uniform(-5, 5)

        self.animation_offset = random.uniform(
            0,
            math.pi * 2
        )

    # =========================================================
    # RECT
    # =========================================================

    def get_rect(self):

        return pygame.Rect(
            int(
                self.x -
                self.SIZE // 2
            ),
            int(
                self.y -
                self.SIZE // 2
            ),
            self.SIZE,
            self.SIZE
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        player_x,
        player_y,
        attraction_radius
    ):

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= attraction_radius:

            if distance > 0:

                dx /= distance
                dy /= distance

                self.x += dx * self.ATTRACTION_SPEED
                self.y += dy * self.ATTRACTION_SPEED

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        return distance <= 12

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        time = pygame.time.get_ticks()

        bob = math.sin(
            time * 0.007 +
            self.animation_offset
        )

        center = (
            int(self.x),
            int(self.y + bob)
        )

        glow = pygame.Surface(
            (40, 40),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (
                255,
                200,
                40,
                25
            ),
            (20, 20),
            13
        )

        screen.blit(
            glow,
            (
                center[0] - 20,
                center[1] - 20
            )
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                center[0] + 2,
                center[1] + 2
            ),
            self.SIZE // 2 + 1
        )

        pygame.draw.circle(
            screen,
            YELLOW_DARK,
            center,
            self.SIZE // 2 + 1
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            center,
            self.SIZE // 2
        )

        pygame.draw.circle(
            screen,
            YELLOW_LIGHT,
            center,
            4,
            1
        )

        pygame.draw.line(
            screen,
            YELLOW_LIGHT,
            (
                center[0],
                center[1] - 2
            ),
            (
                center[0],
                center[1] + 2
            ),
            1
        )


# ============================================================
# ENEMY MANAGER
# ============================================================

class EnemyManager:

    def __init__(
        self,
        screen_width,
        screen_height
    ):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.enemies = []
        self.exp_orbs = []
        self.coins = []

        self.journal = Journal()

        # ====================================================
        # EXP ATTRACTION
        # ====================================================

        self.base_attraction_radius = 100

        self.attraction_radius = (
            self.base_attraction_radius
        )

        # ====================================================
        # COIN ATTRACTION
        # ====================================================

        self.coin_attraction_radius = 100

        # ====================================================
        # WAVE
        # ====================================================

        self.wave = 1

        # ====================================================
        # WAVE TIMER
        # ====================================================

        self.base_wave_duration = 30.0

        self.wave_duration = (
            self.base_wave_duration
        )

        self.wave_time_remaining = (
            self.wave_duration
        )

        self.last_update_time = (
            pygame.time.get_ticks()
        )

        # ====================================================
        # SPAWNING
        # ====================================================

        self.spawn_timer = 0.0

        self.spawn_interval = 1.2

        self.spawned_this_wave = 0

        self.wave_spawning = True

        self.start_wave()

    # =========================================================
    # START WAVE
    # =========================================================

    def start_wave(self):

        self.enemies = []

        self.spawned_this_wave = 0

        self.wave_spawning = True

        self.spawn_timer = 0.0

        # -----------------------------------------------------
        # WAVE LENGTH
        # -----------------------------------------------------

        self.wave_duration = (
            self.base_wave_duration
            +
            min(
                15.0,
                (self.wave - 1) * 1.5
            )
        )

        self.wave_time_remaining = (
            self.wave_duration
        )

        # -----------------------------------------------------
        # SPAWN RATE
        # -----------------------------------------------------

        self.spawn_interval = max(
            0.35,
            1.2 -
            (self.wave - 1) * 0.045
        )

        # -----------------------------------------------------
        # XP ATTRACTION
        # -----------------------------------------------------

        self.attraction_radius = max(
            35,
            self.base_attraction_radius
            -
            (self.wave - 1) * 5
        )

        # -----------------------------------------------------
        # START WITH ONE ENEMY
        # -----------------------------------------------------

        self.spawn_enemy()

    # =========================================================
    # SPAWN ENEMY
    # =========================================================

    def spawn_enemy(self):

        side = random.randint(
            0,
            3
        )

        if side == 0:

            x = random.randint(
                0,
                self.screen_width
            )

            y = -20

        elif side == 1:

            x = self.screen_width + 20

            y = random.randint(
                0,
                self.screen_height
            )

        elif side == 2:

            x = random.randint(
                0,
                self.screen_width
            )

            y = self.screen_height + 20

        else:

            x = -20

            y = random.randint(
                0,
                self.screen_height
            )

        enemy = Enemy(
            x,
            y
        )

        self.enemies.append(
            enemy
        )

        self.journal.discover_enemy(
            enemy.journal_id
        )

        self.spawned_this_wave += 1

    # =========================================================
    # UPDATE WAVE TIMER
    # =========================================================

    def update_wave_timer(self):

        current_time = pygame.time.get_ticks()

        delta_time = (
            current_time -
            self.last_update_time
        ) / 1000.0

        self.last_update_time = current_time

        delta_time = min(
            delta_time,
            0.1
        )

        if not self.wave_spawning:
            return

        self.wave_time_remaining -= delta_time

        # ====================================================
        # TIMER FINISHED
        # ====================================================

        if self.wave_time_remaining <= 0:

            self.wave_time_remaining = 0

            self.wave_spawning = False

            return

        # ====================================================
        # SPAWN
        # ====================================================

        self.spawn_timer += delta_time

        while (
            self.spawn_timer >=
            self.spawn_interval
        ):

            self.spawn_timer -= (
                self.spawn_interval
            )

            self.spawn_enemy()

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        bullets,
        player_x,
        player_y,
        exp_callback,
        damage_callback,
        coin_callback,
        wave_complete_callback
    ):

        # ====================================================
        # WAVE TIMER
        # ====================================================

        self.update_wave_timer()

        # ====================================================
        # MOVE ENEMIES
        # ====================================================

        for enemy in self.enemies:

            if not enemy.alive:
                continue

            enemy.move_towards_player(
                player_x,
                player_y
            )

        # ====================================================
        # BULLET COLLISIONS
        # ====================================================

        for bullet in bullets[:]:

            bullet_rect = pygame.Rect(
                int(
                    bullet["x"] - 3
                ),
                int(
                    bullet["y"] - 3
                ),
                6,
                6
            )

            for enemy in self.enemies:

                if not enemy.alive:
                    continue

                if enemy.get_rect().colliderect(
                    bullet_rect
                ):

                    damage = bullet.get(
                        "damage",
                        10
                    )

                    enemy.hit(
                        damage
                    )

                    if bullet in bullets:

                        bullets.remove(
                            bullet
                        )

                    # ========================================
                    # ENEMY DIED
                    # ========================================

                    if not enemy.alive:

                        self.exp_orbs.append(
                            ExpOrb(
                                enemy.x,
                                enemy.y
                            )
                        )

                        if random.random() < (
                            Enemy.COIN_DROP_CHANCE
                        ):

                            self.coins.append(
                                Coin(
                                    enemy.x,
                                    enemy.y
                                )
                            )

                    break

        # ====================================================
        # ENEMY / PLAYER COLLISION
        # ====================================================

        player_rect = pygame.Rect(
            int(player_x - 8),
            int(player_y - 8),
            16,
            16
        )

        for enemy in self.enemies:

            if not enemy.alive:
                continue

            if enemy.get_rect().colliderect(
                player_rect
            ):

                damage_callback(
                    enemy.DAMAGE
                )

                enemy.alive = False

        # ====================================================
        # REMOVE DEAD ENEMIES
        # ====================================================

        self.enemies = [
            enemy
            for enemy in self.enemies
            if enemy.alive
        ]

        # ====================================================
        # EXP ORBS
        # ====================================================

        for orb in self.exp_orbs[:]:

            collected = orb.update(
                player_x,
                player_y,
                self.attraction_radius
            )

            if collected:

                exp_callback(
                    orb.EXP_VALUE
                )

                self.exp_orbs.remove(
                    orb
                )

        # ====================================================
        # COINS
        # ====================================================

        for coin in self.coins[:]:

            collected = coin.update(
                player_x,
                player_y,
                self.coin_attraction_radius
            )

            if collected:

                coin_callback(
                    coin.VALUE
                )

                self.coins.remove(
                    coin
                )

        # ====================================================
        # NEXT WAVE
        # ====================================================

        if (
            not self.wave_spawning
            and
            len(self.enemies) == 0
        ):

            completed_wave = self.wave

            self.wave += 1

            if completed_wave % 5 == 0:

                wave_complete_callback(
                    completed_wave
                )

            else:

                self.start_wave()

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        # -----------------------------------------------------
        # COLLECTIBLES
        # -----------------------------------------------------

        for orb in self.exp_orbs:

            orb.draw(
                screen
            )

        for coin in self.coins:

            coin.draw(
                screen
            )

        # -----------------------------------------------------
        # ENEMIES
        # -----------------------------------------------------

        for enemy in self.enemies:

            enemy.draw(
                screen
            )

    # =========================================================
    # DRAW WAVE TIMER
    # =========================================================

    def draw_wave_timer(self, screen):

        # ====================================================
        # TIMER BAR SETTINGS
        # ====================================================

        bar_width = 420
        bar_height = 18

        x = (
            self.screen_width -
            bar_width
        ) // 2

        y = 18

        # ====================================================
        # PROGRESS
        # ====================================================

        if self.wave_duration > 0:

            progress = (
                self.wave_time_remaining /
                self.wave_duration
            )

        else:

            progress = 0

        progress = max(
            0,
            min(
                1,
                progress
            )
        )

        # ====================================================
        # COLOUR
        # ====================================================
        #
        # 100% = green
        # 50%  = yellow
        # 0%   = red
        #
        # ====================================================

        if progress > 0.5:

            amount = (
                (1.0 - progress) * 2
            )

            red = int(
                80 +
                amount * 175
            )

            green = 235

        else:

            amount = (
                progress * 2
            )

            red = 255

            green = int(
                70 +
                amount * 165
            )

        timer_color = (
            red,
            green,
            70
        )

        # ====================================================
        # TIMER BACKGROUND
        # ====================================================

        pygame.draw.rect(
            screen,
            (
                12,
                15,
                20
            ),
            (
                x - 3,
                y - 3,
                bar_width + 6,
                bar_height + 6
            ),
            border_radius=6
        )

        # ====================================================
        # EMPTY BAR
        # ====================================================

        pygame.draw.rect(
            screen,
            (
                35,
                38,
                45
            ),
            (
                x,
                y,
                bar_width,
                bar_height
            ),
            border_radius=4
        )

        # ====================================================
        # CURRENT TIMER
        # ====================================================

        current_width = int(
            bar_width *
            progress
        )

        if current_width > 0:

            pygame.draw.rect(
                screen,
                timer_color,
                (
                    x,
                    y,
                    current_width,
                    bar_height
                ),
                border_radius=4
            )

        # ====================================================
        # FONT
        # ====================================================

        font = pygame.font.Font(
            None,
            24
        )

        # ====================================================
        # WAVE TEXT
        # ====================================================

        wave_text = font.render(
            f"WAVE {self.wave}",
            True,
            WHITE
        )

        wave_rect = wave_text.get_rect(
            center=(
                self.screen_width // 2,
                y + bar_height + 23
            )
        )

        screen.blit(
            wave_text,
            wave_rect
        )

        # ====================================================
        # TIME TEXT
        # ====================================================

        seconds = max(
            0,
            self.wave_time_remaining
        )

        # Make the actual number increasingly red too.
        if progress > 0.5:

            text_color = WHITE

        else:

            danger = (
                1.0 -
                progress * 2
            )

            text_color = (
                255,
                int(
                    245 -
                    danger * 190
                ),
                int(
                    245 -
                    danger * 190
                )
            )

        time_text = font.render(
            f"{seconds:.1f}",
            True,
            text_color
        )

        time_rect = time_text.get_rect(
            center=(
                self.screen_width // 2,
                y + bar_height // 2
            )
        )

        screen.blit(
            time_text,
            time_rect
        )