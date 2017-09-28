from english2039 import word_dict, word_inv_dict
from hashlib import sha256

def mnemonic_to_bits(mnemonic):
    """Convert a mnemonic to a bitstring"""
    
    return ''.join(['{0:011b}'.format(word_inv_dict[w]-1) for w in mnemonic])

def bits_to_mnemonic(bitstring):
    """Convert a bitstring to a mnemonic"""
    
    n = len(bitstring) / 11
    return [word_dict[int(bitstring[(i*11):(i+1)*11],2)+1] for i in range(n)]

def compute_mnemonic_lengths(len_bits):
    """Compute valid lengths for the components of mnemonics"""
    
    len_cs = len_bits / 32
    len_ms = (len_cs + len_bits) / 11

    return len_ms, len_cs

def compute_checksum(bitstring, len_checksum):
    """Compute the checksum for a mnemonic"""
    
    len_hex_string = len(bitstring) / 4
    format_str = '{0:0>' + ('%d' % len_hex_string) + 'X}'
    hex_str = format_str.format(int(bitstring, 2))
    hash = sha256(hex_str.decode('hex')).hexdigest()
    
    return '{0:08b}'.format(int(hash[:2],16))[:len_checksum]

def check_mnemonic_checksum(mnemonic):
    """Check that a mnemonic has a valid checksum"""
    
    bits = mnemonic_to_bits(mnemonic)
    len_bits = len(bits)
    len_ms, len_cs = compute_mnemonic_lengths(len_bits)

    return compute_checksum(bits[:(len_bits - len_cs)], len_cs) == bits[-len_cs:]

def complete_partial_mnemonic(partial_mnemonic):
    """Append the checksum to a partial mnemonic"""
    
    bits = mnemonic_to_bits(partial_mnemonic)
    len_bits = len(bits) + 11
    len_ms, len_cs = compute_mnemonic_lengths(len_bits)

    bits += '0'*(11-len_cs)
    checksum = compute_checksum(bits, len_cs)
    mnemonic = bits_to_mnemonic(bits + checksum)
    assert check_mnemonic_checksum(mnemonic)

    return mnemonic
