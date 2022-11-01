import hmac
import pickle
import base64
import cgi

username = "notKyle"
secret = b'|\xb8\xd4\x7f\x1a\x97\xb5\xf3h"W@\xd0\r\t'
hash = hmac.HMAC(secret, username.encode('ascii')).hexdigest()
cookieInfo = [username, hash]
dumpedCookie = pickle.dumps(cookieInfo)
encodedCookie = base64.b64encode(dumpedCookie)
print(str(encodedCookie).replace("=", "%3D").replace("'", "%27"))
