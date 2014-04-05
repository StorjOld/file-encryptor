
import hashlib
import pycryptopp

CHUNK_SIZE=8

def sha256_feed(h, path):
    with open(path) as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            h.update(chunk)

def key(filename, passphrase):
    h = hashlib.sha256()

    sha256_feed(h, filename)

    if passphrase is not None:
        h.update(passphrase)

    h2 = hashlib.sha256()
    h2.update(h.digest())
    return h2.digest()


def encrypt_file_inline(filename, passphrase):
    k = key(filename, passphrase)
    inline_transform(filename, k)

    return k.encode("hex")

def decrypt_file_inline(filename, k):
    k = k.decode("hex")
    inline_transform(filename, k)

def encrypt(filename, k):
    k = key(filename, passphrase)
    for chunk, _ in iter_transform(filename, k):
        yield chunk

def decrypt(filename, k):
    k = k.decode("hex")
    for chunk, _ in iter_transform(filename, k):
        yield chunk

def iter_transform(filename, key):
    aes = pycryptopp.cipher.aes.AES(key=key)

    with open(filename, "r+b") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            yield aes.process(chunk), f

def inline_transform(filename, key):
    pos = 0
    for chunk, fp in iter_transform(filename, key):
        fp.seek(pos)
        fp.write(chunk)
        pos = fp.tell()

k = encrypt_file_inline("test.txt", "potato")
decrypt_file_inline("test.txt", k)
print k
