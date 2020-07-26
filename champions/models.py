from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

def insert_all_objects():
    f = open('champions.csv')
    f = open('abilities.csv')
    f = open('effects.csv')
    champion = Champion(name='')


class Champion(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    health = models.FloatField(default=None, blank=True, null=True)
    health_scaling = models.FloatField(default=None, blank=True, null=True)
    health_regen = models.FloatField(default=None, blank=True, null=True)
    health_regen_scaling = models.FloatField(default=None, blank=True, null=True)
    mana = models.FloatField(default=None, blank=True, null=True)
    mana_scaling = models.FloatField(default=None, blank=True, null=True)
    mana_regen = models.FloatField(default=None, blank=True, null=True)
    mana_regen_scaling = models.FloatField(default=None, blank=True, null=True)
    attack_damage = models.FloatField(default=None, blank=True, null=True)
    attack_damage_scaling = models.FloatField(default=None, blank=True, null=True)
    attack_speed = models.FloatField(default=None, blank=True, null=True)
    attack_speed_scaling = models.FloatField(default=None, blank=True, null=True)
    armor = models.FloatField(default=None, blank=True, null=True)
    armor_scaling = models.FloatField(default=None, blank=True, null=True)
    magic_resist = models.FloatField(default=None, blank=True, null=True)
    magic_resist_scaling = models.FloatField(default=None, blank=True, null=True)
    movement_speed = models.FloatField(default=None, blank=True, null=True)
    range = models.FloatField(default=None, blank=True, null=True)
    ability_q1 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_q1", null=True,
                                   default=None, blank=True)
    ability_w1 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_w1", null=True,
                                   default=None, blank=True)
    ability_e1 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_e1", null=True,
                                   default=None, blank=True)
    ability_r1 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_r1", null=True,
                                   default=None, blank=True)
    ability_q2 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_q2", null=True,
                                   default=None, blank=True)
    ability_w2 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_w2", null=True,
                                   default=None, blank=True)
    ability_e2 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_e2", null=True,
                                   default=None, blank=True)
    ability_r2 = models.ForeignKey('Ability', on_delete=models.CASCADE, related_name="ability_r2", null=True,
                                   default=None, blank=True)

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    ability_position = models.CharField(max_length=200, null=True)
    max_charges = models.IntegerField(null=True, blank=True)
    max_stacks = models.IntegerField(null=True, blank=True)
    cooldown_ranks = models.CharField(max_length=200, null=True)
    recharge_cooldown_ranks = models.CharField(max_length=200, null=True)
    # cost
    cost_ranks = models.CharField(max_length=200, null=True)
    cost_type = models.ForeignKey('CostType', on_delete=models.CASCADE, related_name="cost_type", null=True,
                                  default=None,
                                  blank=True)
    # cost2
    cost2_ranks = models.CharField(max_length=200, null=True)
    cost2_type = models.ForeignKey('CostType', on_delete=models.CASCADE, related_name="cost2_type", null=True,
                                   default=None,
                                   blank=True)
    effect1 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_1", null=True, default=None,
                                blank=True)
    effect2 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_2", null=True, default=None,
                                blank=True)
    effect3 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_3", null=True, default=None,
                                blank=True)
    effect4 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_4", null=True, default=None,
                                blank=True)
    effect5 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_5", null=True, default=None,
                                blank=True)
    effect6 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_6", null=True, default=None,
                                blank=True)
    effect7 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_7", null=True, default=None,
                                blank=True)
    effect8 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_8", null=True, default=None,
                                blank=True)
    effect9 = models.ForeignKey('Effect', on_delete=models.CASCADE, related_name="effect_9", null=True, default=None,
                                blank=True)

    def __str__(self):
        return self.name


class Effect(models.Model):
    effect_ability_name = models.CharField(max_length=200, null=True)
    effect_name = models.CharField(max_length=200, null=True)
    effect_ranks = models.CharField(max_length=200, null=True)
    effect_type = models.ForeignKey('EffectType', on_delete=models.CASCADE, related_name="effect_type", null=True,
                                    default=None,
                                    blank=True)
    # scaling
    scaling_ranks = models.CharField(max_length=200, null=True)
    scaling_type = models.ForeignKey('ScalingType', on_delete=models.CASCADE, related_name="scaling_type", null=True,
                                     default=None,
                                     blank=True)
    # scaling2
    scaling2_ranks = models.CharField(max_length=200, null=True)
    scaling2_type = models.ForeignKey('ScalingType', on_delete=models.CASCADE, related_name="scaling2_type", null=True,
                                      default=None,
                                      blank=True)

    def __str__(self):
        if self.effect_name is not None and self.effect_name != "":
            return f'{self.effect_ability_name}: {self.effect_name.replace(":", "")}'
        else:
            return self.effect_ability_name


class CostType(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name


class EffectType(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name


class ScalingType(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.name