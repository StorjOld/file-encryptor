import unittest
import tempfile
import os

import key_generators

class TestKeyGenerators(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()

        self.sample1 = os.path.join(self.directory, "super1.txt")
        self.sample2 = os.path.join(self.directory, "super2.txt")
        self.sample3 = os.path.join(self.directory, "frowny.txt")

        with open(self.sample1, "wb") as f:
            f.write("Superstar!\n")

        with open(self.sample2, "wb") as f:
            f.write("Superstar!\n")

        with open(self.sample3, "wb") as f:
            f.write("Frowny face :(\n")

    def tearDown(self):
        os.remove(self.sample1)
        os.remove(self.sample2)
        os.remove(self.sample3)
        os.rmdir(self.directory)

    def test_key_generation(self):
        key_generators.key_from_file(self.sample1, None)

    def test_deterministic_key_generation(self):
        self.assertEqual(
            key_generators.key_from_file(self.sample1, None),
            key_generators.key_from_file(self.sample2, None))

    def test_passphrase_does_something(self):
        self.assertNotEqual(
            key_generators.key_from_file(self.sample1, "Shh!"),
            key_generators.key_from_file(self.sample2, "Hello"))

    def test_different_files_yield_different_keys(self):
        self.assertNotEqual(
            key_generators.key_from_file(self.sample1, None),
            key_generators.key_from_file(self.sample3, None))
