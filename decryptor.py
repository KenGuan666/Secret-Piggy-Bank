import Crypto
from Crypto.PublicKey import RSA

from interface import createNewInterface

def decrypt_piggy_bank(name, password, interface, path='data/'):
    data_file = open((path + name + '.txt'), 'r')
    data_content = data_file.read().split('\n')[:-1]
    N, e = [int(s.split(':')[1].strip()) for s in data_content[:2]]

    try:
        key = RSA.construct((N, e, int(password)))
    except ValueError:
        interface.display('Incorrect password. Piggy Bank destructed.')
        return
    
    for i in range(2, len(data_content)):
        encrypted_int = int(data_content[i].strip())
        decrypted_int = key.decrypt(encrypted_int)
        decrypted_message = bytearray.fromhex(hex(decrypted_int)[2:]).decode()
        interface.display(decrypted_message)

    interface.display('Entries retrieved. Piggy Bank destructed.')
    data_file.close()
