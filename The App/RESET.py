from cryptography.fernet import Fernet


def TBR():
    # Step 1: Generate a key and save it
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # The original password
    original_password = "Admin@123"

    # Encrypt the password
    ciphered_password = cipher_suite.encrypt(original_password.encode())

    # Save the key and ciphered password to a file
    with open("secrets.txt", "wb") as file:
        file.write(key + b"\n" + ciphered_password)

    print("Password encrypted and saved to secrets.txt")

    # Step 2: Read the key and ciphered password from the file and decrypt it
    with open("secrets.txt", "rb") as file:
        saved_key = file.readline().strip()
        saved_ciphered_password = file.readline().strip()

    # Initialize the cipher suite with the saved key
    cipher_suite = Fernet(saved_key)

    # Decrypt the password
    decrypted_password = cipher_suite.decrypt(saved_ciphered_password).decode()
    print("Decrypted password:", decrypted_password)

TBR()