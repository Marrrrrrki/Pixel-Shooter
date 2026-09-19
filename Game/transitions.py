import pygame
import math


class Transition:

    def __init__(
        self,
        width,
        height
    ):

        self.width = width
        self.height = height

        self.active = False

        self.alpha = 0

        self.speed = 15

        self.direction = "in"

        # =====================================================
        # VISUAL STATE
        # =====================================================

        self.flash = 0

    # =========================================================
    # FADE OUT
    # =========================================================

    def fade_out(self):

        self.active = True

        self.direction = "out"

        self.alpha = 0

        self.flash = 0

    # =========================================================
    # FADE IN
    # =========================================================

    def fade_in(self):

        self.active = True

        self.direction = "in"

        self.alpha = 255

        self.flash = 0

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        if not self.active:
            return False

        if self.direction == "out":

            self.alpha += self.speed

            if self.alpha >= 255:

                self.alpha = 255

                self.active = False

                self.flash = 1

                return True

        elif self.direction == "in":

            self.alpha -= self.speed

            if self.alpha <= 0:

                self.alpha = 0

                self.active = False

                self.flash = 1

                return True

        return False

    # =========================================================
    # DRAW BORDER
    # =========================================================

    def draw_border(
        self,
        screen,
        intensity
    ):

        if intensity <= 0:
            return

        # -----------------------------------------------------
        # Cyan outer lines
        # -----------------------------------------------------

        color = (
            int(55 * intensity),
            int(220 * intensity),
            int(255 * intensity)
        )

        thickness = max(
            1,
            int(3 * intensity)
        )

        pygame.draw.rect(
            screen,
            color,
            (
                0,
                0,
                self.width - 1,
                self.height - 1
            ),
            thickness
        )

        # -----------------------------------------------------
        # Corner brackets
        # -----------------------------------------------------

        length = int(
            25 + 30 * intensity
        )

        bracket_color = (
            int(90 * intensity),
            int(235 * intensity),
            int(255 * intensity)
        )

        # Top left

        pygame.draw.line(
            screen,
            bracket_color,
            (0, length),
            (0, 0),
            3
        )

        pygame.draw.line(
            screen,
            bracket_color,
            (0, 0),
            (length, 0),
            3
        )

        # Top right

        pygame.draw.line(
            screen,
            bracket_color,
            (
                self.width - 1,
                length
            ),
            (
                self.width - 1,
                0
            ),
            3
        )

        pygame.draw.line(
            screen,
            bracket_color,
            (
                self.width - 1,
                0
            ),
            (
                self.width - length,
                0
            ),
            3
        )

        # Bottom left

        pygame.draw.line(
            screen,
            bracket_color,
            (
                0,
                self.height - length
            ),
            (
                0,
                self.height - 1
            ),
            3
        )

        pygame.draw.line(
            screen,
            bracket_color,
            (
                0,
                self.height - 1
            ),
            (
                length,
                self.height - 1
            ),
            3
        )

        # Bottom right

        pygame.draw.line(
            screen,
            bracket_color,
            (
                self.width - 1,
                self.height - length
            ),
            (
                self.width - 1,
                self.height - 1
            ),
            3
        )

        pygame.draw.line(
            screen,
            bracket_color,
            (
                self.width - 1,
                self.height - 1
            ),
            (
                self.width - length,
                self.height - 1
            ),
            3
        )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        if self.alpha <= 0:
            return

        # =====================================================
        # MAIN DARK OVERLAY
        # =====================================================

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                0,
                2,
                5,
                self.alpha
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # =====================================================
        # NEON SCANLINES
        # =====================================================

        intensity = self.alpha / 255

        scanlines = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        for y in range(
            0,
            self.height,
            8
        ):

            pygame.draw.line(
                scanlines,
                (
                    40,
                    190,
                    220,
                    int(18 * intensity)
                ),
                (
                    0,
                    y
                ),
                (
                    self.width,
                    y
                ),
                1
            )

        screen.blit(
            scanlines,
            (0, 0)
        )

        # =====================================================
        # MOVING CENTER LINE
        # =====================================================

        if self.direction == "out":

            progress = self.alpha / 255

        else:

            progress = 1 - (
                self.alpha / 255
            )

        center_y = int(
            self.height * progress
        )

        line_alpha = int(
            80 * intensity
        )

        line_surface = pygame.Surface(
            (
                self.width,
                5
            ),
            pygame.SRCALPHA
        )

        pygame.draw.line(
            line_surface,
            (
                55,
                220,
                255,
                line_alpha
            ),
            (
                0,
                2
            ),
            (
                self.width,
                2
            ),
            2
        )

        screen.blit(
            line_surface,
            (
                0,
                center_y - 2
            )
        )

        # =====================================================
        # CENTER GLOW
        # =====================================================

        glow = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        pulse = (
            math.sin(
                pygame.time.get_ticks() * 0.015
            ) + 1
        ) / 2

        glow_alpha = int(
            20 * intensity +
            pulse * 8 * intensity
        )

        pygame.draw.circle(
            glow,
            (
                35,
                190,
                255,
                glow_alpha
            ),
            (
                self.width // 2,
                center_y
            ),
            int(
                70 +
                pulse * 20
            )
        )

        screen.blit(
            glow,
            (0, 0)
        )

        # =====================================================
        # BORDER
        # =====================================================

        self.draw_border(
            screen,
            intensity
        )