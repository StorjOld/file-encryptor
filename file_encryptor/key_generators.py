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

import hashlib
import hmac

from file_encryptor.settings import CHUNK_SIZE, DEFAULT_HMAC_PASSPHRASE


def sha256_file(path):
    """Calculate sha256 hex digest of a file.

    :param path: The path of the file you are calculating the digest of.
    :type path: str
    :returns: The sha256 hex digest of the specified file.
    :rtype: builtin_function_or_method
    """
    h = hashlib.sha256()

    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            h.update(chunk)

    return h.hexdigest()


def key_from_file(filename, passphrase):
    """Calculate convergent encryption key.

    This takes a filename and an optional passphrase.
    If no passphrase is given, a default is used.
    Using the default passphrase means you will be
    vulnerable to confirmation attacks and
    learn-partial-information attacks.

    :param filename: The filename you want to create a key for.
    :type filename: str
    :param passphrase: The passphrase you want to use to encrypt the file.
    :type passphrase: str or None
    :returns: A convergent encryption key.
    :rtype: str
    """
    hexdigest = sha256_file(filename)

    if passphrase is None:
        passphrase = DEFAULT_HMAC_PASSPHRASE

    return keyed_hash(hexdigest, passphrase)


def keyed_hash(digest, passphrase):
    """Calculate a HMAC/keyed hash.

    :param digest: Digest used to create hash.
    :type digest: str
    :param passphrase: Passphrase used to generate the hash.
    :type passphrase: str
    :returns: HMAC/keyed hash.
    :rtype: str
    """
    encodedPassphrase = passphrase.encode()
    encodedDigest = digest.encode()

    return hmac.new(encodedPassphrase, encodedDigest, hashlib.sha256).digest()
