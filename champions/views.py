# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

# Import Django Models
from .models import Champion, Ability, Effect, CostType, EffectType, ScalingType

# Import Django Forms
from .forms import ChampionForm

# Python standard imports
import os
import random
import base64

# Import Plotly
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.offline as opy
import plotly.graph_objs as go

# Import simulation types
from .simulation_types import SimulationChampion

# Import BASE_DIR
from django.conf import settings

# champion_squares_path = os.path.join(settings.BASE_DIR, 'static\\images\\champion_square_icons\\')


# global variables
# action_history = []
# current_seconds = -1


def remove_chars(input_string, chars_to_remove):
    chars_to_remove = list(chars_to_remove)
    for char in chars_to_remove:
        input_string = input_string.lower().replace(char, '')
    return input_string


def print_dict(target_dict):
    for k, v in target_dict:
        print(str(k) + ':' + str(v))


def make_title_case(input_string):
    return ''.join(x for x in input_string.strip().title())


def null_if_html(var_name, var):
    null_value_html = '<p style="color: red; background-color: yellow;">NULL</p>'
    if var is not None:
        return f'{var_name}: {var}<br>'
    else:
        return null_value_html


def fix_filename(source_string):
    return source_string \
        .strip() \
        .replace(' ', '_') \
        .replace('\\', '') \
        .replace('/', '') \
        .replace(':', '') \
        .replace('*', '?') \
        .replace('"', '') \
        .replace('<', '') \
        .replace('>', '') \
        .replace('|', '')


def get_ability_effect_types(effect_types, ability):
    if ability is not None:
        if ability.effect1 is not None:
            get_ability_effect_type(effect_types, ability.effect1)
        print(f'Ability: {ability}', 'Effect_types:', effect_types)


def get_ability_effect_type(effect_types, effect):
    if effect.effect_type not in effect_types:
        effect_types.append(effect.effect_type)


def make_graph(x_data, y_data):
    plot_div = plot([Scatter(x=x_data,
                             y=y_data,
                             mode='lines',
                             name='test',
                             opacity=0.8,
                             marker_color='green')],
                    output_type='div')
    return plot_div


# replace champion name/ability name spaces with underscores in champion square filenames


# VIEW RENDER FUNCTIONS:

def dashboard_view(request):
    return render(request, 'champions/dashboard.html')


def champions(request):
    # take all champions from the database
    champion_objs = Champion.objects.all()

    # get all champion img paths
    # global champion_squares_path
    champion_squares_path = os.path.join(settings.STATIC_ROOT, 'images/champion_square_icons/')
    champion_img_dirs = []
    for f in os.listdir(champion_squares_path):
        # problem line in remote file...
        #                BASE_DIR + 'static\\images\\champion_square_icons\\'
        #                /app/    + 'static\\images\\champion_square_icons\\'
        # remote error: '/app/static\\images\\champion_square_icons\\'
        if os.path.isfile(os.path.join(champion_squares_path, f)):
            champion_img_dirs.append('images/champion_square_icons/' + f)

    # get db champion img paths
    db_champion_img_dirs = []
    for c in champion_objs:
        champion_square_fp = os.path.join('images/champion_square_icons/', c.name.replace(' ', '_') + 'Square.png')
        db_champion_img_dirs.append(champion_square_fp)

    # final context to be sent to template
    context = {'champion_objs': champion_objs,
               'champion_img_dirs': champion_img_dirs,
               'db_champion_img_dirs': db_champion_img_dirs,
               'champion_squares_path': champion_squares_path, }

    for champion_img_dir in champion_img_dirs:
        print('champion_img_dir', champion_img_dir)

    return render(request, 'champions/champions.html', context)


def champion(request, champion_name, *args, **kwargs):
    champion = Champion.objects.get(name=champion_name)
    effect_types = []
    get_ability_effect_types(effect_types, champion.ability_q1)
    get_ability_effect_types(effect_types, champion.ability_w1)
    get_ability_effect_types(effect_types, champion.ability_e1)
    get_ability_effect_types(effect_types, champion.ability_r1)
    get_ability_effect_types(effect_types, champion.ability_q2)
    get_ability_effect_types(effect_types, champion.ability_w2)
    get_ability_effect_types(effect_types, champion.ability_e2)
    get_ability_effect_types(effect_types, champion.ability_r2)

    ability_img_dirs = {'q': os.path.join('/images/ability_icons/', fix_filename(champion.ability_q1.name) + '.png'),
                        'w': os.path.join('/images/ability_icons/', fix_filename(champion.ability_w1.name) + '.png'),
                        'e': os.path.join('/images/ability_icons/', fix_filename(champion.ability_e1.name) + '.png'),
                        'r': os.path.join('/images/ability_icons/', fix_filename(champion.ability_r1.name) + '.png')}
    # if ability_img_dirs
    if champion.ability_q2 is not None:
        ability_img_dirs['q2'] = os.path.join('/images/ability_icons/', fix_filename(champion.ability_q2.name) + '.png')
    if champion.ability_w2 is not None:
        ability_img_dirs['w2'] = os.path.join('/images/ability_icons/', fix_filename(champion.ability_w2.name) + '.png')
    if champion.ability_e2 is not None:
        ability_img_dirs['e2'] = os.path.join('/images/ability_icons/', fix_filename(champion.ability_e2.name) + '.png')
    if champion.ability_r2 is not None:
        ability_img_dirs['r2'] = os.path.join('/images/ability_icons/', fix_filename(champion.ability_r2.name) + '.png')

    # make the graph figure using plotly.js
    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = make_graph(x_data, y_data)

    context = {'champion_name': champion_name,
               'champion_img_path': '/images/champion_square_icons/' + champion_name + 'Square.png',
               'champion': champion,
               'ability_img_dirs': ability_img_dirs,
               'plot_div': plot_div,
               'effect_types': effect_types, }
    return render(request, 'champions/champion.html', context)


def import_data(request):
    body_string = '<body style="font-weight: bold; font-size: 9px; font-family: Arial, Helvetica, sans-serif;">'
    import_data_flag = True
    body_string = f'<p>import_data_flag: {import_data_flag}</p>'
    if import_data_flag:
        # Save a Champion using the base_stats.csv file.
        body_string = import_base_stats(body_string)
        # Save a Champion using the data.csv file.
        body_string = import_from_data_csv(body_string)
    body_string += '</body>'
    return HttpResponse(body_string)


def about(request):
    return render(request, 'champions/about.html')


