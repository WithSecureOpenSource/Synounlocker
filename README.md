Synounlocker.py
===============

synounlocker.py is a tool for decrypting files encrypted by the SynoLocker family of ransomware.

The tool works by first looking in a file for the magic string "THE_REAL_PWNED_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_1337" that is used by SynoLocker to identify files it has encrypted. Next, it will attempt to decrypt the file. During this process, it will also attempt to check that the encrypted file has not been corrupted. This is possible, because SynoLocker stores a [HMAC](http://en.wikipedia.org/wiki/Hash-based_message_authentication_code) of the encrypted data as part of the file. If all seems to have gone well, the tool will write the decrypted contents to a new file, with the name of the original file appended with ".dec". The tool will not remove or overwrite the original encrypted file.

IMPORTANT
=========

This tool will only work if the decryption key is already known. It will not bruteforce the decryption key and it will not break any encryption. The tool is only meant to be used, if the decryption key is already known. You should never pay online criminals. There is no guarantee it will help you in getting your files back. It will only encourages the criminals to continue their criminal activities.

Requirements
------------

This tool requires the [pycrypto](https://pypi.python.org/pypi/pycrypto) -package. It has been tested to work with Python 2.7.8 and pycrypto 2.6.1.

Installation
------------

First, ensure you have Python 2.7.8 and pycrypto 2.6.1 installed. Then simply copy the `synounlocker.py` -script to a directory of your choosing.

Usage
-----

From the command line: `synounlocker.py <path to encrypted file> <path to private key file>`

License
-------

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)