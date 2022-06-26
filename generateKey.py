from Crypto.PublicKey import RSA

def export_private_key(private_key, filename):

    with open(filename, "wb") as file:
        file.write(private_key.exportKey('PEM'))
        file.close()

def export_public_key(public_key1, filename):

    with open(filename, "wb") as file:
        file.write(public_key1.exportKey('PEM'))
        file.close()

keypair = RSA.generate(2048)
public_key = keypair.publickey()

export_private_key(keypair, 'privateKey.pem')
export_public_key(public_key, 'publicKey.pem')