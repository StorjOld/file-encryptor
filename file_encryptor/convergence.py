from Crypto.Cipher import AES
from Crypto.Util import Counter
from settings import CHUNK_SIZE

import key_generators

def encrypt_file_inline(filename, passphrase):
    """Encrypt file inline, with an optional passphrase.

    Returns the key that will be required in order to
    decrypt the file.

    If you set the passphrase to None, a default is used.
    This will make you vulnerable to confirmation attacks
    and learn-partial-information attacks.

    """
    k = key_generators.key_from_file(filename, passphrase)

    inline_transform(filename, k)
    
    return k
    # return k.encode("hex")


def decrypt_file_inline(filename, k):
    """Decrypt file inline with key k.

    The given key must be the same that was
    returned by encrypt_file_inline.

    """
    #k = k.decode("hex")
    inline_transform(filename, k)


def decrypt_generator(filename, k):
    """Stream decrypted file with key k.

    The given key must be the same that was
    returned by encrypt_file_inline.

    """
    #k = k.decode("hex")

    for chunk, _ in iter_transform(filename, k):
        yield chunk


def inline_transform(filename, key):
    """Encrypt file inline.

    Encrypts a given file with the given key,
    and replaces it directly without any extra
    space requirement.
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

    """
    # We are not specifying the IV here.
    aes = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))

    with open(filename, "rb+") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            yield aes.encrypt(chunk), f
