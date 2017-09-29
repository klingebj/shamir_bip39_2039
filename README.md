# shamir_bip39_2039
A simple tool for generating and manipulating BIP39 mnemonics with special properties that make it easy to use the 2-out-of-3 Shamir's secret sharing algorithm (SSS) where the *shares are also each themselves valid BIP39 mnemonics*.

## Overview

Rather than full-featured this is meant to be a short and extremely simple implementation that you can (actually) audit in its entirety and trust with your private keys. The only external libraries used are *sys*, *random*, *hashlib.sha256*. If you don't trust your system RNG you can supply your own.

The code breaks up a mnemonic into three SSS shares that are also each themselves valid mnemonics. Someone coming into possession of a share will have no immediate indication of whether it is a share or is itself a mnemonic. **Bonus**: you can use the share-as-mnemonic property to create trip-wires to reveal if a share has been compromised (by funding a honeypot at a corresponding BIP39 bitcoin address, for example) 

## Details

The package uses what we will call 'BIP39-2039' mnemonics. BIP39-2039 mnemonics are BIP39 mnemonics with some extra properties

- BIP39-2039 mnemonics use a dictionary of size 2039 (a prime number) instead of size 2048 (used in BIP39 mnemonics)
- All BIP39-2039 mnemonics are valid BIP39 mnemonics (so you can use them with your hardware wallet, etc)
- All BIP39-2039 mnemonics can be easily shared with SSS, where the *shares are also valid BIP39-2039 mnemonics* (and therefore also valid BIP39 mnemonics)
- BIP39-2039 mnemonics of length N are determined by the first N-1 words. So for example when creating a 24-word mnemonic you only get to choose 23 words. The last word is reserved as a special checksum.

**NB**: The following words are excluded from the BIP39-2039 dictionary because it is easier to use a very simple version of SSS with a dictionary of size 2039 (a prime number) than of size 2048 (used in BIP39 mnemonics). Make sure your mnemonics don't include these words. Code for generating compatible mnemonics is included.

The blacklist: "year", "yellow", "you", "young", "youth", "zebra", "zero", "zone", and "zoo"

## Examples

It is easy to create a BIP39-2039 mnemonic

```
mnemonic = generate_mnemonic(length=12)
print "Mnemonic:", mnemonic
```

```
Mnemonic: ['patrol', 'ankle', 'hire', 'long', 'present', 'seminar',
           'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']
```

Under the hood we are randomly choosing the first eleven of the twelve words (alternatively you can specify them yourself having chosen them any way you like). The twelfth word is a checksum determined by the first eleven. The mnemonic can then be broken into three shares, which are themselves valid mnemonics

```
shares = mnemonic_to_shares(mnemonic)
print "Shares:", shares
```

```
Shares: {'share1': ['tornado', 'actress', 'measure', 'service', 'learn', 'blush',
                    'space', 'because', 'drum', 'hockey', 'negative', 'absorb'],
         'share2': ['client', 'win', 'pond', 'aisle', 'fatal', 'hockey',
                    'bronze', 'twelve', 'charge', 'bubble', 'income', 'access'],
         'share3': ['humor', 'visual', 'shield', 'ecology', 'choose', 'scare',
                    'gun', 'sell', 'another', 'snack', 'eye', 'able']}
```

Recall that each of these shares is also a valid BIP39-2039 mnemonic! You can use them as you would any other BIP39 mnemonic. Finally, the original mnemonic can be recovered from any two of the three shares

```
print "Recovered from shares 1 and 2:", shares_to_mnemonic(share1=shares['share1'], share2=shares['share2'])
```

```
Recovered from shares 1 and 2: ['patrol', 'ankle', 'hire', 'long', 'present','seminar',
                                'lunar', 'derive', 'gauge', 'romance', 'relief', 'acid']
```
