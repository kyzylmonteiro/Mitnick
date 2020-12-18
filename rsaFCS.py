from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Hash import SHA256
import hashlib
import base64

import numpy as np
from PIL import Image


def read_msg(encrypted_text, public_key):
    # input: bytes; output: string
    # rsa_public_key = RSA.importKey(public_key)
    rsa_public_key = PKCS1_OAEP.new(public_key)
    encrypted_text = base64.b64decode(encrypted_text)
    decrypted_text = rsa_public_key.decrypt(encrypted_text)

    # print('your decrypted_text is : {}'.format(decrypted_text))
    return decrypted_text.decode('utf-8')


def gen_SHA256_digest(message):
    #input: message (string); output: hexdigest (string)
    # obj = SHA256.new()
    # obj.update(message)
    # return obj.hexdigest()  # string
    # print("hashlib.sha256(message).hexdigest()")
    # print(hashlib.sha256(message).hexdigest())
    return hashlib.sha256(message).hexdigest()


def encode_msg(message, private_key):
    # '''uses RSA, input: nof (int); output: cipher, private key, public key'''
    # key = RSA.generate(key_size)
    # public_key = key.export_key('PEM')
    # private_key = key.publickey().exportKey('PEM')
    # message = input('plain nof for RSA encryption and decryption:')
    message = str.encode(message)

    # rsa_private_key = RSA.importKey(private_key)
    rsa_private_key = PKCS1_OAEP.new(private_key)
    encrypted_nof = rsa_private_key.encrypt(message)
    #encrypted_nof = b64encode(encrypted_nof)

    # print("encrypted_nof")
    # print(encrypted_nof)
    # print("base64.b64encode(encrypted_nof)")
    # print(base64.b64encode(encrypted_nof))
    return base64.b64encode(encrypted_nof)


# def update_msg(encrypted_nof, public_key, private_key):
#     # input: bytes; output: bytes
#     rsa_public_key = RSA.importKey(public_key)
#     rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
#     decrypted_nof = rsa_public_key.decrypt(encrypted_nof)

#     nof = int(decrypted_nof) + 1
#     message = str(nof)
#     message = str.encode(message)

#     rsa_private_key = RSA.importKey(private_key)
#     rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
#     encrypted_nof = rsa_private_key.encrypt(message)
#     # print('your decrypted_nof is : {}'.format(decrypted_nof))

#     return encrypted_nof


# c = b"\xc6\xf5\xf8\xb8\xcd2\x10M\x84\x7f\x86\xaa3\x86\xbf_\xa7\x058\x0e.\x94\xfe\x08\xa5\xcbA\x0b\x82\x88\xd8\x8e\xc6w\xf3\xe4\xb4\xa6F\xe90\xb5\x0b\xfb\xe2@z\x1d\x93P\x1fZZ\x8fW%\x14\xcd!\xe6\xb2\x93\xd5Ou\xae'y\x8f\xf8\xcf\xf9\x17=S\x18\xe1\xcfH 2\xba\xe2\xb5-y\xd9\x07\x98\x94\xad7f\xaf\xf7Q\x91P\x06o,\xd6\x94\xa4\x94\xc0+\xa0Hd\xed\xe4\x9c\xda\xacg\x88crEY\x94\xbe\xe4@<\xa5`H#\xd1<\xbab5\x18\xc0\x9a(]\x14\xc7]r\xf9\xcb\x91\t\x1e0_\xc2o\xb8\x9d\xe8\xe2\x8a2\xee\xdb\x99\x9e\xba@;>\xf8\x07\x1e?\xa8\xea\x0e\xb1\xbb\xa1\x91a\xa9\xd8:\r\x1e\xdd}\x1fT\xc7,*\x9aV9F\x12M\xed\xd0e\xb7\xd7D\x89nbs\xb3\x95L]\xbc\x04\x1a\x88<\x01\xe6\xe5<\x00\x0c\xcf.\x9e7&.\x89\x1c\xc2\xc1\xb4\xd2\xa8\xcf\xde\xd6\xcas\xbb\xa2-#~s$0\xcb\x0cV\xbck\xf7;?"
def extract_code(image):
    # c=b'R0+kdh3W0aia6cMQk4TEi9Q8rHEFCiaK+C21Q57GTf+IPDAKoOr8kQlHwaPa9ELeGiP5ksyz6lIMjJf9BxdJf/GBvw17K+y1KdJuhaiGJCGS9baFgwdSRZ+OjdsAt5xyGrev8j2h8kbDQWG0sqFjz1jCZZfUX+12bOPUZPtcPMDW3T2gvcCrlTvsZldmh4kHFetD2lyOd4+kHpe5SLsgTaHLhHyw2a74wxF13b7Ksf8mITMlSNtbsnVvMdJ5AhgbGPGy5ntT7OAOksJ7HCpo74vmXrXMYU9iedl663BxuecC9YXEP2SE/QK9O9eSwP43R1O9NsI35AmC1TYzTGodUg=='

    img = Image.open(image)
    img_arr = np.array(img)
    index = np.shape(img_arr[:, 1])[0]

    arr = img_arr[index-1]

    # print(arr)
    # print(arr[-1])
    # for i in range(len(whr[0])):
    #   if(whr[0][i]==whr[0][i+1] and whr[0][i+1]==whr[0][i+2] ):
    if np.sum(arr[arr.shape[0]-1] == [0, 0, 0, 0]) != 4:
        return False
    else:
        encoded_arr = arr.reshape(-1)
        whr = np.where(encoded_arr == 100)
        encoded_arr = encoded_arr[:whr[0][0]]

        encoded_list = encoded_arr.tolist()
        print("encoded_list")
        print(encoded_list)
        s = ''
        for i in encoded_list:
            if(len(str(i)) < 2):
                s = s + '0' + str(i)
            else:
                s = s + str(i)

        x = int(s)

        new_img_arr = img_arr[:index-1]
        new_img = Image.fromarray(new_img_arr)
        new_img.save("recovered.png", format="png")

        print("x")
        print(x)
        encoded_hash = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
        print("encoded_hash")
        print(type(encoded_hash))
        print(encoded_hash)

        return encoded_hash


