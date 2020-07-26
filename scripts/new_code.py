def print_dict(target_dict):
    for k, v in target_dict:
        print(str(k) + ':' + str(v))


def combat_simulation(champion_a, champion_b):
    a_offense = []
    b_offense = []
    a_defense = []
    b_defense = []
    damage_over_time_list = []
    # fight_count
    max_fight_count = 100
    current_fight_count = 0
    # simulation_time
    max_seconds = 100
    current_seconds = 0
    # wins
    champion_a_wins = 0
    champion_b_wins = 0
    draw_count = 0
    # win probability
    champion_a_probability = 0
    champion_b_probability = 0
    # determine which abilities are offensive and defensive
    # ... for champion a
    for ability in champion_a.abilities:
        if ability.type in ('a', 'b', 'c'):
            a_offense.append(ability)
        if ability.type in ('d', 'e', 'f'):
            a_defense.append(ability)
    # ... for champion b
    for ability in champion_b.abilities:
        if ability.type in ('a', 'b', 'c'):
            b_offense.append(ability)
        if ability.type in ('d', 'e', 'f'):
            b_defense.append(ability)

    # start simulation
    for i in range(max_fight_count):
        while current_seconds < max_seconds:
            # apply abilities
            for ability in a_defense:
                if ability.next_available == current_seconds:
                    ability.use()
                    ability.next_available = ability.cooldown + current_seconds
            for ability in b_defense:
                if ability.next_available == current_seconds:
                    ability.use()
                    ability.next_available = ability.cooldown + current_seconds
            for ability in a_offense:
                if ability.next_available == current_seconds:
                    ability.use()
                    ability.next_available = ability.cooldown + current_seconds
            for ability in b_defense:
                if ability.next_available == current_seconds:
                    ability.use()
                    ability.next_available = ability.cooldown + current_seconds

            # apply damage

            # apply crowd control

            # determine if a player won.
            if champion_a.hp <= 0 and champion_b.hp > 0:
                champion_b_wins += 1
                break
            if champion_b.hp <= 0 and champion_a.hp > 0:
                champion_a_wins += 1
                break
            if champion_a.hp <= 0 and champion_b.hp <= 0:
                draw_count += 1
                break

            current_seconds += 0.01


def reduce_damage(damage, damage_type, target):
    resist = 0
    if damage_type == 'PHYSICAL':
        resist = target.armor
    elif damage_type == 'MAGICAL':
        resist = target.magic_resist

    if resist >= 0:
        damage_multiplier = 100 / (100 + resist)
    else:
        damage_multiplier = 2 - 100 / (100 - resist)
    return damage * damage_multiplier


def apply_damage(damage, damage_type, target):
    damage = reduce_damage(damage, damage_type, target)
    if target.shield >= damage:
        target.shield -= damage
    elif target.shield < damage:
        damage -= target.shield
        target.shield = 0
    if target.hp >= 0:
        target.hp -= damage
