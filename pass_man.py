import json
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

def deriveEncryptionKey(masterPassword, salt):
    password = masterPassword.encode()
    key = PBKDF2(password, salt, 32, 1000000, hmac_hash_module=SHA256)
    return key;

def encryptData(data, key):
    nonce = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encryptedData = nonce + ciphertext + tag
    return encryptedData;

def decryptData(encryptedData, key):
    if len(encryptedData) < 48:
        print('No data available.')
        return None
    nonce = encryptedData[:16]
    ciphertext = encryptedData[16:-16]
    tag = encryptedData[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data
    except ValueError:
        return None

def initializeTool(masterPassword):
    salt = get_random_bytes(16)
    key = deriveEncryptionKey(masterPassword, salt)
    with open('database.txt', 'wb') as f:
        f.write(salt)
    print("Initialization completed.")

def reinitializeTool(oldMaster, newMaster):
    with open('database.txt', 'rb+') as f:
        salt = f.read(16)
        key = deriveEncryptionKey(oldMaster, salt)
        encrypted = f.read()
        data = decryptData(encrypted, key)
        if data is None:
             print('Incorrect master password or integrity check failed.')
             return
        else:
            f.seek(0)
            f.truncate()
            initializeTool(newMaster)

def addPassword(masterPassword, address, password):
     with open('database.txt', 'rb+') as f:
        salt = f.read(16)
        key = deriveEncryptionKey(masterPassword, salt)
        encrypted = f.read()
        if encrypted:
            data = decryptData(encrypted, key)
            if data is None:
             print('Incorrect master password or integrity check failed.')
             return 
            pairs = json.loads(data.decode())
            #azuriraj lozinku za vec postojecu adresu
            if address in pairs:
                pairs[address] = password
        else:
            pairs = {}
        pairs[address] = password
        encrypted = encryptData(json.dumps(pairs).encode(), key)
        f.seek(0)
        f.write(salt + encrypted)
        f.truncate()
        print("Password stored.")

def retrievePassword(masterPassword, address):
    with open('database.txt', 'rb+') as f:
        salt = f.read(16)
        key = deriveEncryptionKey(masterPassword, salt)
        encrypted = f.read()
        data = decryptData(encrypted, key)
        if data is None:
             print('Incorrect master password or integrity check failed.')
             return
        pairs = json.loads(data.decode())
        if address in pairs:
            print("Password for", address, "is", pairs[address])
        else:
            print("No password found for this address.")

def isEmpty(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            if f.read():
                return False
    return True            

def main():

    if isEmpty('database.txt'):
        print('To start using the tool please set up the master password by writing it after the \'init\' command')
    else:
        print('Use:\n\'put\' and master password to store/update passwords\n\'get\' and master password to retrieve passwords\n\'init\' to reinitialize tool\n\'q\' to quit program') 

    while(True):   
    
        userInput = input()
        data = userInput.split()

        command = data[0]

        if command == 'init':
            if isEmpty('database.txt'):
                if len(data) < 2:
                    print('Incorrect input format.')
                else:    
                    initializeTool(data[1])
                    print('Use:\n\'put\' and master password to store/update passwords\n\'get\' and master password to retrieve passwords\n\'init\' to reinitialize tool\n\'q\' to quit program') 
            else:
                print('Already initialized. Do you want to reinitialize the tool? (y/n)')
                answer = input()
                if answer == 'y':
                    print('Are you sure you want to reinitialize the tool? Keep in mind that you will lose all your saved data! (y/n)')
                    answer = input()
                    if answer == 'y':
                        print('Input the old master password:')
                        oldMaster = input()
                        print('Input the new master password:')
                        newMaster = input()
                        reinitializeTool(oldMaster, newMaster)
                    else:
                        print('Reinitialization cancelled.')  
                else:
                        print('Reinitialization cancelled.')                   	
        elif command == 'put':
            if len(data) < 4:
                print('Incorrect input format.')
            else:     
                addPassword(data[1], data[2], data[3]) #masterPassword = data[1], address=data[2], password=data[3] 
               
        elif command == 'get':
            if len(data) < 3:
                print('Incorrect input format.') 
            else:    
                retrievePassword(data[1], data[2])   #masterPassword = data[1], address=data[2]             
        elif command == 'q':
            print('Password manager closed.')
            break
        else:
            print('Unknown command.')  


if __name__=="__main__":
    main()

