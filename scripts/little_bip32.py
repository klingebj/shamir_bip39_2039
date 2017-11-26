# Simple script for generating (hardened) BIP32 addresses from a mnemonic. Require additional libraries.

# Example: python scripts/little_bip32.py --mnemonic $mnemonic --passphrase $passphrase --path 0 0 0
# Example with BIP39-2039 shares: python scripts/little_bip32.py --share1 $share1 --share2 $share2 --passphrase $passphrase --path 0 0 0

# https://github.com/vbuterin/pybitcointools
import bitcoin as btc
# https://github.com/klingebj/shamir_bip39_2039
from shamir_bip39_2039.api import shares_to_mnemonic, check_mnemonic_checksum
from shamir_bip39_2039 import seed
import binascii
import hashlib
import argparse

parser = argparse.ArgumentParser(
    description='Generate BIP32 addresses from mnemonic')

parser.add_argument(
    '--mnemonic',
    type=str,
    help='Mnemonic (space delimited string)',
    default=None)
parser.add_argument(
    '--share1',
    type=str,
    help='Mnemonic share (space delimited string)',
    default=None)
parser.add_argument(
    '--share2',
    type=str,
    help='Mnemonic share (space delimited string)',
    default=None)
parser.add_argument(
    '--share3',
    type=str,
    help='Mnemonic share (space delimited string)',
    default=None)
parser.add_argument(
    '--passphrase', type=str, help='BIP32 passphrase', default=None)
parser.add_argument(
    '--path',
    type=int,
    nargs=3,
    required=True,
    help='BIP32 derivation path (e.g. 0 0 0)')
parser.add_argument(
    '--sha256pass',
    dest='sha256pass',
    action='store_true',
    help='Apply sha256 to passphrase before use')
parser.add_argument(
    '--key',
    dest='return_key',
    action='store_true',
    help='Return the (hex) private key')
parser.add_argument(
    '--wif',
    dest='return_wif',
    action='store_true',
    help='Return the (wif) private key')
parser.add_argument(
    '--args',
    dest='print_args',
    action='store_true',
    help='Print input to script')
parser.add_argument(
    '--show_tests',
    dest='show_tests',
    action='store_true',
    help='Print test output')


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


def mnemonic_to_wif(mnemonic, passphrase, path):
    """Return the (wif) private key"""

    return btc.encode_privkey(
        mnemonic_to_key(mnemonic, passphrase, path), 'wif_compressed')


def mnemonic_to_address(mnemonic, passphrase, path):
    """Return the (compressed) bitcoin address"""

    masterkey = btc.bip32_master_key(
        seed.mnemonic_to_seed(mnemonic, passphrase))
    _, addr = key_address(masterkey, path)
    return addr


