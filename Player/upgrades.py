import pygame
import random
import os
import math

from Game.journal import Journal


class UpgradeManager:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.active = False

        self.choices = []

        self.upgrade_rects = []

        self.hover_index = -1

        self.journal = Journal()

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(
            None,
            64
        )

        self.font_subtitle = pygame.font.Font(
            None,
            22
        )

        self.font_name = pygame.font.Font(
            None,
            29
        )

        self.font_description = pygame.font.Font(
            None,
            18
        )

        self.font_number = pygame.font.Font(
            None,
            16
        )

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (3, 4, 7)

        self.PANEL = (12, 15, 22)

        self.PANEL_LIGHT = (21, 25, 34)

        self.PANEL_HOVER = (24, 31, 42)

        self.WHITE = (245, 248, 255)

        self.GRAY = (135, 145, 160)

        self.LIGHT_GRAY = (195, 202, 215)

        self.CYAN = (55, 220, 255)

        self.CYAN_DARK = (20, 75, 95)

        self.BLUE = (65, 135, 255)

        self.BLUE_DARK = (20, 45, 90)

        self.YELLOW = (255, 210, 65)

        self.YELLOW_DARK = (95, 72, 20)

        # =====================================================
        # ANIMATION
        # =====================================================

        self.animation_start = 0

        self.hover_scale = [
            1.0,
            1.0,
            1.0
        ]

        # =====================================================
        # LOAD UPGRADE ICONS
        # =====================================================

        self.icons = {}

        icon_folder = os.path.join(
            os.path.dirname(__file__),
            "upgrade_icons"
        )

        icon_names = [
            "rapid_fire",
            "bullet_speed",
            "bullet_power",
            "max_hp",
            "repair",
            "move_speed",
            "sight",
            "coin"
        ]

        for icon_name in icon_names:

            path = os.path.join(
                icon_folder,
                icon_name + ".png"
            )

            if os.path.exists(path):

                try:

                    image = pygame.image.load(
                        path
                    ).convert_alpha()

                    image = pygame.transform.smoothscale(
                        image,
                        (58, 58)
                    )

                    self.icons[
                        icon_name
                    ] = image

                except pygame.error:

                    pass

        # =====================================================
        # UPGRADES
        # =====================================================

        self.upgrades = [

            {
                "name": "RAPID FIRE",
                "description": "Fire 20% faster",
                "type": "fire_rate",
                "icon": "rapid_fire"
            },

            {
                "name": "BULLET SPEED",
                "description": "Bullets move 25% faster",
                "type": "bullet_speed",
                "icon": "bullet_speed"
            },

            {
                "name": "BULLET POWER",
                "description": "Bullets deal 5 more damage",
                "type": "damage",
                "icon": "bullet_power"
            },

            {
                "name": "MAX HP",
                "description": "Increase maximum HP by 25",
                "type": "max_hp",
                "icon": "max_hp"
            },

            {
                "name": "REPAIR",
                "description": "Restore 30 HP",
                "type": "heal",
                "icon": "repair"
            },

            {
                "name": "MOVE SPEED",
                "description": "Move 15% faster",
                "type": "move_speed",
                "icon": "move_speed"
            },

            {
                "name": "SIGHT",
                "description": "Increase shooting range by 50",
                "type": "sight",
                "icon": "sight"
            },

            {
                "name": "ARMS",
                "description": "Increase pickup range by 50",
                "type": "pickup_range",
                "icon": "coin"
            }
        ]

    # =========================================================
    # OPEN
    # =========================================================

    def open(self):

        self.active = True

        self.choices = random.sample(
            self.upgrades,
            3
        )

        for upgrade in self.choices:
            self.journal.discover_upgrade(upgrade["type"])

        self.upgrade_rects = []

        self.animation_start = (
            pygame.time.get_ticks()
        )

        self.hover_index = -1

        self.hover_scale = [
            1.0,
            1.0,
            1.0
        ]

        # =====================================================
        # CARD POSITIONS
        # =====================================================

        card_width = 650

        card_height = 110

        gap = 18

        total_height = (
            card_height * 3
            + gap * 2
        )

        start_y = (
            self.height // 2
            - total_height // 2
            + 25
        )

        for i in range(3):

            rect = pygame.Rect(
                self.width // 2
                - card_width // 2,

                start_y
                + i * (
                    card_height +
                    gap
                ),

                card_width,

                card_height
            )

            self.upgrade_rects.append(
                rect
            )

    # =========================================================
    # HANDLE CLICK
    # =========================================================

    def handle_click(
        self,
        mouse_pos,
        player,
        bullet_manager,
        enemy_manager
    ):

        if not self.active:

            return False

        for i, rect in enumerate(
            self.upgrade_rects
        ):

            if rect.collidepoint(
                mouse_pos
            ):

                upgrade = self.choices[i]

                self.apply_upgrade(
                    upgrade,
                    player,
                    bullet_manager,
                    enemy_manager
                )

                self.active = False

                return True

        return False

    # =========================================================
    # APPLY UPGRADE
    # =========================================================

    def apply_upgrade(
        self,
        upgrade,
        player,
        bullet_manager,
        enemy_manager
    ):

        upgrade_type = upgrade["type"]

        # =====================================================
        # RAPID FIRE
        # =====================================================

        if upgrade_type == "fire_rate":

            bullet_manager.shoot_delay *= 0.8

            bullet_manager.shoot_delay = max(
                50,
                bullet_manager.shoot_delay
            )

        # =====================================================
        # BULLET SPEED
        # =====================================================

        elif upgrade_type == "bullet_speed":

            bullet_manager.speed *= 1.25

        # =====================================================
        # BULLET POWER
        # =====================================================

        elif upgrade_type == "damage":

            bullet_manager.damage += 5

        # =====================================================
        # MAX HP
        # =====================================================

        elif upgrade_type == "max_hp":

            player.max_hp += 25

            player.hp += 25

            if player.hp > player.max_hp:

                player.hp = player.max_hp

        # =====================================================
        # REPAIR
        # =====================================================

        elif upgrade_type == "heal":

            player.hp += 30

            if player.hp > player.max_hp:

                player.hp = player.max_hp

        # =====================================================
        # MOVE SPEED
        # =====================================================

        elif upgrade_type == "move_speed":

            player.speed *= 1.15

        # =====================================================
        # SIGHT
        # =====================================================

        elif upgrade_type == "sight":

            bullet_manager.sight_range += 50

        # =====================================================
        # ARMS
        # =====================================================

        elif upgrade_type == "pickup_range":

            enemy_manager.base_attraction_radius += 50

            enemy_manager.attraction_radius += 50

            # Make the coin pickup range match the
            # EXP pickup range.

            enemy_manager.coin_attraction_radius += 50

    # =========================================================
    # DRAW PANEL
    # =========================================================

    def draw_panel(
        self,
        screen,
        rect,
        hovered=False
    ):

        # =====================================================
        # SHADOW
        # =====================================================

        shadow = pygame.Rect(
            rect.x + 6,
            rect.y + 7,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow
        )

        # =====================================================
        # PANEL
        # =====================================================

        background = (
            self.PANEL_HOVER
            if hovered
            else self.PANEL
        )

        pygame.draw.rect(
            screen,
            background,
            rect
        )

        # =====================================================
        # TOP EDGE
        # =====================================================

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                rect.x + 10,
                rect.y
            ),
            (
                rect.right - 10,
                rect.y
            ),
            2
        )

        # =====================================================
        # BORDER
        # =====================================================

        border = (
            self.YELLOW
            if hovered
            else self.PANEL_LIGHT
        )

        pygame.draw.rect(
            screen,
            border,
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
            self.CYAN_DARK,
            inner,
            1
        )

        # =====================================================
        # CORNER DETAILS
        # =====================================================

        corner = 10

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                rect.left,
                rect.top + corner
            ),
            (
                rect.left,
                rect.top
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                rect.left,
                rect.top
            ),
            (
                rect.left + corner,
                rect.top
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                rect.right - corner,
                rect.bottom
            ),
            (
                rect.right,
                rect.bottom
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                rect.right,
                rect.bottom
            ),
            (
                rect.right,
                rect.bottom - corner
            ),
            2
        )

    # =========================================================
    # DRAW ICON
    # =========================================================

    def draw_icon(
        self,
        screen,
        upgrade,
        rect,
        hovered
    ):

        icon_box = pygame.Rect(
            rect.x + 16,
            rect.y + 17,
            76,
            76
        )

        # =====================================================
        # ICON SHADOW
        # =====================================================

        pygame.draw.rect(
            screen,
            self.BLACK,
            (
                icon_box.x + 3,
                icon_box.y + 3,
                icon_box.width,
                icon_box.height
            )
        )

        # =====================================================
        # ICON BACKGROUND
        # =====================================================

        icon_background = (
            (18, 30, 42)
            if hovered
            else (11, 20, 30)
        )

        pygame.draw.rect(
            screen,
            icon_background,
            icon_box
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            icon_box,
            2
        )

        # =====================================================
        # ICON CORNERS
        # =====================================================

        pygame.draw.line(
            screen,
            self.YELLOW,
            icon_box.topleft,
            (
                icon_box.left + 10,
                icon_box.top
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.YELLOW,
            icon_box.bottomright,
            (
                icon_box.right - 10,
                icon_box.bottom
            ),
            2
        )

        # =====================================================
        # ICON
        # =====================================================

        icon_name = upgrade["icon"]

        if icon_name in self.icons:

            icon = self.icons[icon_name]

            icon_rect = icon.get_rect(
                center=icon_box.center
            )

            screen.blit(
                icon,
                icon_rect
            )

        else:

            # Fallback if an icon is missing.

            pygame.draw.circle(
                screen,
                self.CYAN,
                icon_box.center,
                18,
                2
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

        # =====================================================
        # DARK OVERLAY
        # =====================================================

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (2, 4, 8, 215)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # =====================================================
        # SCANLINES
        # =====================================================

        scanline_surface = pygame.Surface(
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
                scanline_surface,
                (50, 180, 220, 12),
                (0, y),
                (self.width, y),
                1
            )

        screen.blit(
            scanline_surface,
            (0, 0)
        )

        # =====================================================
        # ANIMATED CENTER GLOW
        # =====================================================

        glow = pygame.Surface(
            (
                500,
                300
            ),
            pygame.SRCALPHA
        )

        pulse = (
            math.sin(
                current_time * 0.004
            )
            + 1
        ) / 2

        pygame.draw.circle(
            glow,
            (
                40,
                190,
                255,
                int(12 + pulse * 10)
            ),
            (
                250,
                150
            ),
            int(
                100 +
                pulse * 30
            )
        )

        screen.blit(
            glow,
            (
                self.width // 2 - 250,
                0
            )
        )

        # =====================================================
        # TITLE
        # =====================================================

        title_y = 68

        # Title shadow

        shadow = self.font_title.render(
            "LEVEL UP!",
            True,
            (5, 30, 40)
        )

        shadow_rect = shadow.get_rect(
            center=(
                self.width // 2 + 3,
                title_y + 3
            )
        )

        screen.blit(
            shadow,
            shadow_rect
        )

        # Main title

        title = self.font_title.render(
            "LEVEL UP!",
            True,
            self.CYAN
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                title_y
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =====================================================
        # TITLE LINES
        # =====================================================

        line_width = 180

        left_line_x = (
            self.width // 2
            - 260
        )

        right_line_x = (
            self.width // 2
            + 80
        )

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                left_line_x,
                title_y
            ),
            (
                left_line_x + line_width,
                title_y
            ),
            2
        )

        pygame.draw.line(
            screen,
            self.CYAN,
            (
                right_line_x,
                title_y
            ),
            (
                right_line_x + line_width,
                title_y
            ),
            2
        )

        # =====================================================
        # SUBTITLE
        # =====================================================

        subtitle = self.font_subtitle.render(
            "SELECT AN UPGRADE",
            True,
            self.LIGHT_GRAY
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                self.width // 2,
                118
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        # =====================================================
        # UPDATE HOVER
        # =====================================================

        mouse_pos = pygame.mouse.get_pos()

        self.hover_index = -1

        for i, rect in enumerate(
            self.upgrade_rects
        ):

            if rect.collidepoint(
                mouse_pos
            ):

                self.hover_index = i

        # =====================================================
        # DRAW CARDS
        # =====================================================

        for i, upgrade in enumerate(
            self.choices
        ):

            rect = self.upgrade_rects[i]

            hovered = (
                i == self.hover_index
            )

            self.draw_panel(
                screen,
                rect,
                hovered
            )

            # =================================================
            # NUMBER
            # =================================================

            number = self.font_number.render(
                str(i + 1),
                True,
                self.GRAY
            )

            number_rect = number.get_rect(
                topright=(
                    rect.right - 12,
                    rect.top + 8
                )
            )

            screen.blit(
                number,
                number_rect
            )

            # =================================================
            # ICON
            # =================================================

            self.draw_icon(
                screen,
                upgrade,
                rect,
                hovered
            )

            # =================================================
            # NAME
            # =================================================

            name_color = (
                self.YELLOW
                if hovered
                else self.WHITE
            )

            name = self.font_name.render(
                upgrade["name"],
                True,
                name_color
            )

            name_rect = name.get_rect(
                midleft=(
                    rect.x + 115,
                    rect.y + 38
                )
            )

            screen.blit(
                name,
                name_rect
            )

            # =================================================
            # DESCRIPTION
            # =================================================

            description = (
                self.font_description.render(
                    upgrade["description"],
                    True,
                    self.LIGHT_GRAY
                )
            )

            description_rect = (
                description.get_rect(
                    midleft=(
                        rect.x + 116,
                        rect.y + 73
                    )
                )
            )

            screen.blit(
                description,
                description_rect
            )

            # =================================================
            # SELECT INDICATOR
            # =================================================

            if hovered:

                pulse = (
                    math.sin(
                        current_time * 0.008
                    )
                    + 1
                ) / 2

                indicator_height = int(
                    20 +
                    pulse * 8
                )

                pygame.draw.rect(
                    screen,
                    self.YELLOW,
                    (
                        rect.right - 8,
                        rect.centery
                        - indicator_height // 2,
                        3,
                        indicator_height
                    )
                )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = self.font_number.render(
            "CHOOSE CAREFULLY",
            True,
            self.GRAY
        )

        footer_rect = footer.get_rect(
            center=(
                self.width // 2,
                self.height - 32
            )
        )

        screen.blit(
            footer,
            footer_rect
        )