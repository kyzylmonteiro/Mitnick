# Mitnick
A Discord Bot that curbs the spread of unverified image in a Discord Server, with a special focus on security. \
Contributors: Kyzyl, Kinshu, Srija, Nishtha Singhal and Nishtha Ahuja

## Features
- Limits number of times an image can be forwarded.
- Role based information verification.
- Readers are cautioned when edited images are sent.

## Meet Mitnick, he processes every image sent in a channel to...

<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/processing.gif"  />
</p>

### Caution readers about unverified information
<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/nonAdminLevel.png"  />
</p>

### Share the Original Sender of the image and the number of times it was forwarded
<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/infoFeature.png" />
</p>

### Retracts unverified images sent more than 5 times 
<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/retractionFeature.png" />
</p>

### Mark images sent by the admin as Verified
<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/adminLevel.png" />
</p>

### Cautions readers when images are edited forwards
<p align="middle" float="left">
<img src="https://github.com/kyzylmonteiro/Mitnick/blob/main/demo/editedImage.png"  />
</p>

## Our Approach
To do his job Mitnick employs the following techniques:
- image steganography - LSB
- integrity check using hashing - SHA256
- Cryptosystem - RSA

### Mitnick's Approach 
Every time an image is sent:
```python
if(checkIfHashPresent(image) == False):
    # hash not present .... i.e. new image
    nof = 0
    source = message.author.id
    #now storing message in image, hashing, encrypting hash and then appending to image
    stego.Encode(image, nof + source)
    hashToBeStored = Hash(image)
    encryptedHash = RSA.encrypt(hashToBeStored, publicKey)
    appendToImage(encryptedHash, image)
else: 
    #hash present
    if(checkIfHashValid(image) == True):
        #hash verified, integrity maintained
        nof, source = stego.decode(image)
        if(nof>5):
            #ignore image sent more than 5 times
            break
        nof++
        #now storing message in image, hashing, encrypting hash and then appending to image
        stego.Encode(image, nof + source)
        hashToBeStored = Hash(image)
        encryptedHash = RSA.encrypt(hashToBeStored, publicKey)
        appendToImage(encryptedHash, image)
    else:
        # hash not valid ...edited image... give caution... treat as new image
        nof = 0
        source = message.author.id
        #now storing message in image, hashing, encrypting hash and then appending to image
        stego.Encode(image, nof + source)
        hashToBeStored = Hash(image)
        encryptedHash = RSA.encrypt(hashToBeStored, publicKey)
        appendToImage(encryptedHash, image)

```





