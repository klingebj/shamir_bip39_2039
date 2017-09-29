from shamir_bip39_2039 import api
from shamir_bip39_2039 import rng
from shamir_bip39_2039 import mnemonic


def test_api():

    r = rng.LCG()
    for length in mnemonic.allowed_mnemonic_lengths:
        for _ in range(100):
            test_mnemonic = mnemonic.generate_mnemonic(
                length, rng=r)
            shares = api.mnemonic_to_shares(test_mnemonic)
            for u, v in zip(test_mnemonic, api.shares_to_mnemonic(share1=shares['share1'], share2=shares['share2'])):
                assert u == v
            for u, v in zip(test_mnemonic, api.shares_to_mnemonic(share1=shares['share1'], share3=shares['share3'])):
                assert u == v
            for u, v in zip(test_mnemonic, api.shares_to_mnemonic(share2=shares['share2'], share3=shares['share3'])):
                assert u == v
