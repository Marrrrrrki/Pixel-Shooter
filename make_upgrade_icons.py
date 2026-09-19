import pygame
import os


pygame.init()


# =========================
# SETTINGS
# =========================

SIZE = 32

SCALE = 8

OUTPUT_FOLDER = "upgrade_icons"


os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =========================
# COLORS
# =========================

TRANSPARENT = (
    0,
    0,
    0,
    0
)

WHITE = (
    245,
    245,
    245
)

GRAY = (
    150,
    150,
    160
)

RED = (
    220,
    55,
    55
)

BLUE = (
    65,
    130,
    230
)

YELLOW = (
    235,
    190,
    55
)

GREEN = (
    70,
    200,
    100
)


# =========================
# CREATE ICON
# =========================

def create_icon(
    name,
    draw_function
):

    surface = pygame.Surface(
        (
            SIZE,
            SIZE
        ),
        pygame.SRCALPHA
    )

    surface.fill(
        TRANSPARENT
    )

    draw_function(
        surface
    )


    # =========================
    # SCALE
    # =========================

    large_surface = pygame.transform.scale(
        surface,
        (
            SIZE * SCALE,
            SIZE * SCALE
        )
    )


    pygame.image.save(
        large_surface,
        os.path.join(
            OUTPUT_FOLDER,
            name + ".png"
        )
    )


# =========================
# RAPID FIRE
# =========================

def rapid_fire(surface):

    pygame.draw.polygon(
        surface,
        YELLOW,
        [
            (17, 2),
            (7, 17),
            (14, 17),
            (11, 30),
            (26, 13),
            (19, 13),
            (23, 2)
        ]
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (
            2,
            10,
            4,
            3
        )
    )

    pygame.draw.rect(
        surface,
        GRAY,
        (
            1,
            17,
            4,
            3
        )
    )

    pygame.draw.rect(
        surface,
        GRAY,
        (
            3,
            24,
            5,
            3
        )
    )


# =========================
# BULLET SPEED
# =========================

def bullet_speed(surface):

    pygame.draw.rect(
        surface,
        GRAY,
        (
            5,
            13,
            17,
            7
        )
    )

    pygame.draw.polygon(
        surface,
        WHITE,
        [
            (22, 13),
            (29, 16),
            (22, 20)
        ]
    )

    pygame.draw.rect(
        surface,
        BLUE,
        (
            0,
            10,
            8,
            3
        )
    )

    pygame.draw.rect(
        surface,
        BLUE,
        (
            1,
            22,
            9,
            3
        )
    )


# =========================
# BULLET POWER
# =========================

def bullet_power(surface):

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            14,
            3,
            4,
            8
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            14,
            21,
            4,
            8
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            3,
            14,
            8,
            4
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            21,
            14,
            8,
            4
        )
    )

    pygame.draw.polygon(
        surface,
        RED,
        [
            (12, 10),
            (20, 10),
            (22, 14),
            (20, 22),
            (12, 22),
            (10, 18),
            (10, 14)
        ]
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (
            14,
            13,
            5,
            7
        )
    )


# =========================
# MAX HP
# =========================

def max_hp(surface):

    pygame.draw.rect(
        surface,
        RED,
        (
            8,
            8,
            5,
            5
        )
    )

    pygame.draw.rect(
        surface,
        RED,
        (
            19,
            8,
            5,
            5
        )
    )

    pygame.draw.rect(
        surface,
        RED,
        (
            5,
            12,
            22,
            8
        )
    )

    pygame.draw.rect(
        surface,
        RED,
        (
            8,
            19,
            16,
            5
        )
    )

    pygame.draw.rect(
        surface,
        RED,
        (
            11,
            23,
            10,
            5
        )
    )

    pygame.draw.rect(
        surface,
        RED,
        (
            14,
            27,
            4,
            3
        )
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (
            10,
            12,
            3,
            3
        )
    )


# =========================
# REPAIR
# =========================

def repair(surface):

    pygame.draw.rect(
        surface,
        WHITE,
        (
            12,
            5,
            8,
            22
        )
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (
            5,
            12,
            22,
            8
        )
    )

    pygame.draw.rect(
        surface,
        GREEN,
        (
            14,
            7,
            4,
            18
        )
    )

    pygame.draw.rect(
        surface,
        GREEN,
        (
            8,
            14,
            16,
            4
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            25,
            4,
            2,
            5
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            23,
            6,
            6,
            2
        )
    )


# =========================
# MOVE SPEED
# =========================

def move_speed(surface):

    pygame.draw.rect(
        surface,
        GRAY,
        (
            12,
            7,
            9,
            14
        )
    )

    pygame.draw.rect(
        surface,
        GRAY,
        (
            10,
            17,
            12,
            7
        )
    )

    pygame.draw.rect(
        surface,
        GRAY,
        (
            7,
            21,
            17,
            6
        )
    )

    pygame.draw.rect(
        surface,
        GRAY,
        (
            3,
            25,
            17,
            4
        )
    )

    pygame.draw.rect(
        surface,
        BLUE,
        (
            2,
            12,
            6,
            3
        )
    )

    pygame.draw.rect(
        surface,
        BLUE,
        (
            1,
            18,
            6,
            3
        )
    )


# =========================
# SIGHT
# =========================

def sight(surface):

    # Outer circle

    pygame.draw.circle(
        surface,
        BLUE,
        (
            16,
            16
        ),
        12,
        2
    )


    # Inner circle

    pygame.draw.circle(
        surface,
        WHITE,
        (
            16,
            16
        ),
        6,
        2
    )


    # Top crosshair

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            14,
            2,
            4,
            8
        )
    )


    # Bottom crosshair

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            14,
            22,
            4,
            8
        )
    )


    # Left crosshair

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            2,
            14,
            8,
            4
        )
    )


    # Right crosshair

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            22,
            14,
            8,
            4
        )
    )


    # Center

    pygame.draw.rect(
        surface,
        WHITE,
        (
            14,
            14,
            4,
            4
        )
    )


# =========================
# COIN
# =========================

def coin(surface):

    # Shadow

    pygame.draw.circle(
        surface,
        (
            90,
            65,
            15
        ),
        (
            17,
            18
        ),
        11
    )


    # Main coin

    pygame.draw.circle(
        surface,
        YELLOW,
        (
            16,
            16
        ),
        11
    )


    # Inner coin

    pygame.draw.circle(
        surface,
        (
            255,
            215,
            70
        ),
        (
            16,
            16
        ),
        7
    )


    # Coin symbol

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            14,
            10,
            4,
            12
        )
    )


    pygame.draw.rect(
        surface,
        YELLOW,
        (
            12,
            10,
            6,
            3
        )
    )

    pygame.draw.rect(
        surface,
        YELLOW,
        (
            12,
            19,
            6,
            3
        )
    )


# =========================
# GENERATE ICONS
# =========================

create_icon(
    "rapid_fire",
    rapid_fire
)

create_icon(
    "bullet_speed",
    bullet_speed
)

create_icon(
    "bullet_power",
    bullet_power
)

create_icon(
    "max_hp",
    max_hp
)

create_icon(
    "repair",
    repair
)

create_icon(
    "move_speed",
    move_speed
)

create_icon(
    "sight",
    sight
)

create_icon(
    "coin",
    coin
)


print(
    "Upgrade and coin icons created in:",
    OUTPUT_FOLDER
)


pygame.quit()