import pygame
import math
import random

from Game.journal import Journal


class MainMenu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (2, 3, 6)

        self.BACKGROUND = (5, 8, 14)

        self.PANEL = (10, 14, 22)

        self.PANEL_LIGHT = (24, 31, 43)

        self.PANEL_HOVER = (17, 27, 39)

        self.WHITE = (245, 248, 255)

        self.GRAY = (115, 128, 145)

        self.LIGHT_GRAY = (185, 195, 210)

        self.CYAN = (55, 220, 255)

        self.CYAN_LIGHT = (125, 240, 255)

        self.CYAN_DARK = (15, 70, 90)

        self.BLUE = (55, 110, 255)

        self.BLUE_DARK = (20, 45, 90)

        self.YELLOW = (255, 210, 65)

        self.YELLOW_DARK = (105, 75, 20)

        self.GREEN = (65, 235, 125)

        self.RED = (255, 70, 80)

        self.RED_LIGHT = (255, 120, 125)

        self.RED_DARK = (95, 20, 28)

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(
            None,
            92
        )

        self.font_subtitle = pygame.font.Font(
            None,
            21
        )

        self.font_button = pygame.font.Font(
            None,
            30
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
        # BUTTONS
        # =====================================================

        button_width = 320

        button_height = 70

        self.play_rect = pygame.Rect(
            width // 2 - button_width // 2,
            height // 2 - 140,
            button_width,
            button_height
        )

        self.journal_rect = pygame.Rect(
            width // 2 - button_width // 2,
            height // 2 - 55,
            button_width,
            button_height
        )

        self.settings_rect = pygame.Rect(
            width // 2 - button_width // 2,
            height // 2 + 30,
            button_width,
            button_height
        )

        self.quit_rect = pygame.Rect(
            width // 2 - button_width // 2,
            height // 2 + 115,
            button_width,
            button_height
        )

        self.journal = Journal()
        self.journal_active = False
        self.journal_tab = "enemies"
        self.journal_enemies_rect = pygame.Rect(width // 2 - 170, 115, 160, 48)
        self.journal_upgrades_rect = pygame.Rect(width // 2 + 10, 115, 160, 48)
        self.journal_back_rect = pygame.Rect(35, height - 75, 150, 48)
        self.journal_hover = 0.0

        # =====================================================
        # PARTICLES
        # =====================================================

        self.particles = []

        for _ in range(110):

            self.particles.append({

                "x": random.uniform(
                    0,
                    width
                ),

                "y": random.uniform(
                    0,
                    height
                ),

                "speed": random.uniform(
                    0.15,
                    0.8
                ),

                "size": random.choice(
                    [
                        1,
                        1,
                        1,
                        2
                    ]
                ),

                "phase": random.uniform(
                    0,
                    math.pi * 2
                )

            })

        # =====================================================
        # GRID ANIMATION
        # =====================================================

        self.grid_offset = 0

        # =====================================================
        # BUTTON ANIMATION
        # =====================================================

        self.play_hover = 0.0

        self.settings_hover = 0.0

        self.quit_hover = 0.0

        # =====================================================
        # BOOT ANIMATION
        # =====================================================

        self.start_time = pygame.time.get_ticks()

    # =========================================================
    # PARTICLES
    # =========================================================

    def update_particles(self):

        self.grid_offset += 0.35

        if self.grid_offset >= 35:

            self.grid_offset -= 35

        for particle in self.particles:

            particle["y"] += particle["speed"]

            if particle["y"] > self.height + 5:

                particle["y"] = -5

                particle["x"] = random.uniform(
                    0,
                    self.width
                )

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

        # =====================================================
        # CENTRAL ATMOSPHERIC GLOW
        # =====================================================

        glow = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        for radius in range(
            520,
            40,
            -35
        ):

            alpha = int(
                1 +
                (520 - radius) * 0.012
            )

            pygame.draw.circle(
                glow,
                (
                    20,
                    130,
                    190,
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

        # =====================================================
        # HORIZONTAL SCANLINES
        # =====================================================

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
            6
        ):

            pygame.draw.line(
                scanlines,
                (
                    40,
                    120,
                    150,
                    10
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
        # PERSPECTIVE GRID
        # =====================================================

        horizon = int(
            self.height * 0.61
        )

        grid_color = (
            12,
            34,
            48
        )

        # Vertical perspective lines

        spacing = 55

        for x in range(
            -self.width * 2,
            self.width * 3,
            spacing
        ):

            pygame.draw.line(
                screen,
                grid_color,
                (
                    center_x,
                    horizon
                ),
                (
                    x,
                    self.height
                ),
                1
            )

        # Moving horizontal grid

        grid_y = horizon + self.grid_offset

        while grid_y < self.height:

            pygame.draw.line(
                screen,
                grid_color,
                (
                    0,
                    int(grid_y)
                ),
                (
                    self.width,
                    int(grid_y)
                ),
                1
            )

            distance = (
                grid_y -
                horizon
            )

            grid_y += max(
                14,
                distance * 0.16
            )

        # =====================================================
        # HORIZON GLOW
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                0,
                horizon
            ),
            (
                self.width,
                horizon
            ),
            1
        )

        pygame.draw.line(
            screen,
            (
                25,
                100,
                125
            ),
            (
                center_x - 250,
                horizon
            ),
            (
                center_x + 250,
                horizon
            ),
            2
        )

        # =====================================================
        # PARTICLES
        # =====================================================

        current_time = pygame.time.get_ticks()

        for particle in self.particles:

            pulse = (
                math.sin(
                    current_time * 0.002
                    + particle["phase"]
                )
                + 1
            ) / 2

            brightness = int(
                70 +
                pulse * 70
            )

            pygame.draw.rect(
                screen,
                (
                    brightness // 2,
                    brightness,
                    min(
                        255,
                        brightness + 25
                    )
                ),
                (
                    int(
                        particle["x"]
                    ),
                    int(
                        particle["y"]
                    ),
                    particle["size"],
                    particle["size"]
                )
            )

    # =========================================================
    # TOP HUD
    # =========================================================

    def draw_top_hud(
        self,
        screen
    ):

        center_x = self.width // 2

        # =====================================================
        # LEFT LINE
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                45,
                42
            ),
            (
                center_x - 185,
                42
            ),
            1
        )

        # =====================================================
        # RIGHT LINE
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                center_x + 185,
                42
            ),
            (
                self.width - 45,
                42
            ),
            1
        )

        # =====================================================
        # CENTER MARKER
        # =====================================================

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                center_x - 65,
                40,
                130,
                3
            )
        )

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            (
                center_x - 110,
                47,
                220,
                1
            )
        )

        # =====================================================
        # LEFT SYSTEM STATUS
        # =====================================================

        status = self.font_tiny.render(
            "SYS_01",
            True,
            self.CYAN
        )

        screen.blit(
            status,
            (
                45,
                54
            )
        )

        # =====================================================
        # RIGHT SYSTEM STATUS
        # =====================================================

        status = self.font_tiny.render(
            "ONLINE",
            True,
            self.GREEN
        )

        status_rect = status.get_rect(
            topright=(
                self.width - 45,
                54
            )
        )

        screen.blit(
            status,
            status_rect
        )

    # =========================================================
    # SIDE DECORATION
    # =========================================================

    def draw_side_decoration(
        self,
        screen
    ):

        center_y = self.height // 2

        # =====================================================
        # LEFT BRACKET
        # =====================================================

        left_x = 55

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                left_x,
                center_y - 110
            ),
            (
                left_x,
                center_y + 110
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                left_x,
                center_y - 110
            ),
            (
                left_x + 28,
                center_y - 110
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                left_x,
                center_y + 110
            ),
            (
                left_x + 28,
                center_y + 110
            ),
            2
        )

        # =====================================================
        # RIGHT BRACKET
        # =====================================================

        right_x = self.width - 55

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                right_x,
                center_y - 110
            ),
            (
                right_x,
                center_y + 110
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                right_x,
                center_y - 110
            ),
            (
                right_x - 28,
                center_y - 110
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                right_x,
                center_y + 110
            ),
            (
                right_x - 28,
                center_y + 110
            ),
            2
        )

        # =====================================================
        # SMALL TICKS
        # =====================================================

        for i in range(
            5
        ):

            y = (
                center_y -
                80 +
                i * 40
            )

            pygame.draw.line(
                screen,
                self.CYAN_DARK,
                (
                    left_x + 8,
                    y
                ),
                (
                    left_x + 20,
                    y
                ),
                1
            )

            pygame.draw.line(
                screen,
                self.CYAN_DARK,
                (
                    right_x - 8,
                    y
                ),
                (
                    right_x - 20,
                    y
                ),
                1
            )

    # =========================================================
    # TITLE
    # =========================================================

    def draw_title(
        self,
        screen
    ):

        center_x = self.width // 2

        current_time = pygame.time.get_ticks()

        # =====================================================
        # SYSTEM LABEL
        # =====================================================

        label = self.font_small.render(
            "SYSTEM // ONLINE",
            True,
            self.CYAN
        )

        label_rect = label.get_rect(
            center=(
                center_x,
                104
            )
        )

        screen.blit(
            label,
            label_rect
        )

        # =====================================================
        # TITLE GLOW
        # =====================================================

        glow_surface = pygame.Surface(
            (
                800,
                130
            ),
            pygame.SRCALPHA
        )

        glow_alpha = int(
            25 +
            math.sin(
                current_time * 0.004
            ) * 10
        )

        glow_text = self.font_title.render(
            "PIXEL SHOOTER",
            True,
            (
                30,
                200,
                255,
                glow_alpha
            )
        )

        glow_rect = glow_text.get_rect(
            center=(
                400,
                65
            )
        )

        glow_surface.blit(
            glow_text,
            glow_rect
        )

        screen.blit(
            glow_surface,
            (
                center_x - 400,
                95
            )
        )

        # =====================================================
        # TITLE SHADOW
        # =====================================================

        shadow = self.font_title.render(
            "PIXEL SHOOTER",
            True,
            (
                10,
                55,
                70
            )
        )

        shadow_rect = shadow.get_rect(
            center=(
                center_x + 5,
                151
            )
        )

        screen.blit(
            shadow,
            shadow_rect
        )

        # =====================================================
        # MAIN TITLE
        # =====================================================

        title = self.font_title.render(
            "PIXEL SHOOTER",
            True,
            self.WHITE
        )

        title_rect = title.get_rect(
            center=(
                center_x,
                146
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =====================================================
        # TITLE UNDERLINE
        # =====================================================

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                center_x - 160,
                190,
                320,
                3
            )
        )

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            (
                center_x - 225,
                197,
                450,
                1
            )
        )

        # =====================================================
        # SMALL CENTER DIAMOND
        # =====================================================

        pygame.draw.polygon(
            screen,
            self.CYAN,
            [
                (
                    center_x,
                    184
                ),
                (
                    center_x + 5,
                    189
                ),
                (
                    center_x,
                    194
                ),
                (
                    center_x - 5,
                    189
                )
            ]
        )

        # =====================================================
        # SUBTITLE
        # =====================================================

        subtitle = self.font_subtitle.render(
            "SURVIVE // ADAPT // DESTROY",
            True,
            self.GRAY
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                225
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

    # =========================================================
    # TARGET RETICLE
    # =========================================================

    def draw_reticle(
        self,
        screen
    ):

        center_x = self.width // 2

        center_y = (
            self.height // 2
            + 80
        )

        current_time = pygame.time.get_ticks()

        rotation = (
            current_time *
            0.04
        )

        radius = 210

        # =====================================================
        # OUTER RING
        # =====================================================

        pygame.draw.circle(
            screen,
            (
                15,
                50,
                65
            ),
            (
                center_x,
                center_y
            ),
            radius,
            1
        )

        # =====================================================
        # ROTATING TICKS
        # =====================================================

        for angle in range(
            0,
            360,
            45
        ):

            radians = math.radians(
                angle + rotation
            )

            inner_radius = radius - 7

            outer_radius = radius + 7

            x1 = (
                center_x +
                math.cos(radians)
                * inner_radius
            )

            y1 = (
                center_y +
                math.sin(radians)
                * inner_radius
            )

            x2 = (
                center_x +
                math.cos(radians)
                * outer_radius
            )

            y2 = (
                center_y +
                math.sin(radians)
                * outer_radius
            )

            pygame.draw.line(
                screen,
                self.CYAN_DARK,
                (
                    int(x1),
                    int(y1)
                ),
                (
                    int(x2),
                    int(y2)
                ),
                1
            )

        # =====================================================
        # CENTER CROSSHAIR
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                center_x - 270,
                center_y
            ),
            (
                center_x - 190,
                center_y
            ),
            1
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                center_x + 190,
                center_y
            ),
            (
                center_x + 270,
                center_y
            ),
            1
        )

    # =========================================================
    # BUTTON
    # =========================================================

    def draw_button(
        self,
        screen,
        rect,
        text,
        accent,
        button_id
    ):

        mouse_pos = pygame.mouse.get_pos()

        hovered = rect.collidepoint(
            mouse_pos
        )

        # =====================================================
        # SELECT CORRECT HOVER ANIMATION
        # =====================================================

        if button_id == "play":

            target = (
                1.0
                if hovered
                else 0.0
            )

            self.play_hover += (
                target -
                self.play_hover
            ) * 0.16

            hover_amount = self.play_hover

        elif button_id == "settings":

            target = (
                1.0
                if hovered
                else 0.0
            )

            self.settings_hover += (
                target -
                self.settings_hover
            ) * 0.16

            hover_amount = self.settings_hover

        elif button_id == "journal":

            target = (
                1.0
                if hovered
                else 0.0
            )

            self.journal_hover += (
                target -
                self.journal_hover
            ) * 0.16

            hover_amount = self.journal_hover

        else:

            target = (
                1.0
                if hovered
                else 0.0
            )

            self.quit_hover += (
                target -
                self.quit_hover
            ) * 0.16

            hover_amount = self.quit_hover

        # =====================================================
        # BACKGROUND
        # =====================================================

        background = (

            int(
                10 +
                hover_amount * 12
            ),

            int(
                14 +
                hover_amount * 14
            ),

            int(
                22 +
                hover_amount * 18
            )
        )

        # =====================================================
        # SHADOW
        # =====================================================

        shadow_rect = pygame.Rect(
            rect.x + 7,
            rect.y + 7,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow_rect
        )

        # =====================================================
        # BUTTON
        # =====================================================

        pygame.draw.rect(
            screen,
            background,
            rect
        )

        border_color = (
            accent
            if hovered
            else self.PANEL_LIGHT
        )

        pygame.draw.rect(
            screen,
            border_color,
            rect,
            2
        )

        # =====================================================
        # INNER BORDER
        # =====================================================

        inner = rect.inflate(
            -8,
            -8
        )

        pygame.draw.rect(
            screen,
            (
                accent
                if hovered
                else (
                    15,
                    25,
                    35
                )
            ),
            inner,
            1
        )

        # =====================================================
        # LEFT ACCENT
        # =====================================================

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

        # =====================================================
        # RIGHT ACCENT
        # =====================================================

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

        # =====================================================
        # ANIMATED SCAN BAR
        # =====================================================

        if hovered:

            scan_position = int(
                (
                    pygame.time.get_ticks()
                    * 0.25
                )
                % rect.width
            )

            pygame.draw.rect(
                screen,
                accent,
                (
                    rect.x +
                    scan_position,
                    rect.y + 3,
                    2,
                    rect.height - 6
                )
            )

        # =====================================================
        # ARROW
        # =====================================================

        arrow_x = (
            rect.x +
            27
        )

        arrow_y = rect.centery

        arrow_offset = int(
            hover_amount * 4
        )

        if button_id == "quit":

            # Pointing outward for the exit button.

            pygame.draw.polygon(
                screen,
                accent,
                [
                    (
                        arrow_x -
                        arrow_offset,
                        arrow_y - 7
                    ),
                    (
                        arrow_x +
                        10 -
                        arrow_offset,
                        arrow_y
                    ),
                    (
                        arrow_x -
                        arrow_offset,
                        arrow_y + 7
                    )
                ]
            )

        else:

            pygame.draw.polygon(
                screen,
                accent,
                [
                    (
                        arrow_x +
                        arrow_offset,
                        arrow_y - 7
                    ),
                    (
                        arrow_x +
                        10 +
                        arrow_offset,
                        arrow_y
                    ),
                    (
                        arrow_x +
                        arrow_offset,
                        arrow_y + 7
                    )
                ]
            )

        # =====================================================
        # BUTTON TEXT
        # =====================================================

        text_color = (
            (
                self.RED_LIGHT
                if button_id == "quit"
                else self.CYAN_LIGHT
            )
            if hovered
            else self.WHITE
        )

        text_surface = self.font_button.render(
            text,
            True,
            text_color
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

        # =====================================================
        # HOTKEY
        # =====================================================

        if button_id == "play":

            hotkey_text = "ENTER"

        elif button_id == "settings":

            hotkey_text = "ESC"

        else:

            hotkey_text = "Q"

        hotkey = self.font_tiny.render(
            hotkey_text,
            True,
            self.GRAY
        )

        hotkey_rect = hotkey.get_rect(
            midright=(
                rect.right - 18,
                rect.centery
            )
        )

        screen.blit(
            hotkey,
            hotkey_rect
        )

    # =========================================================
    # BOTTOM HUD
    # =========================================================

    def draw_bottom_hud(
        self,
        screen
    ):

        # =====================================================
        # VERSION
        # =====================================================

        version = self.font_small.render(
            "PIXEL SHOOTER // v1.0",
            True,
            (
                70,
                82,
                98
            )
        )

        screen.blit(
            version,
            (
                20,
                self.height - 28
            )
        )

        # =====================================================
        # READY STATUS
        # =====================================================

        pulse = (
            math.sin(
                pygame.time.get_ticks()
                * 0.008
            )
            + 1
        ) / 2

        status_color = (
            int(
                45 +
                pulse * 20
            ),
            int(
                200 +
                pulse * 35
            ),
            int(
                120 +
                pulse * 30
            )
        )

        pygame.draw.circle(
            screen,
            status_color,
            (
                self.width - 82,
                self.height - 25
            ),
            4
        )

        status = self.font_small.render(
            "READY",
            True,
            status_color
        )

        screen.blit(
            status,
            (
                self.width - 70,
                self.height - 32
            )
        )

        # =====================================================
        # BUILD STATUS
        # =====================================================

        build = self.font_tiny.render(
            "BUILD // STABLE",
            True,
            self.GRAY
        )

        build_rect = build.get_rect(
            center=(
                self.width // 2,
                self.height - 23
            )
        )

        screen.blit(
            build,
            build_rect
        )

    # =========================================================
    # JOURNAL
    # =========================================================

    def draw_journal(self, screen):
        self.journal.load()
        screen.fill(self.BACKGROUND)

        for x in range(0, self.width, 40):
            pygame.draw.line(screen, (10, 25, 35), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 40):
            pygame.draw.line(screen, (10, 25, 35), (0, y), (self.width, y), 1)

        title = self.font_title.render("JOURNAL", True, self.WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 58)))
        subtitle = self.font_small.render("DISCOVERED DATA // FIELD RECORDS", True, self.CYAN)
        screen.blit(subtitle, subtitle.get_rect(center=(self.width // 2, 92)))

        tabs = ((self.journal_enemies_rect, "ENEMIES", "enemies"), (self.journal_upgrades_rect, "UPGRADES", "upgrades"))
        for rect, label, tab in tabs:
            active = self.journal_tab == tab
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, self.PANEL_HOVER if active or hovered else self.PANEL, rect)
            pygame.draw.rect(screen, self.CYAN if active else (self.YELLOW if hovered else self.PANEL_LIGHT), rect, 2)
            text = self.font_small.render(label, True, self.WHITE if active else self.LIGHT_GRAY)
            screen.blit(text, text.get_rect(center=rect.center))

        panel = pygame.Rect(120, 185, self.width - 240, self.height - 290)
        pygame.draw.rect(screen, self.BLACK, panel.move(6, 7))
        pygame.draw.rect(screen, self.PANEL, panel)
        pygame.draw.rect(screen, self.PANEL_LIGHT, panel, 2)

        if self.journal_tab == "enemies":
            records = [
                ("normal", "NORMAL ENEMY", "Standard hostile unit."),
                ("runner", "RUNNER", "Moves slightly faster than a normal enemy.")
            ]
        else:
            records = [
                ("fire_rate", "RAPID FIRE", "Fire 20% faster"),
                ("bullet_speed", "BULLET SPEED", "Bullets move 25% faster"),
                ("damage", "BULLET POWER", "Bullets deal 5 more damage"),
                ("max_hp", "MAX HP", "Increase maximum HP by 25"),
                ("heal", "REPAIR", "Restore 30 HP"),
                ("move_speed", "MOVE SPEED", "Move 15% faster"),
                ("sight", "SIGHT", "Increase shooting range by 50"),
                ("pickup_range", "ARMS", "Increase pickup range by 50")
            ]

        discovered = self.journal.data["journal"][self.journal_tab]
        counter = self.font_small.render(f"{len(discovered)} / {len(records)} DISCOVERED", True, self.CYAN)
        screen.blit(counter, (panel.x + 20, panel.y + 16))

        y = panel.y + 55
        for item_id, name, description in records:
            known = item_id in discovered
            row = pygame.Rect(panel.x + 18, y, panel.width - 36, 45)
            pygame.draw.rect(screen, (9, 13, 20), row)
            pygame.draw.rect(screen, self.CYAN_DARK if known else (30, 32, 38), row, 1)
            pygame.draw.rect(screen, self.CYAN if known else self.GRAY, (row.x, row.y, 4, row.height))

            name_text = self.font_small.render(name if known else "???", True, self.WHITE if known else self.GRAY)
            description_text = self.font_tiny.render(description if known else "UNKNOWN DATA // NOT YET DISCOVERED", True, self.LIGHT_GRAY if known else self.GRAY)
            screen.blit(name_text, (row.x + 16, row.y + 9))
            screen.blit(description_text, (row.x + 16, row.y + 28))
            y += 48

        hovered = self.journal_back_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, self.PANEL_HOVER if hovered else self.PANEL, self.journal_back_rect)
        pygame.draw.rect(screen, self.CYAN if hovered else self.PANEL_LIGHT, self.journal_back_rect, 2)
        back = self.font_small.render("BACK", True, self.WHITE)
        screen.blit(back, back.get_rect(center=self.journal_back_rect.center))

        hint = self.font_tiny.render("ESC // BACK", True, self.GRAY)
        screen.blit(hint, (self.width - 105, self.height - 60))

    # =========================================================
    # HANDLE CLICK
    # =========================================================

    def handle_click(
        self,
        mouse_pos
    ):

        if self.journal_active:
            if self.journal_enemies_rect.collidepoint(mouse_pos):
                self.journal_tab = "enemies"
                return "journal"

            if self.journal_upgrades_rect.collidepoint(mouse_pos):
                self.journal_tab = "upgrades"
                return "journal"

            if self.journal_back_rect.collidepoint(mouse_pos):
                self.journal_active = False
                return None

            return "journal"

        if self.play_rect.collidepoint(mouse_pos):
            return "play"

        if self.journal_rect.collidepoint(mouse_pos):
            self.journal.load()
            self.journal_active = True
            self.journal_tab = "enemies"
            return "journal"

        if self.settings_rect.collidepoint(mouse_pos):
            return "settings"

        if self.quit_rect.collidepoint(mouse_pos):
            return "quit"

        return None

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        screen
    ):

        if self.journal_active:
            self.draw_journal(screen)
            return

        self.update_particles()

        self.draw_background(
            screen
        )

        self.draw_top_hud(
            screen
        )

        self.draw_side_decoration(
            screen
        )

        self.draw_reticle(
            screen
        )

        self.draw_title(
            screen
        )

        self.draw_button(
            screen,
            self.play_rect,
            "PLAY",
            self.CYAN,
            "play"
        )

        self.draw_button(
            screen,
            self.journal_rect,
            "JOURNAL",
            self.BLUE,
            "journal"
        )

        self.draw_button(
            screen,
            self.settings_rect,
            "SETTINGS",
            self.YELLOW,
            "settings"
        )

        self.draw_button(
            screen,
            self.quit_rect,
            "QUIT",
            self.RED,
            "quit"
        )

        self.draw_bottom_hud(
            screen
        )
