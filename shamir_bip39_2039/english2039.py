import pkg_resources

# Get BIP39-2039 dictionary

words = pkg_resources.resource_string(
    'shamir_bip39_2039', 'english.txt').split('\n')[:2039]

blacklist = ["year", "yellow", "you", "young",
             "youth", "zebra", "zero", "zone", "zoo"]

for word in blacklist:
    assert word not in words

word_dict = dict(zip(range(1, 2041), words))
assert len(word_dict) == 2039
word_inv_dict = {v: k for k, v in word_dict.items()}
