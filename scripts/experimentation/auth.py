import bcrypt
import jwt

import jwt_check

from common.config_utils import get_secret_key

password = b'super secret password'
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if bcrypt.checkpw(password, hashed):
    print('It matches')
else:
    print('It doesn\'t')

password = 'passwordabc'

# converting password to array of bytes
bytes = password.encode('utf-8')

# generating the salt
salt = bcrypt.gensalt()

# Hashing the password
hash = bcrypt.hashpw(bytes, salt)

# Taking user entered password
userPassword = 'passwordabc'

# encoding user password
userBytes = userPassword.encode('utf-8')
# checking password
result = bcrypt.checkpw(userBytes, hash)

print(hash, userBytes)
print(result)

key = get_secret_key()
payload = {
    'user_email': 'hugo.huzecardosi@ynov.com',
    'user_id': '6375fb89af475654d23d61d9',
    'expiry': '24h'
}

token = jwt.encode(payload=payload, key=key)
print(token)
data = jwt.decode(token, key=key, algorithms=['HS256', ])
print(data)
