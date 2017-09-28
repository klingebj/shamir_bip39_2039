from shamir_bip39_2039 import mnemonic
from shamir_bip39_2039 import rng
from shamir_bip39_2039 import english2039
from shamir_bip39_2039 import checksum

def test_generate_partial_mnemonic():

    r = rng.LCG()
    for length in mnemonic.allowed_mnemonic_lengths:
        for _ in range(100):
            partial_mnemonic = mnemonic.generate_partial_mnemonic(length-1, rng=r)
            assert len(partial_mnemonic) == length - 1
            for word in partial_mnemonic:
                assert word in english2039.word_dict.values()

def test_generate_mnemonic():

    r = rng.LCG()
    for length in mnemonic.allowed_mnemonic_lengths:
        for _ in range(100):
            test_mnemonic = mnemonic.generate_mnemonic(length, rng=r)
            assert len(test_mnemonic) == length 
            for word in test_mnemonic:
                assert word in english2039.word_dict.values()
            assert checksum.check_mnemonic_checksum(test_mnemonic)


