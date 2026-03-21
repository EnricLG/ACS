"""
Phase 0: Preprocessing
- Converts plain text into 100×100 grid
- Pads real words to at least 6 characters
- Filler items: words (6-9 letters), names, cities, times, numbers (5 digits)
- Dynamically adds filler items to exactly fill 10000 characters (including spaces)
- Final grid contains only words/items and spaces, no extra 'x'
"""

import random
from typing import List, Tuple

class Phase0Preprocessing:
    """
    Handles text preprocessing before encryption.
    All filler items are strings (can be words, names, times, numbers).
    """

    def __init__(self, seed: bytes = None):
        if seed is None:
            seed = random.randbytes(32)
        self.seed = seed
        self.rng = random.Random(seed)

        # Load filler items (all are strings)
        self.filler_items = self._load_filler_items()

    def _load_filler_items(self) -> List[str]:
        """Return a list of filler strings: words, names, cities, times, numbers."""
        items = []

        # 1. Words (6-9 letters) – same as before
        words_6_9 = [
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
        items.extend(words_6_9)

        # 2. Names (50 male + 50 female)
        names_male = [
            "Liam", "Noah", "Oliver", "James", "Elijah", "William", "Henry", "Lucas", "Benjamin", "Theodore",
            "Mateo", "Levi", "Sebastian", "Daniel", "Jack", "Michael", "Alexander", "Owen", "Samuel", "Ethan",
            "David", "Joseph", "John", "Jackson", "Julian", "Christopher", "Luke", "Andrew", "Gabriel", "Joshua",
            "Isaac", "Leo", "Grayson", "Ezra", "Carter", "Thomas", "Dylan", "Charles", "Caleb", "Nathan",
            "Ryan", "Angel", "Lincoln", "Anthony", "Adam", "Christian", "Josiah", "Jonathan", "Landon", "Isaiah"
        ]
        names_female = [
            "Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella", "Ava", "Mia", "Evelyn", "Luna",
            "Harper", "Camila", "Sofia", "Eleanor", "Elizabeth", "Emily", "Chloe", "Mila", "Violet", "Penelope",
            "Abigail", "Ella", "Avery", "Hazel", "Nora", "Lily", "Grace", "Victoria", "Sofia", "Zoe",
            "Stella", "Aria", "Layla", "Madison", "Ellie", "Natalie", "Leah", "Hannah", "Aubrey", "Brooklyn",
            "Addison", "Audrey", "Bella", "Claire", "Skylar", "Anna", "Caroline", "Genesis", "Savannah", "Kennedy"
        ]
        items.extend(names_male)
        items.extend(names_female)

        # 3. Cities (100 cities)
        cities = [
            "Amsterdam", "Athens", "Atlanta", "Auckland", "Baghdad", "Bangalore", "Bangkok", "Barcelona", "Berlin", "Bogota",
            "Boston", "Brussels", "Bucharest", "Budapest", "BuenosAires", "Cairo", "Cancun", "CapeTown", "Caracas", "Casablanca",
            "Chennai", "Chicago", "MexicoCity", "Copenhagen", "Dallas", "Delhi", "Dubai", "Dublin", "Istanbul", "Frankfurt",
            "Guangzhou", "Guadalajara", "Hamburg", "Hanoi", "Houston", "Stockholm", "Jakarta", "Jerusalem", "Johannesburg", "Karachi",
            "Kyiv", "KualaLumpur", "Kuwait", "Lagos", "Lahore", "Lima", "Lisbon", "London", "LosAngeles", "Madrid",
            "Manila", "Melbourne", "Miami", "Milan", "Montreal", "Moscow", "Mumbai", "Munich", "Nairobi", "NewOrleans",
            "NewYork", "Osaka", "Oslo", "Paris", "Beijing", "Philadelphia", "Phoenix", "Prague", "Port-au-Prince", "Rio",
            "Rome", "SanFrancisco", "Santiago", "SaoPaulo", "Seattle", "Seoul", "Shanghai", "Singapore", "Sofia", "Sydney",
            "Taipei", "Tehran", "TelAviv", "Tokyo", "Toronto", "Warsaw", "Vienna", "Washington", "Zurich", "AbuDhabi",
            "AddisAbaba", "Birmingham", "Kolkata", "GuatemalaCity", "Dhaka", "Doha", "Medellin", "Riyadh", "StPetersburg", "Tijuana"
        ]
        items.extend(cities)

        # 4. Times (HH:MM format)
        times = []
        for hour in range(24):
            for minute in [0, 15, 30, 45]:
                times.append(f"{hour:02d}:{minute:02d}")
        items.extend(times)

        # 5. Numbers (5 digits each)
        numbers_5digit = [
            "48219", "73506", "29184", "56723", "84901", "12378", "90546", "37815", "64290", "21657",
            "75943", "83412", "47068", "19532", "60387", "52841", "97605", "34129", "81074", "25763",
            "69418", "43985", "17206", "86539", "52097", "71384", "36821", "94056", "27543", "68970",
            "43158", "80427", "15792", "62340", "79815", "35264", "91680", "47329", "68501", "23974",
            "56083", "81746", "39425", "70291", "14837", "96520", "52173", "83659", "47916", "20865"
        ]
        items.extend(numbers_5digit)

        return items

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
        all_items = padded_real[:]  # list of strings (real words)
        total_len = sum(len(item) for item in all_items) + (len(all_items) - 1)

        # 3. Add filler items until we reach or exceed 10000
        while total_len < 10000:
            filler = self.rng.choice(self.filler_items)
            new_len = total_len + len(filler) + 1  # +1 for the space before it
            if new_len <= 10000:
                all_items.append(filler)
                total_len = new_len
            else:
                # Adding whole item would exceed; break the last item to fit exactly
                remaining = 10000 - total_len - 1
                if remaining > 0:
                    part = filler[:remaining]
                    all_items.append(part)
                    total_len += len(part) + 1
                break

        # Join with spaces and ensure exactly 10000 characters
        continuous = " ".join(all_items)
        if len(continuous) < 10000:
            continuous += " " * (10000 - len(continuous))

        # Create 100x100 grid
        grid = [list(continuous[i*100:(i+1)*100]) for i in range(100)]
        return grid, self.seed