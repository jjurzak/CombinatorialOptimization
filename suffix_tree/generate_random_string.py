import random
import string
import sys

def generate_random_string(length, alphabet=string.ascii_lowercase):
    return ''.join(random.choices(alphabet, k=length))
