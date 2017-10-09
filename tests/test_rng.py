from shamir_bip39_2039 import rng


def test_systemrng():

    r = rng.SystemRNG()
    for _ in range(100):
        assert r.random_int() % 1 == 0


def test_lcg():

    r = rng.LCG()
    for _ in range(100):
        assert r.random_int() % 1 == 0
