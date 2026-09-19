import pygame
import math
import json

from pathlib import Path


from Game.game_state import GameState
from Game.game_over import GameOverScreen
from Game.transitions import Transition


from Player.player import Player
from Player.experience import ExperienceManager
from Player.upgrades import UpgradeManager


from Visuals.weapons import WeaponManager
from Visuals.enemies import EnemyManager
from Visuals.ui import UI
from Visuals.menu import MainMenu
from Visuals.settings import Settings
from Visuals.shop import Shop


class Game:

    def __init__(self):

        pygame.init()

        # =====================================================
        # DISPLAY
        # =====================================================

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )

        self.width, self.height = (
            self.screen.get_size()
        )

        pygame.display.set_caption(
            "Pixel Shooter"
        )

        self.clock = pygame.time.Clock()

        # =====================================================
        # MAP
        # =====================================================

        self.map_width = int(
            self.width * 0.70
        )

        self.map_height = int(
            self.height * 0.70
        )

        self.map_x = (
            self.width -
            self.map_width
        ) // 2

        self.map_y = (
            self.height -
            self.map_height
        ) // 2

        self.game_surface = pygame.Surface(
            (
                self.map_width,
                self.map_height
            )
        )

        # =====================================================
        # STATE
        # =====================================================

        self.state = GameState.MENU

        self.settings_return_to = (
            GameState.MENU
        )

        self.running = True

        # =====================================================
        # FIRST BOOT SYSTEM
        # =====================================================

        self.save_file = (
            Path(__file__).resolve().parent.parent
            / "pixel_shooter_data.json"
        )

        self.first_boot = (
            not self.has_booted_before()
        )

        self.boot_active = self.first_boot

        self.boot_replay = False

        self.boot_time = 0

        self.boot_start_time = 0

        self.boot_hold_time = 0

        self.boot_hold_required = 48

        self.boot_complete = False

        self.boot_fade = 0

        self.boot_lines = []

        self.boot_font = pygame.font.Font(
            None,
            18
        )

        self.boot_small_font = pygame.font.Font(
            None,
            14
        )

        self.boot_title_font = pygame.font.Font(
            None,
            38
        )

        self.boot_big_font = pygame.font.Font(
            None,
            26
        )

        self.boot_cursor_timer = 0

        self.boot_cursor_visible = True

        self.boot_progress = 0

        self.boot_status_messages = [
            "INITIALIZING CORE SYSTEM",
            "CHECKING MEMORY",
            "LOADING PLAYER SYSTEM",
            "LOADING WEAPON SYSTEM",
            "LOADING ENEMY SYSTEM",
            "LOADING EXPERIENCE SYSTEM",
            "LOADING WORLD",
            "CALIBRATING TARGETING SYSTEM",
            "CHECKING GAME DATA",
            "SYSTEMS ONLINE"
        ]

        self.boot_line_times = [
            20,
            45,
            70,
            95,
            120,
            145,
            170,
            195,
            220,
            250
        ]

        # =====================================================
        # OBJECTS
        # =====================================================

        self.player = None
        self.weapon_manager = None
        self.enemy_manager = None
        self.experience = None
        self.upgrades = None
        self.ui = None
        self.menu = None
        self.settings = None
        self.shop = None
        self.game_over = None
        self.transition = None

        # =====================================================
        # PLAYER CURRENCY
        # =====================================================

        self.coins = 0

        # =====================================================
        # EFFECTS
        # =====================================================

        self.screen_shake = 0

        self.damage_flash = 0

        self.wave_flash = 0

        self.wave_text_timer = 0

        self.wave_number_display = 1

        self.visual_time = 0

        # =====================================================
        # AMBIENT PARTICLES
        # =====================================================

        self.particles = []

        for i in range(100):

            self.particles.append({
                "x": (i * 83) % self.map_width,
                "y": (i * 137) % self.map_height,
                "speed": 0.15 + (i % 5) * 0.06,
                "size": 1 if i % 4 else 2,
                "phase": i * 0.37
            })

        # =====================================================
        # CREATE SYSTEMS
        # =====================================================

        self.create_systems()

        self.game_over = GameOverScreen(
            self.width,
            self.height
        )

    # =========================================================
    # FIRST BOOT DATA
    # =========================================================

    def has_booted_before(self):

        try:

            if not self.save_file.exists():
                return False

            with open(
                self.save_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return bool(
                data.get(
                    "booted_before",
                    False
                )
            )

        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):

            return False

    # ---------------------------------------------------------

    def mark_boot_complete(self):

        try:

            data = {
                "booted_before": True
            }

            with open(
                self.save_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except OSError:

            pass

    # =========================================================
    # START BOOT SEQUENCE
    # =========================================================

    def start_boot_sequence(
        self,
        replay=False
    ):

        self.boot_active = True

        self.boot_replay = replay

        self.boot_time = 0

        self.boot_start_time = (
            pygame.time.get_ticks()
        )

        self.boot_complete = False

        self.boot_fade = 0

        self.boot_lines = []

        self.boot_progress = 0

        self.boot_cursor_timer = 0

        self.boot_cursor_visible = True

        # Don't change the first-launch save data here.
        #
        # It is only written after the original boot
        # sequence has completed.

    # =========================================================
    # UPDATE BOOT SEQUENCE
    # =========================================================

    def update_boot(self):

        self.boot_time += 1

        self.boot_cursor_timer += 1

        # -----------------------------------------------------
        # Cursor blink
        # -----------------------------------------------------

        if self.boot_cursor_timer >= 30:

            self.boot_cursor_timer = 0

            self.boot_cursor_visible = (
                not self.boot_cursor_visible
            )

        # -----------------------------------------------------
        # Add boot messages
        # -----------------------------------------------------

        for index, line_time in enumerate(
            self.boot_line_times
        ):

            if (
                self.boot_time >= line_time
                and index >= len(self.boot_lines)
            ):

                message = (
                    self.boot_status_messages[index]
                )

                self.boot_lines.append(
                    message
                )

        # -----------------------------------------------------
        # Progress
        # -----------------------------------------------------

        self.boot_progress = min(
            1.0,
            self.boot_time / 270
        )

        # -----------------------------------------------------
        # Boot finished
        # -----------------------------------------------------

        if self.boot_time >= 300:

            if not self.boot_complete:

                self.boot_complete = True

                # Only the actual first boot writes
                # the permanent save flag.

                if not self.boot_replay:

                    self.mark_boot_complete()

            self.boot_fade += 8

            if self.boot_fade >= 255:

                self.boot_active = False

                self.boot_replay = False

                self.boot_complete = False

                self.boot_fade = 0

                self.state = GameState.MENU

    # =========================================================
    # DRAW BOOT BACKGROUND
    # =========================================================

    def draw_boot_background(self):

        self.screen.fill(
            (
                3,
                5,
                7
            )
        )

        # -----------------------------------------------------
        # Subtle horizontal grid
        # -----------------------------------------------------

        for y in range(
            0,
            self.height,
            32
        ):

            pygame.draw.line(
                self.screen,
                (
                    7,
                    18,
                    22
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

        # -----------------------------------------------------
        # Vertical grid
        # -----------------------------------------------------

        for x in range(
            0,
            self.width,
            64
        ):

            pygame.draw.line(
                self.screen,
                (
                    6,
                    15,
                    19
                ),
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

        # -----------------------------------------------------
        # Moving scanline
        # -----------------------------------------------------

        scan_y = (
            self.boot_time * 4
        ) % self.height

        scan_surface = pygame.Surface(
            (
                self.width,
                4
            ),
            pygame.SRCALPHA
        )

        scan_surface.fill(
            (
                60,
                220,
                255,
                18
            )
        )

        self.screen.blit(
            scan_surface,
            (
                0,
                scan_y
            )
        )

        # -----------------------------------------------------
        # Random-looking signal blocks
        # -----------------------------------------------------

        for i in range(18):

            x = (
                i * 137
                + self.boot_time * (i % 3 + 1)
            ) % self.width

            y = (
                i * 79
                + self.boot_time * 2
            ) % self.height

            pygame.draw.rect(
                self.screen,
                (
                    8,
                    30,
                    36
                ),
                (
                    x,
                    y,
                    2 + i % 5,
                    1
                )
            )

    # =========================================================
    # DRAW BOOT SEQUENCE
    # =========================================================

    def draw_boot(self):

        self.draw_boot_background()

        center_x = self.width // 2

        # =====================================================
        # TOP TITLE
        # =====================================================

        title = self.boot_title_font.render(
            "PIXEL SHOOTER",
            True,
            (
                60,
                220,
                255
            )
        )

        title_rect = title.get_rect(
            center=(
                center_x,
                85
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # -----------------------------------------------------
        # SYSTEM TEXT
        # -----------------------------------------------------

        subtitle = self.boot_small_font.render(
            "SYSTEM BOOT SEQUENCE",
            True,
            (
                105,
                135,
                145
            )
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                116
            )
        )

        self.screen.blit(
            subtitle,
            subtitle_rect
        )

        # =====================================================
        # TERMINAL PANEL
        # =====================================================

        panel_width = min(
            850,
            self.width - 120
        )

        panel_height = 360

        panel_x = (
            center_x -
            panel_width // 2
        )

        panel_y = 155

        # Shadow

        pygame.draw.rect(
            self.screen,
            (
                0,
                0,
                0
            ),
            (
                panel_x + 6,
                panel_y + 6,
                panel_width,
                panel_height
            )
        )

        # Outer

        pygame.draw.rect(
            self.screen,
            (
                20,
                45,
                52
            ),
            (
                panel_x,
                panel_y,
                panel_width,
                panel_height
            )
        )

        # Inner

        pygame.draw.rect(
            self.screen,
            (
                4,
                10,
                13
            ),
            (
                panel_x + 3,
                panel_y + 3,
                panel_width - 6,
                panel_height - 6
            )
        )

        # =====================================================
        # TERMINAL HEADER
        # =====================================================

        header = self.boot_small_font.render(
            "PIXEL SHOOTER // BOOT",
            True,
            (
                70,
                180,
                195
            )
        )

        self.screen.blit(
            header,
            (
                panel_x + 18,
                panel_y + 14
            )
        )

        pygame.draw.line(
            self.screen,
            (
                20,
                65,
                75
            ),
            (
                panel_x + 15,
                panel_y + 38
            ),
            (
                panel_x + panel_width - 15,
                panel_y + 38
            ),
            1
        )

        # =====================================================
        # BOOT LINES
        # =====================================================

        line_y = panel_y + 58

        for index, message in enumerate(
            self.boot_lines
        ):

            if index >= len(
                self.boot_status_messages
            ):
                break

            # Completed lines

            if index < len(
                self.boot_lines
            ) - 1:

                prefix = "[ OK ]"

                color = (
                    70,
                    220,
                    145
                )

            else:

                prefix = "[ .. ]"

                color = (
                    255,
                    205,
                    70
                )

            text = self.boot_font.render(
                prefix + " " + message,
                True,
                color
            )

            self.screen.blit(
                text,
                (
                    panel_x + 24,
                    line_y
                )
            )

            line_y += 27

        # =====================================================
        # CURRENT OPERATION
        # =====================================================

        if (
            self.boot_time < 300
            and len(self.boot_lines) > 0
        ):

            current = (
                self.boot_lines[-1]
            )

            current_text = self.boot_small_font.render(
                "> " + current + "...",
                True,
                (
                    180,
                    200,
                    205
                )
            )

            self.screen.blit(
                current_text,
                (
                    panel_x + 24,
                    panel_y + panel_height - 72
                )
            )

        # =====================================================
        # PROGRESS BAR
        # =====================================================

        bar_x = panel_x + 24

        bar_y = (
            panel_y +
            panel_height -
            42
        )

        bar_width = (
            panel_width -
            48
        )

        bar_height = 12

        pygame.draw.rect(
            self.screen,
            (
                10,
                25,
                30
            ),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        progress_width = int(
            bar_width *
            self.boot_progress
        )

        if progress_width > 0:

            pygame.draw.rect(
                self.screen,
                (
                    40,
                    190,
                    220
                ),
                (
                    bar_x,
                    bar_y,
                    progress_width,
                    bar_height
                )
            )

        # =====================================================
        # PROGRESS TEXT
        # =====================================================

        percent = int(
            self.boot_progress * 100
        )

        percent_text = self.boot_small_font.render(
            f"{percent:03d}%",
            True,
            (
                150,
                190,
                200
            )
        )

        percent_rect = percent_text.get_rect(
            midright=(
                bar_x + bar_width,
                bar_y - 10
            )
        )

        self.screen.blit(
            percent_text,
            percent_rect
        )

        # =====================================================
        # FINISHED MESSAGE
        # =====================================================

        if self.boot_complete:

            complete = self.boot_big_font.render(
                "SYSTEM READY",
                True,
                (
                    65,
                    235,
                    125
                )
            )

            complete_rect = complete.get_rect(
                center=(
                    center_x,
                    self.height - 92
                )
            )

            self.screen.blit(
                complete,
                complete_rect
            )

        else:

            # Blinking cursor

            cursor = ""

            if self.boot_cursor_visible:

                cursor = "_"

            cursor_text = self.boot_small_font.render(
                "PLEASE WAIT" + cursor,
                True,
                (
                    100,
                    125,
                    135
                )
            )

            cursor_rect = cursor_text.get_rect(
                center=(
                    center_x,
                    self.height - 70
                )
            )

            self.screen.blit(
                cursor_text,
                cursor_rect
            )

        # =====================================================
        # FADE OUT
        # =====================================================

        if self.boot_fade > 0:

            fade = pygame.Surface(
                (
                    self.width,
                    self.height
                ),
                pygame.SRCALPHA
            )

            fade.fill(
                (
                    0,
                    0,
                    0,
                    min(
                        255,
                        self.boot_fade
                    )
                )
            )

            self.screen.blit(
                fade,
                (
                    0,
                    0
                )
            )

    # =========================================================
    # CREATE SYSTEMS
    # =========================================================

    def create_systems(self):

        self.player = Player(
            self.map_width // 2,
            self.map_height // 2
        )

        self.weapon_manager = WeaponManager()

        self.enemy_manager = EnemyManager(
            self.map_width,
            self.map_height
        )

        self.experience = ExperienceManager()

        self.upgrades = UpgradeManager(
            self.width,
            self.height
        )

        self.ui = UI(
            self.width,
            self.height
        )

        self.menu = MainMenu(
            self.width,
            self.height
        )

        self.settings = Settings(
            self.width,
            self.height
        )

        self.shop = Shop(
            self.width,
            self.height
        )

        self.transition = Transition(
            self.width,
            self.height
        )

    # =========================================================
    # RESET GAME
    # =========================================================

    def reset_game(self):

        self.shop.close()

        self.player = Player(
            self.map_width // 2,
            self.map_height // 2
        )

        self.weapon_manager = WeaponManager()

        self.enemy_manager = EnemyManager(
            self.map_width,
            self.map_height
        )

        self.experience.reset()

        self.upgrades.active = False

        self.coins = 0

        self.screen_shake = 0

        self.damage_flash = 0

        self.wave_flash = 0

        self.wave_text_timer = 0

        self.wave_number_display = 1

        self.game_over.close()

        self.state = GameState.GAME

    # =========================================================
    # CALLBACKS
    # =========================================================

    def give_exp(self, amount):

        levels_gained = (
            self.experience.give_exp(
                amount
            )
        )

        for _ in range(levels_gained):

            self.upgrades.open()

    # ---------------------------------------------------------

    def give_coins(self, amount):

        self.coins += amount

    # ---------------------------------------------------------

    def damage_player(self, amount):

        self.player.hp -= amount

        if self.player.hp < 0:

            self.player.hp = 0

        self.screen_shake = max(
            self.screen_shake,
            8
        )

        self.damage_flash = 8

    # ---------------------------------------------------------

    def wave_complete(self, wave):

        self.wave_number_display = wave

        self.wave_flash = 255

        self.wave_text_timer = 100

        self.shop.open(
            wave
        )

        self.state = GameState.SHOP

    # =========================================================
    # UPDATE PARTICLES
    # =========================================================

    def update_particles(self):

        for particle in self.particles:

            particle["y"] += (
                particle["speed"]
            )

            if particle["y"] > self.map_height:

                particle["y"] = -5

                particle["x"] = (
                    pygame.time.get_ticks()
                    * 0.03
                    + particle["phase"] * 100
                ) % self.map_width

    # =========================================================
    # MENU
    # =========================================================

    def handle_menu_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.running = False

                return

        # -----------------------------------------------------
        # Minus key boot replay
        # -----------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key in (
                pygame.K_MINUS,
                pygame.K_KP_MINUS
            ):

                self.boot_hold_time = 1

                return

        if event.type == pygame.KEYUP:

            if event.key in (
                pygame.K_MINUS,
                pygame.K_KP_MINUS
            ):

                self.boot_hold_time = 0

                return

        # -----------------------------------------------------
        # Mouse
        # -----------------------------------------------------

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        result = self.menu.handle_click(
            event.pos
        )

        if result == "play":

            self.reset_game()

            self.transition.fade_in()

        elif result == "settings":

            self.settings_return_to = (
                GameState.MENU
            )

            self.state = (
                GameState.SETTINGS
            )

        elif result == "quit":

            self.running = False

    # =========================================================
    # SETTINGS
    # =========================================================

    def handle_settings_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.state = (
                    self.settings_return_to
                )

                return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        result = self.settings.handle_click(
            event.pos
        )

        if result == "close":

            self.state = (
                self.settings_return_to
            )

        elif result == "main_menu":

            self.shop.close()

            self.state = (
                GameState.MENU
            )

    # =========================================================
    # GAME
    # =========================================================

    def handle_game_event(self, event):

        # -----------------------------------------------------
        # LEVEL UP
        # -----------------------------------------------------

        if self.upgrades.active:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    self.upgrades.handle_click(
                        event.pos,
                        self.player,
                        self.weapon_manager.bullet_manager,
                        self.enemy_manager
                    )

            return

        # -----------------------------------------------------
        # ESC
        # -----------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.settings_return_to = (
                    GameState.GAME
                )

                self.state = (
                    GameState.SETTINGS
                )

                return

        # -----------------------------------------------------
        # SETTINGS BUTTON
        # -----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if hasattr(
                    self.settings,
                    "button_rect"
                ):

                    if self.settings.button_rect.collidepoint(
                        event.pos
                    ):

                        self.settings_return_to = (
                            GameState.GAME
                        )

                        self.state = (
                            GameState.SETTINGS
                        )

    # =========================================================
    # SHOP
    # =========================================================

    def handle_shop_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.shop.close()

                self.state = (
                    GameState.GAME
                )

                self.enemy_manager.start_wave()

                return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        self.coins = self.shop.handle_click(
            event.pos,
            self.coins,
            self.player,
            self.weapon_manager.bullet_manager
        )

        if not self.shop.active:

            self.state = (
                GameState.GAME
            )

            self.enemy_manager.start_wave()

    # =========================================================
    # GAME OVER
    # =========================================================

    def handle_game_over_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.shop.close()

                self.state = (
                    GameState.MENU
                )

                return

        result = self.game_over.handle_event(
            event
        )

        if result == "restart":

            self.reset_game()

            self.transition.fade_in()

        elif result == "menu":

            self.shop.close()

            self.state = (
                GameState.MENU
            )

            self.transition.fade_in()

    # =========================================================
    # EVENT ROUTER
    # =========================================================

    def handle_event(self, event):

        if event.type == pygame.QUIT:

            self.running = False

            return

        # -----------------------------------------------------
        # Boot sequence
        # -----------------------------------------------------

        if self.boot_active:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    # Don't allow the first boot sequence
                    # to accidentally be skipped.

                    if self.first_boot:

                        return

                    self.boot_active = False

                    self.state = GameState.MENU

            return

        # -----------------------------------------------------
        # Normal states
        # -----------------------------------------------------

        if self.state == GameState.MENU:

            self.handle_menu_event(
                event
            )

        elif self.state == GameState.GAME:

            self.handle_game_event(
                event
            )

        elif self.state == GameState.SHOP:

            self.handle_shop_event(
                event
            )

        elif self.state == GameState.SETTINGS:

            self.handle_settings_event(
                event
            )

        elif self.state == GameState.GAME_OVER:

            self.handle_game_over_event(
                event
            )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        self.visual_time += 1

        # =====================================================
        # BOOT
        # =====================================================

        if self.boot_active:

            self.update_boot()

            return

        # =====================================================
        # MENU MINUS HOLD
        # =====================================================

        if self.state == GameState.MENU:

            keys = pygame.key.get_pressed()

            minus_down = (
                keys[pygame.K_MINUS]
                or keys[pygame.K_KP_MINUS]
            )

            if minus_down:

                self.boot_hold_time += 1

                # -------------------------------------------------
                # Trigger replay
                # -------------------------------------------------

                if (
                    self.boot_hold_time >=
                    self.boot_hold_required
                ):

                    self.boot_hold_time = 0

                    self.start_boot_sequence(
                        replay=True
                    )

                    return

            else:

                self.boot_hold_time = 0

        # =====================================================
        # NORMAL UPDATE
        # =====================================================

        self.update_particles()

        self.transition.update()

        if self.damage_flash > 0:

            self.damage_flash -= 1

        if self.wave_flash > 0:

            self.wave_flash -= 5

            if self.wave_flash < 0:
                self.wave_flash = 0

        if self.wave_text_timer > 0:

            self.wave_text_timer -= 1

        if self.state != GameState.GAME:
            return

        if self.upgrades.active:
            return

        keys = pygame.key.get_pressed()

        self.player.move(
            keys,
            self.map_width,
            self.map_height
        )

        # -----------------------------------------------------
        # AUTO FIRE
        # -----------------------------------------------------

        self.weapon_manager.auto_shoot(
            self.player,
            self.enemy_manager.enemies
        )

        # -----------------------------------------------------
        # BULLETS
        # -----------------------------------------------------

        self.weapon_manager.update(
            self.map_width,
            self.map_height
        )

        # -----------------------------------------------------
        # ENEMIES
        # -----------------------------------------------------

        self.enemy_manager.update(
            self.weapon_manager.bullet_manager.bullets,
            self.player.x,
            self.player.y,
            self.give_exp,
            self.damage_player,
            self.give_coins,
            self.wave_complete
        )

        # -----------------------------------------------------
        # GAME OVER
        # -----------------------------------------------------

        if self.player.hp <= 0:

            self.player.hp = 0

            self.state = (
                GameState.GAME_OVER
            )

            self.game_over.open(
                self.enemy_manager.wave
            )

            self.screen_shake = 12

    # =========================================================
    # DRAW GAME BACKGROUND
    # =========================================================

    def draw_game_background(self):

        surface = self.game_surface

        surface.fill(
            (
                5,
                7,
                12
            )
        )

        # =====================================================
        # LARGE RADIAL GLOW
        # =====================================================

        glow = pygame.Surface(
            (
                self.map_width,
                self.map_height
            ),
            pygame.SRCALPHA
        )

        center_x = self.map_width // 2
        center_y = self.map_height // 2

        pulse = (
            math.sin(
                self.visual_time * 0.025
            ) + 1
        ) / 2

        for radius in range(
            420,
            80,
            -40
        ):

            alpha = int(
                2 +
                pulse * 3
            )

            pygame.draw.circle(
                glow,
                (
                    10,
                    100,
                    140,
                    alpha
                ),
                (
                    center_x,
                    center_y
                ),
                radius
            )

        surface.blit(
            glow,
            (
                0,
                0
            )
        )

        # =====================================================
        # GRID
        # =====================================================

        grid_color = (
            12,
            30,
            40
        )

        spacing = 50

        for x in range(
            0,
            self.map_width,
            spacing
        ):

            pygame.draw.line(
                surface,
                grid_color,
                (
                    x,
                    0
                ),
                (
                    x,
                    self.map_height
                ),
                1
            )

        for y in range(
            0,
            self.map_height,
            spacing
        ):

            pygame.draw.line(
                surface,
                grid_color,
                (
                    0,
                    y
                ),
                (
                    self.map_width,
                    y
                ),
                1
            )

        # =====================================================
        # SECONDARY GRID
        # =====================================================

        secondary = (
            8,
            19,
            27
        )

        for x in range(
            25,
            self.map_width,
            spacing
        ):

            pygame.draw.line(
                surface,
                secondary,
                (
                    x,
                    0
                ),
                (
                    x,
                    self.map_height
                ),
                1
            )

        # =====================================================
        # AMBIENT PARTICLES
        # =====================================================

        for particle in self.particles:

            flicker = (
                math.sin(
                    self.visual_time * 0.04 +
                    particle["phase"]
                ) + 1
            ) / 2

            brightness = int(
                35 +
                flicker * 45
            )

            pygame.draw.rect(
                surface,
                (
                    20,
                    brightness,
                    brightness + 10
                ),
                (
                    int(particle["x"]),
                    int(particle["y"]),
                    particle["size"],
                    particle["size"]
                )
            )

        # =====================================================
        # CROSS GRID CENTER
        # =====================================================

        pygame.draw.line(
            surface,
            (
                15,
                50,
                62
            ),
            (
                center_x,
                0
            ),
            (
                center_x,
                self.map_height
            ),
            1
        )

        pygame.draw.line(
            surface,
            (
                15,
                50,
                62
            ),
            (
                0,
                center_y
            ),
            (
                self.map_width,
                center_y
            ),
            1
        )

    # =========================================================
    # DRAW MAP BORDER
    # =========================================================

    def draw_map_border(self):

        surface = self.game_surface

        # -----------------------------------------------------
        # Outer border
        # -----------------------------------------------------

        pygame.draw.rect(
            surface,
            (
                30,
                100,
                120
            ),
            (
                0,
                0,
                self.map_width - 1,
                self.map_height - 1
            ),
            2
        )

        # -----------------------------------------------------
        # Inner border
        # -----------------------------------------------------

        pygame.draw.rect(
            surface,
            (
                10,
                40,
                52
            ),
            (
                5,
                5,
                self.map_width - 11,
                self.map_height - 11
            ),
            1
        )

        # -----------------------------------------------------
        # Animated corner accents
        # -----------------------------------------------------

        pulse = (
            math.sin(
                self.visual_time * 0.04
            ) + 1
        ) / 2

        brightness = int(
            100 +
            pulse * 100
        )

        accent = (
            30,
            brightness,
            255
        )

        length = 35

        # Top left

        pygame.draw.line(
            surface,
            accent,
            (
                0,
                length
            ),
            (
                0,
                0
            ),
            3
        )

        pygame.draw.line(
            surface,
            accent,
            (
                0,
                0
            ),
            (
                length,
                0
            ),
            3
        )

        # Top right

        pygame.draw.line(
            surface,
            accent,
            (
                self.map_width - 1,
                0
            ),
            (
                self.map_width - 1,
                length
            ),
            3
        )

        pygame.draw.line(
            surface,
            accent,
            (
                self.map_width - 1,
                0
            ),
            (
                self.map_width - length,
                0
            ),
            3
        )

        # Bottom left

        pygame.draw.line(
            surface,
            accent,
            (
                0,
                self.map_height - length
            ),
            (
                0,
                self.map_height - 1
            ),
            3
        )

        pygame.draw.line(
            surface,
            accent,
            (
                0,
                self.map_height - 1
            ),
            (
                length,
                self.map_height - 1
            ),
            3
        )

        # Bottom right

        pygame.draw.line(
            surface,
            accent,
            (
                self.map_width - 1,
                self.map_height - length
            ),
            (
                self.map_width - 1,
                self.map_height - 1
            ),
            3
        )

        pygame.draw.line(
            surface,
            accent,
            (
                self.map_width - 1,
                self.map_height - 1
            ),
            (
                self.map_width - length,
                self.map_height - 1
            ),
            3
        )

    # =========================================================
    # DRAW SCANLINES
    # =========================================================

    def draw_scanlines(self):

        scanlines = pygame.Surface(
            (
                self.map_width,
                self.map_height
            ),
            pygame.SRCALPHA
        )

        for y in range(
            0,
            self.map_height,
            7
        ):

            pygame.draw.line(
                scanlines,
                (
                    70,
                    180,
                    200,
                    8
                ),
                (
                    0,
                    y
                ),
                (
                    self.map_width,
                    y
                ),
                1
            )

        self.game_surface.blit(
            scanlines,
            (
                0,
                0
            )
        )

    # =========================================================
    # DRAW DAMAGE FLASH
    # =========================================================

    def draw_damage_flash(self):

        if self.damage_flash <= 0:
            return

        alpha = int(
            65 *
            (
                self.damage_flash / 8
            )
        )

        flash = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        flash.fill(
            (
                255,
                35,
                45,
                alpha
            )
        )

        self.screen.blit(
            flash,
            (
                0,
                0
            )
        )

    # =========================================================
    # DRAW WAVE EFFECT
    # =========================================================

    def draw_wave_effect(self):

        if self.wave_text_timer <= 0:
            return

        center_x = self.width // 2

        progress = (
            100 -
            self.wave_text_timer
        ) / 100

        if progress < 0:
            progress = 0

        if progress > 1:
            progress = 1

        offset = int(
            (1 - progress) * 40
        )

        alpha = int(
            255 *
            min(
                1,
                self.wave_text_timer / 25
            )
        )

        font = pygame.font.Font(
            None,
            42
        )

        text = font.render(
            "WAVE "
            + str(self.wave_number_display)
            + " COMPLETE",
            True,
            (
                70,
                225,
                255
            )
        )

        text.set_alpha(
            alpha
        )

        rect = text.get_rect(
            center=(
                center_x,
                self.height // 2 - offset
            )
        )

        # Shadow

        shadow = font.render(
            "WAVE "
            + str(self.wave_number_display)
            + " COMPLETE",
            True,
            (
                10,
                45,
                55
            )
        )

        shadow.set_alpha(
            alpha
        )

        shadow_rect = shadow.get_rect(
            center=(
                center_x + 4,
                self.height // 2 + 4 - offset
            )
        )

        self.screen.blit(
            shadow,
            shadow_rect
        )

        self.screen.blit(
            text,
            rect
        )

        # Accent lines

        line_width = int(
            100 +
            progress * 160
        )

        pygame.draw.line(
            self.screen,
            (
                30,
                130,
                150
            ),
            (
                center_x - line_width,
                rect.bottom + 14
            ),
            (
                center_x + line_width,
                rect.bottom + 14
            ),
            2
        )

    # =========================================================
    # DRAW VIGNETTE
    # =========================================================

    def draw_vignette(self):

        vignette = pygame.Surface(
            (
                self.width,
                self.height
            ),
            pygame.SRCALPHA
        )

        # Top and bottom darkness

        for i in range(90):

            alpha = int(
                1.5 *
                (
                    90 - i
                )
            )

            pygame.draw.rect(
                vignette,
                (
                    0,
                    0,
                    0,
                    alpha
                ),
                (
                    0,
                    i,
                    self.width,
                    1
                )
            )

            pygame.draw.rect(
                vignette,
                (
                    0,
                    0,
                    0,
                    alpha
                ),
                (
                    0,
                    self.height - i - 1,
                    self.width,
                    1
                )
            )

        self.screen.blit(
            vignette,
            (
                0,
                0
            )
        )

    # =========================================================
    # DRAW GAME
    # =========================================================

    def draw_game(self):

        self.draw_game_background()

        # =====================================================
        # DEBUG CIRCLES
        # =====================================================

        if getattr(
            self.settings,
            "debug_mode",
            False
        ):

            pygame.draw.circle(
                self.game_surface,
                (
                    40,
                    90,
                    180
                ),
                (
                    int(self.player.x),
                    int(self.player.y)
                ),
                int(
                    self.weapon_manager
                    .bullet_manager
                    .sight_range
                ),
                1
            )

            pygame.draw.circle(
                self.game_surface,
                (
                    40,
                    180,
                    120
                ),
                (
                    int(self.player.x),
                    int(self.player.y)
                ),
                int(
                    self.enemy_manager
                    .attraction_radius
                ),
                1
            )

        # =====================================================
        # OBJECTS
        # =====================================================

        self.enemy_manager.draw(
            self.game_surface
        )

        self.weapon_manager.draw(
            self.game_surface
        )

        self.player.draw(
            self.game_surface
        )

        # =====================================================
        # MAP BORDER
        # =====================================================

        self.draw_map_border()

        # =====================================================
        # SCANLINES
        # =====================================================

        self.draw_scanlines()

        # =====================================================
        # SCREEN SHAKE
        # =====================================================

        shake_x = 0
        shake_y = 0

        if self.screen_shake > 0:

            angle = (
                self.visual_time * 37
            ) % 360

            shake_x = (
                pygame.math.Vector2(
                    1,
                    0
                ).rotate(angle).x
                * self.screen_shake
            )

            shake_y = (
                pygame.math.Vector2(
                    0,
                    1
                ).rotate(angle).y
                * self.screen_shake
            )

        self.screen.blit(
            self.game_surface,
            (
                self.map_x + int(shake_x),
                self.map_y + int(shake_y)
            )
        )

        # =====================================================
        # UI
        # =====================================================

        self.ui.draw(
            self.screen,
            self.player.hp,
            self.player.max_hp,
            self.experience.exp,
            self.experience.max_exp,
            self.experience.level,
            self.enemy_manager.wave
        )

        # =====================================================
        # SETTINGS BUTTON
        # =====================================================

        self.settings.draw_button(
            self.screen
        )

        # =====================================================
        # EFFECTS
        # =====================================================

        self.draw_damage_flash()

        self.draw_wave_effect()

        self.draw_vignette()

        # =====================================================
        # SHAKE DECAY
        # =====================================================

        if self.screen_shake > 0:

            self.screen_shake -= 1

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self):

        self.screen.fill(
            (
                3,
                4,
                8
            )
        )

        # =====================================================
        # BOOT SEQUENCE
        # =====================================================

        if self.boot_active:

            self.draw_boot()

        elif self.state == GameState.MENU:

            self.menu.draw(
                self.screen
            )

            # -------------------------------------------------
            # MINUS HOLD INDICATOR
            # -------------------------------------------------

            keys = pygame.key.get_pressed()

            minus_down = (
                keys[pygame.K_MINUS]
                or keys[pygame.K_KP_MINUS]
            )

            if minus_down:

                progress = min(
                    1.0,
                    self.boot_hold_time /
                    self.boot_hold_required
                )

                text = pygame.font.Font(
                    None,
                    16
                ).render(
                    "HOLD - TO REBOOT SYSTEM",
                    True,
                    (
                        130,
                        150,
                        160
                    )
                )

                text_rect = text.get_rect(
                    center=(
                        self.width // 2,
                        self.height - 55
                    )
                )

                self.screen.blit(
                    text,
                    text_rect
                )

                bar_width = 180
                bar_height = 5

                bar_x = (
                    self.width // 2 -
                    bar_width // 2
                )

                bar_y = (
                    self.height - 32
                )

                pygame.draw.rect(
                    self.screen,
                    (
                        15,
                        30,
                        35
                    ),
                    (
                        bar_x,
                        bar_y,
                        bar_width,
                        bar_height
                    )
                )

                pygame.draw.rect(
                    self.screen,
                    (
                        60,
                        220,
                        255
                    ),
                    (
                        bar_x,
                        bar_y,
                        int(
                            bar_width *
                            progress
                        ),
                        bar_height
                    )
                )

        elif self.state == GameState.GAME:

            self.draw_game()

            if self.upgrades.active:

                self.upgrades.draw(
                    self.screen
                )

        elif self.state == GameState.SHOP:

            self.draw_game()

            self.shop.draw(
                self.screen,
                self.coins
            )

        elif self.state == GameState.SETTINGS:

            self.settings.draw(
                self.screen
            )

        elif self.state == GameState.GAME_OVER:

            self.draw_game()

            self.game_over.draw(
                self.screen
            )

        # =====================================================
        # TRANSITION
        # =====================================================

        if not self.boot_active:

            self.transition.draw(
                self.screen
            )

        pygame.display.flip()

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        # =====================================================
        # START FIRST BOOT
        # =====================================================

        if self.first_boot:

            self.start_boot_sequence(
                replay=False
            )

        # =====================================================
        # MAIN LOOP
        # =====================================================

        while self.running:

            for event in pygame.event.get():

                self.handle_event(
                    event
                )

            self.update()

            self.draw()

            self.clock.tick(60)

        self.shop.close()

        pygame.quit()