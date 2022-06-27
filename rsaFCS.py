from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Hash import SHA256
import hashlib
import base64

import numpy as np
from PIL import Image


def read_msg(encrypted_text, public_key):
    # print("encrypted text")
    # print(encrypted_text)
    encrypted_text = bytes.fromhex(encrypted_text)
    rsa_public_key = PKCS1_OAEP.new(public_key)
    decrypted_text = rsa_public_key.decrypt(encrypted_text)

    return decrypted_text.decode('utf-8')


def gen_SHA256_digest(message):
    hashop = hashlib.sha256(message).hexdigest()
    return hashop


def encode_msg(message, private_key):
    message = str.encode(message)

    rsa_private_key = PKCS1_OAEP.new(private_key)
    encrypted_nof = rsa_private_key.encrypt(message)
    
    ret_val = encrypted_nof.hex()
    if(len(ret_val)%2!=0):
        ret_val = '0' + ret_val
    return ret_val




def extract_code(image):  # extracts hash from image and removes hash to recover original image
    img = Image.open(image)
    img_arr = np.array(img)
    index = np.shape(img_arr[:, 1])[0]

    arr = img_arr[index-1]

    if np.sum(arr[arr.shape[0]-1] == [69, 69, 69, 69]) != 4:
        return False
    else:
        encoded_arr = arr.reshape(-1)
        whr = np.where(encoded_arr == 100)
        encoded_arr = encoded_arr[:whr[0][0]]

        encoded_list = encoded_arr.tolist()
        # print("encoded_list")
        # print(encoded_list) # debug comment
        s = ''
        for i in encoded_list:
            s = s + hex(i)[2:]

        new_img_arr = img_arr[:index-1]
        new_img = Image.fromarray(new_img_arr)
        new_img.save("recovered.png", format="png")
        # print("extractd_code")
        # print(s) # debug comment
        return s


def append2img(c, image):
    # c is a string with hex values
    # print(c) # debug comment
    s = c
    arr = []
    temp = []
    chunks = [s[i:i+1] for i in range(0, len(s), 1)]
    for i in range(0, len(chunks)):
        if((i+1) % 4 == 0):
            temp.append(int(chunks[i], 16))
            arr.append(temp)
            temp = []
        else:
            temp.append(int(chunks[i], 16))

    if(len(temp) != 0):
        for i in range(4-len(temp)):
            temp.append(100)
    else:
        for i in range(4):
            temp.append(100)
    arr.append(temp)

    t = np.array([arr], dtype=np.uint8)
    img = Image.open(image)
    img_arr = np.array(img)
    tt = np.ones(
        (1, int(np.shape(img_arr[1, :])[0] - np.shape(t)[1]), 4), dtype=np.uint8)
    tt = tt * 69
    key_arr = np.concatenate((t, tt), axis=1)
    new_img_arr = np.concatenate((img_arr, key_arr), axis=0)

    new_img = Image.fromarray(new_img_arr)
    new_img.save("encoded.png", format="png")
