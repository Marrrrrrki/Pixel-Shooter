import pygame
import math


class GameOverScreen:

    def __init__(
        self,
        width,
        height
    ):

        self.width = width
        self.height = height

        self.active = False
        self.wave = 1

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (3, 4, 7)
        self.BACKGROUND = (7, 9, 14)

        self.PANEL = (12, 15, 22)
        self.PANEL_LIGHT = (24, 28, 38)
        self.PANEL_HOVER = (22, 28, 38)

        self.WHITE = (245, 248, 255)
        self.GRAY = (125, 135, 150)
        self.LIGHT_GRAY = (195, 202, 215)

        self.CYAN = (55, 220, 255)
        self.CYAN_DARK = (20, 75, 95)

        self.RED = (255, 65, 75)
        self.RED_DARK = (100, 20, 28)

        self.YELLOW = (255, 210, 65)
        self.YELLOW_DARK = (100, 75, 20)

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(
            None,
            76
        )

        self.font_status = pygame.font.Font(
            None,
            18
        )

        self.font_wave = pygame.font.Font(
            None,
            30
        )

        self.font_button = pygame.font.Font(
            None,
            24
        )

        self.font_small = pygame.font.Font(
            None,
            13
        )

        self.font_tiny = pygame.font.Font(
            None,
            11
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_width = 300
        button_height = 62

        center_x = self.width // 2

        self.restart_rect = pygame.Rect(
            center_x - button_width // 2,
            self.height // 2 + 65,
            button_width,
            button_height
        )

        self.menu_rect = pygame.Rect(
            center_x - button_width // 2,
            self.height // 2 + 145,
            button_width,
            button_height
        )

        # =====================================================
        # ANIMATION
        # =====================================================

        self.animation_start = 0

        self.particles = []

        for i in range(90):

            self.particles.append({
                "x": (i * 137) % width,
                "y": (i * 83) % height,
                "speed": 0.2 + (i % 5) * 0.08,
                "size": 1 if i % 4 else 2
            })

    # =========================================================
    # OPEN
    # =========================================================

    def open(self, wave):

        self.active = True

        self.wave = wave

        self.animation_start = (
            pygame.time.get_ticks()
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.active = False

    # =========================================================
    # EVENTS
    # =========================================================

    def handle_event(self, event):

        if not self.active:
            return None

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        if self.restart_rect.collidepoint(
            event.pos
        ):

            self.close()

            return "restart"

        if self.menu_rect.collidepoint(
            event.pos
        ):

            self.close()

            return "menu"

        return None

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

    def draw_background(self, screen):

        screen.fill(
            self.BACKGROUND
        )

        center_x = self.width // 2
        center_y = self.height // 2

        # -----------------------------------------------------
        # RED CENTRAL GLOW
        # -----------------------------------------------------

        glow = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        for radius in range(
            430,
            40,
            -35
        ):

            alpha = int(
                3 +
                (430 - radius) * 0.012
            )

            pygame.draw.circle(
                glow,
                (
                    180,
                    25,
                    35,
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
        # GRID
        # -----------------------------------------------------

        grid_color = (
            22,
            24,
            34
        )

        spacing = 60

        for x in range(
            0,
            self.width,
            spacing
        ):

            pygame.draw.line(
                screen,
                grid_color,
                (x, 0),
                (x, self.height),
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
                (0, y),
                (self.width, y),
                1
            )

        # -----------------------------------------------------
        # PARTICLES
        # -----------------------------------------------------

        for particle in self.particles:

            pygame.draw.rect(
                screen,
                (
                    125,
                    45,
                    55
                ),
                (
                    int(particle["x"]),
                    int(particle["y"]),
                    particle["size"],
                    particle["size"]
                )
            )

    # =========================================================
    # CORNER DECORATION
    # =========================================================

    def draw_decoration(self, screen):

        center_x = self.width // 2

        # -----------------------------------------------------
        # TOP LINE
        # -----------------------------------------------------

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (70, 42),
            (center_x - 190, 42),
            1
        )

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (center_x + 190, 42),
            (self.width - 70, 42),
            1
        )

        pygame.draw.rect(
            screen,
            self.RED,
            (
                center_x - 65,
                40,
                130,
                3
            )
        )

        # -----------------------------------------------------
        # SIDE BRACKETS
        # -----------------------------------------------------

        bracket_y = (
            self.height // 2 - 155
        )

        # Left

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (55, bracket_y),
            (55, bracket_y + 100),
            2
        )

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (55, bracket_y),
            (82, bracket_y),
            2
        )

        # Right

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (
                self.width - 55,
                bracket_y
            ),
            (
                self.width - 55,
                bracket_y + 100
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (
                self.width - 55,
                bracket_y
            ),
            (
                self.width - 82,
                bracket_y
            ),
            2
        )

    # =========================================================
    # CENTRAL WARNING ICON
    # =========================================================

    def draw_warning_icon(self, screen):

        center_x = self.width // 2
        center_y = self.height // 2 - 125

        pulse = (
            math.sin(
                pygame.time.get_ticks() * 0.006
            ) + 1
        ) / 2

        radius = int(
            31 +
            pulse * 3
        )

        # Outer glow

        glow = pygame.Surface(
            (100, 100),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (
                255,
                45,
                55,
                18
            ),
            (50, 50),
            radius + 8
        )

        pygame.draw.circle(
            glow,
            (
                255,
                45,
                55,
                28
            ),
            (50, 50),
            radius
        )

        screen.blit(
            glow,
            (
                center_x - 50,
                center_y - 50
            )
        )

        # Outer ring

        pygame.draw.circle(
            screen,
            self.RED_DARK,
            (
                center_x,
                center_y
            ),
            radius + 5,
            2
        )

        pygame.draw.circle(
            screen,
            self.RED,
            (
                center_x,
                center_y
            ),
            radius,
            2
        )

        # Warning triangle

        triangle = [

            (
                center_x,
                center_y - 17
            ),

            (
                center_x - 18,
                center_y + 15
            ),

            (
                center_x + 18,
                center_y + 15
            )
        ]

        pygame.draw.polygon(
            screen,
            self.RED_DARK,
            triangle
        )

        pygame.draw.polygon(
            screen,
            self.RED,
            triangle,
            2
        )

        # Exclamation mark

        pygame.draw.rect(
            screen,
            self.WHITE,
            (
                center_x - 2,
                center_y - 8,
                4,
                12
            )
        )

        pygame.draw.rect(
            screen,
            self.WHITE,
            (
                center_x - 2,
                center_y + 7,
                4,
                4
            )
        )

    # =========================================================
    # BUTTON
    # =========================================================

    def draw_button(
        self,
        screen,
        rect,
        text
    ):

        mouse_pos = pygame.mouse.get_pos()

        hovered = rect.collidepoint(
            mouse_pos
        )

        if text == "RESTART":

            accent = self.CYAN

        else:

            accent = self.YELLOW

        if hovered:

            background = self.PANEL_HOVER
            border = accent
            thickness = 3

        else:

            background = self.PANEL
            border = self.PANEL_LIGHT
            thickness = 2

        # -----------------------------------------------------
        # Shadow
        # -----------------------------------------------------

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
        # Accent bars
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            accent,
            (
                rect.x,
                rect.y,
                5,
                rect.height
            )
        )

        if hovered:

            pygame.draw.rect(
                screen,
                accent,
                (
                    rect.right - 5,
                    rect.y,
                    5,
                    rect.height
                )
            )

        # -----------------------------------------------------
        # Arrow
        # -----------------------------------------------------

        arrow_x = rect.x + 25
        arrow_y = rect.centery

        if text == "RESTART":

            points = [

                (
                    arrow_x + 8,
                    arrow_y - 7
                ),

                (
                    arrow_x,
                    arrow_y
                ),

                (
                    arrow_x + 8,
                    arrow_y + 7
                )
            ]

        else:

            points = [

                (
                    arrow_x,
                    arrow_y - 7
                ),

                (
                    arrow_x + 8,
                    arrow_y
                ),

                (
                    arrow_x,
                    arrow_y + 7
                )
            ]

        pygame.draw.polygon(
            screen,
            accent,
            points
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
            center=(
                rect.centerx + 5,
                rect.centery
            )
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        if not self.active:
            return

        current_time = (
            pygame.time.get_ticks()
        )

        elapsed = (
            current_time -
            self.animation_start
        )

        self.update_particles()

        self.draw_background(
            screen
        )

        # -----------------------------------------------------
        # DARK OVERLAY
        # -----------------------------------------------------

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 65)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        self.draw_decoration(
            screen
        )

        # -----------------------------------------------------
        # MAIN PANEL
        # -----------------------------------------------------

        panel_width = 560
        panel_height = 480

        panel = pygame.Rect(
            self.width // 2 - panel_width // 2,
            self.height // 2 - 235,
            panel_width,
            panel_height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            (
                panel.x + 8,
                panel.y + 8,
                panel.width,
                panel.height
            )
        )

        pygame.draw.rect(
            screen,
            self.PANEL_LIGHT,
            panel
        )

        inner = panel.inflate(
            -4,
            -4
        )

        pygame.draw.rect(
            screen,
            self.PANEL,
            inner
        )

        pygame.draw.rect(
            screen,
            self.RED_DARK,
            panel,
            2
        )

        # -----------------------------------------------------
        # PANEL TOP ACCENT
        # -----------------------------------------------------

        pygame.draw.rect(
            screen,
            self.RED,
            (
                panel.x + 20,
                panel.y,
                panel.width - 40,
                3
            )
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        status = self.font_status.render(
            "SYSTEM FAILURE",
            True,
            self.RED
        )

        status_rect = status.get_rect(
            center=(
                self.width // 2,
                panel.y + 28
            )
        )

        screen.blit(
            status,
            status_rect
        )

        # -----------------------------------------------------
        # WARNING ICON
        # -----------------------------------------------------

        self.draw_warning_icon(
            screen
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        pulse = (
            math.sin(
                current_time * 0.004
            ) + 1
        ) / 2

        title_color = (
            255,
            int(60 + pulse * 35),
            int(70 + pulse * 25)
        )

        shadow = self.font_title.render(
            "GAME OVER",
            True,
            self.RED_DARK
        )

        shadow_rect = shadow.get_rect(
            center=(
                self.width // 2 + 4,
                self.height // 2 - 48
            )
        )

        screen.blit(
            shadow,
            shadow_rect
        )

        title = self.font_title.render(
            "GAME OVER",
            True,
            title_color
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                self.height // 2 - 52
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # -----------------------------------------------------
        # TITLE LINE
        # -----------------------------------------------------

        center_x = self.width // 2

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (
                center_x - 190,
                self.height // 2 - 8
            ),
            (
                center_x - 80,
                self.height // 2 - 8
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.RED_DARK,
            (
                center_x + 80,
                self.height // 2 - 8
            ),
            (
                center_x + 190,
                self.height // 2 - 8
            ),
            2
        )

        # -----------------------------------------------------
        # WAVE
        # -----------------------------------------------------

        wave_text = self.font_wave.render(
            "REACHED WAVE "
            + str(self.wave),
            True,
            self.LIGHT_GRAY
        )

        wave_rect = wave_text.get_rect(
            center=(
                center_x,
                self.height // 2 + 22
            )
        )

        screen.blit(
            wave_text,
            wave_rect
        )

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        self.draw_button(
            screen,
            self.restart_rect,
            "RESTART"
        )

        self.draw_button(
            screen,
            self.menu_rect,
            "MAIN MENU"
        )

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        footer = self.font_tiny.render(
            "RUN TERMINATED // "
            "AWAITING COMMAND",
            True,
            self.GRAY
        )

        footer_rect = footer.get_rect(
            center=(
                center_x,
                self.height - 18
            )
        )

        screen.blit(
            footer,
            footer_rect
        )