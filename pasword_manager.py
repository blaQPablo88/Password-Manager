import json
import os
from cryptography.fernet import Fernet
import getpass

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.filename = 'passwords.json'
        self.key = self.generate_key(master_password)
        self.credentials = self.load_credentials()

    def generate_key(self, password):
        # Generate a key based on the master password
        return Fernet.generate_key()

    def load_credentials(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                encrypted_data = f.read()
                fernet = Fernet(self.key)
                decrypted_data = fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)
        return {}

    def save_credentials(self):
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(json.dumps(self.credentials).encode())
        with open(self.filename, 'wb') as f:
            f.write(encrypted_data)

    def add_credentials(self, service_name, username, password):
        self.credentials[service_name] = {
            'username': username,
            'password': password
        }
        self.save_credentials()

    def retrieve_credentials(self, service_name):
        return self.credentials.get(service_name, 'No credentials found for this service.')

def main():
    master_password = getpass.getpass("Enter your master password: ")
    password_manager = PasswordManager(master_password)

    while True:
        print("\n1. Add Credential")
        print("2. Retrieve Credential")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            service_name = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            password_manager.add_credentials(service_name, username, password)
            print("Credential added successfully.")

        elif choice == '2':
            service_name = input("Enter service name to retrieve: ")
            credentials = password_manager.retrieve_credentials(service_name)
            print(credentials)

        elif choice == '3':
            print("Exiting the password manager.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
