import json
def create_moves_files():
    with open('source-files/moves.json', 'r') as file:
        data = json.load(file)

    fm_data = []
    cm_data = []
    for move in data:
        if move["energyGain"] != 0:
            fm_data.append({"id": move["moveId"], "name": move["name"], "type": move["type"], "energy": move["energyGain"]})
        else:
            cm_data.append({"id": move["moveId"], "name": move["name"], "type": move["type"], "energy": move["energy"]})

    with open('data-files/fast_moves.json', 'w') as fm_file, open('data-files/charged_moves.json', 'w') as cm_file:
        json.dump(fm_data, fm_file, indent=2)
        json.dump(cm_data, cm_file, indent=2)
def create_pokemons_file():
    with open('source-files/pokemon.json', 'r') as file:
        data = json.load(file)

    mons_data = []
    for pokemon in data:
        if pokemon["speciesId"][-7:] != "_shadow":
            mons_data.append({"name": pokemon["speciesName"], "id": pokemon["dex"], "types": pokemon["types"], "fastMoves": pokemon["fastMoves"], "chargedMoves": pokemon["chargedMoves"]})

    with open('data-files/pokemons.json', 'w') as mons_file:
        json.dump(mons_data, mons_file, indent=2)
def create_preferences_file():
    with open('source-files/preferences.json', 'r') as file:
        data = json.load(file)

    mons_data = []
    for pokemon in data:
        if pokemon["speciesId"][-7:] != "_shadow":
            mons_data.append({"name": pokemon["speciesName"], "fastMove": pokemon["moveset"][0], "chargedMoves": pokemon["moveset"][1:]})

    with open('data-files/preferences.json', 'w') as preferences_file:
        json.dump(mons_data, preferences_file, indent=2)
create_preferences_file()