from rng import SystemRNG
from english2039 import word_dict

def generate_mnemonic(length=24, rng=SystemRNG()):

    return [word_dict[rng.random_int() % len(word_dict)] for _ in range(length)]
