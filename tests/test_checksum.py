from shamir_bip39_2039 import mnemonic
from shamir_bip39_2039 import rng
from shamir_bip39_2039 import checksum


def test_mnemonic_to_bits():

    r = rng.LCG()

    for length in mnemonic.allowed_mnemonic_lengths:
        for _ in range(100):
            test_mnemonic = mnemonic.generate_mnemonic(length, rng=r)
            bitstring = checksum.mnemonic_to_bits(test_mnemonic)
            assert len(bitstring) == length * 11
            assert int(bitstring, 2) > -1
            for u, v in zip(test_mnemonic,
                            checksum.bits_to_mnemonic(bitstring)):
                assert u == v


def test_checksum_bip39():

    # See https://github.com/trezor/python-mnemonic/blob/master/vectors.json

    test_vectors = {
        '00000000000000000000000000000000':
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        '80808080808080808080808080808080':
        "letter advice cage absurd amount doctor acoustic avoid letter advice cage above",
        '000000000000000000000000000000000000000000000000':
        'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon agent',
        '808080808080808080808080808080808080808080808080':
        'letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter always',
        '9e885d952ad362caeb4efe34a8e91bd2':
        'ozone drill grab fiber curtain grace pudding thank cruise elder eight picnic',
        '6610b25967cdcca9d59875f5cb50b0ea75433311869e930b':
        'gravity machine north sort system female filter attitude volume fold club stay feature office ecology stable narrow fog',
        '68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c':
        'hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length',
        'c0ba5a8e914111210f2bd131f3d5e08d':
        'scheme spot photo card baby mountain device kick cradle pact join borrow',
        '6d9be1ee6ebd27a258115aad99b7317b9c8d28b6d76431c3':
        'horn tenant knee talent sponsor spell gate clip pulse soap slush warm silver nephew swap uncle crack brave',
        '9f6a2878b2520799a44ef18bc7df394e7061a224d2c33cd015b157d746869863':
        'panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside',
        '23db8160a31d3e0dca3688ed941adbf3':
        'cat swing flag economy stadium alone churn speed unique patch report train',
        '8197a4a47f0425faeaa69deebc05ca29c0a5b5cc76ceacc0':
        'light rule cinnamon wrap drastic word pride squirrel upgrade then income fatal apart sustain crack supply proud access',
        '066dca1a2bb7e8a1db2832148ce9933eea0f3ac9548d793112d9a95c9407efad':
        'all hour make first leader extend hole alien behind guard gospel lava path output census museum junior mass reopen famous sing advance salt reform',
        'f30f8c1da665478f49b001d94c5fc452':
        'vessel ladder alter error federal sibling chat ability sun glass valve picture',
        'c10ec20dc3cd9f652c7fac2f1230f7a3c828389a14392f05':
        'scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump',
        'f585c11aec520db57dd353c69554b21a89b20fb0650966fa0a9d6f74fd989d8f':
        'void come effort suffer camp survey warrior heavy shoot primary clutch crush open amazing screen patrol group space point ten exist slush involve unfold'
    }

    for entropy in test_vectors:
        len_bits = len(entropy) * 4
        cs = len_bits / 32
        ms = (len_bits + cs) / 11
        bitstring = ('{0:0%db}' % len_bits).format(int(entropy, 16))
        checksum_string = checksum.compute_checksum(bitstring, cs)
        for u, v in zip(
                checksum.bits_to_mnemonic(bitstring + checksum_string),
                test_vectors[entropy].split(' ')):
            assert u == v
