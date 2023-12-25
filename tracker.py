import json
class pokemon:
    def __init__(self, name):
        self.name = name

        self.id = None
        self.types = None
        self.fastMoves = None
        self.chargedMoves = None
        self.thrownChargedMoves = []
        self.isImagePulled = False
        self.content = None
        self.lowestRequiredEnergy = None

        self.get_mon_data()
        self.get_fm_data()
        self.get_cm_data()
        self.make_preferred_moves_first()
        self.lowest_required_energy()

        self.energy = 0

    def get_mon_data(self):
        with open('data-files/pokemons.json', 'r') as file:
            data = json.load(file)
            for mon in data:
                if mon["name"] == self.name:
                    self.id = mon["id"]
                    self.types = mon["types"]
                    self.fastMoves = mon["fastMoves"]
                    self.chargedMoves = mon["chargedMoves"]
    def get_fm_data(self):
        fms = []
        with open('data-files/fast_moves.json', 'r') as file:
            fast_moves = json.load(file)
            for fm in fast_moves:
                if fm["id"] in self.fastMoves:
                    fms.append(fm)
        self.fastMoves = fms
    def get_cm_data(self):
        cms = []
        with open('data-files/charged_moves.json', 'r') as file:
            charged_moves = json.load(file)
            for cm in charged_moves:
                if cm["id"] in self.chargedMoves:
                    cms.append(cm)
        self.chargedMoves = cms
    def make_preferred_moves_first(self):
        with open('data-files/preferences.json', 'r') as file:
            data = json.load(file)
            for mon in data:
                if mon["name"] == self.name:
                    for move in self.fastMoves:
                        if move["id"] == mon["fastMove"]:
                            tmp = move
                            self.fastMoves.remove(move)
                            self.fastMoves.insert(0, tmp)
                    for move in self.chargedMoves:
                        for cm in mon["chargedMoves"]:
                            if move["id"] == cm:
                                tmp = move
                                self.chargedMoves.remove(move)
                                self.chargedMoves.insert(0, tmp)
    def change_fast_moves_order(self):
        a = self.fastMoves.pop(0)
        self.fastMoves.append(a)
    def change_1st_cm(self):
        a = self.chargedMoves.pop(0)
        self.chargedMoves.append(a)
        self.chargedMoves[0], self.chargedMoves[1] = self.chargedMoves[1], self.chargedMoves[0]
    def change_2nd_cm(self):
        a = self.chargedMoves.pop(1)
        self.chargedMoves.append(a)
    def change_relevant_cm(self):
        for move in self.thrownChargedMoves:
            if move not in self.chargedMoves[:2]:
                if self.chargedMoves[1] not in self.thrownChargedMoves:
                    self.chargedMoves.remove(move)
                    self.chargedMoves.insert(1, move)
                    return None
                if self.chargedMoves[0] not in self.thrownChargedMoves:
                    a = self.chargedMoves.pop(0)
                    self.chargedMoves.remove(move)
                    self.chargedMoves.insert(0, move)
                    self.chargedMoves.insert(2, a)
    def update_energy(self, fast_moves):
        self.energy += fast_moves * int(self.fastMoves[0]["energy"])
        if self.energy > 100:
            self.energy = 100
    def lowest_required_energy(self):
        energy_costs = []
        if len(self.thrownChargedMoves) == 2:
            for move in self.thrownChargedMoves:
                energy_costs.append(move["energy"])
                self.lowestRequiredEnergy = min(energy_costs)
        else:
            for move in self.chargedMoves:
                energy_costs.append(move["energy"])
                self.lowestRequiredEnergy = min(energy_costs)


def get_possible_options(str1):
    valid_options = []
    with open('data-files/pokemons.json', 'r') as file:
        data = json.load(file)
        for mon in data:
            if str1.lower() == mon["name"][:len(str1)].lower():
                valid_options.append(mon["name"])
    return valid_options

#a = pokemon("Skarmory")

# print(get_possible_options("la"))












