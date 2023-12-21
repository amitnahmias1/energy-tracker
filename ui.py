import pygame
import sys
from tracker import pokemon
from tracker import get_possible_options
import requests
from io import BytesIO

pygame.init()
colors = {"poison": "#bb62d0", "normal": "#939ba1", "psychic": "#f97277", "rock": "#cabb8c", "steel": "#53899d", "water": "#5399d8",
          "fire": "#ff9f53", "flying": "#95aedd", "ghost": "#535fa2", "grass": "#5ab560", "ground": "#b97046", "ice": "#7bd2c6",
          "bug": "#a5c731", "dark": "#646475", "dragon": "#0775bf", "electric": "#f6da57", "fairy": "#ef9ce2", "fighting": "#d8435d",
          }

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
yellow = [255, 255, 0]


screen = pygame.display.set_mode([1300, 800])
screen.fill(black)

def draw_pokemons():
    for i, mon in enumerate(pokemons):
        if mon:
            if screen.get_at((101 + 400 * i, 101)) == (255, 255, 255, 255):
                draw_border(mon.types, i)

            if not mon.isImagePulled:
                draw_pokemon_image(i, mon.id, mon.name)
                mon.isImagePulled = True

            draw_pokemon_name(i, mon.name, mon.types[0])
            draw_fast_move(i, mon.fastMoves)

        else:
            if pokemon_pointer != i or user_text == "":
                draw_none_mon(i)
def draw_border(types, index):
    pygame.draw.rect(screen, colors[types[0]], (100 + 400 * index, 100, 300, 600), 20)
    pygame.draw.rect(screen, colors[types[1]] if types[1] != "none" else colors[types[0]], (120 + 400 * index, 120, 260, 560), 20)
    pygame.draw.rect(screen, black, (140 + 400 * index, 140, 220, 520))

    pygame.display.flip()
def draw_none_mon(index):
    pygame.draw.rect(screen, white, (100 + 400 * index, 100, 300, 600))
    text = my_font.render('Enter Pokemon!', False, black)
    screen.blit(text, (center_pos(100 + 400 * index, 300, text.get_rect().width), 120))
def draw_pointer(index):
    for i in range(3):
        pygame.draw.rect(screen, green if i == index else black, (85 + 400 * i, 85, 330, 630), 10)
    pygame.display.flip()
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
def draw_pokemon_image(index, mon_id, name):
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
    try:
        response = requests.get(f'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/images/{mon_id}.png')
        image_data = BytesIO(response.content)
        image = pygame.image.load(image_data)
    except:
        response = requests.get(f'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/images/352.png')
        image_data = BytesIO(response.content)
        image = pygame.image.load(image_data)
    scaled_image = pygame.transform.scale(image, (150, 150))
    screen.blit(scaled_image, (center_pos(100 + 400 * index, 300, scaled_image.get_rect().width), 150))
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
    pygame.draw.rect(screen, colors[typ], (center_pos(100, 300, text_width + 30) + 400 * index, 385, text_width + 30, 50), 5)
    screen.blit(text, (center_pos(100 + 400 * index, 300, text_width), 388))
# default settings


pokemons = [None for i in range(3)]
pokemon_pointer = 0
option_pointer = 0
mon_options = []
user_text = ""




# pokemons = [pokemon("Skarmory"), pokemon("Vigoroth"), None]

running = True
while running:

    x, y = pygame.mouse.get_pos()
    #print(x, y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and pokemon_pointer >= 1:
                pokemon_pointer -= 1
            if event.key == pygame.K_RIGHT and pokemon_pointer <= 1:
                pokemon_pointer += 1
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


    draw_pokemons()
    draw_pointer(pokemon_pointer)
    if user_text != "":
        mon_options = draw_options(user_text, pokemon_pointer)


    pygame.display.flip()

pygame.quit()