def fight_simulator(request):
    champions_dict = {}
    champion_objs = Champion.objects.all()
    champions_with_abilities = []
    for champion_obj in champion_objs:
        if champion_obj.ability_q1 is not None and champion_obj.ability_q1 != '':
            champions_with_abilities.append(champion_obj)
            champions_dict[champion_obj.name] = {}
            # effect_types = []
            # get_ability_effect_types(effect_types, champion_obj.ability_q1)
            # get_ability_effect_types(effect_types, champion_obj.ability_w1)
            # get_ability_effect_types(effect_types, champion_obj.ability_e1)
            # get_ability_effect_types(effect_types, champion_obj.ability_r1)
            # get_ability_effect_types(effect_types, champion_obj.ability_q2)
            # get_ability_effect_types(effect_types, champion_obj.ability_w2)
            # get_ability_effect_types(effect_types, champion_obj.ability_e2)
            # get_ability_effect_types(effect_types, champion_obj.ability_r2)
            img_dirs = {}
            if champion_obj.name is not None:
                img_dirs['square'] = '/images/champion_square_icons/' + champion_obj.name + 'Square.png'
            if champion_obj.ability_q1 is not None:
                img_dirs['q'] = os.path.join('/images/ability_icons/',
                                             fix_filename(champion_obj.ability_q1.name) + '.png')
            if champion_obj.ability_w1 is not None:
                img_dirs['w'] = os.path.join('/images/ability_icons/',
                                             fix_filename(champion_obj.ability_w1.name) + '.png')
            if champion_obj.ability_e1 is not None:
                img_dirs['e'] = os.path.join('/images/ability_icons/',
                                             fix_filename(champion_obj.ability_e1.name) + '.png')
            if champion_obj.ability_r1 is not None:
                img_dirs['r'] = os.path.join('/images/ability_icons/',
                                             fix_filename(champion_obj.ability_r1.name) + '.png')
            if champion_obj.ability_q2 is not None:
                img_dirs['q2'] = os.path.join('/images/ability_icons/',
                                              fix_filename(champion_obj.ability_q2.name) + '.png')
            if champion_obj.ability_w2 is not None:
                img_dirs['w2'] = os.path.join('/images/ability_icons/',
                                              fix_filename(champion_obj.ability_w2.name) + '.png')
            if champion_obj.ability_e2 is not None:
                img_dirs['e2'] = os.path.join('/images/ability_icons/',
                                              fix_filename(champion_obj.ability_e2.name) + '.png')
            if champion_obj.ability_r2 is not None:
                img_dirs['r2'] = os.path.join('/images/ability_icons/',
                                              fix_filename(champion_obj.ability_r2.name) + '.png')

            # assign lists to champion dict
            champions_dict['objs'] = champions_with_abilities
            champions_dict[champion_obj.name]['img_dirs'] = img_dirs

    # make the graph figure using plotly.js
    x_data = [0, 1, 2, 3]
    y_data = [x ** 2 for x in x_data]
    plot_div = make_graph(x_data, y_data)

    context = {'champions_dict': champions_dict,
               'plot_div': plot_div}

    return render(request, 'champions/fight_simulator.html', context)


# FORM VIEWS

def champion_form_view(request):
    form = ChampionForm()
    champions = Champion.objects.all()
    return render(request, "champions/index.html", {"form": form, "champions": champions})


