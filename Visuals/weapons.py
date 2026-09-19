from Visuals.bullets import BulletManager


class WeaponManager:

    def __init__(self):

        self.bullet_manager = BulletManager()


    # =========================
    # SHOOT
    # =========================

    def auto_shoot(
        self,
        player,
        enemies
    ):

        self.bullet_manager.auto_shoot(
            player,
            enemies
        )


    # =========================
    # UPDATE
    # =========================

    def update(
        self,
        width,
        height
    ):

        self.bullet_manager.update(
            width,
            height
        )


    # =========================
    # DRAW
    # =========================

    def draw(self, screen):

        self.bullet_manager.draw(
            screen
        )