import os
import random
import discord
# import aiohttp
from dotenv import load_dotenv
import io
from PIL import Image
import PIL
import stego
import rsaFCS
from Cryptodome.PublicKey import RSA
import base64

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
privateKey = RSA.importKey(open("privateKey.pem").read())
publicKey = RSA.importKey(open("publicKey.pem").read())


@client.event
async def on_ready():
    print(f'{client.user} is online!')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    print("Somebody joined.")
    await channel.send(f"""Yo {member.mention}! you have a FCS project todo""")


def checkIfHashPresent(imageSrc):
    # print("Reached here")
    if(rsaFCS.extract_code(imageSrc) == False):
        # print("Hash Not present")
        return -1
    else:
        # print("Hash PRESENT")
        return 1


def checkIfHashValid(imageSrc, hashStored):
    with open(imageSrc, 'rb') as imageFile:
        imageString = base64.b64encode(imageFile.read())
    hashComputed = rsaFCS.gen_SHA256_digest(imageString)
    print(hashStored)
    print(len(hashStored))
    print(hashComputed)
    print(len(hashComputed))
    if(hashStored == hashComputed):
        return 1
    else:
        return -1


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    bad_words = ["bad", "stop"]

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)

    if message.content == "!help":
        embed = discord.Embed(title="Help on Mitnick",
                              description="Some useful commands")
        embed.add_field(name="!todo", value="To see whats pending.")
        embed.add_field(name="upload an image",
                        value="To see our FCS Project progress.")
        await message.channel.send(content=None, embed=embed)

    if message.content == "!todo":
        await message.channel.send(" 1. Image Stegnography \n 2. Encrypt & Decrypt message \n 3. Use Discord.py to upload encrypted image \n 4. Integrate 1,2&3 \n 5. Get full in project.")

    if message.content == "!hello":
        await message.channel.send(" Hello. I am Mitnick. \nI try to reduce the spread of fake news and unverified images. \n Beta testing in #bot-testing .")

    if message.content == "!info":
        async for m in message.channel.history(limit=10):
            if m.author.name == "Mitnick" and len(m.attachments) > 0:
                msg = m
                break

        pic_ext = ['.jpg', '.png', '.jpeg']
        for ext in pic_ext:
            if msg.attachments[0].url.endswith(ext):
                f = msg.attachments[0]
                await f.save(r"E:\Projects\MitnickDiscordBot\A.png")
                hashAisehi = rsaFCS.extract_code("A.png")
                stegoData = stego.Decode("recovered.png")
                user = await client.fetch_user(int(stegoData[1:]))
                await message.channel.send("Hey <@" + str(message.author.id) + ">! The last image has been forwarded " + stegoData[0] + " times. It was originally sent by \"" + user.name + "\"")

    pic_ext = ['.jpg', '.png', '.jpeg']

    for ext in pic_ext:
        if len(message.attachments) > 0:
            if message.attachments[0].url.endswith(ext):
                print("Image uploaded.")
                f = message.attachments[0]
                nf = await f.to_file()
                await f.save(r"E:\Projects\MitnickDiscordBot\A.png")

                if(checkIfHashPresent("A.png") == 1):
                    # hash present

                    hashStoredEncrypted = rsaFCS.extract_code("A.png")

                    # print(type(hashStoredEncrypted))
                    # print(len(hashStoredEncrypted))
                    print("enc h")
                    print(hashStoredEncrypted)
                    # print(privateKey)
                    hashStored = rsaFCS.read_msg(
                        hashStoredEncrypted, privateKey)
                    print("h")
                    print(hashStored)
                    if(checkIfHashValid("recovered.png", hashStored) == -1):
                        # hash not valid ... caution given ... treated as new image
                        print("This image has been edited.")
                        nof = str(0)
                        source = str(message.author.id)
                        stego.Encode("recovered.png", nof + source, "B.png")

                        with open("B.png", 'rb') as imageFile:
                            imageString = base64.b64encode(imageFile.read())
                        hashToBeStored = rsaFCS.gen_SHA256_digest(imageString)
                        encryptedHash = rsaFCS.encode_msg(
                            hashToBeStored, publicKey)

                        rsaFCS.append2img(encryptedHash, "B.png")

                        await message.channel.purge(limit=1)
                        await message.channel.send("Sent by <@" + str(message.author.id) + "> \n\n Caution this image has been edited by <@" + str(message.author.id) + ">  \n\n")
                        await message.channel.send(content=encryptedHash, file=discord.File('encoded.png'))
                        break

                    else:
                        # hash has been verified, integrity is maintained
                        print("hash has been verified, integrity is maintained")
                        data = stego.Decode("recovered.png")
                        nof = data[0]
                        if(int(nof) >= 5):
                            await message.channel.purge(limit=1)
                            await message.channel.send("Hey <@" + str(message.author.id) + ">!  That was an unverified image/information and has reached its forwarding limit.")
                            break

                        nof = str(int(nof) + 1)
                        source = data[1:]
                        stego.Encode("recovered.png", nof + source, "B.png")

                        with open("B.png", 'rb') as imageFile:
                            imageString = base64.b64encode(imageFile.read())
                        hashToBeStored = rsaFCS.gen_SHA256_digest(imageString)
                        encryptedHash = rsaFCS.encode_msg(
                            hashToBeStored, publicKey)

                        print("enc hs")
                        print(encryptedHash)
                        print("hs")
                        print(hashToBeStored)
                        rsaFCS.append2img(encryptedHash, "B.png")
                else:
                    # hash not present .... i.e. new image
                    print("hash not present .... i.e. new image")
                    nof = str(0)
                    source = str(message.author.id)
                    stego.Encode("A.png", nof + source, "B.png")

                    with open("B.png", 'rb') as imageFile:
                        imageString = base64.b64encode(imageFile.read())
                    hashToBeStored = rsaFCS.gen_SHA256_digest(imageString)
                    encryptedHash = rsaFCS.encode_msg(
                        hashToBeStored, publicKey)
                    rsaFCS.append2img(encryptedHash, "B.png")

                # print(encryptedHash)
                # print(len(encryptedHash))
                # print(type(encryptedHash))
                await message.channel.purge(limit=1)
                await message.channel.send(content="Sent by <@" + str(message.author.id) + ">  \n\n", file=discord.File('encoded.png'))


client.run(TOKEN)
