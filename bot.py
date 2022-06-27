import os
import random
import discord
from dotenv import load_dotenv
import io
from PIL import Image
import PIL
import stego
import rsaFCS
from Cryptodome.PublicKey import RSA
import base64

load_dotenv()  # loading environment variables
# loading discord bot's app token for authorization
TOKEN = os.getenv('DISCORD_TOKEN')

# a client connection that connects to Discord. This class is used to interact with the Discord WebSocket and API.
client = discord.Client()
# import private and public keys for RSA cryptography
privateKey = RSA.importKey(open("privateKey.pem").read())
publicKey = RSA.importKey(open("publicKey.pem").read())


@client.event  # registers an event to listen to
async def on_ready():
    # on ready prints acknowledgement on terminal
    print(f'{client.user} is online!')


# returns 1 if hash is present else -1, helps infer if its a new image or a forwarded image
def checkIfHashPresent(imageSrc):
    if(rsaFCS.extract_code(imageSrc) == False):
        return -1
    else:
        return 1


# returns 1 if hash stored is the same as calculated hash of the image else -1, helps infer if image was edited or not
def checkIfHashValid(imageSrc, hashStored):
    with open(imageSrc, 'rb') as imageFile:
        # encodes binary data to ASCII charachters
        imageString = base64.b64encode(imageFile.read())
    # SHA256 hash of the image is generated for the image at hand
    hashComputed = rsaFCS.gen_SHA256_digest(imageString)
    if(hashStored == hashComputed):
        return 1
    else:
        return -1


