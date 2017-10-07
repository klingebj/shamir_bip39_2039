from hashlib import pbkdf2_hmac
from mnemonic import allowed_mnemonic_lengths
from checksum import check_mnemonic_checksum


def mnemonic_to_seed(mnemonic, passphrase=b''):

    # Based on Vitalik's code
    # https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/mnemonic.py
    assert len(mnemonic) in allowed_mnemonic_lengths
    assert check_mnemonic_checksum(mnemonic)

    def pbkdf2_hmac_sha256(password, salt, iters=2048):
        return pbkdf2_hmac(hash_name='sha512', password=password, salt=salt, iterations=iters)

    return pbkdf2_hmac_sha256(password=' '.join(mnemonic), salt=b'mnemonic' + passphrase)
