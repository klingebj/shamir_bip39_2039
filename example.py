from shamir_bip39_2039.api import mnemonic_to_shares, shares_to_mnemonic, generate_mnemonic, check_mnemonic_checksum

mnemonic = generate_mnemonic(length=12)

print "Mnemonic:", mnemonic
# Mnemonic: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

shares = mnemonic_to_shares(mnemonic)

print "Shares valid mnemonics?", check_mnemonic_checksum(
    shares['share1']) and check_mnemonic_checksum(
        shares['share2']) and check_mnemonic_checksum(shares['share3'])
# Shares valid mnemonics? True

print "\nShares:", shares
# Shares: {'share1': ['tornado', 'actress', 'measure', 'service', 'learn', 'blush',
#                    'space', 'because', 'drum', 'hockey', 'negative', 'absorb'],
#         'share2': ['client', 'win', 'pond', 'aisle', 'fatal', 'hockey',
#                    'bronze', 'twelve', 'charge', 'bubble', 'income', 'access'],
#         'share3': ['humor', 'visual', 'shield', 'ecology', 'choose', 'scare',
#                    'gun', 'sell', 'another', 'snack', 'eye', 'able']}

print "\nRecovered from shares 1 and 2:", shares_to_mnemonic(
    share1=shares['share1'], share2=shares['share2'])
# Recovered from shares 1 and 2: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

print "Recovered from shares 1 and 3:", shares_to_mnemonic(
    share1=shares['share1'], share3=shares['share3'])
# Recovered from shares 1 and 3: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

print "Recovered from shares 2 and 3:", shares_to_mnemonic(
    share2=shares['share2'], share3=shares['share3'])
# Recovered from shares 2 and 3: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']
