from cryptography.fernet import Fernet
import getpass
import os
import sys

try:
    from msvcrt import getch 
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
MASTER_PASSWORD = input("Enter your master password: ")

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("key.key"):
        write_key()
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

key = load_key()
fer = Fernet(key)

def view():
    if not os.path.exists('passwords.txt'):
        print("No passwords to view.")
        return
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|", 1)
            print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode(), "\n")

def add():
    name = input('Account Name: ')
    if not name:
        print("Account name cannot be empty.")
        return
    pwd = getpass.getpass("Password: ")
    if not pwd:
        print("Password cannot be empty.")
        return
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

def verify_master_password():
    attempts = 3
    while attempts > 0:
        password = ""
        sys.stdout.write("\nEnter the master password: ")
        sys.stdout.flush()
        while True:
            key = ord(getch())
            if key == 13:
                break
            if key == 8:
                if len(password) > 0:
                    sys.stdout.write("\b" + " " + "\b")
                    sys.stdout.flush()
                    password = password[:-1]
            else:
                char = chr(key)
                password += char
                sys.stdout.write("*")
                sys.stdout.flush()
        if password == MASTER_PASSWORD:
            return True
        else:
            attempts -= 1
            print(f"\nIncorrect password. {attempts} attempts remaining.")
    return False

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        break
    if mode == "view":
        if verify_master_password():
            view()
        else:
            print("Access denied.")
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue