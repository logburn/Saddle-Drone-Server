from Crypto.PublicKey import ECC

# generate keypair
key = ECC.generate(curve='NIST P-256')

# export private key
f = open("privatekey.pem", "wt+")
f.write(key.export_key(format='PEM'))
f.close()

# export public key
f = open("publickey.pem", "wt+")
f.write(key.public_key().export_key(format='PEM'))
f.close()

f = open("publickey.pem", "rt")
key = ECC.import_key(f.read())
print(key)