# c = b"\xc6\xf5\xf8\xb8\xcd2\x10M\x84\x7f\x86\xaa3\x86\xbf_\xa7\x058\x0e.\x94\xfe\x08\xa5\xcbA\x0b\x82\x88\xd8\x8e\xc6w\xf3\xe4\xb4\xa6F\xe90\xb5\x0b\xfb\xe2@z\x1d\x93P\x1fZZ\x8fW%\x14\xcd!\xe6\xb2\x93\xd5Ou\xae'y\x8f\xf8\xcf\xf9\x17=S\x18\xe1\xcfH 2\xba\xe2\xb5-y\xd9\x07\x98\x94\xad7f\xaf\xf7Q\x91P\x06o,\xd6\x94\xa4\x94\xc0+\xa0Hd\xed\xe4\x9c\xda\xacg\x88crEY\x94\xbe\xe4@<\xa5`H#\xd1<\xbab5\x18\xc0\x9a(]\x14\xc7]r\xf9\xcb\x91\t\x1e0_\xc2o\xb8\x9d\xe8\xe2\x8a2\xee\xdb\x99\x9e\xba@;>\xf8\x07\x1e?\xa8\xea\x0e\xb1\xbb\xa1\x91a\xa9\xd8:\r\x1e\xdd}\x1fT\xc7,*\x9aV9F\x12M\xed\xd0e\xb7\xd7D\x89nbs\xb3\x95L]\xbc\x04\x1a\x88<\x01\xe6\xe5<\x00\x0c\xcf.\x9e7&.\x89\x1c\xc2\xc1\xb4\xd2\xa8\xcf\xde\xd6\xcas\xbb\xa2-#~s$0\xcb\x0cV\xbck\xf7;?"
def append2img(c, image):
    # print("c")
    # print(c)
    # c=b'R0+kdh3W0aia6cMQk4TEi9Q8rHEFCiaK+C21Q57GTf+IPDAKoOr8kQlHwaPa9ELeGiP5ksyz6lIMjJf9BxdJf/GBvw17K+y1KdJuhaiGJCGS9baFgwdSRZ+OjdsAt5xyGrev8j2h8kbDQWG0sqFjz1jCZZfUX+12bOPUZPtcPMDW3T2gvcCrlTvsZldmh4kHFetD2lyOd4+kHpe5SLsgTaHLhHyw2a74wxF13b7Ksf8mITMlSNtbsnVvMdJ5AhgbGPGy5ntT7OAOksJ7HCpo74vmXrXMYU9iedl663BxuecC9YXEP2SE/QK9O9eSwP43R1O9NsI35AmC1TYzTGodUg=='
    a = int.from_bytes(c, byteorder='big', signed=False)

    s = str(a)
    arr = []
    temp = []
    chunks = [s[i:i+2] for i in range(0, len(s), 2)]
    for i in range(0, len(chunks)):
        if((i+1) % 4 == 0):
            temp.append(int(chunks[i]))
            arr.append(temp)
            temp = []
        else:
            temp.append(int(chunks[i]))

    if(len(temp) != 0):
        for i in range(4-len(temp)):
            temp.append(100)
    else:
        for i in range(4):
            temp.append(100)
    arr.append(temp)

    # for i in range(0,len(s),8):
    #   temp = []
    #   print(i)
    #   for j in range(4):
    #     temp.append(int(s[ i+(2*j) : i+2+(2*j) ]))
    #   arr.append(temp)

    # print(arr)
    t = np.array([arr], dtype=np.uint8)
    img = Image.open(image)
    img_arr = np.array(img)
    tt = np.zeros(
        (1, int(np.shape(img_arr[1, :])[0] - np.shape(t)[1]), 4), dtype=np.uint8)

    key_arr = np.concatenate((t, tt), axis=1)
    new_img_arr = np.concatenate((img_arr, key_arr), axis=0)

    new_img = Image.fromarray(new_img_arr)
    new_img.save("encoded.png", format="png")
