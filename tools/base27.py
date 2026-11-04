"""27-symbol ↔ 3 balanced trits: mathematics demo, NOT official CVNSS4.0."""
import argparse, json
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def check_alphabet(a):
    if len(a) != 27 or len(set(a)) != 27:
        raise ValueError("Exactly 27 unique symbols required")

def index_to_trits(i):
    if not isinstance(i, int) or not 0 <= i < 27:
        raise ValueError("Index outside 0..26")
    return (i // 9 - 1, (i // 3) % 3 - 1, i % 3 - 1)

def trits_to_index(t):
    if len(t) != 3 or any(v not in (-1, 0, 1) for v in t):
        raise ValueError("Expected exactly three balanced trits")
    return 9 * (t[0]+1) + 3 * (t[1]+1) + (t[2]+1)

def encode(text, alphabet=ALPHABET):
    check_alphabet(alphabet)
    indices = {c:i for i,c in enumerate(alphabet)}
    try:
        return [index_to_trits(indices[c]) for c in text]
    except KeyError as e:
        raise ValueError("Outside alphabet: " + repr(e.args[0])) from e

def decode(groups, alphabet=ALPHABET):
    check_alphabet(alphabet)
    return "".join(alphabet[trits_to_index(t)] for t in groups)

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("text", nargs="?", default="CVNSS_TERNARY")
    p.add_argument("--alphabet", default=ALPHABET)
    a=p.parse_args()
    trits=encode(a.text,a.alphabet)
    print(json.dumps({"status":"MATH_DEMO_NOT_OFFICIAL_CVNSS",
          "balanced_trits":trits,"roundtrip":decode(trits,a.alphabet),
          "minimum_fixed_binary_bits_per_symbol":5}, ensure_ascii=False, indent=2))
