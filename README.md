# Password Manager CLI (AES-GCM Encryption)

### Description

This is a simple command-line password manager written in Python 3.10.12. The application is run from the terminal using commands explained below.<br>
Requires: `pycryptodome`  
Install it using:
```bash
pip install pycryptodome
```
### Usage
To start the program, open a terminal, navigate to the directory containing the file `pass_man.py`, and run:

```bash
python3 pass_man.py
```
On the first run, use the init command to set a master password.<br>
The password is not stored; it is used with a randomly generated salt to derive an encryption key.<br>
A database.txt file is created to store the salt and encrypted data.<br>

If init is run again:
- The user must enter the original master password
- A new password can then be set, but all previous data will be erased

To save data, use the put command with the address and password.<br>
To retrieve data, use the get command with the address.<br>
Use q to quit the program.<br>

### Error Handling
- Incorrect master password or integrity check failed. — Shown if the master password is wrong or database.txt is modified
- Incorrect input format. — Shown for badly formatted put/get commands
- Unknown command — Shown for any unrecognized command

### Encryption Details
Uses AES-GCM encryption for the entire database.<br>
The salt is read from database.txt and combined with the master password using PBKDF2 (SHA-256) to derive a 256-bit key.<br>
A new salt and nonce are generated every time a new password is added or updated.<br>
This ensures:
- No one can tell how many passwords or addresses are stored.
- Identical passwords appear different after re-encryption.
- Full confidentiality and integrity through encryption and authentication tags.
