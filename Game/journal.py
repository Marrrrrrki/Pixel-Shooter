import json
from pathlib import Path


SAVE_FILE = Path(__file__).resolve().parent.parent / "pixel_shooter_data.json"


class Journal:

    ENEMY_NAMES = {
        "normal": "NORMAL ENEMY"
    }

    UPGRADE_NAMES = {
        "fire_rate": "RAPID FIRE",
        "bullet_speed": "BULLET SPEED",
        "damage": "BULLET POWER",
        "max_hp": "MAX HP",
        "heal": "REPAIR",
        "move_speed": "MOVE SPEED",
        "sight": "SIGHT",
        "pickup_range": "ARMS"
    }

    def __init__(self):

        self.data = {}

        self.load()

    # =========================================================
    # LOAD
    # =========================================================

    def load(self):

        try:

            self.data = (
                json.loads(
                    SAVE_FILE.read_text(
                        encoding="utf-8"
                    )
                )
                if SAVE_FILE.exists()
                else {}
            )

        except (
            OSError,
            json.JSONDecodeError
        ):

            self.data = {}

        journal = self.data.setdefault(
            "journal",
            {}
        )

        journal.setdefault(
            "enemies",
            []
        )

        journal.setdefault(
            "upgrades",
            []
        )

        # Remove the old Runner entry
        if "runner" in journal["enemies"]:

            journal["enemies"].remove(
                "runner"
            )

            self.save()

    # =========================================================
    # SAVE
    # =========================================================

    def save(self):

        try:

            SAVE_FILE.write_text(
                json.dumps(
                    self.data,
                    indent=4
                ),
                encoding="utf-8"
            )

        except OSError:

            pass

    # =========================================================
    # DISCOVER ENEMY
    # =========================================================

    def discover_enemy(
        self,
        enemy_id
    ):

        self.load()

        enemies = self.data[
            "journal"
        ][
            "enemies"
        ]

        if enemy_id not in enemies:

            enemies.append(
                enemy_id
            )

            self.save()

    # =========================================================
    # DISCOVER UPGRADE
    # =========================================================

    def discover_upgrade(
        self,
        upgrade_id
    ):

        self.load()

        upgrades = self.data[
            "journal"
        ][
            "upgrades"
        ]

        if upgrade_id not in upgrades:

            upgrades.append(
                upgrade_id
            )

            self.save()

    # =========================================================
    # ENEMY COUNT
    # =========================================================

def enemy_count(self):

        return len(
            self.data[
                "journal"
            ][
                "enemies"
            ]
        )

    # =========================================================
    # UPGRADE COUNT
    # =========================================================

def upgrade_count(self):

        return len(
            self.data[
                "journal"
            ][
                "upgrades"
            ]
        )