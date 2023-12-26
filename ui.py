import pygame
import sys
from tracker import pokemon
from tracker import get_possible_options
import requests
from io import BytesIO
import get_source_files
import create_data_files

pygame.init()
pygame.display.set_caption('Pokemon Go Energy Tracker')
colors = {"poison": "#bb62d0", "normal": "#939ba1", "psychic": "#f97277", "rock": "#cabb8c", "steel": "#53899d", "water": "#5399d8",
          "fire": "#ff9f53", "flying": "#95aedd", "ghost": "#535fa2", "grass": "#5ab560", "ground": "#b97046", "ice": "#7bd2c6",
          "bug": "#a5c731", "dark": "#646475", "dragon": "#0775bf", "electric": "#f6da57", "fairy": "#ef9ce2", "fighting": "#d8435d",
          }

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
font20 = pygame.font.SysFont('Comic Sans MS', 22)
font35 = pygame.font.SysFont('Comic Sans MS', 40)
font15 = pygame.font.SysFont('Comic Sans MS', 15)
font60 = pygame.font.SysFont('Comic Sans MS', 60)


red = [255, 0, 0]
black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]
shade1 = [0, 0, 0, 60]
shade2 = [0, 0, 0, 130]
shade3 = [0, 0, 0, 180]
q = 0
e = 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode([1700, 800])
screen.fill(black)

def draw_pokemons():
    for i, mon in enumerate(pokemons):
        if mon:

            draw_border(mon.types, i)
            mon.content = draw_pokemon_image(i, mon.id, mon.name, mon.content)
            draw_pokemon_name(i, mon.name, mon.types[0])
            draw_fast_move(i, mon.fastMoves)
            draw_energy_amount(i, mon.energy)
            draw_charged_moves(i, mon.fastMoves, mon.chargedMoves, mon.energy)

        else:
            if pokemon_pointer != i or user_text == "":
                draw_none_mon(i)
def draw_border(types, index):
    pygame.draw.rect(screen, colors[types[0]], (100 + 400 * index, 100, 300, 600), 20)
    pygame.draw.rect(screen, colors[types[1]] if types[1] != "none" else colors[types[0]], (120 + 400 * index, 120, 260, 560), 20)
    pygame.draw.rect(screen, black, (140 + 400 * index, 140, 220, 520))
def draw_none_mon(index):
    pygame.draw.rect(screen, white, (100 + 400 * index, 100, 300, 600))
    text = my_font.render('Enter Pokemon!', False, black)
    screen.blit(text, (center_pos(100 + 400 * index, 300, text.get_rect().width), 120))
def draw_pointer(index):
    for i in range(3):
        pygame.draw.rect(screen, green if i == index else black, (85 + 400 * i, 85, 330, 630), 10)
def center_pos(starting, rect_len, word_len):
    return (rect_len - word_len) // 2 + starting
def draw_options(starting_text, index, max_rows=13):
    pygame.draw.rect(screen, white, (100 + 400 * index, 100, 300, 600))

    options = get_possible_options(starting_text)
    if options:
        pygame.draw.rect(screen, yellow, (100 + 400 * index, 110 + 45 * option_pointer, 300, 45))
    for j, option in enumerate(options):
        if j < max_rows:
            text = my_font.render(option, False, black)
            screen.blit(text, (center_pos(100 + 400 * index, 300, text.get_rect().width), 110 + 45 * j))

    return options
def draw_pokemon_image(index, mon_id, name, content):
    mon_id = str(mon_id).zfill(3)
    if name[-1] == ")":
        if name[-10:] == "(Galarian)":
            mon_id = mon_id + "-Galar"
        if name[-9:] == "(Hisuian)":
            mon_id = mon_id + "-Hisui"
        if name[-6:] == "(Mega)":
            mon_id = mon_id + "-Mega"
        if name[-8:] == "(Alolan)":
            mon_id = mon_id + "-Alola"
        if name[-9:] == "(Defense)":
            mon_id = mon_id + "-Defense"

    if content:
        image = pygame.image.load(BytesIO(content))
    else:
        try:
            response = requests.get(f'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/images/{mon_id}.png')
            content = response.content
            image_data = BytesIO(content)
            image = pygame.image.load(image_data)
        except:
            response = requests.get(f'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/images/352.png')
            content = response.content
            image_data = BytesIO(content)
            image = pygame.image.load(image_data)
    scaled_image = pygame.transform.scale(image, (150, 150))
    screen.blit(scaled_image, (center_pos(100 + 400 * index, 300, scaled_image.get_rect().width), 150))
    return content
def draw_pokemon_name(index, name, typ):
    name_list = name.split()
    for j, str1 in enumerate(name_list):
        text = my_font.render(str1, False, colors[typ])
        screen.blit(text, (center_pos(100 + 400 * index, 300, text.get_rect().width), 300 + 37 * j))
