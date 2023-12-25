import requests
import os
try:
    os.mkdir('source-files')
except:
    pass
files = ['pokemon.json', 'moves.json', 'preferences.json']
for index, file in enumerate(files):
    save_path = f'source-files/{file}'
    if index == 2:
        response = requests.get(f'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/all/overall/rankings-1500.json')
    else:
        response = requests.get(f'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster/{file}')
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f'The file has been saved to {save_path}')
    else:
        print(f'Failed to download the file. Status code: {response.status_code}')



