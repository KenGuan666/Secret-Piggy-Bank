import os
import re

import Crypto
from Crypto.PublicKey import RSA

from interface import createNewInterface

class PiggyBankManager:

    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        self.interface = createNewInterface()
        self.existing_names = set([file_name[:-4] for file_name in os.listdir('data') if re.match('.*\.txt', file_name)])

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
            response = self.interface.await_input()
            if response == 'exit':
                return
            func = response_mapping.get(response, None)
            func() if func else self.interface.display('Please select a valid operation. Type \"Help\" for help')
            self.interface.display('\nCreate, Insert, Break, Exit, Help')


    def create(self):
        name = ''
        while not name:
            typed_name = self.interface.display_and_await_input('Name your Piggy Bank:')
            if not typed_name or typed_name in illegal_piggy_bank_names:
                self.interface.display('Please use another name.')
            elif typed_name in self.existing_names:
                self.interface.display('Piggy bank with name \"{}\" already exists.'.format(typed_name))
            else:
                name = typed_name

        data_file = open('data/{}'.format(name + '.txt'), 'w')
        key = RSA.generate(1024)
        self.interface.display('Your password: {}. Please keep safely.'.format(key.d))
        data_file.write('N: {} \n'.format(key.n))
        data_file.write('e: {} \n'.format(key.e))
        data_file.close()

        self.existing_names.add(name)


    def insert(self):
        self.interface.display('Which of the following Piggy Bank would you like to insert to? Type \'Quit\' to quit.')
        self.interface.display(', '.join(self.existing_names))

        name = ''
        while not name:
            typed_name = self.interface.await_input()
            if typed_name == 'quit':
                return
            if typed_name in self.existing_names:
                name = typed_name
            else:
                self.interface.display('No Piggy Bank named {}.'.format(typed_name))

        message = self.interface.display_and_await_input('Please type your message:')
        hex_encoded_message = int(message.encode('utf-8').hex(), 16)

        data_file = open('data/{}'.format(name + '.txt'), 'r')
        data_content = data_file.read()
        N, e = [int(s.split(':')[1].strip()) for s in data_content.split('\n')[:2]]
        data_file.close()

        pub_key = RSA.construct((N, e))
        encrypted_int = pub_key.encrypt(hex_encoded_message, 32)[0]
        
        data_file = open('data/{}'.format(name + '.txt'), 'a')
        data_file.write(str(encrypted_int) + '\n')
        data_file.close()

    def _break(self):
        if not self.existing_names:
            self.interface.display('You don\'t have any Piggy Banks.')
            return
        self.interface.display('Which of the following Piggy Bank would you like to break? Type \'Quit\' to quit.')
        self.interface.display(', '.join(self.existing_names))

        name, password = '', ''
        while not name:
            typed_name = self.interface.await_input()
            if typed_name == 'quit':
                return
            if typed_name in self.existing_names:
                typed_password = self.interface.display_and_await_input('Please enter your password. The Piggy Bank will be deleted after this operation! Type \'Quit\' to quit.')
                if typed_password == 'quit':
                    return
                name, password = typed_name, typed_password
            else:
                self.interface.display('No Piggy Bank named {}.'.format(typed_name))
        
        self.decrypt_piggy_bank(name, password)
        os.remove('data/{}.txt'.format(name))
        self.existing_names.remove(name)

    def decrypt_piggy_bank(self, name, password):
        data_file = open('data/{}'.format(name + '.txt'), 'r')
        data_content = data_file.read().split('\n')[:-1]
        N, e = [int(s.split(':')[1].strip()) for s in data_content[:2]]

        try:
            key = RSA.construct((N, e, int(password)))
        except ValueError:
            self.interface.display('Incorrect password. Piggy Bank Destructed.')
            return
            
        for i in range(2, len(data_content)):
            encrypted_int = int(data_content[i].strip())
            decrypted_int = key.decrypt(encrypted_int)
            decrypted_message = bytearray.fromhex(hex(decrypted_int)[2:]).decode()
            self.interface.display(decrypted_message)

        data_file.close()

    def help(self):
        self.interface.display('Create: Make a new Piggy Bank and generate a password.')
        self.interface.display('Insert: Add an entry to a Piggy Bank.')
        self.interface.display('Break: Delete a Piggy Bank and access all its entries. Breaking with an incorrect password will delete the Piggy Bank without gaining access to any entries.')
        self.interface.display('Exit: Exit the program')
        

illegal_piggy_bank_names = ['quit']

def main():
    manager = PiggyBankManager()
    manager.run()

if __name__ == '__main__':
    main()
