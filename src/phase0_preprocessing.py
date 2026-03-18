"""
Phase 0: Preprocessing
- Converts plain text into 100×100 grid
- Adds padding to short words
- Interleaves random filler words
"""

import random
import hashlib
from typing import List, Tuple

class Phase0Preprocessing:
    """
    Handles text preprocessing before encryption.
    """
    
    def __init__(self, seed: bytes = None):
        """
        Initialize with a seed for pseudo-random generation.
        If no seed is given, uses os.urandom.
        """
        if seed is None:
            seed = random.randbytes(32)
        self.seed = seed
        self.rng = random.Random(seed)
        
        # Load filler words list (simulated for now)
        self.filler_words = self._load_filler_words()
    
    def _load_filler_words(self) -> List[str]:
        """
        Load or generate filler words list.
        Currently creating a simulated list.
        """
        common_words = [
            "the", "and", "for", "with", "but", "not", "you", "this", "have",
            "from", "they", "will", "one", "all", "can", "get", "has", "was",
            "are", "had", "their", "what", "there", "been", "into", "more",
            "some", "time", "other", "such", "than", "then", "them", "these"
        ]
        # Duplicate to have enough words
        return common_words * 20
    
    def _pad_word(self, word: str, dictionary: List[str]) -> str:
        """
        If word has less than 5 letters, add an extra character.
        The extra character is calculated as sum of positions of its letters
        in the base alphabet.
        """
        if len(word) >= 5:
            return word
        
        # Simulated alphabet for position calculation
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        total = 0
        for letter in word.lower():
            if letter in alphabet:
                total += alphabet.index(letter) + 1
        
        # Determine extra character (simplified)
        index = total % len(dictionary)
        return word + dictionary[index][0]  # First letter of chosen word
    
    def _generate_filler_word(self) -> str:
        """Generate a random 6-9 letter filler word."""
        return self.rng.choice(self.filler_words)
    
    def process(self, plain_text: str) -> Tuple[List[List[str]], bytes]:
        """
        Process plain text and return:
        - 100x100 grid of characters (list of lists)
        - Seed used (so receiver can reproduce the shuffling)
        """
        # 1. Split into words (by spaces)
        real_words = plain_text.split()
        
        # 2. Apply padding to short words
        padded_words = []
        for word in real_words:
            padded = self._pad_word(word, self.filler_words)
            padded_words.append(padded)
        
        # 3. Calculate how many words needed (estimate)
        # 100x100 = 10000 characters, each word + space ~7-10 chars → ~1000-1500 words
        words_needed = 1200  # Adjustable
        
        # 4. Generate filler words
        filler_words = []
        for _ in range(words_needed - len(padded_words)):
            filler_words.append(self._generate_filler_word())
        
        # 5. Randomly shuffle real and filler words
        all_words = padded_words + filler_words
        self.rng.shuffle(all_words)
        
        # 6. Form continuous text
        continuous_text = " ".join(all_words)
        
        # Ensure exactly 10000 characters
        if len(continuous_text) < 10000:
            missing = 10000 - len(continuous_text)
            continuous_text += "x" * missing
        else:
            continuous_text = continuous_text[:10000]
        
        # 7. Create 100x100 grid
        grid = []
        for i in range(100):
            row = list(continuous_text[i*100:(i+1)*100])
            grid.append(row)
        
        return grid, self.seed