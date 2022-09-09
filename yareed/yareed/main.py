import argparse
import yaml

def main():
    """Parser arguments and calls function"""

    parser = argparse.ArgumentParser(
        description="An over-simplified key-value parser for yaml documents."
    )
    parser.add_argument(
        "-file", type=argparse.FileType('r'), metavar='', required=True,
        help="The name of the Yaml file to read from."
    )
    parser.add_argument(
        "-keys", type=str, nargs='+', default=[], required=True, metavar='',
        help="The key to read from the Yaml document."
    )

    args = parser.parse_args()
    yreader(args.file.name, args.keys)

def yreader(file, keys):
    """Print key values"""

    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if len(keys) == 1:
        k = keys[0]

        # Key error
        if k not in data:
            print(f'key \'{k}\' not found...')
            print(f'available keys are \'{data.keys()}\'.')
            print(f'exiting now...')
            exit(1)

        if isinstance(data[k], str):
            print(data[k])
        if isinstance(data[k], list):
            for item in data[k]:
                print(item)
        if isinstance(data[k], dict):
            _leafs_from_tree(data[k])
    else:
        _this_leaf(data, keys)

def _leafs_from_tree(d):
    """Return the value of every leaf"""
    if isinstance(d, dict):
        for k in d.keys():
            _leafs_from_tree(d[k])
    if isinstance(d, str):
        print(d)

def _this_leaf(d, keys):
    """Return the leave value of a nested dict"""

    for k in keys:

        # Key error
        if k not in d:
            print(f'key \'{k}\' not found...')
            if isinstance(d, dict):
                print(f'available keys are \'{d.keys()}\'.')
            if isinstance(d, str):
                print(f'No more keys for this dictionary')
            print(f'exiting now...')
            exit(1)

        d = d.get(k)
    if isinstance(d, str):
        print(d)
    if isinstance(d, dict):
        _leafs_from_tree(d)

if __name__ == "__main__":
    main()
