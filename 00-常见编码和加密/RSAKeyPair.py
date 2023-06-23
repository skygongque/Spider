import rsa


class Encrypt():
    """
    该类为参考的这篇文章：https://www.52pojie.cn/forum.php?mod=viewthread&tid=874374
    主要用于对应JS中的RSAKeyPair的RSA加密，每次对相同明文加密后的密文都是相同的，原因为NoPadding
    """
    def __init__(self, e, n):
        self.e = e
        self.n = n

    def encrypt(self, message):
        ee = int(self.e, 16)
        nn = int(self.n, 16)
        rsa_pubkey = rsa.PublicKey(e=ee, n=nn)
        crypto = self._encrypt(message.encode(), rsa_pubkey)
        return crypto.hex()

    def _pad_for_encryption(self, message, target_length):
        message = message[::-1]
        max_msglength = target_length - 11
        msglength = len(message)

        padding = b''
        padding_length = target_length - msglength - 3

        for i in range(padding_length):
            padding += b'\x00'

        return b''.join([b'\x00\x00',padding,b'\x00',message])

    def _encrypt(self, message, pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, keylength)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, keylength)

        return block


def USE_RSA(message):
    e = "010001"
    n = "81eb7e93bc0e458f67ad208ffb8039a139dffab9b576309212b6c5b411c0f32266ab8700c617562f294abda31f1195163a058637dfebeb80fa0b8cfa0ef63fac3a52b8c3ecf26cb334745d4c850cb5c7fd0bac81ce39e8814c7284fa8bc9721d66189fe5c6d7a3b1046cfdecc4e2976238ccc0a8a6ebbf0ebdedf4737d2dfc99"
    en = Encrypt(e, n)
    return en.encrypt(message)

ciphertext = USE_RSA("111111")
print(ciphertext)

from Crypto.PublicKey import RSA
import base64

private_key_str = """-----BEGIN RSA PRIVATE KEY-----
MIICXwIBAAKBgQCB636TvA5Fj2etII/7gDmhOd/6ubV2MJIStsW0EcDzImarhwDG
F1YvKUq9ox8RlRY6BYY33+vrgPoLjPoO9j+sOlK4w+zybLM0dF1MhQy1x/0LrIHO
OeiBTHKE+ovJch1mGJ/lxtejsQRs/ezE4pdiOMzAqKbrvw697fRzfS38mQIDAQAB
AoGAYWca+Muur3v6MJQPHnFdw4BOaf09DKURfrJEuuHslNwfuU13yQvJ84WzoUVg
j6AEj++AVvesOl3yGSLR+OIBnqMFZvs6MjBzn5RdKjD3PiiBdUgBh+bGA+9peeqo
8E0FBiPLkedXorM1YtR39cxPPhreNO/R+ApMLA/Z3RZDeWECRQCypZ9xrqWTMYDg
imfyQbKyX2F1ow/fyC29G/ysuT/x8TyiJwWR0QjKEYA1H1G+jEZALJj2H/N9rUFk
ad6ZmN5lPfBCDQI9ALospps+/QyVQl6yIp13XskhjGOhhyzmEOlkeOJbDcy+eLey
ND8jj32YhNMXe29r/InC6msuuLIo9ujdvQJEMzg1PLzcEBWzY62LG/QmLeoW4Ul9
NaYJJx0tFsCOSunlfoA9oo8SPA1Eevad00oYojGnMXn7r97KzuVjwxoHOXPGvMkC
PCxmpb10wkkT9+Y5ucOwSmzRkXfZeDGfFP10ttfVO29PJd85ovhD9N7RVyw493lV
Wb9JOzsgw2/KEUjsSQJEWrAxPbERzSsM+syfrcOhs424v4m97v10kdYXcpuWuAuy
v8yozU2CM1cFEg3CxNJEw1dF9bHon2LJtz2W6gjDLtm9y4I=
-----END RSA PRIVATE KEY-----"""



private_key = RSA.import_key(private_key_str)

ct = base64.b64decode(ciphertext)
ct_int = int.from_bytes(ct, 'big')
pt_int = pow(ct_int, private_key.d, private_key.n)
pt = pt_int.to_bytes(private_key.size_in_bytes(), 'big').lstrip(b'\x00')
print(pt)
