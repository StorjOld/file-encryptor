#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Storj Labs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
import tempfile
import os

from file_encryptor import key_generators


class TestKeyGenerators(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp()

        self.sample1 = os.path.join(self.directory, 'super1.txt')
        self.sample2 = os.path.join(self.directory, 'super2.txt')
        self.sample3 = os.path.join(self.directory, 'frowny.txt')

        with open(self.sample1, 'wb') as f:
            f.write('Superstar!\n'.encode())

        with open(self.sample2, 'wb') as f:
            f.write('Superstar!\n'.encode())

        with open(self.sample3, 'wb') as f:
            f.write('Frowny face :(\n'.encode())

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
            key_generators.key_from_file(self.sample1, 'Shh!'),
            key_generators.key_from_file(self.sample2, 'Hello'))

    def test_different_files_yield_different_keys(self):
        self.assertNotEqual(
            key_generators.key_from_file(self.sample1, None),
            key_generators.key_from_file(self.sample3, None))
