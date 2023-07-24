"""crypto.py
Cryptographic functions for use in eyeflask.server
"""

import binascii
import hashlib
import array


def create_credential(macaddress, nonce, upload_key, from_eyefi=False):
    """Returns an EyeFi credential.

    Generates the credential used by the EyeFi for authentication purposes. The
    credential is generated slightly differently based on if it is EyeFlask
    authenticating the EyeFi or the other way around.
    """

    if from_eyefi:
        cred_binary = binascii.unhexlify(macaddress + upload_key + nonce)
    else:
        cred_binary = binascii.unhexlify(macaddress + nonce + upload_key)
    cred_md5 = hashlib.md5()
    cred_md5.update(cred_binary)
    credential = cred_md5.hexdigest()
    return credential


def gen_checksums(file_handler):
    """Generates the TCP checksums used to calculate `INTEGRITYDIGEST`."""

    while True:
        chunk = file_handler.read(512)
        if chunk:
            tcp_sum = sum(array.array("H", chunk))

            # while tcp_sum > 65535
            while (tcp_sum >> 16):

                # tcp_sum = sum of left 16 bytes and right 16 bytes
                tcp_sum = (tcp_sum >> 16) + (tcp_sum & 0xFFFF)

            # take complement of the result
            checksum = tcp_sum ^ 0xFFFFFFFF

            # take only last 16 bits
            checksum = (checksum & 0xFFFF)
            yield checksum
        else:
            break


def make_digest(upfile, upload_key):
    """Returns the `INTEGRITYDIGEST`

    `INTEGRITYDIGEST` is used to verify the integrity of the file transfer,
    calculated using the content of the compressed image and the upload_key
    """

    checksums = array.array("H", gen_checksums(upfile))
    checksums.frombytes(binascii.unhexlify(upload_key))
    digest = checksums.tostring()

    m = hashlib.md5()
    m.update(digest)
    hexdigest = m.hexdigest()
    return hexdigest
