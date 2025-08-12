# pip install cryptography pyperclip
import os
import sqlite3
from cryptography.fernet import Fernet
import pyperclip
import getpass
import secrets
import string


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    if not os.path.exists("secret.key"):
        generate_key()
    return open("secret.key", "rb").read()


key = load_key()
fernet = Fernet(key)


def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


init_db()


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()


def add_password():
    service = input("Enter service name (e.g., Google): ")
    username = input("Enter username/email: ")
    password = getpass.getpass("Enter password (leave empty to generate): ")
    if not password:
        password = generate_password()
        print(f"Generated password: {password}")
    encrypted_pwd = encrypt_password(password)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
                   (service, username, encrypted_pwd))
    conn.commit()
    conn.close()
    print("✅ Password saved securely!")


def get_password():
    service = input("Enter service name: ")
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, password FROM passwords WHERE service = ?", (service,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, encrypted_pwd = result
        password = decrypt_password(encrypted_pwd)
        print(f"\nService: {service}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        copy = input("Copy to clipboard? (y/n): ").lower()
        if copy == 'y':
            pyperclip.copy(password)
            print("📋 Password copied to clipboard!")
    else:
        print("❌ No password found for this service.")


def list_services():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service FROM passwords")
    services = cursor.fetchall()
    conn.close()
    if services:
        print("\nSaved services:")
        for service in services:
            print(f"- {service[0]}")
    else:
        print("No passwords stored yet.")


def main():
    while True:
        print("\n🔐 Python Password Manager")
        print("1. Add new password")
        print("2. Retrieve password")
        print("3. List all services")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            add_password()
        elif choice == "2":
            get_password()
        elif choice == "3":
            list_services()
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