@client.event
async def on_message(message):  # handles the event of when a message is sent
    if message.author == client.user:
        return

    # future feature can remove messages with curse words
    bad_words = ["curse", "words"]
    for word in bad_words:
        if message.content.count(word) > 0:
            print("Dont you curse.")  # printed in terminal
            await message.channel.purge(limit=1)  # removes last message

    if message.content == "!help":  # lists commands available
        embed = discord.Embed(title="Help",
                              description="Some useful commands")
        embed.add_field(name="!hello",
                        value="To know more \n about me.")
        embed.add_field(name="Upload an image",
                        value="To see me work.")
        embed.add_field(name="!info",
                        value="To know more about \n the last image sent.")
        await message.channel.send(content=None, embed=embed)

    if message.content == "!hello":  # Mitnick introduces himself
        await message.channel.send(" Hello. I am Mitnick. \nI try to reduce the spread of fake news and unverified images.")

    if message.content == "!info":  # provides original author of image and number of times image was forwarded forwards
        async for m in message.channel.history(limit=10):
            # ignore if author is bot itself
            if m.author.name == "Mitnick" and len(m.attachments) > 0:
                msg = m
                break

        pic_ext = ['.png']  # current extensions accepted
        for ext in pic_ext:
            if msg.attachments[0].url.endswith(ext):
                f = msg.attachments[0]
                await f.save(r".\A.png")
                hashExtracted = rsaFCS.extract_code("A.png")  # extracting hash
                # extracting data stored in image
                stegoData = stego.Decode("recovered.png")
                user = await client.fetch_user(int(stegoData[1:]))
                await message.channel.send("Hey <@" + str(message.author.id) + ">! \nThe last image has been forwarded " + stegoData[0] + " times. It was originally sent by \"" + user.name + "\"")

    pic_ext = ['.png']
    for ext in pic_ext:
        if len(message.attachments) > 0:
            if message.attachments[0].url.endswith(ext):
                print("Image uploaded.")  # printed in terminal
                f = message.attachments[0]  # image attachment of message stored
                nf = await f.to_file()  
                await f.save(r".\A.png")  # stored image file save as A.png
                if(checkIfHashPresent("A.png") == 1):  # true if hash present i.e. either forwarded image or editted image

                    encryptedHashStored = rsaFCS.extract_code("A.png")  # extarcting encrypted hash that was stored in image
                    hashStored = rsaFCS.read_msg(
                        encryptedHashStored, privateKey)  # decrypting message to form hash

                    
                    if(checkIfHashValid("recovered.png", hashStored) == -1):  # check if calculated hash matches with hash found in image
                        # hash dont match i.e. image editted since last forward... treated as new image
                        print("This image has been edited.")  # printed in terminal
                        nof = str(0)  # number of forwards
                        source = str(message.author.id)  # message author is source
                        stego.Encode("recovered.png", nof + source, "B.png")  # recovered png is png without previous hash, hiding (steganography) number of forwards and source in image

                        with open("B.png", 'rb') as imageFile:
                            imageString = base64.b64encode(imageFile.read())  # image converted to ASCII
                        hashToBeStored = rsaFCS.gen_SHA256_digest(imageString)  # hash generated of image (i.e. stegno(image))
                        encryptedHash = rsaFCS.encode_msg(
                            hashToBeStored, publicKey)  # hash encrypted

                        rsaFCS.append2img(encryptedHash, "B.png")   # encrypted hash appended to image

                        await message.channel.purge(limit=1)  # removes previous message/image to send its marked message/image
                        await message.channel.send(content="Sent by <@" + str(message.author.id) + "> \n\n Caution this image has been edited by <@" + str(message.author.id) + ">  \n\n", file=discord.File('encoded.png'))
                        break

                    else:  # hash verified, integrity is maintained
                        print(" This is a forwarded image.") # printed in terminal
                        data = stego.Decode("recovered.png")
                        nof = data[0]
                        gu = message.author.guild
                        originalAuthor = await gu.fetch_member(int(data[1:]))
                        if(int(nof) >= 5 and originalAuthor.top_role.name != "admin"):  # if number of forwards > 5 and never verified by an admin
                            await message.channel.purge(limit=1)  # removes previous message/image to send its marked message/image
                            await message.channel.send("Hey <@" + str(message.author.id) + ">!  \nThat was an unverified image/information and has reached its forwarding limit, therefore has been retracted.")
                            break

                        nof = str(int(nof) + 1)  # number of forwards 
                        source = data[1:]  # getting author of original image
                        stego.Encode("recovered.png", nof + source, "B.png")  # recovered png is png without previous hash, hiding (steganography) number of forwards and source in image

                        with open("B.png", 'rb') as imageFile:
                            imageString = base64.b64encode(imageFile.read())  # image converted to ASCII
                        hashToBeStored = rsaFCS.gen_SHA256_digest(imageString) # hash generated of image (i.e. stegno(image))
                        encryptedHash = rsaFCS.encode_msg(
                            hashToBeStored, publicKey)  # hash encrypted

                        rsaFCS.append2img(encryptedHash, "B.png")  # encrypted hash appended to image

                else: # hash not present .... i.e. new image
                    print("This is a new image.") # printed in terminal
                    nof = str(0)  # number of forwards is 0
                    source = str(message.author.id)  # image converted to ASCII
                    stego.Encode("A.png", nof + source, "B.png")  # image encoded with number of Forwards & source 

                    with open("B.png", 'rb') as imageFile:
                        imageString = base64.b64encode(imageFile.read())  # image converted to ASCII
                    hashToBeStored = rsaFCS.gen_SHA256_digest(imageString)  # hash generated of image (i.e. stegno(image)
                    encryptedHash = rsaFCS.encode_msg(
                        hashToBeStored, publicKey)  # hash encrypted
                    rsaFCS.append2img(encryptedHash, "B.png")  # encrypted hash appended to image
                    originalAuthor = message.author

                await message.channel.purge(limit=1)  # removes previous message/image, to send its marked messsage/image
                if(originalAuthor.top_role.name == "admin"):
                    await message.channel.send(content="Sent by <@" + str(message.author.id) + ">. \n:white_check_mark: Verified image.", file=discord.File('encoded.png'))
                else:
                    await message.channel.send(content="Sent by <@" + str(message.author.id) + ">. \n:warning: Caution: This image is unverified.", file=discord.File('encoded.png'))

client.run(TOKEN)
