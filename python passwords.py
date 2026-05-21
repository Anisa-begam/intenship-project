import string

password = input("Enter password: ")

special_chars = string.punctuation

has_special = any(char in special_chars for char in password)

if len(password) > 8 and has_special:
    print("Strong Password")
else:
    print("Weak Password")