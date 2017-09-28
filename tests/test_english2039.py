from shamir_bip39_2039 import english2039

def test_english2039():

    assert len(english2039.word_dict) == 2039
    for k in english2039.word_dict.keys():
        assert english2039.word_inv_dict[english2039.word_dict[k]] == k
