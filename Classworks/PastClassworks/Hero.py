class Hero:
    def __init__(self, name, initial_xp=0, initial_lives=3):
        self._name = name
        self._xp = initial_xp
        self._live = initial_lives

    def get_xp(self, x):
        if 0 < x < 30:
            self._xp += x
        else:
            self._xp += 1

    def get_hurt(self, damage=20):
        if 0 < damage < 50:
            self._live -= damage
        else:
            self._live -= 1

    def __str__(self):
        return f"Hero {self._name}: XP={self._xp}, Lives={self._live}"

hero = Hero("Aragorn")

print(hero)
hero.get_xp(10)
print(hero)
hero.get_hurt(60)
print(hero)
hero.get_xp(25)
hero.get_hurt()
print(hero)