def draw_fast_move(index, fast_moves):
    fm = fast_moves[0]
    name, typ = fm["name"], fm["type"]
    text = my_font.render(name, False, colors[typ])
    text_width = text.get_rect().width
    pygame.draw.rect(screen, colors[typ], (center_pos(100, 300, text_width + 20) + 400 * index, 385, text_width + 20, 50), 5)
    screen.blit(text, (center_pos(100 + 400 * index, 300, text_width), 388))
def draw_energy_amount(index, energy):
    if e == 0:
        pygame.draw.rect(screen, black,  (150 + 400 * index, 445, 200, 40))
        text = my_font.render(f'Energy: {energy}', False, white)
        screen.blit(text, (center_pos(100 + 400 * index, 300, text.get_rect().width), 440))
def draw_charged_moves(index, fast_moves, charged_moves, energy):
    cms = charged_moves[:2]
    for i, cm in enumerate(cms):
        name, typ = cm["name"], cm["type"]
        draw_charged_move_names(name, typ, index, i)
        pygame.draw.circle(screen, colors[typ], (200 + 100 * i + 400 * index, 530), 36)
        draw_charged_move_percentage(index, i, cm["energy"], energy)
        draw_number_on_charged_move(index, i, fast_moves[0]["energy"], cm["energy"], energy)
    for i, cm in enumerate(cms):
        draw_charged_move_border(index, i, energy)
def draw_charged_move_names(name, typ, pokemon_i, move_i):
    names = name.split()
    for j, name in enumerate(names):
        text = font20.render(name, False, colors[typ])
        screen.blit(text, (center_pos(200 + 100 * move_i + 400 * pokemon_i, 0, text.get_rect().width), 575 + j * 25))
