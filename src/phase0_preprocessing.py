"""
Phase 0: Preprocessing
- Converts plain text into 100×100 grid
- Pads real words to at least 6 characters
- Filler words are taken from a fixed list of 6-9 letter words
- All words in final grid have 6-9 characters
"""

import random
import hashlib
from typing import List, Tuple

class Phase0Preprocessing:
    """
    Handles text preprocessing before encryption.
    Final words always have 6-9 characters.
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
        
        # Load fixed list of filler words (6-9 letters)
        self.filler_words = self._get_filler_words()
    
    def _get_filler_words(self) -> List[str]:
        """
        Returns a fixed list of words with 6-9 letters.
        """
        return [
            "between", "through", "however", "therefore", "meanwhile",
            "together", "although", "complete", "consider", "continue",
            "decision", "direction", "distance", "election", "employee",
            "essential", "eventually", "financial", "following", "generally",
            "important", "including", "individual", "information", "interesting",
            "knowledge", "language", "marketing", "material", "operation",
            "opportunity", "organization", "particular", "political", "population",
            "position", "positive", "possible", "practical", "president",
            "pressure", "previous", "primarily", "principle", "probably",
            "problem", "process", "product", "program", "progress",
            "property", "propose", "protect", "provide", "purpose",
            "quality", "question", "reaction", "reality", "receive",
            "recently", "recognize", "recommend", "reference", "reflect",
            "regardless", "register", "regular", "relation", "relative",
            "release", "relevant", "religious", "remember", "remove",
            "replace", "represent", "require", "research", "resource",
            "respond", "response", "responsibility", "responsible", "result",
            "return", "reveal", "review", "revolution", "schedule",
            "security", "serious", "service", "several", "significant",
            "similar", "situation", "society", "someone", "something",
            "sometimes", "somewhere", "statement", "strategy", "strength",
            "student", "subject", "success", "successful", "suddenly",
            "suggest", "summer", "supply", "support", "suppose",
            "surface", "surprise", "system", "teacher", "technology",
            "television", "temperature", "tendency", "theory", "therefore",
            "these", "things", "thinking", "thought", "throughout",
            "thousand", "together", "tomorrow", "toward", "tradition",
            "training", "transfer", "travel", "trouble", "truly",
            "understand", "university", "unless", "unlikely", "until",
            "welcome", "whatever", "whenever", "wherever", "whether",
            "which", "whoever", "within", "without", "wonderful",
            "working", "would", "writing", "written", "young",
            "yourself", "yourselves"
        ]
    
    def _pad_real_word(self, word: str) -> str:
        """
        Pads real word to at least 6 characters.
        If word already has 6+ letters, returns unchanged.
        If word has less than 6 letters, adds characters deterministically.
        """
        if len(word) >= 6:
            return word
        
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        padded = word
        while len(padded) < 6:
            total = 0
            for letter in padded.lower():
                if letter in alphabet:
                    total += alphabet.index(letter) + 1
            next_char = alphabet[total % 26]
            padded += next_char
        return padded
    
    def process(self, plain_text: str) -> Tuple[List[List[str]], bytes]:
        """
        Process plain text and return:
        - 100x100 grid of characters (list of lists)
        - Seed used (so receiver can reproduce the shuffling)
        """
        # 1. Split real words
        real_words = plain_text.split()
        
        # 2. Pad real words
        padded_real = [self._pad_real_word(w) for w in real_words]
        
        # 3. Estimate total words needed (roughly 1200 to fill 10000 chars)
        words_needed = 1200
        
        # 4. Generate filler words (already 6-9 letters)
        filler_needed = max(0, words_needed - len(padded_real))
        filler_words = self.rng.choices(self.filler_words, k=filler_needed)
        
        # 5. Combine and shuffle
        all_words = padded_real + filler_words
        self.rng.shuffle(all_words)
        
        # 6. Form continuous text
        continuous = " ".join(all_words)
        if len(continuous) < 10000:
            continuous += "x" * (10000 - len(continuous))
        else:
            continuous = continuous[:10000]
        
        # 7. Create grid
        grid = [list(continuous[i*100:(i+1)*100]) for i in range(100)]
        return grid, self.seed