def test_addresses(show_tests=False):
    """Test address generation"""

    test_vectors = [
        ("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
         [0, 0, 0], '1EbiwdYNzJ9jyJVsnEKkgV8cmi5iDvDMiS', 'TREZOR'),
        ("letter advice cage absurd amount doctor acoustic avoid letter advice cage above",
         [0, 0, 1], '16MYqD3yixDdP2wSZN2r6eLQRZjTeVZKqs', 'TREZOR'),
        ("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent",
         [14, 14, 14], '17sheBr8x4kaApiMQSPzzbZYNKU5gs9csM', 'TREZOR'),
        ("letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always",
         [3, 4, 5], '1EyvTRpcWq17HN7veVrzbUECxPjwcTVNyA', 'TREZOR'),
        ("ozone drill grab fiber curtain grace pudding thank cruise elder eight picnic",
         [1, 1, 1], '1JmDtj3aHuTknXtxPW7o9xUBiASzPD5VDu', 'TREZOR'),
        ("gravity machine north sort system female filter attitude volume fold club stay feature office ecology stable narrow fog",
         [120, 14, 21], '16RJtTjpPF59b76vadgNUjgPqLVdZLAL8t', 'TREZOR'),
        ("hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length",
         [1, 2, 3], '14w6DaQ4FkE7xtjovUrhSpThwNbSKydHBc', 'TREZOR'),
        ("scheme spot photo card baby mountain device kick cradle pact join borrow",
         [0, 0, 17], '19okVLmMQcz6yKisknSQQMutAsC1XszRdu', 'TREZOR'),
        ("horn tenant knee talent sponsor spell gate clip pulse soap slush warm silver nephew swap uncle crack brave",
         [1, 0, 0], '15q3smKAzaXsCJAbY6sGevZsE415xSijjL', 'TREZOR'),
        ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside",
         [12, 0, 90], '1Kfm6D7oYtEijcqRiEkTA6SnMoH6o3uWnj', 'TREZOR'),
        ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside",
         [12, 0, 90], '17FngVD55Rh6qkxcwpwadV29KuydXPzR57', ''),
        ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside",
         [12, 0, 90], '1GQsb7tCBAKvvxRXwv9ixD67NMuSaeRGeM',
         'ab8arstoienA$aoarsto_AST8405582811-arstarfcf292dnastratoarston4uq03gda'
         ),
        ("panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost adult",
         [12, 0, 90], '1Ho6ueo9mrtGfQgaPiNXDVs5Ecmfsp6V5e',
         'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'),
        ("craft tide sword holiday resemble process mammal hawk top seven reform thumb please blade million rich deny airport civil rough property torch raven beyond",
         [81, 22, 86], "1CBRcSVCj9YJ4SMceyWeHJSpokeEnRaS1N",
         "047bbab9d3c9a818b3107747da1b7fe1d22fbe5c733d78b6de0a33e7a3bee955"),
        ("surface book trick bicycle wisdom donkey slight flight this chicken unusual explain quit proof creek brisk brother rent swamp earn else penalty lyrics account",
         [16, 21, 58], "142bJdVy1JZEeFYXyEBUT99nSbRQ26aDXQ",
         "f5953d27c02783e3ab28138de27c68eb3f0331047efe8d2efa47c6b38c855004"),
        ("delay easily trumpet crane about cushion indoor vendor hockey duty resource fly exit member juice thunder snake unhappy school shift nature doll cousin alarm",
         [85, 51, 49], "13J1zrUvuRzraBNEW8vP1ZpnMBc4KuaSTn",
         "ff70868760c428fe5b76cb7f9204e0d0296109bfd3158bc4be4653e48f847d8c"),
        ("grit idea display balcony twist planet embody oval chicken liberty boss very wreck vapor embody visa unable country false atom athlete access unaware awful",
         [65, 47, 97], "112EJEA6v3iWafpgXS5j4kmujJX4U128mr",
         "2c96814bd95ba61ecc46cda371e1f538d81cd03f4f0211004ef4ecd2affee0a1")
    ]

    for i, (mnemonic, path, addr, passphrase) in enumerate(test_vectors):
        assert addr == mnemonic_to_address(
            mnemonic.split(' '), passphrase, path)
        if show_tests:
            print i, addr, mnemonic_to_address(
                mnemonic.split(' '), passphrase, path)


if __name__ == '__main__':

    args = parser.parse_args()

    # Be sure everything is working...
    test_addresses(args.show_tests)

    #Check that either a mnemomic or two shares are provided
    num_shares = (args.share1 is not None) + (args.share2 is not None) + (
        args.share3 is not None)
    assert (args.mnemonic is not None) or (
        num_shares == 2), "Must provide mnemonic or two shares"

    def split(x):
        return None if x is None else x.split(' ')

    if args.mnemonic is not None:
        mnemonic = split(args.mnemonic)
    else:
        mnemonic = shares_to_mnemonic(
            share1=split(args.share1),
            share2=split(args.share2),
            share3=split(args.share3))

    assert check_mnemonic_checksum(mnemonic)

    if args.sha256pass:
        passphrase = hashlib.sha256(args.passphrase).hexdigest()
    else:
        passphrase = args.passphrase

    if args.print_args:
        print "\nMnemonic:", mnemonic
        print "Mnemonic length:", len(mnemonic), '\n'
        print "Passphrase:", passphrase
        print "Passphrase length:", len(passphrase), '\n'
        print "Path:", args.path
        print "Path length:", len(args.path), '\n'

    if args.return_wif:
        print mnemonic_to_wif(mnemonic, passphrase, args.path)
    elif args.return_key:
        print mnemonic_to_key(mnemonic, passphrase, args.path)
    else:
        print mnemonic_to_address(mnemonic, passphrase, args.path)
