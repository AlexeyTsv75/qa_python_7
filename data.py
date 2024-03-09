import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


login = generate_random_string(10)
password = generate_random_string(10)
first_name = generate_random_string(10)