def post_champion(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = ChampionForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new champion object in json
            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def post_champion_graph(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        try:
            # get the form data
            # request.POST
            print('request.body:', request.body)
            # print('request.POST.get(')')
            print('request.POST.items()')
            for k, v in request.POST.items():
                print(f'{k}:{v}')
            # print('request.POST:', request.POST.get())
            # serialize in new champion object in json
            # ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            # return JsonResponse({"instance": ser_instance}, status=200)
        except Exception as e:
            print('In post_champion_graph:', e)
    # some error occured
    # return JsonResponse({"error": ""}, status=400)


def check_name(request):
    # request should be ajax and method should be GET.
    print('check_name view called')
    if request.is_ajax and request.method == "GET":
        print('request is ajax and GET')
        # get the champion name from the client side.
        name = request.GET.get("name", None)
        # check for the champion name in the database.
        if Champion.objects.filter(name=name).exists():
            # if name found return not valid new champion
            return JsonResponse({"valid": False}, status=200)
        else:
            # if name not found, then user can create a new champion.
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


def get_graph_data(request):
    if request.is_ajax and request.method == "GET":
        selected_stat = request.GET['selected_stat']
        print('selected_stat:', selected_stat)
        # determine which effect_type to use
        effect_type_objs = EffectType.objects.all()
        selected_effect_type = None
        for effect_type in effect_type_objs:
            if effect_type.name == selected_stat:
                selected_effect_type = effect_type
        # get effects with the selected stat
        same_stat_effect_objs = Effect.objects.filter(effect_type=selected_effect_type)
        # add each individual rank as a separate list element
        same_stat_effects = []
        for sseo in same_stat_effect_objs:
            if '%' in sseo.effect_ranks:
                sseo.effect_ranks = sseo.effect_ranks.replace('%', '')
                ss_effect_values = sseo.effect_ranks.strip().split('/')
                for ev in ss_effect_values:
                    ev = float(ev) / 100
            else:
                ss_effect_values = sseo.effect_ranks.strip().split('/')
                for ev in ss_effect_values:
                    ev = float(ev)
            temp_list = []
            rank_counter = 1
            for item in ss_effect_values:
                temp_list.append(
                    [sseo.effect_ability_name + ': ' + sseo.effect_name + 'Lv' + str(rank_counter), item])
                # temp_list.append(['', item])
                rank_counter += 1
            same_stat_effects.extend(temp_list)
        print('same_stat_effects:', same_stat_effects)
        x_data = []
        y_data = []
        # sort the stat list
        print('BEFORE: same_stat_effects:', same_stat_effects)
        same_stat_effects.sort(key=lambda x: float(x[1]))
        for dp in same_stat_effects:
            x_data.append(dp[0])
            y_data.append(dp[1])
        print('AFTER: xy_data:', same_stat_effects)
        print('x_data:', x_data)
        print('y_data:', y_data)
        # make a graph object and return it.
        # make bar chart
        plot_div = plot([go.Bar(x=x_data,
                                y=y_data,
                                name='test',
                                opacity=0.8,
                                marker_color='blue')],
                        output_type='div')
        return JsonResponse({"valid": True, "x_data": x_data, "y_data": y_data, "plot_divider": plot_div},
                            status=200)
    return JsonResponse({}, status=400)


def get_simulation_results(request):
    # print('simulation request')
    if request.is_ajax and request.method == "GET":
        # print('ajax and GET')
        # for k, v in request.GET.items():
        #     print(f'key:{k}:, value:{v}')

        # retrieve champions 1 and 2
        champion_1_obj = Champion.objects.get(name=request.GET['c1_select_val'])
        champion_2_obj = Champion.objects.get(name=request.GET['c2_select_val'])
        simulation_results = combat_simulation(champion_1_obj, champion_2_obj, request.GET)

        x_data = []
        y_data = []

        # make a graph object and return it.
        for round in simulation_results['round_win_loss']:
            x_data.append(round[0])
            y_data.append(round[1])

        c1_image_path = 'staticfiles/static/images/champion_square_icons/' + request.GET['c1_select_val'].replace(' ',
                                                                                                                  '_') + 'Square.png'
        with open(c1_image_path, "rb") as image_file:
            c1_img = base64.b64encode(image_file.read()).decode('utf-8')
        c2_image_path = 'staticfiles/static/images/champion_square_icons/' + request.GET['c2_select_val'].replace(' ',
                                                                                                                  '_') + 'Square.png'
        with open(c2_image_path, "rb") as image_file:
            c2_img = base64.b64encode(image_file.read()).decode('utf-8')

        # make bar chart
        # +1 for c1 win, -1 for c2 win (y), 0 for draw.
        # number for iteration of simulation
        plot_div = plot([go.Bar(x=x_data,
                                y=y_data,
                                name='test',
                                opacity=0.8,
                                marker_color='blue')],
                        output_type='div')

        return JsonResponse({"valid": True, "plot_divider": plot_div,
                             "simulation_results": simulation_results,
                             "c1_img": c1_img,
                             "c2_img": c2_img},
                            status=200)

    return JsonResponse({}, status=400)


def combat_simulation(champion_a_obj: Champion, champion_b_obj: Champion, fight_settings):
    # contains the final results of the simulation
    simulation_results = {}
    round_win_loss = []

    # simulation champions
    champion_a = SimulationChampion(champion_a_obj)
    champion_b = SimulationChampion(champion_b_obj)

    # effect type category lists. these categorize which abilities are offensive or defensive

    # defensive abilities have cast priority when more than one ability is available for casting.
    offensive_types = ['Attack Damage', 'Physical Damage', 'Magic Damage', 'Mixed Damage', 'Attack Speed']
    defensive_types = ['Total Regen', 'Bonus HP Regen', 'Health', 'Health Regeneration', 'Magic Resistance',
                       'Health Refund', 'Healing %', 'Healing', 'Magic Shield', 'Shield', 'Heal', 'Stun',
                       'Damage Reduction', 'Stasis', 'Attack Speed', 'Mana Restore', 'Taunt', 'Attack Damage Reduction',
                       'Magic Resistance Reduction', 'CDR', 'Ground Duration', 'Slow Duration', 'Bonus AP',
                       'Fear Duration']

    # these lists contain the abilities of the champions.
    champion_a_abilities = [champion_a_obj.ability_q1, champion_a_obj.ability_w1, champion_a_obj.ability_e1,
                            champion_a_obj.ability_r1]
    champion_b_abilities = [champion_b_obj.ability_q1, champion_b_obj.ability_w1, champion_b_obj.ability_e1,
                            champion_b_obj.ability_r1]

    # print('champion_a_abilities:', champion_a_abilities)
    # print('champion_b_abilities:', champion_b_abilities)

    # fight_count
    max_fight_count = 100

    # current_seconds gives the current time of the simulation, used for simulating ability cooldowns and regeneration.
    current_seconds = 0

    # wins
    champion_a_wins = 0
    champion_b_wins = 0
    draw_count = 0

    # win probability
    champion_a_probability = 0
    champion_b_probability = 0

    ability_cast_queue = []
    continue_fight = True
    # action history will contain the HTML divs representing each action taken.
    action_history = []
    # start simulation (outer loop controls how many fights occur in the simulation)
    for i in range(max_fight_count):
        action_history.append(f'''<div class="card card-body">
                                        <h3>Round #{i + 1}</h3>
                                        <hr>''')
        continue_fight = True
        current_seconds = 0
        champion_a = SimulationChampion(champion_a_obj)
        champion_b = SimulationChampion(champion_b_obj)
        # while loop concludes when a winner for the current iteration is determined.
        print(f'''***********ROUND #: {i + 1}/100***************''')
        while continue_fight:
            # print('NEXT LOOP')
            # print(f'''current_seconds: {round(current_seconds, 2)}''')
            # print(f'''{champion_a.name}'s Health: {champion_a.current_health}''')
            # print(f'''{champion_b.name}'s Health: {champion_b.current_health}''')
            # the logic here represents the simulation actions at each time step (0.01 seconds).

            # check for disable/cooldown removal:
            if champion_a.disabled_cd < current_seconds:
                champion_a.disabled = False
                champion_a.disabled_cd = 0
            if champion_b.disabled_cd < current_seconds:
                champion_b.disabled = False
                champion_b.disabled_cd = 0

            # for each ability that is ready for casting, determine the cast order and place into the queue.
            champion_a_abilities_ready = []
            champion_b_abilities_ready = []
            # add champion_a's abilities to the ready list if they are ready.
            if champion_a.q_cd <= current_seconds:
                # print(f"champion_a.q_cd <= current_seconds: {champion_a.q_cd} <= {current_seconds} == {champion_a.q_cd <= current_seconds}")
                champion_a_abilities_ready.append(champion_a_obj.ability_q1)
            if champion_a.w_cd <= current_seconds:
                # print(f"champion_a.w_cd <= current_seconds: {champion_a.w_cd} <= {current_seconds} == {champion_a.w_cd <= current_seconds}")
                champion_a_abilities_ready.append(champion_a_obj.ability_w1)
            if champion_a.e_cd <= current_seconds:
                # print(f"champion_a.e_cd <= current_seconds: {champion_a.e_cd} <= {current_seconds} == {champion_a.e_cd <= current_seconds}")
                champion_a_abilities_ready.append(champion_a_obj.ability_e1)
            if champion_a.r_cd <= current_seconds:
                # print(f"champion_a.r_cd <= current_seconds: {champion_a.r_cd} <= {current_seconds} == {champion_a.r_cd <= current_seconds}")
                champion_a_abilities_ready.append(champion_a_obj.ability_r1)
            # add champion_b's abilities to the ready list if they are ready.
            if champion_b.q_cd <= current_seconds:
                # print(f"champion_b.q_cd <= current_seconds: {champion_b.q_cd} <= {current_seconds} == {champion_b.q_cd <= current_seconds}")
                champion_b_abilities_ready.append(champion_b_obj.ability_q1)
            if champion_b.w_cd <= current_seconds:
                # print(f"champion_b.w_cd <= current_seconds: {champion_b.w_cd} <= {current_seconds} == {champion_b.w_cd <= current_seconds}")
                champion_b_abilities_ready.append(champion_b_obj.ability_w1)
            if champion_b.e_cd <= current_seconds:
                # print(f"champion_b.e_cd <= current_seconds: {champion_b.e_cd} <= {current_seconds} == {champion_b.e_cd <= current_seconds}")
                champion_b_abilities_ready.append(champion_b_obj.ability_e1)
            if champion_b.r_cd <= current_seconds:
                # print(f"champion_b.r_cd <= current_seconds: {champion_b.r_cd} <= {current_seconds} == {champion_b.r_cd <= current_seconds}")
                champion_b_abilities_ready.append(champion_b_obj.ability_r1)

            # print('COOLDOWNS:')
            # print(f'A Q: {champion_a.q_cd}')
            # print(f'A W: {champion_a.w_cd}')
            # print(f'A E: {champion_a.e_cd}')
            # print(f'A R: {champion_a.r_cd}')
            # print(f'B Q: {champion_b.q_cd}')
            # print(f'B W: {champion_b.w_cd}')
            # print(f'B E: {champion_b.e_cd}')
            # print(f'B R: {champion_b.r_cd}')

            # print('champion_a_abilities_ready:', champion_a_abilities_ready)
            # print('champion_b_abilities_ready:', champion_b_abilities_ready)

            # determine cast order of ready abilities and auto attacks.
            while len(champion_a_abilities_ready) > 0 or len(champion_b_abilities_ready) > 0:
                # print(f'len(champion_a_abilities_ready): {len(champion_a_abilities_ready)}')
                # print(f'len(champion_b_abilities_ready): {len(champion_b_abilities_ready)}')
                # if both champions have abilities ready
                if len(champion_a_abilities_ready) > 0 and len(champion_b_abilities_ready) > 0:
                    # print('both have abilities ready')
                    # determine which champion's abilities are removed for this iteration
                    champion_a_roll = random.random() * 100
                    champion_b_roll = random.random() * 100
                    # print(f'A roll: {champion_a_roll}, B roll: {champion_b_roll}')
                    # print(f'Champion A moves first: : {champion_a_roll > champion_b_roll}')
                    # print(f'Champion B moves first: {champion_a_roll < champion_b_roll}')
                    # if they get the same value, reroll.
                    while champion_a_roll == champion_b_roll:
                        champion_a_roll = random.random() * 100
                        champion_b_roll = random.random() * 100
                        # print(f'A re-roll: {champion_a_roll}, B re-roll: {champion_b_roll}')
                        # print(f'Champion A moves first: : {champion_a_roll > champion_b_roll}')
                        # print(f'Champion B moves first: {champion_a_roll < champion_b_roll}')
                    # if champion_a rolled higher, add one of their abilities to the queue.
                    if champion_a_roll > champion_b_roll:
                        # remove the first defensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability = champion_a_abilities_ready[ability_index]
                            if ability.effect1.effect_type in defensive_types:
                                ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                                break
                        # remove the first offensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability = champion_a_abilities_ready[ability_index]
                            if ability.effect1.effect_type in offensive_types:
                                ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                                break
                        # remove all other abilities and add them to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                            break
                    # else if champion_b rolled higher, add one of their abilities to the queue.
                    else:
                        # remove the first defensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability = champion_b_abilities_ready[ability_index]
                            if ability.effect1.effect_type in defensive_types:
                                ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                                break
                        # remove the first offensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability = champion_b_abilities_ready[ability_index]
                            if ability.effect1.effect_type in offensive_types:
                                ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                                break
                        # remove all other abilities and add them to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                            break

                # if only champion_a has abilities ready
                if len(champion_a_abilities_ready) > 0 and len(champion_b_abilities_ready) == 0:
                    # print('only champion a has abilities ready')
                    while len(champion_a_abilities_ready) > 0:
                        # remove the first defensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability = champion_a_abilities_ready[ability_index]
                            if ability.effect1.effect_type in defensive_types:
                                ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                                break
                        # remove the first offensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability = champion_a_abilities_ready[ability_index]
                            if ability.effect1.effect_type in offensive_types:
                                ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                                break
                        # remove all other abilities and add them to the cast queue.
                        for ability_index in range(len(champion_a_abilities_ready)):
                            ability_cast_queue.append(champion_a_abilities_ready.pop(ability_index))
                            break

                # if only champion_b has abilities ready
                if len(champion_b_abilities_ready) > 0 and len(champion_a_abilities_ready) == 0:
                    # print('only champion b has abilities ready')
                    while len(champion_b_abilities_ready) > 0:
                        # remove the first defensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability = champion_b_abilities_ready[ability_index]
                            if ability.effect1.effect_type in defensive_types:
                                ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                                break
                        # remove the first offensive ability if one is found and add it to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability = champion_b_abilities_ready[ability_index]
                            if ability.effect1.effect_type in offensive_types:
                                ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                                break
                        # remove all other abilities and add them to the cast queue.
                        for ability_index in range(len(champion_b_abilities_ready)):
                            ability_cast_queue.append(champion_b_abilities_ready.pop(ability_index))
                            break

            # apply each ability in the cast queue in order with hit probability.
            # print('END OF ABILITY CAST QUEUE APPENDING')
            # if len(ability_cast_queue) > 0:
            #     print(f'[{round(current_seconds, 2)}s]: ability_cast_queue: {ability_cast_queue}')
            while len(ability_cast_queue) > 0:

                # print(f'[{round(current_seconds, 2)}]: ability_cast_queue: {ability_cast_queue}')
                # for ability in ability_cast_queue:
                # print(f'champion_a.disabled == {champion_a.disabled}')
                # print(f'champion_b.disabled == {champion_b.disabled}')
                # print(f"{ability.name} cooldown: {ability.cooldown_ranks.split('/')[-1]}")
                # print('length of ability_cast_queue:', len(ability_cast_queue))
                # print('length of ability_cast_queue > 0:', len(ability_cast_queue) > 0)
                current_ability = ability_cast_queue.pop(0)
                current_ability_position = str(current_ability.ability_position)
                # print('current_ability:', current_ability)
                # print('length of ability_cast_queue after pop:', len(ability_cast_queue))

                # if the current ability belongs to champion a
                if current_ability in champion_a_abilities:
                    # print('the current_ability belongs to champion a')
                    # if the champion is disabled, skip casting
                    if champion_a.disabled:
                        continue
                    # if the champion cooldown is greater than the current seconds, skip casting.
                    if current_ability_position == 'Q' and champion_a.q_cd >= current_seconds:
                        # print('cooldown remaining...', champion_a.q_cd)
                        continue
                    elif current_ability_position == 'W' and champion_a.w_cd >= current_seconds:
                        # print('cooldown remaining...', champion_a.w_cd)
                        continue
                    elif current_ability_position == 'E' and champion_a.e_cd >= current_seconds:
                        # print('cooldown remaining...', champion_a.e_cd)
                        continue
                    elif current_ability_position == 'R' and champion_a.r_cd >= current_seconds:
                        # print('cooldown remaining...', champion_a.r_cd)
                        continue
                    # else cast the ability
                    else:
                        # determine if ability hits
                        roll = random.random() * 100

                        # set minimum roll for the ability
                        min_roll_to_cast = -1
                        if current_ability_position == 'Q':
                            min_roll_to_cast = float(100 - float(fight_settings['c1_q_hit_val']))
                        if current_ability_position == 'W':
                            min_roll_to_cast = float(100 - float(fight_settings['c1_w_hit_val']))
                        if current_ability_position == 'E':
                            min_roll_to_cast = float(100 - float(fight_settings['c1_e_hit_val']))
                        if current_ability_position == 'R':
                            min_roll_to_cast = float(100 - float(fight_settings['c1_r_hit_val']))

                        # apply the ability if it hits
                        if min_roll_to_cast == -1:
                            print(f'the minimum roll was not set for the ability. current_ability_position: {current_ability_position}')
                        elif roll >= min_roll_to_cast:
                            apply_ability_results = apply_ability(champion_a, champion_b, current_ability, action_history, current_seconds)
                            champion_a = apply_ability_results['casting_champion']
                            champion_b = apply_ability_results['defending_champion']
                        # if they miss, the ability still goes on cooldown
                        elif roll < min_roll_to_cast:
                            action_history.append(f'[{round(current_seconds, 2)}s]: {champion_a} missed {current_ability}!<br>')
                            champion_a = apply_ability_cooldown(champion_a, current_ability, current_seconds)
                elif current_ability in champion_b_abilities:
                    # print('the current_ability belongs to champion b')
                    # if the champion is disabled, skip casting
                    if champion_b.disabled:
                        continue
                    # if the ability is on cooldown, skip casting.
                    if current_ability_position == 'Q' and champion_b.q_cd >= current_seconds:
                        # print('cooldown remaining...', champion_b.q_cd)
                        continue
                    elif current_ability_position == 'W' and champion_b.w_cd >= current_seconds:
                        # print('cooldown remaining...', champion_b.w_cd)
                        continue
                    elif current_ability_position == 'E' and champion_b.e_cd >= current_seconds:
                        # print('cooldown remaining...', champion_b.e_cd)
                        continue
                    elif current_ability_position == 'R' and champion_b.r_cd >= current_seconds:
                        # print('cooldown remaining...', champion_b.r_cd)
                        continue
                    # else cast the ability
                    else:
                        # determine if ability hits
                        roll = random.random() * 100

                        # set minimum roll for the ability
                        min_roll_to_cast = -1
                        if current_ability_position == 'Q':
                            min_roll_to_cast = float(100 - float(fight_settings['c2_q_hit_val']))
                        if current_ability_position == 'W':
                            min_roll_to_cast = float(100 - float(fight_settings['c2_w_hit_val']))
                        if current_ability_position == 'E':
                            min_roll_to_cast = float(100 - float(fight_settings['c2_e_hit_val']))
                        if current_ability_position == 'R':
                            min_roll_to_cast = float(100 - float(fight_settings['c2_r_hit_val']))

                        # apply the ability if it hits
                        if min_roll_to_cast == -1:
                            print(f'the minimum roll was not set for the ability. current_ability_position: {current_ability_position}')
                        elif roll >= min_roll_to_cast:
                            apply_ability_results = apply_ability(champion_b, champion_a, current_ability, action_history, current_seconds)
                            champion_b = apply_ability_results['casting_champion']
                            champion_a = apply_ability_results['defending_champion']
                        # if they miss, the ability still goes on cooldown
                        elif roll < min_roll_to_cast:
                            action_history.append(f'[{round(current_seconds, 2)}s]: {champion_b} missed {current_ability}!<br>')
                            champion_b = apply_ability_cooldown(champion_b, current_ability, current_seconds)

                if champion_a.current_health <= 0 and champion_b.current_health <= 0:
                    draw_count += 1
                    continue_fight = False
                    round_win_loss.append((i + 1, 0))
                    action_history.append(f'<b>Round #{i + 1} ended in a draw!</b><br></div>')
                    break
                if champion_a.current_health <= 0:
                    champion_b_wins += 1
                    continue_fight = False
                    round_win_loss.append((i + 1, -1))
                    action_history.append(f'<b>{champion_b.name} wins Round #{i + 1}!</b><br></div>')
                    break
                if champion_b.current_health <= 0:
                    champion_a_wins += 1
                    continue_fight = False
                    round_win_loss.append((i + 1, 1))
                    action_history.append(f'<b>{champion_a.name} wins Round #{i + 1}!</b><br></div>')
                    break

            current_seconds += 0.01

    # determine win probabilities
    print('champion_a_wins:', champion_a_wins)
    print('champion_b_wins:', champion_b_wins)
    champion_a_probability = champion_a_wins / max_fight_count
    champion_b_probability = champion_b_wins / max_fight_count
    print('champion_a_probability:', champion_a_probability)
    print('champion_b_probability:', champion_b_probability)

    # assign simulation results
    simulation_results = {
        'round_win_loss': round_win_loss,
        'champion_a_wins': champion_a_wins,
        'champion_b_wins': champion_b_wins,
        'draw_count': draw_count,
        'champion_a_probability': champion_a_probability,
        'champion_b_probability': champion_b_probability,
        'action_history': action_history
    }

    return simulation_results


def reduce_damage(damage, damage_type, target: SimulationChampion):
    resist = 0
    if damage_type == 'PHYSICAL':
        resist = float(target.current_armor)
    elif damage_type == 'MAGICAL':
        resist = float(target.current_magic_resist)

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


def import_base_stats(body_string, *args, **kwargs):
    # Save a Champion using the base_stats.csv file.
    file_path = os.path.join(os.getcwd(), 'scripts\\base_stats.csv')
    body_string += 'FILE: ' + file_path + '<br>'
    f = open(file_path)
    count = 0
    for line in f:
        if count == 0:
            body_string += 'headers: ' + line + '<br>'
        else:
            parts = line.split(',')
            try:
                obj = Champion(name=parts[0],
                               health=parts[1],
                               health_scaling=parts[2],
                               health_regen=parts[3],
                               health_regen_scaling=parts[4],
                               mana=parts[5],
                               mana_scaling=parts[6],
                               mana_regen=parts[7],
                               mana_regen_scaling=parts[8],
                               attack_damage=parts[9],
                               attack_damage_scaling=parts[10],
                               attack_speed=parts[11],
                               attack_speed_scaling=float(parts[12].replace('%', '')) / 100,
                               armor=parts[13],
                               armor_scaling=parts[14],
                               magic_resist=parts[15],
                               magic_resist_scaling=parts[16],
                               movement_speed=parts[17],
                               range=parts[18])
                obj.save()
            except Exception as e:
                print(e)
                body_string += 'Champion base stats row skipped: ' + parts[0] + '<br>'
        count += 1
    return body_string


def import_from_data_csv(body_string, *args, **kwargs):
    file_path = os.path.join(os.getcwd(), 'scripts\\data.csv')
    parts = None
    champion = None
    ability_position = None
    ability = None
    cost = None
    cost_type = None
    cost2 = None
    cost2_type = None
    max_charges = None
    max_stacks = None
    cooldown = None
    recharge_cooldown = None
    effect_type = None
    effect_name = None
    effect_value = None
    effect_scaling = None
    effect_scaling_type = None
    effect_scaling2 = None
    effect_scaling2_type = None
    body_string += '<br><br>FILE: ' + file_path + '<br>'
    f = open(file_path)
    count = 0
    for line in f:
        if count == 0:
            body_string += 'row: ' + line + '<br>'
        else:
            # LAST EDIT WAS HERE
            line = line.rstrip()
            parts = line.split(',')
            champion = parts[0]
            ability_position = parts[1]
            ability = parts[2]
            cost = parts[3]
            cost_type = parts[4]
            cost2 = parts[5]
            cost2_type = parts[6]
            max_charges = parts[7]
            max_stacks = parts[8]
            cooldown = parts[9]
            recharge_cooldown = parts[10]
            effect_type = parts[11]
            effect_name = parts[12]
            effect_value = parts[13]
            effect_scaling = parts[14]
            effect_scaling_type = parts[15]
            effect_scaling2 = parts[16]
            effect_scaling2_type = parts[17]
            cost = remove_chars(cost, 'abcdefghijklmnopqrstuvwxyz+- ')
            cost2 = remove_chars(cost2, 'abcdefghijklmnopqrstuvwxyz+- ')
            cooldown = remove_chars(cooldown, 'abcdefghijklmnopqrstuvwxyz+- ')
            recharge_cooldown = remove_chars(recharge_cooldown, 'abcdefghijklmnopqrstuvwxyz+- ')
            effect_value = remove_chars(effect_value, 'abcdefghijklmnopqrstuvwxyz+- ')
            effect_scaling = remove_chars(effect_scaling, 'abcdefghijklmnopqrstuvwxyz+- ()')
            effect_scaling2 = remove_chars(effect_scaling2, 'abcdefghijklmnopqrstuvwxyz+- ()')

            # CREATE DATABASE OBJECTS FROM DATA
            champion_obj = None
            ability_obj = None
            effect_obj = None
            cost_type_obj = None
            cost2_type_obj = None
            effect_type_obj = None
            scaling_type_obj = None
            scaling2_type_obj = None
            champion_row = None
            ability_row = None
            effect_rows = None

            # Create Champion
            try:
                body_string += '<br><br>'
                body_string += null_if_html('champion', champion)
                body_string += null_if_html('ability_position', ability_position)
                body_string += null_if_html('ability', ability)
                body_string += null_if_html('cost', cost)
                body_string += null_if_html('cost_type', cost_type)
                body_string += null_if_html('cost2', cost2)
                body_string += null_if_html('cost2_type', cost2_type)
                body_string += null_if_html('max_charges', max_charges)
                body_string += null_if_html('max_stacks', max_stacks)
                body_string += null_if_html('cooldown', cooldown)
                body_string += null_if_html('recharge_cooldown', recharge_cooldown)
                body_string += null_if_html('effect_type', effect_type)
                body_string += null_if_html('effect_name', effect_name)
                body_string += null_if_html('effect_value', effect_value)
                body_string += null_if_html('effect_scaling', effect_scaling)
                body_string += null_if_html('effect_scaling_type', effect_scaling_type)
                body_string += null_if_html('effect_scaling2', effect_scaling2)
                body_string += null_if_html('effect_scaling2_type', effect_scaling2_type)

                champion_obj = Champion(name=champion)
                champion_obj.save()
            except Exception as e:
                print('create champion exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped Champion: ' + champion + '<br>'

            # Create Ability
            try:
                if max_charges == '':
                    max_charges = None
                if max_stacks == '':
                    max_stacks = None

                ability_obj = Ability(name=ability,
                                      ability_position=ability_position,
                                      max_charges=int(max_charges) if max_charges is not None else None,
                                      max_stacks=int(max_stacks) if max_stacks is not None else None,
                                      cooldown_ranks=cooldown,
                                      recharge_cooldown_ranks=recharge_cooldown,
                                      cost_ranks=cost,
                                      cost2_ranks=cost2)
                ability_obj.save()
            except Exception as e:
                print('create ability exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped Ability: '
                body_string += null_if_html('ability', ability)

            # Create Effect
            try:
                effect_obj = Effect(effect_ability_name=ability,
                                    effect_name=effect_name,
                                    effect_ranks=effect_value,
                                    scaling_ranks=effect_scaling,
                                    scaling2_ranks=effect_scaling2)
                effect_obj.save()
            except Exception as e:
                print('create effect exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped Effect: '
                body_string += null_if_html('effect_name', effect_name)

            # Create Cost Types
            try:
                cost_type_obj = CostType(name=cost_type)
                cost_type_obj.save()
            except Exception as e:
                print('create cost exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped CostType: '
                body_string += null_if_html('cost_type', cost_type)
            try:
                cost2_type_obj = CostType(name=cost2_type)
                cost2_type_obj.save()
            except Exception as e:
                print('create cost2 exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped CostType: '
                body_string += null_if_html('cost2_type', cost2_type)

            # Create Effect Type
            try:
                effect_type_object = EffectType(name=effect_type)
                effect_type_object.save()
            except Exception as e:
                print('create effect type exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                body_string += 'Skipped EffectType: '
                body_string += null_if_html('effect_type', effect_type)

                # Create Scaling Types
                try:
                    scaling_type_obj = ScalingType(name=effect_scaling_type)
                    scaling_type_obj.save()
                except Exception as e:
                    print('create scaling type exception:', e)
                    body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                    body_string += 'Skipped ScalingType: '
                    body_string += null_if_html('effect_scaling_type', effect_scaling_type)
                try:
                    scaling2_type_obj = ScalingType(name=effect_scaling2_type)
                    scaling2_type_obj.save()
                except Exception as e:
                    print('create scaling2 type exception:', e)
                    body_string += f'''<p style="background-color: red;">{e}<p> <br>'''
                    body_string += 'Skipped ScalingType: '
                    body_string += null_if_html('effect_scaling2_type', effect_scaling2_type)

            # LINK OBJECTS THAT WERE JUST CREATED.

            # Link to Champions
            print('\nBEGIN LINKING DATA')
            try:
                champion_row = Champion.objects.get(name=champion)
                ability_row = Ability.objects.get(name=ability)
                print('ability_row:', ability_row)
                if ability_position == 'Q':
                    champion_row.ability_q1 = ability_row
                    champion_row.ability_q1.save()
                if ability_position == 'W':
                    champion_row.ability_w1 = ability_row
                    champion_row.ability_w1.save()
                if ability_position == 'E':
                    champion_row.ability_e1 = ability_row
                    champion_row.ability_e1.save()
                if ability_position == 'R':
                    champion_row.ability_r1 = ability_row
                    champion_row.ability_r1.save()
                if ability_position == 'Q2':
                    champion_row.ability_q2 = ability_row
                    champion_row.ability_q2.save()
                if ability_position == 'W2':
                    champion_row.ability_w2 = ability_row
                    champion_row.ability_w2.save()
                if ability_position == 'E2':
                    champion_row.ability_e2 = ability_row
                    champion_row.ability_e2.save()
                if ability_position == 'R2':
                    champion_row.ability_r2 = ability_row
                    champion_row.ability_r2.save()
                # Save champion after it's abilities are saved.
                champion_row.save()
            except Exception as e:
                print('link to champion exception:', e)
                body_string += f'''<p style="background-color: red;">{e}<p> <br>'''

            # Link to Abilities
            try:
                # Link Ability to Effect
                ability_row = Ability.objects.get(name=ability)
                effect_rows = Effect.objects.filter(effect_ability_name=ability)

                # print('effect_rows:', effect_rows)
                try:
                    ability_row.effect1 = effect_rows[0]
                    ability_row.effect1.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[0]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect2 = effect_rows[1]
                    ability_row.effect2.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[1]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect3 = effect_rows[2]
                    ability_row.effect3.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[2]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect4 = effect_rows[3]
                    ability_row.effect4.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[3]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect5 = effect_rows[4]
                    ability_row.effect5.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[4]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect6 = effect_rows[5]
                    ability_row.effect6.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[5]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect7 = effect_rows[6]
                    ability_row.effect7.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[6]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect8 = effect_rows[7]
                    ability_row.effect8.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[7]}')
                except Exception as e:
                    print('link to ability exception:', e)
                try:
                    ability_row.effect9 = effect_rows[8]
                    ability_row.effect9.save()
                    # print(f'#{ability_row.id}: [{ability_position}]: Ability:{ability_row}, Effect:{effect_rows[8]}')
                except Exception as e:
                    print('link to ability exception:', e)

                # Link Ability to CostType
                ability_row.cost_type = CostType.objects.get(name=cost2_type)
                ability_row.cost_type.save()
                ability_row.cost2_type = CostType.objects.get(name=cost2_type)
                ability_row.cost2_type.save()
            except Exception as e:
                print('link to ability exception:', e)
                pass

            # Link to Effects
            print('effect_rows:', effect_rows)
            for effect_row in effect_rows:
                # Link Effect to EffectType
                try:
                    print('effect_type:', effect_type)
                    effect_row.effect_type = EffectType.objects.get(name=effect_type)
                    print('effect_type_obj:', EffectType.objects.get(name=effect_type))
                    effect_row.effect_type.save()
                except Exception as e:
                    print('link to effect exception (effect type exception):', e)
                try:
                    print('effect_scaling_type:', effect_scaling_type)
                    effect_row.scaling_type = ScalingType.objects.get(name=effect_scaling_type)
                    print('effect_scaling_type_obj:', ScalingType.objects.get(name=effect_scaling_type))
                    effect_row.scaling_type.save()
                except Exception as e:
                    print('link to effect exception: (scaling type exception)', e)
                try:
                    print('effect_scaling2_type:', effect_scaling2_type)
                    effect_row.scaling2_type = ScalingType.objects.get(name=effect_scaling2_type)
                    print('effect_scaling2_type_obj:', ScalingType.objects.get(name=effect_scaling2_type))
                    effect_row.scaling2_type.save()
                except Exception as e:
                    print('link to effect exception: (scaling2 type exception)', e)
                try:
                    effect_row.save()
                except Exception as e:
                    print('link to effect exception:', e)

            # Save ability after it's effects are saved.
            # print('BEFORE SAVE')
            # print('champion_row: ', champion_row)
            # print('ability_row:', ability_row)
            # print('champion:', champion)
            # print('ability:', ability)
            ability_row.save()

        count += 1
    return body_string


def apply_ability(casting_champion: SimulationChampion, defending_champion: SimulationChampion, ability: Ability, action_history, current_seconds):
    effects = [ability.effect1,
               ability.effect2,
               ability.effect3,
               ability.effect4,
               ability.effect5,
               ability.effect6,
               ability.effect7,
               ability.effect8,
               ability.effect9]
    for effect in effects:
        if effect is None:
            continue
        # get value, scaling, and scaling2 ranks, else give default.
        value = 0
        scaling = 1
        scaling2 = 1
        effect_ranks = effect.effect_ranks.replace('\'', '')
        scaling_ranks = effect.scaling_ranks.replace('\'', '')
        scaling2_ranks = effect.scaling2_ranks.replace('\'', '')
        if effect_ranks != '':
            if '%' in effect_ranks:
                value = float(effect_ranks.replace('%', '').split('/')[-1]) / 100
            else:
                value = float(effect_ranks.split('/')[-1])
        if scaling_ranks != '':
            if '%' in scaling_ranks:
                scaling = float(scaling_ranks.replace('%', '').split('/')[-1]) / 100
            else:
                scaling = float(scaling_ranks)
        if scaling2_ranks != '':
            if '%' in scaling2_ranks:
                scaling2 = float(scaling2_ranks.replace('%', '').split('/')[-1]) / 100
            else:
                scaling2 = float(scaling2_ranks.split('/')[-1])

        # determine ability use based on effect type:
        # current_ability_effect_type = current_ability.
        # Types:
        # Damage
        """
        Physical Damage
        Magic Damage
        """
        # if the effect is magic damage
        effect_type = effect.effect_type.name
        if effect_type == 'Magic Damage':
            damage_amount = value
            # apply scaling values
            damage_amount = determine_scaling_bonus(casting_champion, defending_champion, damage_amount, scaling,
                                                    effect.scaling_type)
            damage_amount = determine_scaling_bonus(casting_champion, defending_champion, damage_amount, scaling2,
                                                    effect.scaling2_type)
            # apply damage
            damage_to_apply = reduce_damage(damage_amount, 'MAGICAL', defending_champion)
            # apply damage to magic shield first
            if defending_champion.magic_shield < damage_to_apply:
                defending_champion.magic_shield = 0
                damage_to_apply -= defending_champion.magic_shield
            else:
                defending_champion.magic_shield -= damage_to_apply
                damage_to_apply = 0
            # apply damage to shield second
            if defending_champion.shield < damage_to_apply:
                defending_champion.shield = 0
                damage_to_apply -= defending_champion.shield
            else:
                defending_champion.shield -= damage_to_apply
                damage_to_apply = 0
            # apply damage to health 3rd
            defending_champion.current_health -= damage_to_apply
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} hit {defending_champion.name} for {round(damage_to_apply)} damage with {ability.name}!<br>''')

        if effect_type == 'Physical Damage':
            # apply scaling values
            damage_amount = value
            # print('damage_amount:', damage_amount)
            damage_amount = determine_scaling_bonus(casting_champion, defending_champion, damage_amount, scaling,
                                                    effect.scaling_type)
            # print('damage_amount:', damage_amount)
            damage_amount = determine_scaling_bonus(casting_champion, defending_champion, damage_amount, scaling2,
                                                    effect.scaling2_type)
            # print('damage_amount:', damage_amount)
            # apply damage
            damage_to_apply = reduce_damage(damage_amount, 'PHYSICAL', defending_champion)
            # print('damage_to_apply:', damage_to_apply)
            # apply damage to shield first
            if defending_champion.shield < damage_to_apply:
                defending_champion.shield = 0
                damage_to_apply -= defending_champion.shield
            else:
                defending_champion.shield -= damage_to_apply
                damage_to_apply = 0
            # apply damage to health after shield
            # print('defending_champion.current_health BEFORE:', defending_champion.current_health)
            defending_champion.current_health -= damage_to_apply
            # print('defending_champion.current_health AFTER:', defending_champion.current_health)
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} hit {defending_champion.name} for {round(damage_to_apply)} damage with {ability.name}!<br>''')

        # Ability Crowd Control
        """
        Fear Duration
        Stun Duration
        Charm Duration
        """
        if effect_type == 'Fear Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.disabled = True
            defending_champion.disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} feared {defending_champion.name} for {round(duration)} seconds!<br>''')
        if effect_type == 'Stun Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.disabled = True
            defending_champion.disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} stunned {defending_champion.name} for {round(duration)} seconds!<br>''')
        if effect_type == 'Charm Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.disabled = True
            defending_champion.disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} charmed {defending_champion.name} for {round(duration)} seconds!<br>''')
        # Movement Crowd Control
        """
        Ground Duration
        Slow Duration
        Root Duration
        """
        if effect_type == 'Ground Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.movement_disabled = True
            defending_champion.movement_disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} grounded {defending_champion.name} for {round(duration)} seconds!<br>''')
        if effect_type == 'Slow Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.movement_disabled = True
            defending_champion.movement_disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} slowed {defending_champion.name} for {round(duration)} seconds!<br>''')
        if effect_type == 'Root Duration':
            duration = value
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling,
                                               effect.scaling_type)
            duration = determine_scaling_bonus(casting_champion, defending_champion, duration, scaling2,
                                               effect.scaling2_type)
            defending_champion.movement_disabled = True
            defending_champion.movement_disabled_cd = current_seconds + duration
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} rooted {defending_champion.name} for {round(duration)} seconds!<br>''')
        # Self-Buff
        """
        Heal
        Shield
        Magic Shield
        """
        if effect_type == 'Heal':
            heal_amount = value
            heal_amount = determine_scaling_bonus(casting_champion, defending_champion, heal_amount, scaling,
                                                  effect.scaling_type)
            heal_amount = determine_scaling_bonus(casting_champion, defending_champion, heal_amount, scaling2,
                                                  effect.scaling2_type)
            if casting_champion.current_health + heal_amount >= casting_champion.max_health:
                casting_champion.current_health = casting_champion.max_health
            else:
                casting_champion.current_health += heal_amount
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} healed themself for {round(heal_amount)}!<br>''')
        if effect_type == 'Shield':
            shield_amount = value
            shield_amount = determine_scaling_bonus(casting_champion, defending_champion, shield_amount, scaling,
                                                    effect.scaling_type)
            shield_amount = determine_scaling_bonus(casting_champion, defending_champion, shield_amount, scaling2,
                                                    effect.scaling2_type)
            casting_champion.shield = shield_amount
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} shielded themself for {round(shield_amount)}!<br>''')
        if effect_type == 'Magic Shield':
            shield_amount = value
            shield_amount = determine_scaling_bonus(casting_champion, defending_champion, shield_amount, scaling,
                                                    effect.scaling_type)
            shield_amount = determine_scaling_bonus(casting_champion, defending_champion, shield_amount, scaling2,
                                                    effect.scaling2_type)
            if casting_champion.current_health + shield_amount >= casting_champion.max_health:
                casting_champion.current_health = casting_champion.max_health
            else:
                casting_champion.magic_shield = shield_amount
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} magic shielded themself for {round(shield_amount)}!<br>''')
        # Enemy Debuff
        """
        Cripple Amount
        Resist Reduction
        """
        if effect_type == 'Cripple Amount':
            cripple_amount = value
            cripple_amount = determine_scaling_bonus(casting_champion, defending_champion, cripple_amount, scaling,
                                                     effect.scaling_type)
            cripple_amount = determine_scaling_bonus(casting_champion, defending_champion, cripple_amount, scaling2,
                                                     effect.scaling2_type)
            defending_champion.current_attack_speed *= 1 - cripple_amount
            defending_champion.current_movement_speed *= 1 - cripple_amount
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} crippled {defending_champion} for {round(cripple_amount)}!<br>''')
        if effect_type == 'Resist Reduction':
            resist_reduction_amount = value
            resist_reduction_amount = determine_scaling_bonus(casting_champion, defending_champion,
                                                              resist_reduction_amount, scaling,
                                                              effect.scaling_type)
            resist_reduction_amount = determine_scaling_bonus(casting_champion, defending_champion,
                                                              resist_reduction_amount, scaling2,
                                                              effect.scaling2_type)
            defending_champion.current_magic_resist -= resist_reduction_amount
            defending_champion.current_armor -= resist_reduction_amount
            action_history.append(
                f'''[{round(current_seconds, 2)}s] {casting_champion.name} reduced {defending_champion}'s resists by {round(resist_reduction_amount)}!<br>''')

    # set ability cooldowns after ability effect is applied
    casting_champion = apply_ability_cooldown(casting_champion, ability, current_seconds)
    return {'casting_champion': casting_champion, 'defending_champion': defending_champion}


