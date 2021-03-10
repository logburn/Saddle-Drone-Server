from Crypto.PublicKey import ECC
from Crypto.Cipher import Salsa20 as salsa

key = ECC.import_key(open("publickey.pem", "r").read())
cipher = salsa.new(key)

message = "attack at dawn"
encd = cipher.encrypt(bytes(message, "utf-8"))
print(encd)

'''
dkey = RSA.import_key(open("privatekey.pem").read())
dcipher = pk.new(dkey)
dmessage = dcipher.decrypt(encd)
print(dmessage)
'''
