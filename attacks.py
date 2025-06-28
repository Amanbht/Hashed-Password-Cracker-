import itertools
import json
from utils import hash_string

def brute_force_crack(hash_val, algo, max_len=4, charset="abcdefghijklmnopqrstuvwxyz0123456789", progress_callback=None):
    total = sum(len(charset) ** i for i in range(1, max_len + 1))
    tried = 0
    for length in range(1, max_len + 1):
        for attempt in itertools.product(charset, repeat=length):
            tried += 1
            if progress_callback:
                progress_callback(tried / total * 100)
            password = ''.join(attempt)
            if hash_string(password, algo) == hash_val:
                return password
    return None

def dictionary_attack(hash_val, algo, dict_file="wordlist.txt", progress_callback=None):
    try:
        with open(dict_file, "r") as file:
            words = [line.strip() for line in file]
        total = len(words)
        for i, word in enumerate(words):
            if progress_callback:
                progress_callback((i + 1) / total * 100)
            if hash_string(word, algo) == hash_val:
                return word
    except FileNotFoundError:
        return None
    return None

def rainbow_table_crack(hash_val, algo, table_file="rainbow_table.json"):
    try:
        with open(table_file, "r") as file:
            table = json.load(file)
        return table.get(hash_val)
    except FileNotFoundError:
        return None
