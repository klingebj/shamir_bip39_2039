from rng import SystemRNG
from english2039 import word_dict
from checksum import complete_partial_mnemonic

allowed_mnemonic_lengths = [12, 15, 18, 21, 24]


def generate_partial_mnemonic(length=23, rng=SystemRNG()):

    assert (length + 1) in allowed_mnemonic_lengths, "Must choose valid mnemonic length"

    return [word_dict[rng.random_int() % len(word_dict) + 1] for _ in range(length)]


def generate_mnemonic(length=24, rng=SystemRNG()):

    assert length in allowed_mnemonic_lengths, "Must choose valid mnemonic length"

    partial_mnemonic = generate_partial_mnemonic(length=length - 1, rng=rng)
    return complete_partial_mnemonic(partial_mnemonic)
