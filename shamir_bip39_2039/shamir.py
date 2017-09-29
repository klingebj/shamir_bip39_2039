from rng import SystemRNG

"""2-of-3 Shamir's secret sharing"""


def secret_to_points(prime, secret, rng=SystemRNG(), include_x=True):
    """Compute points for a secret integer over a field of size 'prime'"""

    assert secret < prime

    slope = rng.random_int() % prime

    def f(x):
        return (secret + slope * x) % prime

    if include_x:
        return [(i, f(i)) for i in range(1, 4)]
    else:
        return [f(i) for i in range(1, 4)]


def points_to_secret(prime, *points):
    """Recover the secret using a lagrange polynomial (with some simplifications for the 2-of-3 case)"""

    assert len(points) == 2

    delta = points[0][0] - points[1][0]
    abs_delta = abs(delta)
    delta_sign = 1 if delta > 0 else -1

    lagrange_numerator = (
        (points[0][0] * points[1][1] - points[1][0] * points[0][1]) * delta_sign) % prime

    if lagrange_numerator % abs_delta == 0:
        return lagrange_numerator / abs_delta
    else:
        return (lagrange_numerator + prime) / abs_delta
