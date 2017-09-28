from rng import SystemRNG
from shamir import secret_to_points, points_to_secret
from english2039 import word_dict, word_inv_dict
from mnemonic import generate_mnemonic, allowed_mnemonic_lengths, complete_partial_mnemonic
from checksum import check_mnemonic_checksum

def mnemonic_to_shares(mnemonic, prime=2039, rng=SystemRNG()):
    """Compute the shares for a mnemonic"""

    assert len(mnemonic) in allowed_mnemonic_lengths, "Must choose valid mnemonic length"
    assert check_mnemonic_checksum(mnemonic)
    
    shares = zip(*[secret_to_points(prime, word_inv_dict[word], rng, include_x=False) for word in mnemonic])

    return dict(zip(['share1','share2','share3'],[complete_partial_mnemonic([word_dict[i] for i in share][:-1]) for share in shares]))

def shares_to_mnemonic(share1=None, share2=None, share3=None, prime=2039):
    """Recover a mnemonic from two shares"""
    
    assert (share1 is None) + (share2 is None) + (share3 is None) == 1, "Must provide exactly two shares."

    shares = [[(i+1, word_inv_dict[word]) for word in share[:-1]] for i, share in enumerate([share1, share2, share3]) if share is not None]
    mnemonic = complete_partial_mnemonic([word_dict[points_to_secret(prime, *w)] for w in zip(*shares)])
    assert check_mnemonic_checksum(mnemonic)
    return mnemonic