def determine_scaling_bonus(casting_champion: SimulationChampion, defending_champion: SimulationChampion, base_value,
                            scaling_value,
                            scaling_type):
    # print('IN: determine_scaling_bonus')
    if scaling_type is None or scaling_type == '':
        return base_value
    # NOTE: bonus scalings do not take effect because there are no items.
    if scaling_type == "% of target's maximum health":
        base_value += float(defending_champion.max_health) * (1 + scaling_value)
    if scaling_type == "% per 100 AP of target's maximum health":
        base_value += float(defending_champion.max_health) * (
                1 + (float(casting_champion.current_ability_power) // 100))
    if scaling_type == "% total magic resistance" or scaling_type == "% magic resist":
        base_value += scaling_value * float(casting_champion.current_magic_resist)
    if scaling_type == "% total armor" or scaling_type == "% armor":
        base_value += scaling_value * float(casting_champion.current_armor)
    if scaling_type == "% of missing mana":
        base_value += scaling_value * (float(casting_champion.max_mana) - float(casting_champion.current_mana))
    if scaling_type == "% per 100 AP":
        base_value += scaling_value * (float(casting_champion.current_ability_power) // 100)
    if scaling_type == "% maxmimum health" or scaling_type == "% of his maximum health" or scaling_type == "% of maximum health":
        base_value += scaling_value * float(casting_champion.max_health)
    if scaling_type == "% of target's current health":
        base_value += scaling_value * float(defending_champion.current_health)
    if scaling_type == "% AD" or scaling_type == "% AD Attack damage modified physical damage":
        base_value += scaling_value * float(casting_champion.current_attack_damage)
    if scaling_type == "% AP":
        base_value += scaling_value * float(casting_champion.current_ability_power)
    return base_value


def apply_ability_cooldown(champion: SimulationChampion, ability: Ability, current_seconds):
    if ability.cooldown_ranks.split('/')[-1] == '':
        new_cd = current_seconds + 10
    else:
        new_cd = current_seconds + float(ability.cooldown_ranks.split('/')[-1])
    if ability.ability_position == 'Q':
        champion.q_cd = new_cd
    if ability.ability_position == 'W':
        champion.w_cd = new_cd
    if ability.ability_position == 'E':
        champion.e_cd = new_cd
    if ability.ability_position == 'R':
        champion.r_cd = new_cd
    return champion
