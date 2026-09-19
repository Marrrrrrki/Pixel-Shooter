import pygame
import math


# ============================================================
# COLOURS
# ============================================================

BULLET_CORE = (255, 245, 220)
BULLET_MAIN = (255, 75, 55)
BULLET_GLOW = (255, 35, 25)
BULLET_DARK = (120, 25, 20)
WHITE = (255, 255, 255)


class BulletManager:

    def __init__(self):

        self.bullets = []

        # =====================================================
        # BULLET STATS
        # =====================================================

        self.speed = 10

        self.damage = 10

        self.shoot_delay = 200

        self.last_shot = 0

        # =====================================================
        # SIGHT RANGE
        # =====================================================

        self.sight_range = 250

        # =====================================================
        # VISUAL EFFECTS
        # =====================================================

        self.muzzle_flash = 0

        self.muzzle_x = 0
        self.muzzle_y = 0

        self.muzzle_dx = 0
        self.muzzle_dy = 0

    # =========================================================
    # AUTOMATIC SHOOTING
    # =========================================================

    def auto_shoot(
        self,
        player,
        enemies
    ):

        current_time = pygame.time.get_ticks()

        # =====================================================
        # SHOOTING COOLDOWN
        # =====================================================

        if (
            current_time - self.last_shot
            < self.shoot_delay
        ):

            return

        # =====================================================
        # FIND VISIBLE ENEMIES
        # =====================================================

        visible_enemies = []

        for enemy in enemies:

            if not enemy.alive:

                continue

            dx = enemy.x - player.x
            dy = enemy.y - player.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance <= self.sight_range:

                visible_enemies.append(
                    enemy
                )

        if not visible_enemies:

            return

        # =====================================================
        # FIND NEAREST ENEMY
        # =====================================================

        nearest_enemy = None

        nearest_distance = float("inf")

        for enemy in visible_enemies:

            dx = enemy.x - player.x
            dy = enemy.y - player.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < nearest_distance:

                nearest_distance = distance

                nearest_enemy = enemy

        if nearest_enemy is None:

            return

        # =====================================================
        # AIM AT ENEMY
        # =====================================================

        dx = nearest_enemy.x - player.x
        dy = nearest_enemy.y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:

            return

        dx /= distance
        dy /= distance

        # =====================================================
        # FIRE
        # =====================================================

        self.last_shot = current_time

        spawn_distance = 18

        spawn_x = (
            player.x +
            dx * spawn_distance
        )

        spawn_y = (
            player.y +
            dy * spawn_distance
        )

        # =====================================================
        # CREATE BULLET
        # =====================================================

        self.bullets.append({

            "x": spawn_x,
            "y": spawn_y,

            "dx": dx,
            "dy": dy,

            "damage": self.damage

        })

        # =====================================================
        # MUZZLE FLASH
        # =====================================================

        self.muzzle_flash = 5

        self.muzzle_x = spawn_x
        self.muzzle_y = spawn_y

        self.muzzle_dx = dx
        self.muzzle_dy = dy

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        width,
        height
    ):

        for bullet in self.bullets[:]:

            bullet["x"] += (
                bullet["dx"] *
                self.speed
            )

            bullet["y"] += (
                bullet["dy"] *
                self.speed
            )

            # =================================================
            # REMOVE OFFSCREEN BULLETS
            # =================================================

            if (
                bullet["x"] < 0
                or bullet["x"] > width
                or bullet["y"] < 0
                or bullet["y"] > height
            ):

                if bullet in self.bullets:

                    self.bullets.remove(
                        bullet
                    )

        # =====================================================
        # MUZZLE FLASH TIMER
        # =====================================================

        if self.muzzle_flash > 0:

            self.muzzle_flash -= 1

    # =========================================================
    # DRAW BULLET GLOW
    # =========================================================

    def draw_bullet_glow(
        self,
        screen,
        x,
        y
    ):

        glow = pygame.Surface(
            (
                34,
                34
            ),
            pygame.SRCALPHA
        )

        # Outer glow

        pygame.draw.circle(
            glow,
            (
                255,
                30,
                20,
                18
            ),
            (
                17,
                17
            ),
            12
        )

        # Inner glow

        pygame.draw.circle(
            glow,
            (
                255,
                65,
                35,
                28
            ),
            (
                17,
                17
            ),
            8
        )

        screen.blit(
            glow,
            (
                int(x - 17),
                int(y - 17)
            )
        )

    # =========================================================
    # DRAW BULLET
    # =========================================================

    def draw_bullet(
        self,
        screen,
        bullet
    ):

        x = bullet["x"]
        y = bullet["y"]

        dx = bullet["dx"]
        dy = bullet["dy"]

        # =====================================================
        # GLOW
        # =====================================================

        self.draw_bullet_glow(
            screen,
            x,
            y
        )

        # =====================================================
        # TRAIL
        # =====================================================

        trail_length = 10

        trail_start = (
            int(
                x -
                dx * trail_length
            ),
            int(
                y -
                dy * trail_length
            )
        )

        trail_end = (
            int(x),
            int(y)
        )

        pygame.draw.line(
            screen,
            BULLET_DARK,
            trail_start,
            trail_end,
            5
        )

        pygame.draw.line(
            screen,
            BULLET_GLOW,
            trail_start,
            trail_end,
            3
        )

        # =====================================================
        # BULLET HEAD
        # =====================================================

        size = 4

        points = [

            (
                int(
                    x +
                    dx * size
                ),
                int(
                    y +
                    dy * size
                )
            ),

            (
                int(
                    x -
                    dy * size
                ),
                int(
                    y +
                    dx * size
                )
            ),

            (
                int(
                    x -
                    dx * size
                ),
                int(
                    y -
                    dy * size
                )
            ),

            (
                int(
                    x +
                    dy * size
                ),
                int(
                    y -
                    dx * size
                )
            )
        ]

        pygame.draw.polygon(
            screen,
            BULLET_MAIN,
            points
        )

        # =====================================================
        # HOT CORE
        # =====================================================

        pygame.draw.rect(
            screen,
            BULLET_CORE,
            (
                int(x - 2),
                int(y - 2),
                4,
                4
            )
        )

    # =========================================================
    # DRAW MUZZLE FLASH
    # =========================================================

    def draw_muzzle_flash(
        self,
        screen
    ):

        if self.muzzle_flash <= 0:

            return

        x = self.muzzle_x
        y = self.muzzle_y

        dx = self.muzzle_dx
        dy = self.muzzle_dy

        # =====================================================
        # FLASH SIZE
        # =====================================================

        size = (
            self.muzzle_flash *
            1.8
        )

        # =====================================================
        # FLASH GLOW
        # =====================================================

        glow = pygame.Surface(
            (
                50,
                50
            ),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (
                255,
                80,
                40,
                35
            ),
            (
                25,
                25
            ),
            int(
                8 +
                size
            )
        )

        screen.blit(
            glow,
            (
                int(x - 25),
                int(y - 25)
            )
        )

        # =====================================================
        # FLASH SPIKES
        # =====================================================

        front_x = (
            x +
            dx * size
        )

        front_y = (
            y +
            dy * size
        )

        side_x = -dy
        side_y = dx

        points = [

            (
                int(x),
                int(y)
            ),

            (
                int(
                    front_x +
                    side_x * size * 0.45
                ),
                int(
                    front_y +
                    side_y * size * 0.45
                )
            ),

            (
                int(
                    front_x +
                    dx * size
                ),
                int(
                    front_y +
                    dy * size
                )
            ),

            (
                int(
                    front_x -
                    side_x * size * 0.45
                ),
                int(
                    front_y -
                    side_y * size * 0.45
                )
            )
        ]

        pygame.draw.polygon(
            screen,
            BULLET_MAIN,
            points
        )

        pygame.draw.polygon(
            screen,
            BULLET_CORE,
            points,
            1
        )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        screen
    ):

        # =====================================================
        # BULLETS
        # =====================================================

        for bullet in self.bullets:

            self.draw_bullet(
                screen,
                bullet
            )

        # =====================================================
        # MUZZLE FLASH
        # =====================================================

        self.draw_muzzle_flash(
            screen
        )