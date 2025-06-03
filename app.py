import json
import os
from cryptography.fernet import Fernet

DB_FILE = 'passwords.json'
KEY_FILE = 'secret.key'

# Generate or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

# Load password database
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Save password database
def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

# Add password
def add_password(site, username, password):
    db = load_db()
    encrypted = fernet.encrypt(password.encode()).decode()
    db[site] = {"username": username, "password": encrypted}
    save_db(db)
    print(f"[+] Added password for {site}")

# View passwords
def view_passwords():
    db = load_db()
    for site, creds in db.items():
        decrypted = fernet.decrypt(creds["password"].encode()).decode()
        print(f"{site}: {creds['username']} | {decrypted}")

# Main loop
def main():
    while True:
        print("\n1. Add Password\n2. View Passwords\n3. Quit")
        choice = input("Choose: ")

        if choice == '1':
            site = input("Site: ")
            username = input("Username: ")
            password = input("Password: ")
            add_password(site, username, password)
        elif choice == '2':
            view_passwords()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
