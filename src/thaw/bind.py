from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()

f = Path('bindings.yml')

checker = None

def put(key, value):
    if checker == None:
        checker == True
    elif checker == False:
        sys.stderr.write('Generator but modify bindings') 

    d = yaml.load(f)
    if d == None:
        d = {}
    d[key] = value
    yaml.dump(d, f)

def get(key):
    if checker == None:
        checker == False
    elif checker == True:
        sys.stderr.write('Checker but read bindings')

    try:
        return yaml.load(f)[key]
    except:
        print('Unexcepted key in bindings')
        raise
