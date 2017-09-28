from shamir_bip39_2039 import shamir
from shamir_bip39_2039 import rng

def test_secret_to_points():

    r = rng.LCG()
    prime = 2039

    for _ in range(100):
        secret = r.random_int() % prime
        points = shamir.secret_to_points(prime, secret, rng=r)
        assert secret == shamir.points_to_secret(prime, points[0], points[1])
        assert secret == shamir.points_to_secret(prime, points[0], points[2])
        assert secret == shamir.points_to_secret(prime, points[1], points[2])
