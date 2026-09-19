import pygame
import math


class Settings:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # =====================================================
        # SETTINGS
        # =====================================================

        self.debug_mode = False
        self.speedometer_mode = "off"

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (3, 4, 7)
        self.BACKGROUND = (7, 9, 14)

        self.PANEL = (12, 15, 22)
        self.PANEL_LIGHT = (22, 27, 38)

        self.WHITE = (245, 248, 255)
        self.GRAY = (125, 135, 150)
        self.LIGHT_GRAY = (190, 198, 210)

        self.CYAN = (55, 220, 255)
        self.CYAN_DARK = (20, 75, 95)

        self.YELLOW = (255, 210, 65)
        self.YELLOW_DARK = (100, 75, 20)

        self.GREEN = (65, 235, 125)
        self.RED = (255, 75, 85)

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(
            None,
            72
        )

        self.font_section = pygame.font.Font(
            None,
            22
        )

        self.font_button = pygame.font.Font(
            None,
            22
        )

        self.font_small = pygame.font.Font(
            None,
            14
        )

        self.font_tiny = pygame.font.Font(
            None,
            11
        )

        # =====================================================
        # BACK BUTTON
        # =====================================================

        self.close_rect = pygame.Rect(
            self.width // 2 - 215,
            self.height - 90,
            200,
            50
        )

        # =====================================================
        # MAIN MENU BUTTON
        # =====================================================

        self.main_menu_rect = pygame.Rect(
            self.width // 2 + 15,
            self.height - 90,
            200,
            50
        )

        # =====================================================
        # DEBUG BUTTON
        # =====================================================

        self.debug_rect = pygame.Rect(
            self.width // 2 - 300,
            205,
            600,
            65
        )

        # =====================================================
        # SPEEDOMETER
        # =====================================================

        self.speedometer_rects = []

        modes = [
            "OFF",
            "HORIZONTAL",
            "VERTICAL",
            "BOTH"
        ]

        button_width = 140
        button_height = 58
        gap = 15

        total_width = (
            len(modes) * button_width
            + (len(modes) - 1) * gap
        )

        start_x = (
            self.width // 2
            - total_width // 2
        )

        for i in range(len(modes)):

            rect = pygame.Rect(
                start_x
                + i * (
                    button_width
                    + gap
                ),
                365,
                button_width,
                button_height
            )

            self.speedometer_rects.append(
                rect
            )

        # =====================================================
        # GAME SETTINGS BUTTON
        # =====================================================

        # Top-center so it does not overlap the wave HUD.
        self.button_rect = pygame.Rect(
            self.width // 2 - 28,
            18,
            56,
            42
        )

        # =====================================================
        # PARTICLES
        # =====================================================

        self.particles = []

        for i in range(60):

            self.particles.append({
                "x": (i * 137) % width,
                "y": (i * 83) % height,
                "speed": 0.15 + (i % 5) * 0.08,
                "size": 1 if i % 4 else 2
            })

    # =========================================================
    # PARTICLES
    # =========================================================

    def update_particles(self):

        for particle in self.particles:

            particle["y"] += particle["speed"]

            if particle["y"] > self.height:

                particle["y"] = -5

    # =========================================================
    # BACKGROUND
    # =========================================================

    def draw_background(
        self,
        screen
    ):

        screen.fill(
            self.BACKGROUND
        )

        center_x = self.width // 2
        center_y = self.height // 2

        # -----------------------------------------------------
        # Central glow
        # -----------------------------------------------------

        glow = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        for radius in range(
            420,
            40,
            -40
        ):

            alpha = int(
                2 + (
                    420 - radius
                ) * 0.009
            )

            pygame.draw.circle(
                glow,
                (
                    25,
                    130,
                    180,
                    alpha
                ),
                (
                    center_x,
                    center_y
                ),
                radius
            )

        screen.blit(
            glow,
            (0, 0)
        )

        # -----------------------------------------------------
        # Grid
        # -----------------------------------------------------

        grid_color = (
            13,
            28,
            40
        )

        spacing = 55

        for x in range(
            0,
            self.width,
            spacing
        ):

            pygame.draw.line(
                screen,
                grid_color,
                (
                    x,
                    0
                ),
                (
                    x,
                    self.height
                ),
                1
            )

        for y in range(
            0,
            self.height,
            spacing
        ):

            pygame.draw.line(
                screen,
                grid_color,
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

        # -----------------------------------------------------
        # Particles
        # -----------------------------------------------------

        for particle in self.particles:

            pygame.draw.rect(
                screen,
                (
                    50,
                    140,
                    175
                ),
                (
                    int(particle["x"]),
                    int(particle["y"]),
                    particle["size"],
                    particle["size"]
                )
            )

    # =========================================================
    # PANEL
    # =========================================================

    def draw_panel(
        self,
        screen,
        rect,
        accent
    ):

        shadow = pygame.Rect(
            rect.x + 6,
            rect.y + 6,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow
        )

        pygame.draw.rect(
            screen,
            self.PANEL_LIGHT,
            rect
        )

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

        # Accent bar

        pygame.draw.rect(
            screen,
            accent,
            (
                rect.x,
                rect.y,
                4,
                rect.height
            )
        )

        # Top-right corner

        pygame.draw.line(
            screen,
            self.GRAY,
            (
                rect.right - 12,
                rect.top
            ),
            (
                rect.right,
                rect.top + 12
            ),
            1
        )

        # Bottom-left corner

        pygame.draw.line(
            screen,
            self.GRAY,
            (
                rect.left,
                rect.bottom - 12
            ),
            (
                rect.left + 12,
                rect.bottom
            ),
            1
        )

    # =========================================================
    # SECTION HEADER
    # =========================================================

    def draw_section_header(
        self,
        screen,
        text,
        y,
        accent
    ):

        center_x = self.width // 2

        label = self.font_section.render(
            text,
            True,
            self.WHITE
        )

        label_rect = label.get_rect(
            center=(
                center_x,
                y
            )
        )

        screen.blit(
            label,
            label_rect
        )

        line_y = y + 18

        pygame.draw.line(
            screen,
            (
                30,
                55,
                70
            ),
            (
                center_x - 300,
                line_y
            ),
            (
                center_x + 300,
                line_y
            ),
            1
        )

        pygame.draw.rect(
            screen,
            accent,
            (
                center_x - 45,
                line_y - 1,
                90,
                2
            )
        )

    # =========================================================
    # HANDLE CLICK
    # =========================================================

    def handle_click(
        self,
        mouse_pos
    ):

        # -----------------------------------------------------
        # BACK
        # -----------------------------------------------------

        if self.close_rect.collidepoint(
            mouse_pos
        ):

            return "close"

        # -----------------------------------------------------
        # MAIN MENU
        # -----------------------------------------------------

        if self.main_menu_rect.collidepoint(
            mouse_pos
        ):

            return "main_menu"

        # -----------------------------------------------------
        # DEBUG
        # -----------------------------------------------------

        if self.debug_rect.collidepoint(
            mouse_pos
        ):

            self.debug_mode = (
                not self.debug_mode
            )

            return None

        # -----------------------------------------------------
        # SPEEDOMETER
        # -----------------------------------------------------

        modes = [
            "off",
            "horizontal",
            "vertical",
            "both"
        ]

        for i, rect in enumerate(
            self.speedometer_rects
        ):

            if rect.collidepoint(
                mouse_pos
            ):

                self.speedometer_mode = (
                    modes[i]
                )

                return None

        return None

    # =========================================================
    # OPTION BUTTON
    # =========================================================

    def draw_option_button(
        self,
        screen,
        rect,
        text,
        selected=False,
        accent=None
    ):

        if accent is None:
            accent = self.CYAN

        mouse_pos = pygame.mouse.get_pos()

        hovered = rect.collidepoint(
            mouse_pos
        )

        # -----------------------------------------------------
        # Colours
        # -----------------------------------------------------

        if selected:

            background = (
                20,
                35,
                43
            )

            border = accent

            thickness = 3

        elif hovered:

            background = (
                18,
                24,
                33
            )

            border = self.LIGHT_GRAY

            thickness = 2

        else:

            background = self.PANEL

            border = self.PANEL_LIGHT

            thickness = 2

        # -----------------------------------------------------
        # Shadow
        # -----------------------------------------------------

        shadow = pygame.Rect(
            rect.x + 5,
            rect.y + 5,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow
        )

        # -----------------------------------------------------
        # Button
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            background,
            rect
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            thickness
        )

        # -----------------------------------------------------
        # Accent strip
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            accent,
            (
                rect.x,
                rect.y,
                4,
                rect.height
            )
        )

        # -----------------------------------------------------
        # Selected indicator
        # -----------------------------------------------------

        if selected:

            pygame.draw.circle(
                screen,
                accent,
                (
                    rect.right - 16,
                    rect.centery
                ),
                5
            )

            pygame.draw.circle(
                screen,
                accent,
                (
                    rect.right - 16,
                    rect.centery
                ),
                9,
                1
            )

        # -----------------------------------------------------
        # Text
        # -----------------------------------------------------

        text_surface = self.font_button.render(
            text,
            True,
            self.WHITE
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # =========================================================
    # GAME SETTINGS BUTTON
    # =========================================================

    def draw_button(
        self,
        screen
    ):

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.button_rect.collidepoint(
            mouse_pos
        )

        if hovered:

            background = (
                20,
                32,
                40
            )

            border = self.CYAN

        else:

            background = self.PANEL

            border = self.PANEL_LIGHT

        # Shadow

        shadow = pygame.Rect(
            self.button_rect.x + 4,
            self.button_rect.y + 4,
            self.button_rect.width,
            self.button_rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow
        )

        pygame.draw.rect(
            screen,
            background,
            self.button_rect
        )

        pygame.draw.rect(
            screen,
            border,
            self.button_rect,
            2
        )

        center = self.button_rect.center

        # Gear-like icon

        pygame.draw.circle(
            screen,
            self.WHITE,
            center,
            10,
            2
        )

        pygame.draw.circle(
            screen,
            self.CYAN,
            center,
            4
        )

        for angle in range(
            0,
            360,
            45
        ):

            radians = math.radians(angle)

            inner_x = (
                center[0]
                + math.cos(radians) * 11
            )

            inner_y = (
                center[1]
                + math.sin(radians) * 11
            )

            outer_x = (
                center[0]
                + math.cos(radians) * 14
            )

            outer_y = (
                center[1]
                + math.sin(radians) * 14
            )

            pygame.draw.line(
                screen,
                self.WHITE,
                (
                    int(inner_x),
                    int(inner_y)
                ),
                (
                    int(outer_x),
                    int(outer_y)
                ),
                2
            )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        screen
    ):

        self.update_particles()

        self.draw_background(
            screen
        )

        center_x = self.width // 2

        # =====================================================
        # TOP DECORATION
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                70,
                42
            ),
            (
                center_x - 190,
                42
            ),
            1
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                center_x + 190,
                42
            ),
            (
                self.width - 70,
                42
            ),
            1
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                center_x - 70,
                40,
                140,
                3
            )
        )

        # =====================================================
        # TITLE
        # =====================================================

        title_shadow = self.font_title.render(
            "SETTINGS",
            True,
            (
                15,
                60,
                75
            )
        )

        shadow_rect = title_shadow.get_rect(
            center=(
                center_x + 4,
                100 + 4
            )
        )

        screen.blit(
            title_shadow,
            shadow_rect
        )

        title = self.font_title.render(
            "SETTINGS",
            True,
            self.WHITE
        )

        title_rect = title.get_rect(
            center=(
                center_x,
                100
            )
        )

        screen.blit(
            title,
            title_rect
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                center_x - 130,
                145,
                260,
                2
            )
        )

        subtitle = self.font_small.render(
            "SYSTEM CONFIGURATION // PLAYER OPTIONS",
            True,
            self.GRAY
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                165
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        # =====================================================
        # DEBUG PANEL
        # =====================================================

        debug_panel = pygame.Rect(
            center_x - 330,
            190,
            660,
            105
        )

        self.draw_panel(
            screen,
            debug_panel,
            self.YELLOW
        )

        debug_label = self.font_tiny.render(
            "DEVELOPER OPTION",
            True,
            self.YELLOW
        )

        screen.blit(
            debug_label,
            (
                debug_panel.x + 18,
                debug_panel.y + 10
            )
        )

        debug_text = (
            "DEBUG MODE: ONLINE"
            if self.debug_mode
            else
            "DEBUG MODE: OFFLINE"
        )

        self.draw_option_button(
            screen,
            self.debug_rect,
            debug_text,
            self.debug_mode,
            self.YELLOW
        )

        # =====================================================
        # SPEEDOMETER
        # =====================================================

        self.draw_section_header(
            screen,
            "SPEEDOMETER DISPLAY",
            330,
            self.CYAN
        )

        modes = [
            "OFF",
            "HORIZONTAL",
            "VERTICAL",
            "BOTH"
        ]

        for i, rect in enumerate(
            self.speedometer_rects
        ):

            self.draw_option_button(
                screen,
                rect,
                modes[i],
                self.speedometer_mode
                == modes[i].lower(),
                self.CYAN
            )

        # =====================================================
        # BOTTOM BUTTONS
        # =====================================================

        self.draw_option_button(
            screen,
            self.close_rect,
            "BACK",
            False,
            self.CYAN
        )

        self.draw_option_button(
            screen,
            self.main_menu_rect,
            "MAIN MENU",
            False,
            self.YELLOW
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = self.font_small.render(
            "CONFIGURATION SAVED AUTOMATICALLY",
            True,
            (
                70,
                80,
                95
            )
        )

        footer_rect = footer.get_rect(
            center=(
                center_x,
                self.height - 25
            )
        )

        screen.blit(
            footer,
            footer_rect
        )

        # =====================================================
        # CORNER STATUS
        # =====================================================

        status = self.font_tiny.render(
            "SYSTEM // READY",
            True,
            self.CYAN
        )

        screen.blit(
            status,
            (
                20,
                20
            )
        )