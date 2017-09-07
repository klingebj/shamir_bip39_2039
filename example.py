from api import mnemonic_to_shares, shares_to_mnemonic
from mnemonic import generate_mnemonic

mnemonic = generate_mnemonic(length=4)

print "Mnemonic:", mnemonic

shares = mnemonic_to_shares(mnemonic)

print "\nShares:", shares

print "\nRecovered from shares 1 and 2:", shares_to_mnemonic(share1=shares['share1'], share2=shares['share2'])
print "Recovered from shares 1 and 3:", shares_to_mnemonic(share1=shares['share1'], share3=shares['share3'])
print "Recovered from shares 2 and 3:", shares_to_mnemonic(share2=shares['share2'], share3=shares['share3'])
