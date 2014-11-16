.. File Encryptor documentation master file, created by
   sphinx-quickstart on Sat Nov 15 22:30:20 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

File Encryptor Documentation
=======================================

This is a library used by MetaDisk to convergently encrypt and decrypt
files. It contains helper methods to encrypt and decrypt files inline
(without using extra space) and to stream decryption.

Usage
-----

Here’s an example to encrypt a file inline using convergent encryption:

.. code:: python

    import file_encryptor.convergence

    key = convergence.encrypt_inline_file("/path/to/file", None)

You can also specify a passphrase:

.. code:: python

    import file_encryptor.convergence

    key = convergence.encrypt_inline_file("/path/to/file", "rainbow dinosaur secret")

To decrypt a file inline, you need the key that was returned by the
encrypt method:

.. code:: python

    import file_encryptor.convergence

    key = convergence.encrypt_inline_file("/path/to/file", "rainbow dinosaur secret")

    convergence.decrypt_inline_file("/path/to/file", key)

The reason why you cannot use the passphrase directly is because the key
is derived from both the passphrase and the SHA-256 of the original
file.

For streaming applications, you can decrypt a file with a generator:

.. code:: python

    for chunk in convergence.decrypt_generator("/path/to/file", key):
        do_something_with_chunk(chunk)

Cryptoconcerns
--------------

The key generation mechanism is the following:

.. code:: python

    key = HMAC-SHA256(passphrase, hex(SHA256(file-contents)))

If no passphrase is given, a default is used.

The file itself is encrypted using AES128-CTR, from pycrypto. We’re not
specifying any IV, thinking that for convergent encryption that is the
right thing to do.

Testing
-------

To run tests, execute the following command in the project root:

::

    python setup.py test -a "--doctest-modules --pep8 -v tests/"

To run tests with detailed coverage output, execute:

::

    coverage run setup.py test -a "--doctest-modules --pep8 -v tests/"
    coverage report -m --include="file_encryptor/*"


.. toctree::
   :maxdepth: 2


Module Indices and Tables
=========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

