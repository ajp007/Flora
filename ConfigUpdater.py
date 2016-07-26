from os.path import exists, join
import json
def write_values(value: dict, file_name: str, data_type: str = 'values'):
    try:
        if exists(data_type) is False:
            mkdir(data_type)
        with open(join(data_type, '{0}.json'.format(file_name)), 'w') as f:
            # text = str(value).replace('}', '}\n').replace('{', '{\n')
            # f.write(text)
            json.dump(value, f, indent=4, sort_keys=True)
        return True
    except Exception:
        return False

def read_values(name: str, data_type: str = 'values'):
    value = None
    if exists('{0}/{1}.json'.format(data_type, name)):
        with open('{0}/{1}.json'.format(data_type, name), 'r') as f:
            # value = eval(f.read())
            value = json.load(f)
    return value
