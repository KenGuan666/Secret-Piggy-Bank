import rsa
import argparse
import os
import re
from interface import createNewInterface

parser = argparse.ArgumentParser(description='Create a new piggy bank.')
parser.add_argument('--name')

def main():
    args = parser.parse_args()
    if not os.path.exists('data'):
        os.mkdir('data')

    _interface = createNewInterface()

    existing_files = set([file_name for file_name in os.listdir('data') if re.match('.*\.txt', file_name)])
    name = args.name
    if name and name + '.txt' in existing_files:
        _interface.display('Piggy bank with name \"{}\" already exists.'.format(name))
        return

    while not name:
        typed_name = _interface.display_and_await_input('Name your piggy bank:').strip()
        if not typed_name:
            _interface.display('Please use characters other than space.')
        elif typed_name + '.txt' in existing_files:
            _interface.display('Piggy bank with name \"{}\" already exists.'.format(typed_name))
        else:
            name = typed_name
    
    open('data/{}'.format(name + '.txt'), 'w')

if __name__ == '__main__':
    main()