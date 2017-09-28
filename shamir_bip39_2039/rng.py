import sys
import random

class RNG(object):
    """Your PRNG of choice. Implement the methods below."""
    
    def __init__(self, max_int=None):
        pass

    def random_int(self):
        raise NotImplementedError("Must implement")

class SystemRNG(RNG):
    """Use the system RNG"""
    
    def __init__(self, max_int=None):

        if max_int is None:
            max_int = sys.maxint
        self.max_int = max_int
        self.rng = random.SystemRandom()
        
    def random_int(self):
        """Generate a random integer"""
        return self.rng.randint(0, self.max_int)
