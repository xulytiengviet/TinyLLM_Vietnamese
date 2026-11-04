"""Unit tests for mathematical mapping and data hygiene; not model quality."""
import json
import tempfile
import unittest
from pathlib import Path
from tools.base27 import ALPHABET, encode, decode, index_to_trits, trits_to_index
from tools.memory_budget import estimate
from training.prepare_data import prepare, split_of, normalize

class CoreTests(unittest.TestCase):
    def test_27_bijection(self):
        self.assertEqual(decode(encode(ALPHABET)), ALPHABET)
        for i in range(27):
            self.assertEqual(trits_to_index(index_to_trits(i)), i)

    def test_reject_non_alphabet(self):
        with self.assertRaises(ValueError): encode("HELLO WORLD")

    def test_min_five_binary_bits(self):
        self.assertEqual((27-1).bit_length(), 5)

    def test_large_28m_not_in_four_mb(self):
        self.assertFalse(estimate(28900000,4,4,1)["raw_weights_fit"])

    def test_small_model_raw_budget(self):
        self.assertTrue(estimate(118784,8,4,1.5)["raw_weights_fit"])

    def test_nfc(self):
        self.assertEqual(normalize("e\u0301"), "é")

    def test_stable_document_split(self):
        self.assertEqual(split_of("doc-one"), split_of("doc-one"))

    def test_prepare_deduplicates(self):
        r={"cqn":"Tôi","cvnss":"Toiy","codec":"5.0.0","source_id":"x","license":"VERIFY_BEFORE_TRAIN"}
        with tempfile.TemporaryDirectory() as folder:
            src,dst=Path(folder)/"in.jsonl",Path(folder)/"out.jsonl"
            src.write_text(json.dumps(r)+"\n"+json.dumps(r)+"\n",encoding="utf-8")
            m=prepare(src,dst)
            self.assertEqual(m["records"],1)
            self.assertTrue(dst.with_suffix(".manifest.json").exists())
if __name__=="__main__":
    unittest.main()
