# GET&%2Fapi%2Fv2%2Felendil%2Fquery_content&1603602528
import base64
import hmac
# message = r'GET&%2Fapi%2Fv2%2Felendil%2Fquery_content&1603602528'.encode()
# key = b'bf7dddc7c9cfe6f7'
# h = hmac.new(key, message, digestmod=base64.b64encode)  
# print(h.hexdigest())

# message = r'GET&%2Fapi%2Fv2%2Felendil%2Fquery_content&1603603638'.encode()

# hashed = hmac.new(b'bf7dddc7c9cfe6f7', message, None)

# result = base64.b64encode(hashed.digest())
# print(result)

import base64
import hmac
import hashlib


""" 
<class: com.douban.frodo.utils.crypto.HMACHash1>
[+] str4:bf7dddc7c9cfe6f7
[+] GET&%2Fapi%2Fv2%2Felendil%2Frecommend_feed&1603603637
[+] 加密后：46rcAiG65DF/jbmQjDmD7Ic9JQw=
[+] str4:bf7dddc7c9cfe6f7
[+] GET&%2Fapi%2Fv2%2Ferebor%2Ffeed_ad&1603603637
[+] 加密后：s7Bq8sbf5o2PS2y2FKe9B6s8RVY=
[+] str4:bf7dddc7c9cfe6f7
[+] GET&%2Fapi%2Fv2%2Felendil%2Fquery_content&1603603638
[+] 加密后：NysD+/sAuZBjBT0WqJJRLFrnakI=

 """
def encrypt():
    digest = hmac.new(b'bf7dddc7c9cfe6f7', r'GET&%2Fapi%2Fv2%2Felendil%2Fquery_content&1603603638'.encode(), hashlib.sha1).digest()
    # result = str(base64.encodebytes(digest))
    result = base64.b64encode(digest).decode("utf-8") 
    print(result)
# /elessar/subject/
# GET&%2Fapi%2Fv2%2Felessar%2Fsubject%2F27503300%2Fphotos&1603605177
digest = hmac.new(b'bf7dddc7c9cfe6f7', r'GET&%2Fapi%2Fv2%2Felessar%2Fsubject%2F27260217%2Fphotos&1603515067'.encode(), hashlib.sha1).digest()
# result = str(base64.encodebytes(digest))
result = base64.b64encode(digest).decode("utf-8") 
print(result)
# MhDCiFIQ/nAhKNAkL7H2KBHbwHg=
# MhDCiFIQ%2FnAhKNAkL7H2KBHbwHg%3D
# lvD/FYS0hbAsQaAq50UbkYYeXBI=
# lvD%2fFYS0hbAsQaAq50UbkYYeXBI%3d

# GET&%2Fapi%2Fv2%2Felessar%2Fsubject%2F27503300%2Fphotos&1603605724
# [+] 加密后：Xqk4KTIzPrMBP6sLN8EO+kvQZz4=