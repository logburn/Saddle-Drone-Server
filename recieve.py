import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as pkrsa
from Crypto.Cipher import AES
import os
import glob
import time
import requests

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

def decryptRSA(data):
    key = RSA.import_key(open("privatekey.pem").read())
    cipher = pkrsa.new(key)
    return cipher.decrypt(data)

# simplifier helper function to call current publickey decryption method
def PKdecrypt(data):
    return decryptRSA(data)

# decrypt files with given keyset
def decryptSet(keyset, vidset, verbose=False):
    location = "videos/plaintext/" + str(int(time.time()))
    os.mkdir(location)
    if verbose:
        print("Created folder to store files")
    for i in range(len(vidset)):
        file_in = open(vidset[i], "rb")
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        key = open(keyset[i], "rb").read()
        key = PKdecrypt(key)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(location + "/" + str(i+1) + ".mp4", "wb+") as mp:
            mp.write(data)
        if verbose:
            print(f"Decrypted file ({i+1}/{len(vidset)})")

def downloadFromServer(urlWithPort, verbose=False):
    url = urlWithPort + '/numFiles.txt'
    r = requests.get(url, allow_redirects=True)
    if verbose:
        print("Downloading files...")
    for i in range(int(r.content)):
        url = urlWithPort + "/keys/" + str(i+1) + ".asc"
        with open("keys/" + str(i+1) + ".asc", "wb+") as keyf:
            keyf.write(requests.get(url, allow_redirects=True).content)
        url = urlWithPort + "/videos/encrypted/" + str(i+1) + ".mpc"
        with open("videos/encrypted/" + str(i+1) + ".mpc", "wb+") as vidf:
            vidf.write(requests.get(url, allow_redirects=True).content)
        if verbose:
            print(f"Recieved ({i+1}/{int(r.content)})")

# establish connection with client and download files
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = get_ip()
print(host)
port = 12352
s.bind((host, port))
s.listen(5)

while True:
    '''
    OBSOLETE
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
    '''

    # download all videos
    downloadFromServer("http://10.25.10.125:63655")

    # get all video and key files in array (strings of file locations)
    vidset = [file for file in glob.glob("videos/encrypted/*", recursive=False)]
    keyset = [file for file in glob.glob("keys/*", recursive=False)]
    decryptSet(keyset, vidset)

    '''
    location = "videos/plaintext/" + str(int(time.time()))
    os.mkdir(location)
    for i in range(len(vidset)):
        file_in = open(vidset[i], "rb")
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        key = open(keyset[i], "rb")
        cipher = AES.new(key.read(), AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(location + "/" + str(i+1) + ".mp4", "wb+") as mp:
            mp.write(data)
    '''
    '''
 
    url = 'http://10.25.10.125:63655/numFiles.txt'
    r = requests.get(url, allow_redirects=True)
    print("Downloading files...")
    for i in range(int(r.content)):
        url = "http://10.25.10.125:63655/keys/" + str(i+1) + ".asc"
        with open("keys/" + str(i+1) + ".asc", "wb+") as keyf:
            keyf.write(requests.get(url, allow_redirects=True).content)
        url = "http://10.25.10.125:63655/videos/encrypted/" + str(i+1) + ".mpc"
        with open("videos/encrypted/" + str(i+1) + ".mpc", "wb+") as vidf:
            vidf.write(requests.get(url, allow_redirects=True).content)
        print(f"Recieved ({i+1}/{int(r.content)})") 
    '''

    print('Done')
    exit()

# stitch files together (TODO later)
