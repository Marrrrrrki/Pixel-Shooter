import pygame
import math


class UI:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (4, 5, 8)
        self.BACKGROUND = (8, 9, 13)

        self.PANEL = (13, 15, 21)
        self.PANEL_LIGHT = (20, 23, 31)
        self.PANEL_DARK = (7, 8, 12)

        self.WHITE = (245, 247, 255)
        self.GRAY = (130, 137, 151)
        self.LIGHT_GRAY = (190, 197, 210)

        self.CYAN = (60, 220, 255)
        self.CYAN_DARK = (20, 75, 95)

        self.BLUE = (65, 145, 255)
        self.BLUE_DARK = (20, 50, 105)

        self.GREEN = (65, 235, 125)
        self.GREEN_DARK = (20, 80, 50)

        self.RED = (255, 65, 75)
        self.RED_DARK = (95, 20, 27)

        self.YELLOW = (255, 210, 65)
        self.YELLOW_DARK = (100, 75, 20)

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(None, 25)
        self.font_large = pygame.font.Font(None, 34)
        self.font_level = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        self.font_micro = pygame.font.Font(None, 11)

    # =========================================================
    # PANEL
    # =========================================================

    def draw_panel(
        self,
        screen,
        rect,
        accent=None
    ):

        # -----------------------------------------------------
        # Shadow
        # -----------------------------------------------------

        shadow_rect = pygame.Rect(
            rect.x + 5,
            rect.y + 5,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow_rect
        )

        # -----------------------------------------------------
        # Outer frame
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.PANEL_LIGHT,
            rect
        )

        # -----------------------------------------------------
        # Inner panel
        # -----------------------------------------------------

        inner = pygame.Rect(
            rect.x + 3,
            rect.y + 3,
            rect.width - 6,
            rect.height - 6
        )

        pygame.draw.rect(
            screen,
            self.PANEL,
            inner
        )

        # -----------------------------------------------------
        # Accent line
        # -----------------------------------------------------

        if accent is not None:

            pygame.draw.rect(
                screen,
                accent,
                (
                    rect.x,
                    rect.y,
                    3,
                    rect.height
                )
            )

        # -----------------------------------------------------
        # Corner details
        # -----------------------------------------------------

        corner = 8

        pygame.draw.line(
            screen,
            self.GRAY,
            (
                rect.right - corner,
                rect.top
            ),
            (
                rect.right,
                rect.top + corner
            ),
            1
        )

        pygame.draw.line(
            screen,
            self.GRAY,
            (
                rect.left,
                rect.bottom - corner
            ),
            (
                rect.left + corner,
                rect.bottom
            ),
            1
        )

    # =========================================================
    # BAR
    # =========================================================

    def draw_bar(
        self,
        screen,
        x,
        y,
        width,
        height,
        value,
        maximum,
        fill_color,
        dark_color,
        label,
        text
    ):

        if maximum <= 0:
            percentage = 0
        else:
            percentage = value / maximum

        percentage = max(
            0,
            min(
                1,
                percentage
            )
        )

        # -----------------------------------------------------
        # Outer border
        # -----------------------------------------------------

        outer = pygame.Rect(
            x,
            y,
            width,
            height
        )

        pygame.draw.rect(
            screen,
            self.PANEL_LIGHT,
            outer
        )

        # -----------------------------------------------------
        # Inner background
        # -----------------------------------------------------

        inner = pygame.Rect(
            x + 3,
            y + 3,
            width - 6,
            height - 6
        )

        pygame.draw.rect(
            screen,
            dark_color,
            inner
        )

        # -----------------------------------------------------
        # Fill
        # -----------------------------------------------------

        fill_width = int(
            (width - 6) * percentage
        )

        if fill_width > 0:

            fill_rect = pygame.Rect(
                x + 3,
                y + 3,
                fill_width,
                height - 6
            )

            pygame.draw.rect(
                screen,
                fill_color,
                fill_rect
            )

            # Highlight

            if fill_width > 5:

                pygame.draw.line(
                    screen,
                    self.WHITE,
                    (
                        fill_rect.left + 2,
                        fill_rect.top + 2
                    ),
                    (
                        fill_rect.right - 2,
                        fill_rect.top + 2
                    ),
                    1
                )

        # -----------------------------------------------------
        # Label
        # -----------------------------------------------------

        if label:

            label_surface = self.font_micro.render(
                label,
                True,
                self.WHITE
            )

            screen.blit(
                label_surface,
                (
                    x + 7,
                    y + 5
                )
            )

        # -----------------------------------------------------
        # Value
        # -----------------------------------------------------

        if text:

            value_surface = self.font_tiny.render(
                text,
                True,
                self.WHITE
            )

            value_rect = value_surface.get_rect(
                midright=(
                    x + width - 8,
                    y + height // 2
                )
            )

            screen.blit(
                value_surface,
                value_rect
            )

    # =========================================================
    # LEVEL
    # =========================================================

    def draw_level(
        self,
        screen,
        level
    ):

        x = 20
        y = 20

        width = 175
        height = 70

        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.draw_panel(
            screen,
            rect,
            self.YELLOW
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        label = self.font_micro.render(
            "CURRENT LEVEL",
            True,
            self.GRAY
        )

        screen.blit(
            label,
            (
                x + 14,
                y + 10
            )
        )

        # -----------------------------------------------------
        # Small yellow status marker
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.YELLOW,
            (
                x + 14,
                y + 30,
                5,
                22
            )
        )

        # -----------------------------------------------------
        # Level number background
        # -----------------------------------------------------

        number_box = pygame.Rect(
            x + 30,
            y + 27,
            width - 44,
            32
        )

        pygame.draw.rect(
            screen,
            self.PANEL_DARK,
            number_box
        )

        pygame.draw.rect(
            screen,
            self.YELLOW_DARK,
            number_box,
            1
        )

        # -----------------------------------------------------
        # Level number
        # -----------------------------------------------------

        level_text = self.font_level.render(
            str(level),
            True,
            self.YELLOW
        )

        level_rect = level_text.get_rect(
            midright=(
                number_box.right - 8,
                number_box.centery
            )
        )

        screen.blit(
            level_text,
            level_rect
        )

        # -----------------------------------------------------
        # Small decorative indicators
        # -----------------------------------------------------

        indicator_y = y + height - 7

        pygame.draw.rect(
            screen,
            self.YELLOW,
            (
                x + 14,
                indicator_y,
                24,
                2
            )
        )

        pygame.draw.rect(
            screen,
            self.YELLOW_DARK,
            (
                x + 42,
                indicator_y,
                8,
                2
            )
        )

        pygame.draw.rect(
            screen,
            self.YELLOW_DARK,
            (
                x + 54,
                indicator_y,
                8,
                2
            )
        )

    # =========================================================
    # WAVE
    # =========================================================

    def draw_wave(
        self,
        screen,
        wave
    ):

        width = 190
        height = 70

        x = self.width - width - 20
        y = 20

        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.draw_panel(
            screen,
            rect,
            self.CYAN
        )

        # -----------------------------------------------------
        # Label
        # -----------------------------------------------------

        label = self.font_micro.render(
            "CURRENT WAVE",
            True,
            self.GRAY
        )

        label_rect = label.get_rect(
            topleft=(
                x + 14,
                y + 10
            )
        )

        screen.blit(
            label,
            label_rect
        )

        # -----------------------------------------------------
        # Wave number
        # -----------------------------------------------------

        wave_text = self.font_title.render(
            f"WAVE {wave}",
            True,
            self.WHITE
        )

        wave_rect = wave_text.get_rect(
            bottomright=(
                x + width - 14,
                y + height - 10
            )
        )

        screen.blit(
            wave_text,
            wave_rect
        )

        # -----------------------------------------------------
        # Decorative marker
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                x + 14,
                y + 38,
                5,
                16
            )
        )

        # -----------------------------------------------------
        # Small status blocks
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            (
                x + 26,
                y + 48,
                18,
                3
            )
        )

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            (
                x + 48,
                y + 48,
                8,
                3
            )
        )

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            (
                x + 60,
                y + 48,
                8,
                3
            )
        )

    # =========================================================
    # XP
    # =========================================================

    def draw_xp(
        self,
        screen,
        exp,
        max_exp
    ):

        x = 20
        y = 105

        width = 330
        height = 34

        # -----------------------------------------------------
        # Panel
        # -----------------------------------------------------

        panel = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.draw_panel(
            screen,
            panel,
            self.BLUE
        )

        # -----------------------------------------------------
        # Label
        # -----------------------------------------------------

        label = self.font_micro.render(
            "EXPERIENCE",
            True,
            self.GRAY
        )

        screen.blit(
            label,
            (
                x + 12,
                y + 5
            )
        )

        # -----------------------------------------------------
        # Percentage
        # -----------------------------------------------------

        if max_exp > 0:
            percentage = (
                exp / max_exp
            ) * 100
        else:
            percentage = 0

        percentage = max(
            0,
            min(
                100,
                percentage
            )
        )

        percent_text = self.font_micro.render(
            f"{int(percentage)}%",
            True,
            self.WHITE
        )

        percent_rect = percent_text.get_rect(
            topright=(
                x + width - 10,
                y + 5
            )
        )

        screen.blit(
            percent_text,
            percent_rect
        )

        # -----------------------------------------------------
        # XP bar
        # -----------------------------------------------------

        self.draw_bar(
            screen,
            x + 10,
            y + 17,
            width - 20,
            11,
            exp,
            max_exp,
            self.BLUE,
            self.BLUE_DARK,
            "",
            ""
        )

    # =========================================================
    # HP
    # =========================================================

    def draw_hp(
        self,
        screen,
        hp,
        max_hp
    ):

        width = 340
        height = 66

        x = 20
        y = self.height - height - 20

        panel = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # -----------------------------------------------------
        # Calculate HP percentage
        # -----------------------------------------------------

        if max_hp > 0:
            percentage = hp / max_hp
        else:
            percentage = 0

        percentage = max(
            0,
            min(
                1,
                percentage
            )
        )

        # -----------------------------------------------------
        # Low HP warning
        # -----------------------------------------------------

        if percentage <= 0.25:

            pulse = (
                math.sin(
                    pygame.time.get_ticks() * 0.01
                )
                + 1
            ) / 2

            accent = (
                255,
                int(40 + pulse * 45),
                int(45 + pulse * 45)
            )

        else:

            accent = self.GREEN

        self.draw_panel(
            screen,
            panel,
            accent
        )

        # -----------------------------------------------------
        # Health label
        # -----------------------------------------------------

        label = self.font_micro.render(
            "HEALTH",
            True,
            self.GRAY
        )

        screen.blit(
            label,
            (
                x + 12,
                y + 8
            )
        )

        # -----------------------------------------------------
        # Health value
        # -----------------------------------------------------

        hp_text = self.font_small.render(
            f"{int(hp)} / {int(max_hp)}",
            True,
            self.WHITE
        )

        hp_rect = hp_text.get_rect(
            topright=(
                x + width - 12,
                y + 7
            )
        )

        screen.blit(
            hp_text,
            hp_rect
        )

        # -----------------------------------------------------
        # Health bar
        # -----------------------------------------------------

        self.draw_bar(
            screen,
            x + 12,
            y + 29,
            width - 24,
            25,
            hp,
            max_hp,
            accent,
            self.RED_DARK,
            "",
            ""
        )

        # -----------------------------------------------------
        # Low HP warning text
        # -----------------------------------------------------

        if percentage <= 0.25:

            warning = self.font_micro.render(
                "LOW",
                True,
                self.WHITE
            )

            warning_rect = warning.get_rect(
                center=(
                    x + width // 2,
                    y + 41
                )
            )

            screen.blit(
                warning,
                warning_rect
            )

    # =========================================================
    # AUTO-FIRE STATUS
    # =========================================================

    def draw_status(
        self,
        screen
    ):

        width = 230
        height = 56

        x = self.width - width - 20
        y = self.height - height - 20

        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.draw_panel(
            screen,
            rect,
            self.GREEN
        )

        # -----------------------------------------------------
        # Animated indicator
        # -----------------------------------------------------

        pulse = (
            math.sin(
                pygame.time.get_ticks() * 0.008
            )
            + 1
        ) / 2

        radius = int(
            5 + pulse * 2
        )

        pygame.draw.circle(
            screen,
            self.GREEN,
            (
                x + 18,
                y + height // 2
            ),
            radius
        )

        pygame.draw.circle(
            screen,
            self.GREEN_DARK,
            (
                x + 18,
                y + height // 2
            ),
            8,
            1
        )

        # -----------------------------------------------------
        # Main text
        # -----------------------------------------------------

        text = self.font_small.render(
            "AUTO-FIRE",
            True,
            self.WHITE
        )

        screen.blit(
            text,
            (
                x + 35,
                y + 10
            )
        )

        # -----------------------------------------------------
        # Subtext
        # -----------------------------------------------------

        subtext = self.font_micro.render(
            "SYSTEM ONLINE",
            True,
            self.GRAY
        )

        screen.blit(
            subtext,
            (
                x + 36,
                y + 31
            )
        )

        # -----------------------------------------------------
        # Status blocks
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.GREEN,
            (
                x + width - 38,
                y + 15,
                4,
                4
            )
        )

        pygame.draw.rect(
            screen,
            self.GREEN,
            (
                x + width - 30,
                y + 15,
                4,
                4
            )
        )

        pygame.draw.rect(
            screen,
            self.GREEN_DARK,
            (
                x + width - 22,
                y + 15,
                4,
                4
            )
        )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        screen,
        hp,
        max_hp,
        exp,
        max_exp,
        level,
        wave
    ):

        self.draw_level(
            screen,
            level
        )

        self.draw_wave(
            screen,
            wave
        )

        self.draw_xp(
            screen,
            exp,
            max_exp
        )

        self.draw_hp(
            screen,
            hp,
            max_hp
        )

        self.draw_status(
            screen
        )