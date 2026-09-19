import pygame
import math


class Player:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.size = 16
        self.speed = 4

        self.max_hp = 100
        self.hp = 100

        # =========================================================
        # COLOURS
        # =========================================================

        self.CYAN = (55, 220, 255)
        self.CYAN_DARK = (15, 70, 90)

        self.WHITE = (245, 248, 255)

        self.DARK = (8, 12, 18)
        self.PANEL = (18, 24, 32)

        self.RED = (255, 65, 75)
        self.YELLOW = (255, 210, 65)

        # =====================================================
        # VISUAL STATE
        # =====================================================

        self.body_color = (
            220,
            225,
            235
        )

        self.body_dark = (
            95,
            105,
            120
        )

        self.outline_color = (
            35,
            45,
            55
        )

        self.eye_color = (
            65,
            225,
            255
        )

        self.eye_glow = (
            25,
            110,
            140
        )

        self.weapon_color = (
            255,
            210,
            65
        )

        self.last_x = x
        self.last_y = y

    # =========================================================
    # MOVE
    # =========================================================

    def move(
        self,
        keys,
        width,
        height
    ):

        self.last_x = self.x
        self.last_y = self.y

        if keys[pygame.K_w] or keys[pygame.K_UP]:

            self.y -= self.speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:

            self.y += self.speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:

            self.x -= self.speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:

            self.x += self.speed

        # =====================================================
        # KEEP PLAYER INSIDE SCREEN
        # =====================================================

        self.x = max(
            self.size,
            min(
                width - self.size,
                self.x
            )
        )

        self.y = max(
            self.size,
            min(
                height - self.size,
                self.y
            )
        )

    # =========================================================
    # SHOOT DIRECTION
    # =========================================================

    def shoot_direction(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:

            return None

        dx /= distance
        dy /= distance

        return dx, dy

    # =========================================================
    # DRAW GLOW
    # =========================================================

    def draw_glow(
        self,
        screen
    ):

        glow = pygame.Surface(
            (
                70,
                70
            ),
            pygame.SRCALPHA
        )

        center = (
            35,
            35
        )

        # Outer glow

        pygame.draw.circle(
            glow,
            (
                35,
                180,
                220,
                12
            ),
            center,
            28
        )

        pygame.draw.circle(
            glow,
            (
                35,
                210,
                255,
                18
            ),
            center,
            21
        )

        pygame.draw.circle(
            glow,
            (
                35,
                220,
                255,
                25
            ),
            center,
            15
        )

        screen.blit(
            glow,
            (
                int(self.x - 35),
                int(self.y - 35)
            )
        )

    # =========================================================
    # DRAW PLAYER
    # =========================================================

    def draw(
        self,
        screen
    ):

        # =====================================================
        # IDLE ANIMATION
        # =====================================================

        time = pygame.time.get_ticks()

        idle_offset = int(
            math.sin(
                time * 0.006
            ) * 1
        )

        draw_x = int(
            self.x
        )

        draw_y = int(
            self.y +
            idle_offset
        )

        # =====================================================
        # GLOW
        # =====================================================

        self.draw_glow(
            screen
        )

        # =====================================================
        # BODY RECT
        # =====================================================

        body_width = 18
        body_height = 18

        body_rect = pygame.Rect(
            draw_x - body_width // 2,
            draw_y - body_height // 2,
            body_width,
            body_height
        )

        # =====================================================
        # SHADOW
        # =====================================================

        shadow_rect = pygame.Rect(
            draw_x - 8,
            draw_y + 9,
            16,
            4
        )

        pygame.draw.rect(
            screen,
            (
                4,
                5,
                7
            ),
            shadow_rect
        )

        # =====================================================
        # OUTLINE
        # =====================================================

        outline_rect = pygame.Rect(
            body_rect.x - 2,
            body_rect.y - 2,
            body_rect.width + 4,
            body_rect.height + 4
        )

        pygame.draw.rect(
            screen,
            self.outline_color,
            outline_rect
        )

        # =====================================================
        # MAIN BODY
        # =====================================================

        pygame.draw.rect(
            screen,
            self.body_color,
            body_rect
        )

        # =====================================================
        # DARK LOWER ARMOUR
        # =====================================================

        lower_body = pygame.Rect(
            body_rect.x + 2,
            body_rect.y + 11,
            body_rect.width - 4,
            5
        )

        pygame.draw.rect(
            screen,
            self.body_dark,
            lower_body
        )

        # =====================================================
        # TOP ARMOUR PANEL
        # =====================================================

        pygame.draw.rect(
            screen,
            (
                245,
                248,
                255
            ),
            (
                body_rect.x + 3,
                body_rect.y + 2,
                body_rect.width - 6,
                3
            )
        )

        # =====================================================
        # SIDE ARMOUR
        # =====================================================

        pygame.draw.rect(
            screen,
            self.body_dark,
            (
                body_rect.x,
                body_rect.y + 5,
                3,
                7
            )
        )

        pygame.draw.rect(
            screen,
            self.body_dark,
            (
                body_rect.right - 3,
                body_rect.y + 5,
                3,
                7
            )
        )

        # =====================================================
        # FACE PANEL
        # =====================================================

        face_rect = pygame.Rect(
            body_rect.x + 3,
            body_rect.y + 5,
            body_rect.width - 6,
            7
        )

        pygame.draw.rect(
            screen,
            (
                15,
                20,
                28
            ),
            face_rect
        )

        pygame.draw.rect(
            screen,
            (
                40,
                55,
                65
            ),
            face_rect,
            1
        )

        # =====================================================
        # EYES
        # =====================================================

        mouse_x, mouse_y = pygame.mouse.get_pos()

        direction_x = mouse_x - self.x
        direction_y = mouse_y - self.y

        distance = math.sqrt(
            direction_x * direction_x +
            direction_y * direction_y
        )

        if distance > 0:

            direction_x /= distance
            direction_y /= distance

        # Small eye movement toward cursor

        eye_offset_x = int(
            direction_x * 1
        )

        eye_offset_y = int(
            direction_y * 1
        )

        eye_width = 4
        eye_height = 3

        left_eye = pygame.Rect(
            body_rect.x + 4 + eye_offset_x,
            body_rect.y + 7 + eye_offset_y,
            eye_width,
            eye_height
        )

        right_eye = pygame.Rect(
            body_rect.x + 10 + eye_offset_x,
            body_rect.y + 7 + eye_offset_y,
            eye_width,
            eye_height
        )

        # Eye glow

        pygame.draw.rect(
            screen,
            self.eye_glow,
            (
                left_eye.x - 1,
                left_eye.y - 1,
                eye_width + 2,
                eye_height + 2
            )
        )

        pygame.draw.rect(
            screen,
            self.eye_glow,
            (
                right_eye.x - 1,
                right_eye.y - 1,
                eye_width + 2,
                eye_height + 2
            )
        )

        # Actual eyes

        pygame.draw.rect(
            screen,
            self.eye_color,
            left_eye
        )

        pygame.draw.rect(
            screen,
            self.eye_color,
            right_eye
        )

        # =====================================================
        # CORE
        # =====================================================

        core_pulse = (
            math.sin(
                time * 0.01
            ) + 1
        ) / 2

        core_color = (
            int(
                40 +
                core_pulse * 35
            ),
            int(
                170 +
                core_pulse * 60
            ),
            255
        )

        pygame.draw.rect(
            screen,
            (
                15,
                30,
                38
            ),
            (
                body_rect.centerx - 3,
                body_rect.bottom - 5,
                6,
                3
            )
        )

        pygame.draw.rect(
            screen,
            core_color,
            (
                body_rect.centerx - 2,
                body_rect.bottom - 5,
                4,
                2
            )
        )

        # =====================================================
        # SHOULDER LIGHTS
        # =====================================================

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                body_rect.x - 3,
                body_rect.y + 5,
                2,
                5
            )
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                body_rect.right + 1,
                body_rect.y + 5,
                2,
                5
            )
        )

    # =========================================================
    # AIM INDICATOR
    # =========================================================

    def draw_aim(
        self,
        screen
    ):

        direction = self.shoot_direction()

        if direction is None:

            return

        dx, dy = direction

        # =====================================================
        # TARGET POINT
        # =====================================================

        aim_distance = 24

        aim_x = (
            self.x +
            dx * aim_distance
        )

        aim_y = (
            self.y +
            dy * aim_distance
        )

        # =====================================================
        # SMALL TRAIL
        # =====================================================

        trail_start = (
            int(
                self.x +
                dx * 13
            ),
            int(
                self.y +
                dy * 13
            )
        )

        trail_end = (
            int(
                self.x +
                dx * 19
            ),
            int(
                self.y +
                dy * 19
            )
        )

        pygame.draw.line(
            screen,
            (
                100,
                100,
                105
            ),
            trail_start,
            trail_end,
            2
        )

        # =====================================================
        # AIM DIAMOND
        # =====================================================

        size = 5

        points = [

            (
                int(aim_x),
                int(aim_y - size)
            ),

            (
                int(aim_x + size),
                int(aim_y)
            ),

            (
                int(aim_x),
                int(aim_y + size)
            ),

            (
                int(aim_x - size),
                int(aim_y)
            )
        ]

        pygame.draw.polygon(
            screen,
            self.weapon_color,
            points,
            2
        )

        # =====================================================
        # CENTER
        # =====================================================

        pygame.draw.rect(
            screen,
            self.weapon_color,
            (
                int(aim_x - 1),
                int(aim_y - 1),
                3,
                3
            )
        )