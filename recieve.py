import socket
from Crypto.Cipher import PKCS1_OAEP as RSA
#from Crypto.Cipher import AES
from cryptography.fernet import Fernet
import os
import glob
import time

# global vars
endmessage = "---endmessage---"
HEADERSIZE = 20
BYTELEN = 1024
BYTELENBIG = 4096

# helper functions
def get_ip():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    if not ip.startswith("127.")][:1], [[(s.connect(('1.1.1.1', 53)),
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

def getStream(bytelen):
    newmsg = True
    done = False
    fullmsg = ""
    while not done:
        msg = c.recv(bytelen)
        if newmsg:
            msglen = int(str(msg[:HEADERSIZE].decode("utf-8")))
            print(str(msglen))
            newmsg = False
        fullmsg += msg.decode("utf-8")
        if len(fullmsg) - HEADERSIZE == msglen:
            print(f"{len(fullmsg) - HEADERSIZE} : {msglen}")
            done = True
            return fullmsg[HEADERSIZE:]
        else:
            if len(fullmsg) - HEADERSIZE > msglen:
                done = True
            print(f"{len(fullmsg) - HEADERSIZE} | {msglen}")

# TODO decrypt text with PGP key
def decryptPGP(text):
    return text
    # keytext = open("prikey.pem", "r").read()
    keytext = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAuk5egzauVPCxuNvWcJAAISIxcvsdXQFFB5lYUdOgv8Dcyva/\n9kh76R2TEay0K3kEpXBx/M4YdiAIg0XoTYUxWNR3vGy4sWuAkF1WPF0hCJcx/GGC\nCszl7NqMDz7uedBSkJG4sIyOCnmxJli/Y7O+xoENb1DvJ4U7b0n3AHkovlsfkw8z\nwOVsc9dUnPbZmrzbd99HYoRFPKnAVgF+vGY62qRj2GvsJzRAC0K8HMxJv0r/V+3O\n+fwqGCnJlCcadgMJUuHPDVdYVXgEZZ1iYdwFpPHLML2DEOd3y3DJAy1F59IkEGAr\nULQbu7SdqwaFkU1Y2euZXb/J1q/9C/GhppQH9QIDAQABAoIBACxgf3W8wCC+Zm7U\neos8WbOKvAGZ3AArzcAGIDn5cUhLjawQw1/MGyvHXiEvJIlYXal0k8o2YzA76Bsw\nuyk/6SWyEkVBFms4YprAiMp/Gl+79+2YYkvlS30z/3mgMVi1rPz/oOD40dqf6vjp\n2cjLZ01MLyGNQzIEM8iJ8zpbIb/Zd496n6awH+am4+9tD5o87aI0mx0PwS0zCUfX\nbFg6ns42XS2FuAiKeqMkmNcoo6G0E/6zDw7dk4MfJ5UNDIkSJ+r3UHjXOi1Zn4BW\n0uNYIV9BdJlyiKTB+edTxe0IzSpaBnPp+3f5CKeR9V/T3apLet/EFbYzyJ0KSi31\nMTUW64ECgYEA0FJ++cqVSUz2AtBOY9yF362LlRH60DQe7JiDHAFZmhN/iMw+VBOr\nKsSOAtSx01Cr5iD9KO/CqJCVFmdM4lzvJklcpOyNhNwt8B8kc8R+QLi+wfBCLy3q\nODp7UcWhKAV3hsAGx1ct8fWNtkfI7v+BaPN6ablNFYKHJa5RvUTsizUCgYEA5PH1\nezOLDukj+QRf3DE2u0HZRWmv807gA1+tuicDn9JAbK7FFLbdANDwd2TC5wYGGUaR\nTrk6CGKlp0H/P0VJbjUIHQOtLz4Xao91wU8iLdrcKeVoELgJqO0em3YUdOEpcdUT\ny06SBImz3T+NS/NP7GcxbSJ+Fqc07p2iAUGAYcECgYEAonQixuK/JklY83rEFsXq\ntDKeziIWSHTMxM5uN9GpsSiRZPl5hZFNAu4CnJyHC/Y2ByEkqt7GGzOcv7rQzxmP\n+XhuQcKi3b/iJwXyJEFP/2LSh2S4CBizNSQN9Qe8E/ynaDKpVpxanPxThZlXTWF8\n5n4wsO+q+CIxCCZ3YbS1Dh0CgYEAuOWwG4/E/oXLR5EA2hPk39aOYkC4mQdaY18i\nLvTTOH/VB/EduVz1n3MewU3fGjUDN+aF884j0CHbJvll6vNKGnc51jTh6QV8Y9L4\nhuYh9GaM6EkdgmMfag4WafczDjHKBuTO16Lcyk1rtYNd2bjnE0VD5Z+1tRXU6eDk\ntZ7w0AECgYEAo+tRkqj12gVWYFNK5Ij7zfzn7Iv0pGiyq+sa+8PBEeziKGGRPyjn\nKlpAYmOlSr9aKAtE8JKCvrAfrQHFo3dQRxWQAppiuY38zu2dxXUOpdF3Wb9Tfk4Y\nMMDhzybUSNa0tq4rVg6xaeQvIwNx2SGk93tUul0JBh6vzrF+eB7WYu8=\n-----END RSA PRIVATE KEY-----"
    key = RSA.importKey(keytext)
    return key.decrypt(text)[0]

# decrypt text
def decryptText(text, fkey):
    return Fernet(fkey).decrypt(text)

# establish connection with client and download files
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = get_ip()
print(host)
port = 12352
s.bind((host, port))
s.listen(5)

while True:
    '''
    # initial vars, connect with client device
    c, addr = s.accept()
    print(f'Got connection from {addr}')

    # get number of files and recieve that num of files
    numFiles = 2 # int(c.recv(80).decode()) TODO
    for i in range(numFiles):
        # get video and key data from remote, store both in respective files
        open("videos/encrypted/" + str(i+1) + ".mpc", "w+").write(getStream(BYTELEN))
        open("keys/" + str(i+1) + ".asc", "w+").write(getStream(BYTELEN))
        # update user because this might take some time
        print("Recieved data (" + str(i+1) + "/" + str(numFiles) + ")")
    c.close()
    '''
    # decrypt the files
    print("Decrypting files...")
    # get all video and key files in array (strings of file locations)
    vidset = [file for file in glob.glob("videos/encrypted/*", recursive=False)]
    keyset = [file for file in glob.glob("keys/*", recursive=False)]
    location = "videos/plaintext/" + str(int(time.time()))
    os.mkdir(location)
    for i in range(len(vidset)):
        # read the key and video file into vars
        key = bytes(open(keyset[i], "r").read(), 'utf-8')
        text = bytes(str(open(vidset[i], "r").read()), 'utf-8')
        # write the decrypted video file info into an mp4 file
        with open(location + "/" + str(i+1) + ".mp4", "wb+") as mp4:
            mp4.write(decryptText(text, key))
        # delete the old files
        #os.remove(vidset[i])
        #os.remove(keyset[i])
        print(f"(dev mode) Would have deleted {vidset[i]} and {keyset[i]}")

    print('Done')
    exit()

# stitch files together (TODO later)
