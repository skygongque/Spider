from Crypto.Cipher import AES  # pip install pycryptodome
import base64
import binascii

def encrypt(k, iv, content):
    # k:密钥，iv:偏移量，content:需加密的内容
    k = k.encode("utf-8")
    iv = iv.encode("utf-8")
    # pad = lambda s: s + (16 - len(s)%16) * chr(0) # AES加密时，明文长度需为16的倍数。这里的pad用来填充，chr(0)表示为ZeroPadding，在最后填充0直到长度为16的倍数
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16) # 这里为Pkcs7填充
    content = pad(content).encode("utf-8")
    cipher = AES.new(k, AES.MODE_CBC, iv)  # CBC模式加密，还有ECB模式
    cipher_text = cipher.encrypt(content)
    enc = base64.b64encode(cipher_text).decode("utf-8")
    # enc = binascii.b2a_hex(cipher_text).decode("utf-8")
    return enc
    
    
k = "u2oh6Vu^HWe4_AES"
iv = "u2oh6Vu^HWe4_AES"
print(encrypt(k, iv, "13512341234"))