from BigramFreqs import *
from collections import Counter
from cipher_solver.simple import SimpleSolver
from itertools import combinations
from secretpy import Vigenere
from sortedcontainers import SortedDict
import string


class AutomaticDecrypter:
    def __init__(self, text, n_grams=2, max_keylen=10):
        # Sanitize input text (make all lowercase letters)
        self.ctext = ''.join(c.lower() for c in text if c.isalpha())

        self.ORIGINAL_TEXT = text
        self.N = n_grams
        self.MAX_KEYLEN = max_keylen # len(self.ctext) // n_grams
        self.IOC_THRESHOLD = 0.05

        self.ALPHABET = string.ascii_lowercase

    def solve(self):
        ptext = None
        key = "[NO KEY]"

        # Is the cipher text monoalphabetic or polyalphabetic?
        if self.index_of_coincidence(self.ctext) < self.IOC_THRESHOLD:
            # Polyalphabetic cipher
            key, ptext = self.kasiski()
        else:
            # Monoalphabetic Cipher
            ptext = self.substitution()

        return key, ptext, self.best_langs(ptext)

    def kasiski(self):
        ALL_NGRAMS = list(map(''.join, combinations(self.ALPHABET, self.N)))

        keys_to_ptext = dict()
        for keylen in range(2, self.MAX_KEYLEN):
            chunks = [
                [self.ctext[j] for j in range(i, len(self.ctext), keylen)]
                for i in range(keylen)
            ]

            chars_to_weights = [dict() for _ in range(keylen)]
            for idx, (x, y) in enumerate(zip(chunks, chunks[1:])):
                max_score = 0
                max_key = ""

                ctext_bigrams = list(map(''.join, zip(x, y)))
                for key in ALL_NGRAMS:
                    for bigram_freqs in (BigramFreqs.EN, BigramFreqs.FR):
                        score = sum(
                            bigram_freqs[Vigenere().decrypt(enc, key)]
                            for enc in ctext_bigrams
                        )
                        if score > max_score:
                            max_score = score
                            max_key = key

                for key_idx, c in enumerate(max_key):
                    if idx + key_idx >= keylen:
                        break

                    if c in chars_to_weights[idx + key_idx]:
                        chars_to_weights[idx + key_idx][c] = max(
                            chars_to_weights[idx + key_idx][c], max_score)
                    else:
                        chars_to_weights[idx + key_idx][c] = max_score

            # Determine final key from possibilities (by weight)
            top_key = "".join(
                max(char_to_weight, key=char_to_weight.get)
                for char_to_weight in chars_to_weights
            )

            keys_to_ptext[top_key] = Vigenere().decrypt(self.ctext, top_key)

        best_solve = None
        best_ioc = 0
        for key, ptext in keys_to_ptext.items():
            if (ioc := self.index_of_coincidence(ptext)) > best_ioc:
                best_solve = (key, ptext)
                best_ioc = ioc

        return best_solve

    def substitution(self):
        solver = SimpleSolver(self.ORIGINAL_TEXT)
        solver.solve()
        return solver.plaintext()

    def best_langs(self, text=None):
        """Returns best fitting languages from index of coincidence"""
        # Margin of error for IOC
        IOC_TOLERANCE = 0.012
        # Dict of language to avg index of coincidence, sorted from min to max
        IOC_TO_LANG = SortedDict({
            0.0667: "EN",
            0.0778: "FR",
        })

        if text is None:
            text = self.ctext

        # Does input represent cleartext?
        if (ioc := self.index_of_coincidence(text)) < self.IOC_THRESHOLD:
            return None

        best_langs = [
            IOC_TO_LANG[key]
            for key in IOC_TO_LANG.irange(ioc - IOC_TOLERANCE,
                                          ioc + IOC_TOLERANCE)
        ]

        return best_langs

    def index_of_coincidence(self, text=None):
        """Returns the index of coincidence of input text"""
        if text is None:
            text = self.ctext

        N = len(text)
        char_counts = Counter(text)
        return (1 / (N * (N - 1))) * sum (
            char_counts[c] * (char_counts[c] - 1)
            for c in self.ALPHABET
        )
