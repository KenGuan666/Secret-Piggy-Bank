import rsa
import os
import re
from interface import createNewInterface

class PiggyBankManager:

    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        self.interface = createNewInterface()
        self.update_existing_files()

    def update_existing_files(self):
        self.existing_files = set([file_name for file_name in os.listdir('data') if re.match('.*\.txt', file_name)])

    def run(self):
        self.interface.display('Welcome to Secret Piggy Bank system. Please choose one of the following operations')
        self.interface.display('Create, Insert, Break, Exit, Help')

        response_mapping = {
            'create': self.create,
            'insert': self.insert,
            'break': self._break,
            'help': self.help,
        }

        while True:
            response = str.lower(input())
            if response == 'exit':
                return
            func = response_mapping.get(response, None)
            func() if func else self.interface.display('Please select a valid operation. Type \"Help\" for help')


    def create(self):
        name = ''
        while not name:
            typed_name = self.interface.display_and_await_input('Name your Piggy Bank:').strip()
            if not typed_name:
                self.interface.display('Please use characters other than space.')
            elif typed_name + '.txt' in self.existing_files:
                self.interface.display('Piggy bank with name \"{}\" already exists.'.format(typed_name))
            else:
                name = typed_name + '.txt'

        open('data/{}'.format(name), 'w')
        self.existing_files.add(name)

        pubkey, privkey = rsa.newkeys(512)
        print(pubkey, privkey)


    def insert(self):
        pass

    def _break(self):
        pass
    
    def help(self):
        self.interface.display('Create: Make a new Piggy Bank and generate a password.')
        self.interface.display('Insert: Add an entry to a Piggy Bank.')
        self.interface.display('Break: Delete a Piggy Bank and access all its entries. Breaking with an incorrect password will delete the Piggy Bank without gaining access to any entries.')
        self.interface.display('Exit: Exit the program')
        

def main():
    manager = PiggyBankManager()
    manager.run()

if __name__ == '__main__':
    main()
