# shamir-bip39
A simple implementation of the 2-out-of-3 Shamir's secret sharing algorithm (SSSA) for BIP39-like mnemonics

# Overview

Rather than full-featured this is meant to be a short and extremely simple implementation that you can (actually) audit in its entirety and trust with your private keys. The only libraries used are *sys* and *random*, and these are only used for random number generation. If you don't trust your system RNG you can supply your own.

The code breaks up a mnemonic into three SSSA shares that are also each themselves valid mnemonics. Someone coming into possession of a share will have no immediate indiciation of whether it is a share or is itself a mnemonic. Bonus: you can use the share-as-mnemonic property to create trip-wires to reveal if a share has been compromised (by funding a honeypot at a corresponding BIP39 bitcoin address, for example) 

**NB**: The following words are excluded because it is easier to use a very simple version of SSSA with a dictionary of size 2039 (a prime number) than of size 2048 (used in BIP39 mnemonics). Make sure your mnemonics don't include these words. Code for generating compatible mnemonics is included.

The blacklist: "year", "yellow", "you", "young", "youth", "zebra", "zero", "zone", and "zoo"

# Examples

You can use an existing mnemonic or create a new one

```
mnemonic = generate_mnemonic(length=4)
print "Mnemonic:", mnemonic
```

```
Mnemonic: ['session', 'quiz', 'swamp', 'quantum']
```

The mnemonic can then be broken into three shares, which are themselves mnemonics

```
shares = mnemonic_to_shares(mnemonic)
print "\nShares:", shares
```

```
Shares: {'share1': ['lazy', 'dizzy', 'viable', 'impulse'],
         'share2': ['decade', 'soon', 'arrive', 'crush'],
         'share3': ['various', 'garbage', 'caution', 'walnut']}
```

Finally, the original mnemonic can be recovered from any two of three shares

```
print "\nRecovered from shares 1 and 2:", shares_to_mnemonic(share1=shares['share1'], share2=shares['share2'])
print "Recovered from shares 1 and 3:", shares_to_mnemonic(share1=shares['share1'], share3=shares['share3'])
print "Recovered from shares 2 and 3:", shares_to_mnemonic(share2=shares['share2'], share3=shares['share3'])
```

```
Recovered from shares 1 and 2: ['session', 'quiz', 'swamp', 'quantum']
Recovered from shares 1 and 3: ['session', 'quiz', 'swamp', 'quantum']
Recovered from shares 2 and 3: ['session', 'quiz', 'swamp', 'quantum']
```