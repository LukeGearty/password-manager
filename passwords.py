import bcrypt, secrets
import string
from cryptography.fernet import Fernet
import os


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)


def is_valid_master_password(password: str):
    """
        Requirements:
        password length greater than or equal to 12
        Combines uppercase, lowercase, and numbers, and special characters

    """
    try:
        if len(password) < 12:
            return False
        
        has_upper_case = False
        has_lower_case = False
        has_number = False
        has_special_character = False

        special_chars = "!@#$"
        for char in password:
            if char.islower():
                has_lower_case = True
            elif char.isupper():
                has_upper_case = True
            elif char.isnumeric():
                has_number = True
            elif char in special_chars:
                has_special_character = True
        
        if has_upper_case and has_lower_case and has_number and has_special_character:
            return True
        else:
            return False
    except TypeError:
        return False


def create_password():
    """
        Requirements: minimum length should be 12
        contain one uppercase, one lowercase, one digit, one special character

        Utilizing secrets.choice
    """
    special_chars = ['!', '@', '#', '$']

    password = ""

    for _ in range(9):
        password += secrets.choice(string.ascii_lowercase)
    
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    password += secrets.choice(special_chars)
    return password


def encrypt_password(password):
    key = os.environ.get("ENCRYPTION_KEY")
    cipher_suite = Fernet(key)

    # encrypt the password
    new_password = password.encode()
    encrypted_password = cipher_suite.encrypt(new_password)

    return encrypted_password
    
