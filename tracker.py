import json
class pokemon:
    def __init__(self, name):
        self.name = name

        self.types = None
        self.fastMoves = None
        self.chargedMoves = None

        self.get_mon_data()
        self.get_fm_data()
        self.get_cm_data()

        self.energy = 0


    def get_mon_data(self):
        with open('data-files/mons.json', 'r') as file:
            data = json.load(file)
            for mon in data:
                if mon["name"] == self.name:
                    self.types = mon["types"]
                    self.fastMoves = mon["fastMoves"]
                    self.chargedMoves = mon["chargedMoves"]
    def get_fm_data(self):
        fms = []
        with open('data-files/fast_moves.json', 'r') as file:
            fast_moves = json.load(file)
            for fm in fast_moves:
                if fm["id"] in self.fastMoves:
                    del fm["id"]
                    fms.append(fm)
        self.fastMoves = fms
    def get_cm_data(self):
        cms = []
        with open('data-files/charged_moves.json', 'r') as file:
            charged_moves = json.load(file)
            for cm in charged_moves:
                if cm["id"] in self.chargedMoves:
                    del cm["id"]
                    cms.append(cm)
        self.chargedMoves = cms


a = pokemon("Skarmory")












