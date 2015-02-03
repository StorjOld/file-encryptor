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

from Crypto.Cipher import AES
from Crypto.Util import Counter
from file_encryptor.settings import CHUNK_SIZE

from file_encryptor import key_generators


def encrypt_file_inline(filename, passphrase):
    """Encrypt file inline, with an optional passphrase.

    If you set the passphrase to None, a default is used.
    This will make you vulnerable to confirmation attacks
    and learn-partial-information attacks.

    :param filename: The name of the file to encrypt.
    :type filename: str
    :param passphrase: The passphrase used to decrypt the file.
    :type passphrase: str or None
    :returns: The key required to decrypt the file.
    :rtype: str
    """
    key = key_generators.key_from_file(filename, passphrase)

    inline_transform(filename, key)

    return key


def decrypt_file_inline(filename, key):
    """Decrypt file inline with given key.

    The given key must be the same that was
    returned by encrypt_file_inline.

    :param filename: The name of the file to decrypt.
    :type filename: str
    :param key: The key used to decrypt the file.
    :type key: str
    """
    inline_transform(filename, key)


def decrypt_generator(filename, key):
    """Stream decrypted file with given key.

    The given key must be the same that was
    returned by encrypt_file_inline.

    :param filename: The name of the file to decrypt.
    :type filename: str
    :param key: The key used to decrypt the file.
    :type key: str
    :returns: A generator that streams decrypted file chunks.
    :rtype: generator
    """
    for chunk, _ in iter_transform(filename, key):
        yield chunk


def inline_transform(filename, key):
    """Encrypt file inline.

    Encrypts a given file with the given key,
    and replaces it directly without any extra
    space requirement.

    :param filename: The name of the file to encrypt.
    :type filename: str
    :param key: The key used to encrypt the file.
    :type key: str
    """
    pos = 0
    for chunk, fp in iter_transform(filename, key):
        fp.seek(pos)
        fp.write(chunk)
        fp.flush()
        pos = fp.tell()


def iter_transform(filename, key):
    """Generate encrypted file with given key.

    This generator function reads the file
    in chunks and encrypts them using AES-CTR,
    with the specified key.

    :param filename: The name of the file to encrypt.
    :type filename: str
    :param key: The key used to encrypt the file.
    :type key: str
    :returns: A generator that produces encrypted file chunks.
    :rtype: generator
    """
    # We are not specifying the IV here.
    aes = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))

    with open(filename, 'rb+') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            yield aes.encrypt(chunk), f
