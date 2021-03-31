import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as pkrsa
from Crypto.Cipher import AES
import zipfile
import os
import glob
import time
import requests

# global vars
endmessage = "---endmessage---"
servername = "http://10.25.10.177:63654"
HEADERSIZE = 20
BYTELEN = 1024
BYTELENBIG = 4096
verbose = True

# helper functions
def get_ip():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    if not ip.startswith("127.")][:1], [[(s.connect(('1.1.1.1', 53)),
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

# returns the decompressed file
def decompress(filename):
    zf = zipfile.ZipFile(filename, mode='r', compression=zipfile.ZIP_DEFLATED)
    internalfile = zf.namelist()[0]
    with open(filename[:-4], "wb+") as returnfile:
        returnfile.write(zf.read(internalfile))

def decryptRSA(data):
    key = RSA.import_key(open("privatekey.pem").read())
    cipher = pkrsa.new(key)
    return cipher.decrypt(data)

# simplifier helper function to call current publickey decryption method
def PKdecrypt(data):
    return decryptRSA(data)

# decrypt files with given keyset
def decryptSet(keyset, vidset):
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
        with open(location + "/" + str(i+1) + ".mp4.zip", "wb+") as zp:
            zp.write(data)
        decompress(location + "/" + str(i+1) + ".mp4.zip")
        if verbose:
            print(f"Decrypted file ({i+1}/{len(vidset)})")

def downloadFromServer(urlWithPort):
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

while True:
    # download all videos
    downloadFromServer(servername)

    # get all video and key files in array (strings of file locations)
    vidset = [file for file in glob.glob("videos/encrypted/*", recursive=False)]
    keyset = [file for file in glob.glob("keys/*", recursive=False)]
    decryptSet(keyset, vidset)
    if(verbose):
        print('Done')
    exit()

# stitch files together (TODO later)
