import pygame
import os
import math


class Shop:

    def __init__(
        self,
        width,
        height
    ):

        self.width = width
        self.height = height

        self.active = False
        self.current_wave = 0
        self.message = ""

        # =====================================================
        # COLOURS
        # =====================================================

        self.BLACK = (3, 4, 7)
        self.BACKGROUND = (7, 9, 14)

        self.PANEL = (12, 15, 22)
        self.PANEL_LIGHT = (23, 28, 39)

        self.WHITE = (245, 248, 255)
        self.GRAY = (125, 135, 150)
        self.LIGHT_GRAY = (190, 198, 210)

        self.CYAN = (55, 220, 255)
        self.CYAN_DARK = (20, 75, 95)

        self.YELLOW = (255, 210, 65)
        self.YELLOW_DARK = (100, 75, 20)

        self.GREEN = (65, 235, 125)
        self.GREEN_DARK = (20, 80, 50)

        self.RED = (255, 75, 85)

        # =====================================================
        # MUSIC
        # =====================================================

        self.music_path = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            "shop_music.mp3"
        )

        self.music_loaded = False

        if os.path.exists(
            self.music_path
        ):

            try:

                pygame.mixer.music.load(
                    self.music_path
                )

                self.music_loaded = True

            except pygame.error as error:

                print(
                    "Could not load shop music:",
                    error
                )

        else:

            print(
                "Shop music not found:",
                self.music_path
            )

        # =====================================================
        # FONTS
        # =====================================================

        self.font_title = pygame.font.Font(
            None,
            68
        )

        self.font_subtitle = pygame.font.Font(
            None,
            18
        )

        self.font_item = pygame.font.Font(
            None,
            27
        )

        self.font_description = pygame.font.Font(
            None,
            17
        )

        self.font_coins = pygame.font.Font(
            None,
            28
        )

        self.font_button = pygame.font.Font(
            None,
            21
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
        # SHOP ITEMS
        # =====================================================

        self.items = [

            {
                "name": "MAX HP",
                "description": "+25 maximum HP",
                "price": 25,
                "type": "max_hp"
            },

            {
                "name": "BULLET POWER",
                "description": "+5 bullet damage",
                "price": 30,
                "type": "damage"
            },

            {
                "name": "SIGHT",
                "description": "+50 shooting range",
                "price": 35,
                "type": "sight"
            },

            {
                "name": "MOVE SPEED",
                "description": "+15% movement speed",
                "price": 25,
                "type": "move_speed"
            },

            {
                "name": "REPAIR",
                "description": "Restore 50 HP",
                "price": 20,
                "type": "heal"
            }
        ]

        self.item_rects = []

        self.close_rect = pygame.Rect(
            0,
            0,
            0,
            0
        )

        # =====================================================
        # PARTICLES
        # =====================================================

        self.particles = []

        for i in range(70):

            self.particles.append({
                "x": (i * 173) % width,
                "y": (i * 97) % height,
                "speed": 0.15 + (i % 5) * 0.06,
                "size": 1 if i % 4 else 2
            })

    # =========================================================
    # PLAY MUSIC
    # =========================================================

    def play_music(self):

        if not self.music_loaded:
            return

        try:

            pygame.mixer.music.play(
                loops=-1
            )

            pygame.mixer.music.set_volume(
                0.5
            )

        except pygame.error as error:

            print(
                "Could not play shop music:",
                error
            )

    # =========================================================
    # STOP MUSIC
    # =========================================================

    def stop_music(self):

        if self.music_loaded:

            pygame.mixer.music.stop()

    # =========================================================
    # OPEN
    # =========================================================

    def open(
        self,
        wave
    ):

        self.active = True

        self.current_wave = wave

        self.message = ""

        for item in self.items:

            item["bought"] = False

        self.play_music()

        # =====================================================
        # ITEM RECTANGLES
        # =====================================================

        self.item_rects = []

        item_width = 700
        item_height = 78

        start_y = 205

        gap = 12

        for i in range(
            len(self.items)
        ):

            rect = pygame.Rect(
                self.width // 2
                - item_width // 2,

                start_y
                + i * (
                    item_height
                    + gap
                ),

                item_width,
                item_height
            )

            self.item_rects.append(
                rect
            )

        # =====================================================
        # CLOSE BUTTON
        # =====================================================

        self.close_rect = pygame.Rect(
            self.width // 2 - 120,
            self.height - 78,
            240,
            48
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.active = False

        self.stop_music()

    # =========================================================
    # HANDLE CLICK
    # =========================================================

    def handle_click(
        self,
        mouse_pos,
        coins,
        player,
        bullet_manager
    ):

        if not self.active:

            return coins

        # =====================================================
        # ITEMS
        # =====================================================

        for i, rect in enumerate(
            self.item_rects
        ):

            if rect.collidepoint(
                mouse_pos
            ):

                item = self.items[i]

                # -------------------------------------------------
                # Already bought
                # -------------------------------------------------

                if item.get(
                    "bought",
                    False
                ):

                    self.message = (
                        "ALREADY PURCHASED"
                    )

                    return coins

                # -------------------------------------------------
                # Not enough coins
                # -------------------------------------------------

                if coins < item["price"]:

                    self.message = (
                        "NOT ENOUGH COINS"
                    )

                    return coins

                # -------------------------------------------------
                # BUY
                # -------------------------------------------------

                coins -= item["price"]

                self.apply_item(
                    item,
                    player,
                    bullet_manager
                )

                item["bought"] = True

                self.message = (
                    item["name"]
                    + " PURCHASED!"
                )

                return coins

        # =====================================================
        # CLOSE SHOP
        # =====================================================

        if self.close_rect.collidepoint(
            mouse_pos
        ):

            self.close()

        return coins

    # =========================================================
    # APPLY ITEM
    # =========================================================

    def apply_item(
        self,
        item,
        player,
        bullet_manager
    ):

        item_type = item["type"]

        # =====================================================
        # MAX HP
        # =====================================================

        if item_type == "max_hp":

            player.max_hp += 25

            player.hp += 25

            if player.hp > player.max_hp:

                player.hp = player.max_hp

        # =====================================================
        # BULLET POWER
        # =====================================================

        elif item_type == "damage":

            bullet_manager.damage += 5

        # =====================================================
        # SIGHT
        # =====================================================

        elif item_type == "sight":

            bullet_manager.sight_range += 50

        # =====================================================
        # MOVE SPEED
        # =====================================================

        elif item_type == "move_speed":

            player.speed *= 1.15

        # =====================================================
        # REPAIR
        # =====================================================

        elif item_type == "heal":

            player.hp += 50

            if player.hp > player.max_hp:

                player.hp = player.max_hp

    # =========================================================
    # UPDATE PARTICLES
    # =========================================================

    def update_particles(self):

        for particle in self.particles:

            particle["y"] += (
                particle["speed"]
            )

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

        # -----------------------------------------------------
        # Grid
        # -----------------------------------------------------

        grid_color = (
            12,
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
                    40,
                    125,
                    160
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

        # Accent strip

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
    # COIN ICON
    # =========================================================

    def draw_coin(
        self,
        screen,
        x,
        y,
        radius=11
    ):

        pygame.draw.circle(
            screen,
            (
                90,
                65,
                15
            ),
            (
                x + 2,
                y + 2
            ),
            radius
        )

        pygame.draw.circle(
            screen,
            self.YELLOW,
            (
                x,
                y
            ),
            radius
        )

        pygame.draw.circle(
            screen,
            (
                255,
                235,
                125
            ),
            (
                x - 2,
                y - 2
            ),
            radius - 4
        )

        pygame.draw.circle(
            screen,
            self.YELLOW,
            (
                x - 2,
                y - 2
            ),
            radius - 6
        )

    # =========================================================
    # ITEM ICON
    # =========================================================

    def draw_item_icon(
        self,
        screen,
        rect,
        item
    ):

        center_x = rect.x + 42
        center_y = rect.centery

        icon_box = pygame.Rect(
            center_x - 22,
            center_y - 22,
            44,
            44
        )

        pygame.draw.rect(
            screen,
            (
                8,
                11,
                17
            ),
            icon_box
        )

        pygame.draw.rect(
            screen,
            self.CYAN_DARK,
            icon_box,
            2
        )

        item_type = item["type"]

        # -----------------------------------------------------
        # MAX HP
        # -----------------------------------------------------

        if item_type == "max_hp":

            pygame.draw.line(
                screen,
                self.RED,
                (
                    center_x - 10,
                    center_y
                ),
                (
                    center_x + 10,
                    center_y
                ),
                4
            )

            pygame.draw.line(
                screen,
                self.RED,
                (
                    center_x,
                    center_y - 10
                ),
                (
                    center_x,
                    center_y + 10
                ),
                4
            )

        # -----------------------------------------------------
        # DAMAGE
        # -----------------------------------------------------

        elif item_type == "damage":

            pygame.draw.polygon(
                screen,
                self.YELLOW,
                [
                    (
                        center_x - 5,
                        center_y - 16
                    ),
                    (
                        center_x + 8,
                        center_y - 2
                    ),
                    (
                        center_x + 2,
                        center_y - 2
                    ),
                    (
                        center_x + 8,
                        center_y + 16
                    ),
                    (
                        center_x - 8,
                        center_y + 1
                    ),
                    (
                        center_x - 1,
                        center_y + 1
                    )
                ]
            )

        # -----------------------------------------------------
        # SIGHT
        # -----------------------------------------------------

        elif item_type == "sight":

            pygame.draw.circle(
                screen,
                self.CYAN,
                (
                    center_x,
                    center_y
                ),
                13,
                2
            )

            pygame.draw.circle(
                screen,
                self.CYAN,
                (
                    center_x,
                    center_y
                ),
                4
            )

            pygame.draw.line(
                screen,
                self.CYAN,
                (
                    center_x - 18,
                    center_y
                ),
                (
                    center_x + 18,
                    center_y
                ),
                1
            )

            pygame.draw.line(
                screen,
                self.CYAN,
                (
                    center_x,
                    center_y - 18
                ),
                (
                    center_x,
                    center_y + 18
                ),
                1
            )

        # -----------------------------------------------------
        # MOVE SPEED
        # -----------------------------------------------------

        elif item_type == "move_speed":

            pygame.draw.line(
                screen,
                self.GREEN,
                (
                    center_x - 14,
                    center_y
                ),
                (
                    center_x + 10,
                    center_y
                ),
                4
            )

            pygame.draw.polygon(
                screen,
                self.GREEN,
                [
                    (
                        center_x + 15,
                        center_y
                    ),
                    (
                        center_x + 5,
                        center_y - 8
                    ),
                    (
                        center_x + 5,
                        center_y + 8
                    )
                ]
            )

        # -----------------------------------------------------
        # REPAIR
        # -----------------------------------------------------

        elif item_type == "heal":

            pygame.draw.circle(
                screen,
                self.GREEN,
                (
                    center_x,
                    center_y
                ),
                14,
                2
            )

            pygame.draw.line(
                screen,
                self.GREEN,
                (
                    center_x - 7,
                    center_y
                ),
                (
                    center_x + 7,
                    center_y
                ),
                3
            )

            pygame.draw.line(
                screen,
                self.GREEN,
                (
                    center_x,
                    center_y - 7
                ),
                (
                    center_x,
                    center_y + 7
                ),
                3
            )

    # =========================================================
    # DRAW ITEM
    # =========================================================

    def draw_item(
        self,
        screen,
        rect,
        item,
        coins
    ):

        mouse_pos = pygame.mouse.get_pos()

        bought = item.get(
            "bought",
            False
        )

        affordable = (
            coins >= item["price"]
        )

        hovered = rect.collidepoint(
            mouse_pos
        )

        # =====================================================
        # STATE COLOURS
        # =====================================================

        if bought:

            background = (
                12,
                30,
                23
            )

            border = self.GREEN

            accent = self.GREEN

        elif not affordable:

            background = (
                10,
                12,
                17
            )

            border = (
                55,
                62,
                72
            )

            accent = (
                75,
                80,
                90
            )

        elif hovered:

            background = (
                18,
                28,
                38
            )

            border = self.CYAN

            accent = self.CYAN

        else:

            background = self.PANEL

            border = self.PANEL_LIGHT

            accent = self.CYAN_DARK

        # =====================================================
        # SHADOW
        # =====================================================

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

        # =====================================================
        # MAIN CARD
        # =====================================================

        pygame.draw.rect(
            screen,
            background,
            rect
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            2
        )

        # =====================================================
        # ACCENT STRIP
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
        # ICON
        # =====================================================

        self.draw_item_icon(
            screen,
            rect,
            item
        )

        # =====================================================
        # NAME
        # =====================================================

        if bought:

            name_color = self.GREEN

        elif not affordable:

            name_color = (
                100,
                105,
                115
            )

        else:

            name_color = self.WHITE

        name = self.font_item.render(
            item["name"],
            True,
            name_color
        )

        screen.blit(
            name,
            (
                rect.x + 78,
                rect.y + 11
            )
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        description = (
            self.font_description.render(
                item["description"],
                True,
                self.GRAY
            )
        )

        screen.blit(
            description,
            (
                rect.x + 78,
                rect.y + 45
            )
        )

        # =====================================================
        # PRICE AREA
        # =====================================================

        if bought:

            bought_text = self.font_button.render(
                "PURCHASED",
                True,
                self.GREEN
            )

            bought_rect = bought_text.get_rect(
                midright=(
                    rect.right - 18,
                    rect.centery
                )
            )

            screen.blit(
                bought_text,
                bought_rect
            )

            pygame.draw.circle(
                screen,
                self.GREEN,
                (
                    bought_rect.left - 13,
                    bought_rect.centery
                ),
                5
            )

        else:

            price_text = self.font_button.render(
                str(item["price"]),
                True,
                (
                    self.YELLOW
                    if affordable
                    else self.GRAY
                )
            )

            price_rect = price_text.get_rect(
                midright=(
                    rect.right - 38,
                    rect.centery
                )
            )

            screen.blit(
                price_text,
                price_rect
            )

            self.draw_coin(
                screen,
                rect.right - 20,
                rect.centery,
                8
            )

        # =====================================================
        # HOVER INDICATOR
        # =====================================================

        if hovered and not bought:

            pygame.draw.line(
                screen,
                accent,
                (
                    rect.right - 80,
                    rect.top + 10
                ),
                (
                    rect.right - 12,
                    rect.top + 10
                ),
                2
            )

            pygame.draw.line(
                screen,
                accent,
                (
                    rect.right - 12,
                    rect.top + 10
                ),
                (
                    rect.right - 12,
                    rect.top + 25
                ),
                2
            )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(
        self,
        screen,
        coins
    ):

        if not self.active:

            return

        self.update_particles()

        self.draw_background(
            screen
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
            (0, 0, 0, 90)
        )

        screen.blit(
            overlay,
            (0, 0)
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
                38
            ),
            (
                center_x - 180,
                38
            ),
            1
        )

        pygame.draw.line(
            screen,
            self.CYAN_DARK,
            (
                center_x + 180,
                38
            ),
            (
                self.width - 70,
                38
            ),
            1
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                center_x - 65,
                36,
                130,
                3
            )
        )

        # =====================================================
        # TITLE
        # =====================================================

        title_shadow = self.font_title.render(
            "UPGRADE TERMINAL",
            True,
            (
                15,
                65,
                80
            )
        )

        shadow_rect = title_shadow.get_rect(
            center=(
                center_x + 4,
                76
            )
        )

        screen.blit(
            title_shadow,
            shadow_rect
        )

        title = self.font_title.render(
            "UPGRADE TERMINAL",
            True,
            self.WHITE
        )

        title_rect = title.get_rect(
            center=(
                center_x,
                72
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # =====================================================
        # SUBTITLE
        # =====================================================

        subtitle = self.font_subtitle.render(
            "WAVE "
            + str(self.current_wave)
            + " COMPLETE  //  SELECT AN UPGRADE",
            True,
            self.GRAY
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                122
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        # =====================================================
        # COIN PANEL
        # =====================================================

        coin_panel = pygame.Rect(
            center_x - 125,
            145,
            250,
            42
        )

        self.draw_panel(
            screen,
            coin_panel,
            self.YELLOW
        )

        self.draw_coin(
            screen,
            coin_panel.x + 24,
            coin_panel.centery,
            10
        )

        coin_text = self.font_coins.render(
            str(coins),
            True,
            self.YELLOW
        )

        coin_rect = coin_text.get_rect(
            midleft=(
                coin_panel.x + 43,
                coin_panel.centery
            )
        )

        screen.blit(
            coin_text,
            coin_rect
        )

        coin_label = self.font_small.render(
            "CREDITS AVAILABLE",
            True,
            self.GRAY
        )

        coin_label_rect = coin_label.get_rect(
            midright=(
                coin_panel.right - 14,
                coin_panel.centery
            )
        )

        screen.blit(
            coin_label,
            coin_label_rect
        )

        # =====================================================
        # ITEMS
        # =====================================================

        for i, item in enumerate(
            self.items
        ):

            self.draw_item(
                screen,
                self.item_rects[i],
                item,
                coins
            )

        # =====================================================
        # MESSAGE
        # =====================================================

        if self.message:

            pulse = (
                math.sin(
                    pygame.time.get_ticks()
                    * 0.008
                )
                + 1
            ) / 2

            message_color = (
                self.GREEN
                if "PURCHASED"
                in self.message
                else self.YELLOW
            )

            message_surface = (
                self.font_button.render(
                    self.message,
                    True,
                    message_color
                )
            )

            message_rect = (
                message_surface.get_rect(
                    center=(
                        center_x,
                        self.height - 112
                    )
                )
            )

            screen.blit(
                message_surface,
                message_rect
            )

            pygame.draw.line(
                screen,
                (
                    int(
                        message_color[0]
                        * (0.5 + pulse * 0.5)
                    ),
                    int(
                        message_color[1]
                        * (0.5 + pulse * 0.5)
                    ),
                    int(
                        message_color[2]
                        * (0.5 + pulse * 0.5)
                    )
                ),
                (
                    center_x - 100,
                    self.height - 96
                ),
                (
                    center_x + 100,
                    self.height - 96
                ),
                1
            )

        # =====================================================
        # CONTINUE BUTTON
        # =====================================================

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.close_rect.collidepoint(
            mouse_pos
        )

        if hovered:

            background = (
                18,
                30,
                38
            )

            border = self.CYAN

        else:

            background = self.PANEL

            border = self.PANEL_LIGHT

        shadow = pygame.Rect(
            self.close_rect.x + 5,
            self.close_rect.y + 5,
            self.close_rect.width,
            self.close_rect.height
        )

        pygame.draw.rect(
            screen,
            self.BLACK,
            shadow
        )

        pygame.draw.rect(
            screen,
            background,
            self.close_rect
        )

        pygame.draw.rect(
            screen,
            border,
            self.close_rect,
            2
        )

        pygame.draw.rect(
            screen,
            self.CYAN,
            (
                self.close_rect.x,
                self.close_rect.y,
                4,
                self.close_rect.height
            )
        )

        continue_text = self.font_button.render(
            "CONTINUE",
            True,
            self.WHITE
        )

        continue_rect = continue_text.get_rect(
            center=self.close_rect.center
        )

        screen.blit(
            continue_text,
            continue_rect
        )

        # =====================================================
        # MUSIC STATUS
        # =====================================================

        music_text = self.font_tiny.render(
            "♪ SHOP MUSIC // "
            + (
                "ONLINE"
                if self.music_loaded
                else "UNAVAILABLE"
            ),
            True,
            (
                self.CYAN
                if self.music_loaded
                else self.GRAY
            )
        )

        screen.blit(
            music_text,
            (
                20,
                20
            )
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = self.font_tiny.render(
            "UPGRADE TERMINAL // SYSTEM READY",
            True,
            (
                70,
                80,
                95
            )
        )

        footer_rect = footer.get_rect(
            bottomright=(
                self.width - 20,
                self.height - 15
            )
        )

        screen.blit(
            footer,
            footer_rect
        )