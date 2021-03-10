from Crypto.PublicKey import RSA

# generate keypair
key = RSA.generate(2048)

# export private key
f = open("privatekey.pem", "wb+")
f.write(key.export_key('PEM'))
f.close()

# export public key
f = open("publickey.pem", "wb+")
f.write(key.public_key().export_key(format='PEM'))
f.close()

f = open("publickey.pem", "rt")
key = RSA.import_key(f.read())
print(key.encrypt(b"attack at dawn",32))
