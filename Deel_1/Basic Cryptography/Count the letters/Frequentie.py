
from collections import defaultdict
from wordfreq import zipf_frequency

ciphertext = "qnb{vsi-fihczlnb-dlyi-vsi-fibv-plaahib-fi-zv-l-hzici-plaahi-mr-l-frtbbihb-plaahi}"

def get_pattern(word):
    mapping = {}
    pattern = []
    next_number = 0

    for letter in word:
        if letter not in mapping:
            mapping[letter] = next_number
            next_number += 1

        pattern.append(mapping[letter])

    return tuple(pattern)


def test_mapping(cipherword, plainword, mapping):
    new_mapping = mapping.copy()

    for c, p in zip(cipherword, plainword):
        if c in new_mapping:
            if new_mapping[c] != p:
                return None
        else:
            if p in new_mapping.values():
                return None

            new_mapping[c] = p

    return new_mapping


def solve(ciphertext):
    body = ciphertext.split("{")[1].split("}")[0]
    cipher_words = list(dict.fromkeys(body.split("-")))

    with open("wordlist.txt", encoding="utf-8") as file:
        words = [line.strip().lower() for line in file]

    # Group dictionary words by pattern
    word_patterns = defaultdict(list)

    for word in words:
        if not word.isalpha():
            continue

        # Ignore extremely uncommon dictionary entries
        score = zipf_frequency(word, "en")

        if score < 2.5:
            continue

        key = (len(word), get_pattern(word))
        word_patterns[key].append(word)

    # Try common words first
    for candidates in word_patterns.values():
        candidates.sort(
            key=lambda w: zipf_frequency(w, "en"),
            reverse=True
        )

    candidates = {}

    for cword in cipher_words:
        key = (len(cword), get_pattern(cword))
        candidates[cword] = word_patterns.get(key, [])

    # Known flag prefix: qnb -> cns
    mapping = {"q": "c", "n": "n", "b": "s"}

    def backtrack(remaining, mapping):
        if not remaining:
            return mapping

        # Choose the word with fewest valid candidates
        best_word = None
        best_options = None

        for cword in remaining:
            options = []

            for pword in candidates[cword]:
                new_mapping = test_mapping(
                    cword, pword, mapping
                )

                if new_mapping is not None:
                    options.append(new_mapping)

            if not options:
                return None

            if best_options is None or len(options) < len(best_options):
                best_word = cword
                best_options = options

        next_words = [
            w for w in remaining if w != best_word
        ]

        # Try candidates, and backtrack on failure
        for new_mapping in best_options:
            solution = backtrack(next_words, new_mapping)

            if solution is not None:
                return solution

        return None

    solution = backtrack(cipher_words, mapping)

    if solution is None:
        print("No solution found")
        return

    decoded = ""

    for char in ciphertext:
        decoded += solution.get(char, char)

    print("Decoded:", decoded)
    print("Mapping:", solution)


solve(ciphertext)
