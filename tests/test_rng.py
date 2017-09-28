from shamir_bip39_2039 import rng

def test_systemrng():

    r = rng.SystemRNG()
    for _ in range(100):
        assert isinstance(r.random_int(), int)

def test_lcg():

    r = rng.LCG()
    for _ in range(100):
        assert isinstance(r.random_int(), int)
        
