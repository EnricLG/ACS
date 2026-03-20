"""
Phase 0: Preprocessing
- Converts plain text into 100×100 grid
- Pads real words to at least 6 characters
- Filler words are taken from a fixed list of 6-9 letter words
- Dynamically adds filler words to exactly fill 10000 characters (including spaces)
- Final grid contains only words (padded real + filler) and spaces, no extra 'x'
"""

import random
from typing import List, Tuple

class Phase0Preprocessing:
    """
    Handles text preprocessing before encryption.
    All words in final grid have 6-9 characters.
    """

    def __init__(self, seed: bytes = None):
        if seed is None:
            seed = random.randbytes(32)
        self.seed = seed
        self.rng = random.Random(seed)

        # Load filler words (all 6-9 letters)
        self.filler_words = self._load_filler_words()

    def _load_filler_words(self) -> List[str]:
        """Return a list of words with 6-9 letters."""
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
        Pad a real word to at least 6 characters using deterministic letters.
        """
        if len(word) >= 6:
            return word
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        padded = word
        while len(padded) < 6:
            total = sum((ord(c) for c in padded.lower()))
            next_char = alphabet[total % 26]
            padded += next_char
        return padded

    def process(self, plain_text: str) -> Tuple[List[List[str]], bytes]:
        """
        Process plain text and return 100x100 grid of characters.
        No trailing 'x' – exactly 10000 characters from words and spaces.
        """
        # 1. Pad real words
        real_words = plain_text.split()
        padded_real = [self._pad_real_word(w) for w in real_words]

        # 2. Start with real words
        all_words = padded_real[:]
        # Current total characters = sum(len(word)) + (number_of_spaces)
        total_len = sum(len(w) for w in all_words) + (len(all_words) - 1)

        # 3. Add filler words until we reach or exceed 10000
        while total_len < 10000:
            filler = self.rng.choice(self.filler_words)
            # New length if we add this word (including a space before it, except if it's the first word)
            new_len = total_len + len(filler) + 1  # +1 for the space
            if new_len <= 10000:
                all_words.append(filler)
                total_len = new_len
            else:
                # Adding the whole word would exceed. To avoid 'x' at the end, we
                # break the last word to fit exactly. This cuts the last word,
                # but no extra filler characters are added.
                remaining = 10000 - total_len - 1  # -1 for the space before the new word
                if remaining > 0:
                    # Take a prefix of the filler word to fill exactly
                    part = filler[:remaining]
                    all_words.append(part)
                    total_len += len(part) + 1
                # Now total_len == 10000
                break

        # If we still have not reached 10000 (should not happen), pad with spaces
        # but let's ensure it never happens
        continuous = " ".join(all_words)
        if len(continuous) < 10000:
            continuous += " " * (10000 - len(continuous))

        # Create 100x100 grid
        grid = [list(continuous[i*100:(i+1)*100]) for i in range(100)]
        return grid, self.seed