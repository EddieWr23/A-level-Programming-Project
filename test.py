import hashlib
import pygame as p
p.init()

passwordhash = hashlib.sha256(('password123').encode('ascii')).hexdigest()

print(passwordhash)
