class ExperienceManager:

    def __init__(self):

        # =========================
        # LEVEL
        # =========================

        self.level = 1

        self.exp = 0

        self.max_exp = 10


    # =========================
    # GIVE EXPERIENCE
    # =========================

    def give_exp(self, amount):

        self.exp += amount

        levels_gained = 0

        while self.exp >= self.max_exp:

            self.exp -= self.max_exp

            self.level += 1

            levels_gained += 1

            # Increase XP requirement

            self.max_exp = int(
                self.max_exp * 1.45
            )

        return levels_gained


    # =========================
    # RESET
    # =========================

    def reset(self):

        self.level = 1

        self.exp = 0

        self.max_exp = 10