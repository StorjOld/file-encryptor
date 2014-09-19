import hashlib
import hmac

from file_encryptor.settings import CHUNK_SIZE, DEFAULT_HMAC_PASSPHRASE

def sha256_file(path):
    """Calculate sha256 hex digest of a file."""
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

    """
    hexdigest = sha256_file(filename)

    if passphrase is None:
        passphrase = DEFAULT_HMAC_PASSPHRASE

    return keyed_hash(hexdigest, passphrase)

def keyed_hash(digest, passphrase):
    """Calculate a HMAC/keyed hash."""
    encodedPassphrase = passphrase.encode()
    encodedDigest = digest.encode()
    return hmac.new(encodedPassphrase, encodedDigest, hashlib.sha256).digest()
