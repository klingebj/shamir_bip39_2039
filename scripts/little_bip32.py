# Simple script for generating (hardened) BIP32 addresses from a mnemonic. Require additional libraries.

# Example: python scripts/little_bip32.py $mnemonic $passphrase 0 0 0


# https://github.com/vbuterin/pybitcointools
import bitcoin as btc
# https://github.com/klingebj/shamir_bip39_2039
from shamir_bip39_2039 import seed
import binascii
import hashlib
import argparse

parser = argparse.ArgumentParser(
    description='Generate BIP32 addresses from mnemonic')

parser.add_argument('mnemonic', type=str,
                    help='Mnemonic (space delimited string)')
parser.add_argument('passphrase', type=str, help='BIP32 passphrase')
parser.add_argument('path', type=int, nargs=3,
                    help='BIP32 derivation path (e.g. 0 0 0)')
parser.add_argument('--key', dest='return_key',
                    action='store_true', help='Return the (hex) private key')
parser.add_argument('--args', dest='print_args',
                    action='store_true', help='Print input to script')


def child(x, i):
    # See https://github.com/vbuterin/pybitcointools/issues/58
    return btc.bip32_ckd(x, 2**31 + i)


def descend(k, params):
    for param in params:
        k = child(k, param)
    return k


def key_address(masterkey, path):
    """Compute address and private key (hex) for path"""

    derived_key = descend(masterkey, path)
    priv_key = btc.bip32_deserialize(derived_key)[-1]
    pub_key = btc.bip32_extract_key(btc.bip32_privtopub(derived_key))
    priv_key_hex = btc.encode_privkey(
        btc.decode_privkey(priv_key, 'bin_compressed'), 'hex')
    address = btc.pubkey_to_address(pub_key)

    return priv_key_hex, address


def mnemonic_to_key(mnemonic, passphrase, path):
    """Return the (hex) private key"""

    masterkey = btc.bip32_master_key(
        seed.mnemonic_to_seed(mnemonic, passphrase))
    key, _ = key_address(masterkey, path)
    return key


def mnemonic_to_address(mnemonic, passphrase, path):
    """Return the (compressed) bitcoin address"""

    masterkey = btc.bip32_master_key(
        seed.mnemonic_to_seed(mnemonic, passphrase))
    _, addr = key_address(masterkey, path)
    return addr


def test_addresses():
    """Test address generation"""

    test_vectors = [("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about", [0, 0, 0], '1EbiwdYNzJ9jyJVsnEKkgV8cmi5iDvDMiS', 'TREZOR'),
                    ("letter advice cage absurd amount doctor acoustic avoid letter advice cage above", [
                        0, 0, 1], '16MYqD3yixDdP2wSZN2r6eLQRZjTeVZKqs', 'TREZOR'),
                    ("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent", [
                        14, 14, 14], '17sheBr8x4kaApiMQSPzzbZYNKU5gs9csM', 'TREZOR'),
                    ("letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always", [
                        3, 4, 5], '1EyvTRpcWq17HN7veVrzbUECxPjwcTVNyA', 'TREZOR'),
                    ("ozone drill grab fiber curtain grace pudding thank cruise elder eight picnic", [
                        1, 1, 1], '1JmDtj3aHuTknXtxPW7o9xUBiASzPD5VDu', 'TREZOR'),
                    ("gravity machine north sort system female filter attitude volume fold club stay feature office ecology stable narrow fog", [
                        120, 14, 21], '16RJtTjpPF59b76vadgNUjgPqLVdZLAL8t', 'TREZOR'),
                    ("hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length", [
                        1, 2, 3], '14w6DaQ4FkE7xtjovUrhSpThwNbSKydHBc', 'TREZOR'),
                    ("scheme spot photo card baby mountain device kick cradle pact join borrow", [
                        0, 0, 17], '19okVLmMQcz6yKisknSQQMutAsC1XszRdu', 'TREZOR'),
                    ("horn tenant knee talent sponsor spell gate clip pulse soap slush warm silver nephew swap uncle crack brave", [
                        1, 0, 0], '15q3smKAzaXsCJAbY6sGevZsE415xSijjL', 'TREZOR'),
                    ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside", [
                        12, 0, 90], '1Kfm6D7oYtEijcqRiEkTA6SnMoH6o3uWnj', 'TREZOR'),
                    ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside", [
                        12, 0, 90], '17FngVD55Rh6qkxcwpwadV29KuydXPzR57', ''),
                    ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside", [
                     12, 0, 90], '1GQsb7tCBAKvvxRXwv9ixD67NMuSaeRGeM', 'ab8arstoienA$aoarsto_AST8405582811-arstarfcf292dnastratoarston4uq03gda'),
                    ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside", [12, 0, 90], '13fEzRvL63LZES8stDQGYiGH8i1ME496Yo', 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')]

    for (mnemonic, path, addr, passphrase) in test_vectors:
        assert addr == mnemonic_to_address(
            mnemonic.split(' '), passphrase, path)


if __name__ == '__main__':

    # Be sure everything is working...
    test_addresses()

    args = parser.parse_args()

    if args.print_args:
        print "Mnemonic:", args.mnemonic
        print "Mnemonic length:", len(args.mnemonic.split(' ')), '\n'
        print "Passphrase:", args.passphrase
        print "Passphrase length:", len(args.passphrase), '\n'
        print "Path:", args.path
        print "Path length:", len(args.path), '\n'

    if args.return_key:
        print mnemonic_to_key(args.mnemonic.split(' '), args.passphrase, args.path)
    else:
        print mnemonic_to_address(args.mnemonic.split(' '), args.passphrase, args.path)
