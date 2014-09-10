from distutils.core import setup

try:
    longdescription = open('README.md').read()
except:
    longdescription = 'Convergent encryption, focused on file handling'

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
    long_description=longdescription,
    install_requires=[
        'pycryptopp >= 0.6.0',
    ],
    extras_require={
        'test': [
            'tox',
            'unittest2'
        ]
    }
)