def draw_number_on_charged_move(pokemon_i, move_i, fm_energy, cm_energy, energy):
    a = [(cm_energy * i - energy - 1) // fm_energy + 1 for i in range(1, 4)]
    for i, item in enumerate(a):
        if item < 0:
            a[i] = 0
    if q == 1:
        a[2] = a[2] - a[1]
        a[1] = a[1] - a[0]
    main_text = font35.render(str(a[0]), False, black)
    screen.blit(main_text, (center_pos(200 + 100 * move_i + 400 * pokemon_i, 0, main_text.get_rect().width) - 8 + q * (q - 1) * 4, 500))
    if q != 2:
        sub_text = font15.render(f'({str(a[1])})', False, black)
        screen.blit(sub_text, (center_pos(200 + 100 * move_i + 400 * pokemon_i, 0, sub_text.get_rect().width) + 16, 525))
def draw_charged_move_percentage(pokemon_i, move_i, cm_energy, energy):
    surface = pygame.Surface([1300, 800], pygame.SRCALPHA)

    shade = shade1
    percentage = energy / cm_energy
    if percentage >= 2:
        pygame.draw.rect(surface, shade2, (160 + 100 * move_i + 400 * pokemon_i, 490, 80, 80))
        shade = shade3
    elif percentage >= 1:
        pygame.draw.rect(surface, shade1, (160 + 100 * move_i + 400 * pokemon_i, 490, 80, 80))
        shade = shade2
    height = round(percentage % 1, 3) * 80
    pygame.draw.rect(surface, shade, (160 + 100 * move_i + 400 * pokemon_i, 490 + 80 - height, 80, height))
    screen.blit(surface, (0, 0))
def draw_charged_move_border(pokemon_i, move_i, energy):
    if energy == 100:
        pygame.draw.circle(screen, black, (200 + 100 * move_i + 400 * pokemon_i, 530), 37, 3)
        pygame.draw.circle(screen, white, (200 + 100 * move_i + 400 * pokemon_i, 530), 40, 9)
    else:
        pygame.draw.circle(screen, white, (200 + 100 * move_i + 400 * pokemon_i, 530), 40, 5)
def draw_fast_move_input():
    mon_name = pokemons[pokemon_pointer].name
    mon_type_color = colors[pokemons[pokemon_pointer].types[0]]
    mon_fast_move_color = colors[pokemons[pokemon_pointer].fastMoves[0]["type"]]
    if user_fast_moves == 0:
        text = font35.render(f"ENTER the amount of fast moves done by", False, red)
        text2 = font35.render(mon_name, False, mon_type_color)
        starting_x = center_pos(0, 1300, text.get_rect().width + text2.get_rect().width)
        screen.blit(text, (starting_x, 15))
        screen.blit(text2, (starting_x + text.get_rect().width + 16, 15))
    else:
        text = font60.render(str(user_fast_moves), False, mon_fast_move_color)
        screen.blit(text, (center_pos(0, 1300, text.get_rect().width), 0))
def draw_user_text_input():
    text = font35.render(user_text, False, red)
    screen.blit(text, (center_pos(0, 1300, text.get_rect().width), 15))
def draw_pokemon_is_throwing():
    mon = pokemons[pokemon_pointer]
    if mon.energy >= mon.lowestRequiredEnergy:
        mon_name = mon.name
        mon_type_color = colors[mon.types[0]]
        text = font35.render(mon_name, False, mon_type_color)
        text2 = font35.render('is throwing a Charged Move! press SPACE', False, red)
        starting_x = center_pos(0, 1300, text.get_rect().width + text2.get_rect().width)
        screen.blit(text, (starting_x, 720))
        screen.blit(text2, (starting_x + text.get_rect().width + 16, 720))
def draw_throwing_menu(mon_name, mon_type, charged_moves, thrown_moves, energy, move_pointer):
    draw_cover(2)
    pygame.draw.rect(screen, red, (300, 200, 700, 400))
    pygame.draw.rect(screen, black, (300 + 5, 205, 690, 390))
    pygame.draw.rect(screen, red, (300 + 15, 215, 670, 370), 5)
    text = font35.render(f'{mon_name} is throwing:', False, colors[mon_type])
    screen.blit(text, (center_pos(300, 700, text.get_rect().width), 245))

    relevant_moves = []
    if len(thrown_moves) == 2:
        relevant_moves = [move for move in thrown_moves if move["energy"] <= energy]
    else:
        relevant_moves = [move for move in charged_moves if move["energy"] <= energy]
    for i, cm in enumerate(relevant_moves):
        name = cm["name"]
        color = colors[cm["type"]]
        if cm in charged_moves[:2]:
            pygame.draw.circle(screen, color, (400 + i * 120, 380), 50)
            pygame.draw.circle(screen, white, (400 + i * 120, 380), 50, 5)
            if i == move_pointer:
                pygame.draw.circle(screen, green, (400 + i * 120, 380), 58, 5)
            names = name.split()
            for j, name in enumerate(names):
                text = my_font.render(name, False, color)
                screen.blit(text, (center_pos(400 + i * 120, 0, text.get_rect().width), 435 + j * 32))

        else:
            pygame.draw.circle(screen, color, (500 + i * 70, 380), 30)
            pygame.draw.circle(screen, white, (500 + i * 70, 380), 30, 5)
            if i == move_pointer:
                pygame.draw.circle(screen, green, (500 + i * 70, 380), 37, 4)
            names = name.split()
            for j, name in enumerate(names):
                text = font15.render(name, False, color)
                screen.blit(text, (center_pos(500 + i * 70, 0, text.get_rect().width), 412 + j * 16))
    return relevant_moves
def draw_cover(level):
    if level == 1:
        pygame.draw.rect(screen, black, (0, 0, 1300, 82))
    elif level == 2:
        pygame.draw.rect(screen, black, (0, 718, 1300, 82))
    elif level == 3:
        pygame.draw.rect(screen, black, (0, 0, 1300, 82))
        pygame.draw.rect(screen, black, (0, 718, 1300, 82))
def draw_timer(timer_seconds):
    if int(timer_seconds) == 0:
        pygame.draw.rect(screen, black, (1350, 665, 200, 85))
        return 60
    color = white
    timer_seconds -= clock.get_rawtime() / 1000.0
    if timer_seconds <= 5:
        color = red
    timer_text = font60.render(f'0:{str(int(timer_seconds)).rjust(2, '0')}', True, color)
    pygame.draw.rect(screen, color, (1350, 665, 200, 85))
    pygame.draw.rect(screen, black, (1355, 670, 190, 75))
    screen.blit(timer_text, (center_pos(1350, 200, timer_text.get_rect().width), 665))
    return timer_seconds
def draw_menu():
    texts = ['developed by barthegamer',
             'M - start a new game',
             'R - reset the current pokemon',
             'E - hide / show energy',
             'F - change the current fast move',
             'Z - drain the current pokemon energy',
             'C - change the first charged move',
             'B - change the second charged move',
             'Q - change the charged move format',
             'T - start a 59 seconds timer',
             '0-9 - enter the amount of fast moves']
    for i, text in enumerate(texts):
        text_td = font20.render(text, False, white)
        screen.blit(text_td, (1250, 100 + 50 * i))

# default settings
pokemons = [None for i in range(3)]
pokemon_pointer = 0
option_pointer = 0
mon_options = []
user_text = ""
user_fast_moves = 0
throwing = False
move_pointer = 0
available_moves = None
timer_seconds = 60

running = True
while running:
    clock.tick()
    x, y = pygame.mouse.get_pos()
    #print(x, y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not throwing:
                if event.key == pygame.K_LEFT and pokemon_pointer >= 1:
                    pokemon_pointer -= 1
                    draw_cover(3)
                if event.key == pygame.K_RIGHT and pokemon_pointer <= 1:
                    pokemon_pointer += 1
                    draw_cover(3)
                if pokemons[pokemon_pointer] == None:
                    draw_cover(3)
                    if user_text != "":
                        if event.key == pygame.K_RETURN:
                            pokemons[pokemon_pointer] = pokemon(mon_options[option_pointer])
                            user_text = ""
                            option_pointer = 0
                        if event.key == pygame.K_DOWN and option_pointer <= 11 and option_pointer < len(mon_options) - 1:
                            option_pointer += 1
                        if event.key == pygame.K_UP and option_pointer >= 1:
                            option_pointer -= 1

                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]

                    else:
                        if event.unicode >= 'A' and event.unicode <= 'z':
                            user_text += event.unicode
                else:
                    mon = pokemons[pokemon_pointer]
                    if event.unicode.lower() == 'm':
                        pokemons = [None for i in range(3)]
                        timer_seconds = 60
                        screen.fill(black)
                    if event.unicode.lower() == 'r':
                        pokemons[pokemon_pointer] = None
                        draw_cover(3)
                    if event.unicode.lower() == 'e':
                        e = (e + 1) % 2
                    if event.unicode.lower() == 't':
                        timer_seconds = 59
                    if event.unicode.lower() == 'q':
                        q = (q + 1) % 3
                    if event.unicode.lower() == 'f':
                        pygame.draw.rect(screen, black, (140 + 400 * pokemon_pointer, 385, 220, 50))
                        mon.change_fast_moves_order()
                    if event.unicode.lower() == 'b' and mon.chargedMoves[1] not in mon.thrownChargedMoves:
                        pygame.draw.rect(screen, black, (140 + 400 * pokemon_pointer, 577, 220, 68))
                        mon.change_2nd_cm()
                    if event.unicode.lower() == 'z':
                        mon.energy = 0
                    if event.unicode.lower() == 'c' and mon.chargedMoves[0] not in mon.thrownChargedMoves:
                        pygame.draw.rect(screen, black, (140 + 400 * pokemon_pointer, 577, 220, 68))
                        mon.change_1st_cm()
                    if event.unicode >= '0' and event.unicode <= '9':
                        user_fast_moves = user_fast_moves * 10 + int(event.unicode)
                        draw_cover(1)
                    if event.key == pygame.K_BACKSPACE:
                        user_fast_moves = user_fast_moves // 10
                        draw_cover(1)
                    if event.key == pygame.K_RETURN:
                        if user_fast_moves > 0:
                            mon.update_energy(user_fast_moves)
                            user_fast_moves = 0
                            draw_cover(3)
                    if event.key == pygame.K_SPACE:
                        if mon.energy >= mon.lowestRequiredEnergy:
                            throwing = True
                            available_moves = draw_throwing_menu(mon.name, mon.types[0], mon.chargedMoves, mon.thrownChargedMoves, mon.energy, move_pointer)
            else:
                mon = pokemons[pokemon_pointer]
                if event.key == pygame.K_LEFT and move_pointer >= 1:
                    move_pointer -= 1
                    draw_throwing_menu(mon.name, mon.types[0], mon.chargedMoves, mon.thrownChargedMoves, mon.energy, move_pointer)
                if event.key == pygame.K_RIGHT and move_pointer < len(available_moves) - 1:
                    move_pointer += 1
                    draw_throwing_menu(mon.name, mon.types[0], mon.chargedMoves, mon.thrownChargedMoves, mon.energy, move_pointer)
                if event.unicode.lower() == 'r':
                    throwing = False
                    screen.fill(black)
                if event.key == pygame.K_RETURN:
                    move = available_moves[move_pointer]
                    mon.energy -= move["energy"]
                    if move not in mon.thrownChargedMoves:
                        mon.thrownChargedMoves.append(move)
                    if move not in mon.chargedMoves[:2]:
                        mon.change_relevant_cm()
                    throwing = False
                    move_pointer = 0
                    screen.fill(black)

    if not throwing:
        draw_pokemons()
        draw_pointer(pokemon_pointer)
        if user_text != "":
            mon_options = draw_options(user_text, pokemon_pointer)
        if pokemons[pokemon_pointer] != None:
            draw_fast_move_input()
            draw_pokemon_is_throwing()
        else:
            draw_user_text_input()
            user_fast_moves = 0
    else:
        pass
    if timer_seconds < 60:
        timer_seconds = draw_timer(timer_seconds)
    draw_menu()
    pygame.display.flip()

pygame.quit()