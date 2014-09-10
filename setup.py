from distutils.core import setup

setup(
    name='file_encryptor',
    version='0.1.0',
    author='Hugo Peixoto',
    author_email='hugo.peixoto@gmail.com',
    packages=['file_encryptor'],
    scripts=[],
    url='https://github.com/Storj/file-encryptor',
    license='LICENSE',
    description='Convergent encryption, focused on file handling',
    long_description=open('README.md').read(),
    install_requires=[
        'pycryptopp >= 0.6.0',
    ],
    extras_require={
        'test': [
            'tox'
        ]
    }
)
