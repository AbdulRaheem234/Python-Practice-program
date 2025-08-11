import string
import random
if __name__ == "__main__":
    characters = []
    characters.extend(string.ascii_letters)
    characters.extend(string.digits)
    characters.extend(string.punctuation)
    characters = list(set(characters))
    plen = int(input("Enter the password length: "))
    if plen <= 0:
        print("Password length must be positive!")
    else:
        password = random.sample(characters, plen)
        print("Your password is: ")
        print("".join(password))
