import hashlib

passwordhash = hashlib.sha256(('password123').encode('ascii')).hexdigest()

print(passwordhash)
