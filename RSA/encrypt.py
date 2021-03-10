from Crypto.Cipher import PKCS1_OAEP as pk
from Crypto.PublicKey import RSA

key = RSA.import_key(open("publickey.pem", "r").read())
cipher = pk.new(key)

message = "attack at dawn"
encd = cipher.encrypt(bytes(message, "utf-8"))
print(encd)

dkey = RSA.import_key(open("privatekey.pem").read())
dcipher = pk.new(dkey)
dmessage = dcipher.decrypt(encd)
print(dmessage)
