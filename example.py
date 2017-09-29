from api import mnemonic_to_shares, shares_to_mnemonic, generate_mnemonic, check_mnemonic_checksum

mnemonic = generate_mnemonic(length=12)

print "Mnemonic:", mnemonic
# Mnemonic: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

shares = mnemonic_to_shares(mnemonic)

print "Shares valid mnemonics?", check_mnemonic_checksum(shares['share1']) and check_mnemonic_checksum(shares['share2']) and check_mnemonic_checksum(shares['share3'])
# Shares valid mnemonics? True

print "\nShares:", shares
# Shares: {'share1': ['document', 'direct', 'dilemma', 'hero', 'almost', 'device',
#                     'effort', 'useful', 'all', 'visual', 'fetch', 'absent'],
#          'share2': ['teach', 'initial', 'aware', 'fan', 'give', 'regret',
#                     'analyst', 'pitch', 'private', 'control', 'vintage', 'absurd'],
#          'share3': ['lava', 'power', 'throw', 'demise', 'safe', 'column',
#                     'silver', 'forest', 'extra', 'hand', 'neither', 'accident']}

print "\nRecovered from shares 1 and 2:", shares_to_mnemonic(share1=shares['share1'], share2=shares['share2'])
# Recovered from shares 1 and 2: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

print "Recovered from shares 1 and 3:", shares_to_mnemonic(share1=shares['share1'], share3=shares['share3'])
# Recovered from shares 1 and 3: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']

print "Recovered from shares 2 and 3:", shares_to_mnemonic(share2=shares['share2'], share3=shares['share3'])
# Recovered from shares 2 and 3: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar', 'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']
