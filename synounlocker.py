#!/usr/bin/env python

############################################################################
# Copyright 2014 F-Secure                                                  #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

import sys
import os

from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC

def checkHeader(fp):
    magic = "THE_REAL_PWNED_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_1337"
    fp.seek(256) # magic marker should be located 256 bytes from the beginning
    marker = fp.read(60)
    return marker == magic

def generateKey(iv, base_string):
    key = iv + '\x00' * 16
    for i in range(8192):
        key = SHA256.new(key + base_string).digest()
    return key

def decrypt(enc_file_path, priv_key_file_path):
    # First check file is big enough to plausibly be generated by SynoLocker
    try:
        # size <= encrypted key + magic string + IV + HMAC
        if os.path.getsize(enc_file_path) <= 256 + 60 + 16 + 32:
            print "Error: file too small to be encrypted by SynoLocker!"
            return
    except os.error:
        print "Error: unable to access encrypted file!"
        return
    
    try:
        with open(enc_file_path, 'rb') as enc_file:
            if not checkHeader(enc_file):
                print "Error: file not recognized as encrypted by SynoLocker!"
                return

            try:
                with open(priv_key_file_path) as priv_key_file:
                    priv_key = RSA.importKey(priv_key_file.read())
            except:
                print "Error: unable to open private key file!"
                return

            rsa_cipher = PKCS1_v1_5.new(priv_key)
            
            # Read encrypted string from file
            enc_file.seek(0)
            enc_str = enc_file.read(256)
            dec_str = rsa_cipher.decrypt(enc_str, "ERROR_SENTINEL")
            if dec_str == "ERROR_SENTINEL":
                print "Error: failed to decrypt key from file!"
                return

            # Skip magic string
            enc_file.seek(60, os.SEEK_CUR)

            # Read IV
            iv = enc_file.read(16)

            # Read rest of file
            remaining = enc_file.read()

            # Split into encrypted contents and HMAC
            encrypted = remaining[:-32]

            # HMAC is the last 32 bytes of the file
            hmac = remaining[-32:]

            # Get key
            key = generateKey(iv, dec_str)

            # Check that HMAC matches
            h = HMAC.new(key, digestmod=SHA256)
            h.update(encrypted)

            if not h.digest() == hmac:
                print "Error: content verification failed!"
                return

            # Decrypt data
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted)

            # Write decrypted data to <encrypted file name>.dec
            try:
                with open(enc_file_path + ".dec", 'wb') as ofile:
                    ofile.write(decrypted)
            except:
                "Error: unable to write decrypted file to disk!"
                return

            print "Successfully decrypted file!"
            return

    except:
        print "Error: unable to decrypt file!"
        return

if __name__ == "__main__":
    if len(sys.argv) == 3:
        decrypt(sys.argv[1], sys.argv[2])
    else:
        print "Usage: %s <path to encrypted file> <path to private key>" % sys.argv[0]
        print ""
        print "         decrypted file will be written to <encrypted file name>.dec"
