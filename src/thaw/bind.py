from pathlib import Path

import yaml

a = Path('bindings.yml')

class bind:
    checker = False

    def __init__(self):
        a.touch(exist_ok=True)

    def __del__(self):
        # compatible with python 3.7
        if self.checker == True and a.is_file():
            a.unlink()

b = bind()

def put(key, value):
    b.checker = True
    with open(a, 'r') as f:
        d = yaml.safe_load(f)
    if d == None:
        d = {}

    d[key] = value
    
    with open(a, 'w') as f:
        f.write(yaml.dump(d))

def get(key):
    with open(a, 'r') as f:
        try:
            return yaml.safe_load(f)[key]
        except:
            print('Unexcepted key in bindings')
            raise
