from .models import Champion


class SimulationChampion:

    def __init__(self, champion: Champion):
        self.name = champion.name
        # all champions are simulated at maximum level
        self.level = 18
        # max value stats
        self.max_health = champion.health + champion.health_scaling * (self.level - 1)
        self.max_health_regen = champion.health_regen + champion.health_regen_scaling * (self.level - 1)
        self.max_mana = champion.mana + champion.mana_scaling * (self.level - 1)
        self.max_mana_regen = champion.mana_regen + champion.mana_regen_scaling * (self.level - 1)
        self.max_attack_damage = champion.attack_damage + champion.attack_damage_scaling * (self.level - 1)
        # attack speed scaling is based on percentage of base attack speed
        self.max_attack_speed = champion.attack_speed * (1 + (champion.attack_speed_scaling * (self.level - 1)))
        self.max_armor = champion.armor + champion.armor_scaling * (self.level - 1)
        self.max_magic_resist = champion.magic_resist + champion.magic_resist_scaling * (self.level - 1)
        # movement speed and range do not scale with level
        self.max_movement_speed = champion.movement_speed
        self.max_range = champion.range
        # current value stats start at the maximum value.
        # current value stats are needed for each stat because they will be affected by ability modifiers from
        # the champions abilities and their enemy's abilities.
        self.current_health = self.max_health
        self.current_health_regen = self.max_health_regen
        self.current_mana = self.max_mana
        self.current_mana_regen = self.max_mana_regen
        self.current_attack_damage = self.max_attack_damage
        self.current_attack_speed = self.max_attack_speed
        self.current_armor = self.max_armor
        self.current_magic_resist = self.max_magic_resist
        self.current_movement_speed = self.max_movement_speed
        self.current_range = self.max_range
        # additional stats that have no base value but instead are affected by items and abilities:
        self.current_ability_power = 0
        self.current_critical_strike_chance = 0
        self.current_critical_strike_damage = 0
        self.tenacity = 0
        self.cooldown_reduction = 0
        # additional stats for simulation
        self.disabled = False
        self.disabled_cd = 0
        self.movement_disabled = False
        self.movement_disabled_cd = 0
        self.q_cd = 0
        self.w_cd = 0
        self.e_cd = 0
        self.r_cd = 0
        self.aa_cd = 0
        self.shield = 0
        self.magic_shield = 0

    def __str__(self):
        return self.name
