import sys
import pip
import base58
import base64
import os
import importlib
import re
import requests
import uuid
import time
import hashlib
import json
import argon2




# FUNCTIONS





def base_58_encode(string):
    return (base58.b58encode(string))


def base_58_decode(string):
    return (base58.b58decode(string))


def random_bytes(size):
    return (os.urandom(int(size)))


def base_64_encode(data):
    return (base64.b64encode(data))


def base_64_decode(data):
    return (base64.b64decode(data))


def replace_all_except_pattern(string, pattern):
    return (re.sub(pattern, '', string.decode('utf-8')))


def gen_argon(base):
    if (height % 2 == 0):
        argon2Hasher = argon2.PasswordHasher(
            time_cost=1,
            memory_cost=524288,
            parallelism=1,
            type=argon2.Type.I
        )

    else:
        argon2Hasher = argon2.PasswordHasher(
            time_cost=4,
            memory_cost=16384,
            parallelism=4,
            type=argon2.Type.I
        )

    hash = argon2Hasher.hash(base)

    return (hash)





def prepare(publicKey, privateKey, node, steroidtype, worker):
    global globalpublicKey
    global globalprivateKey
    global globalnode
    global globalsteroidtype
    global globalworker
    global counter
    global varsubmit
    global confirm
    global found
    global speed
    global avgSpeed


    globalpublicKey = str(publicKey)
    globalprivateKey = str(privateKey)
    globalnode = str(node)
    globalsteroidtype = str(steroidtype)
    globalworker = str(worker)
    counter = 0
    varsubmit = 0
    confirm = 0
    found = 0
    speed = 0
    avgSpeed = 0


    return ()

def update():


    global lastUpdate
    lastUpdate = time.time()

    extra = ''

    if(globalsteroidtype == "pool"):
        extra = "&worker=" + globalworker + "&address=" + globalprivateKey + "&hashrate=" + str(speed)


    resapi = requests.get(globalnode + "/?q=info" + extra).text
    info = json.loads(resapi)




    if(info['status'] != "ok"):
        return False

    data = info['data'][0]

    global block
    global difficulty
    global limit
    global height
    global testnet

    block = data['block']
    difficulty = data['difficulty']

    diff = int(data['difficulty'])
    limit = diff * 10000


    if(steroidtype == "pool"):
        limit = data['limit']
        globalpublicKey = data['difficulty']

    height = data['height']
    testnet = data['testnet']





    return True


def run():
    global varsubmit
    global found
    global speed
    global avgSpeed
    global confirm
    global difficulty


    allTime = round(time.time() * 1000)
    beginTime = time.time()
    it = 0
    counter = 0
    start = round(time.time() * 1000)
    while (1):
        counter = counter + 1
        if (time.time() - lastUpdate > 2):
            print(
                "--> Last hash rate: " + str(speed) + " H/s  Average: " + str(avgSpeed) + " H/s  Total hashes: " + str(
                    counter) + "  Mining Time: "
                + str(int(time.time() - beginTime)) + " s  Shares: " + str(confirm) + "  Finds: " + str(
                    found) + "  Diff: " + str(difficulty + "\n"))
            update()

        nonce = base_64_encode(random_bytes(32))
        pattern = "[^A-Za-z0-9]"
        newnonce = replace_all_except_pattern(nonce, pattern)
        base = publicKey + "-" + newnonce + "-" + block + "-" + difficulty

        argon = gen_argon(base)

        thishash = base+argon
        #print(base + " | " + argon)
        thishash = hashlib.sha512(thishash.encode('utf-8')).digest()

        for x in range(4):
            thishash = hashlib.sha512(thishash).digest()

        thishash = hashlib.sha512(thishash).hexdigest()

        split = [thishash[i:i + 2] for i in range(0, len(thishash), 2)]

        duration = str(int(split[10], base=16)) + str(int(split[15], base=16)) + str(int(split[20], base=16)) + str(
            int(split[23], base=16)) + str(int(split[31], base=16)) + str(int(split[40], base=16)) + str(
            int(split[45], base=16)) + str(int(split[55], base=16))
        duration = duration.lstrip("0")

        divresult = int(duration) / int(difficulty)
        divresult = int(divresult)
        if (divresult > 0 and divresult <= int(limit)):
            confirmed = submit(newnonce, argon)


            if (confirmed):
                found = found + 1
                confirm = confirm + 1

                print("Found: " + str(found) + " Blocks")
            else:
                print("Block not found \n")
                print("Found: " + str(found) + " Blocks")

            varsubmit = varsubmit + 1

        it = it + 1
        if (it == 10):
            it = 0
            end = round(time.time() * 1000)
            speed = 10 / (end - start)
            avgSpeed = counter / (end - allTime)
            start = end



def submit(nonce, argon):

    if(height % 2 == 0):
        argon = argon[30:]
    else:
        argon = argon[29:]

    url = (str(globalnode) + "/?q=submitNonce")
    postData = {"argon": str(argon), "nonce": str(nonce), "private_key": str(privateKey), "public_key": str(publicKey), "address": str(privateKey)}
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    mydata = requests.post(url, data=postData, headers=headers).text

    mydata = json.loads(mydata)


    if (mydata['status'] == "ok"):
        print("\n--> Nonce confirmed.\n")
        return True
    elif (mydata['status'] == "error"):
        print("--> The nonce did not confirm." + mydata["data"] + "\n\n")
        return False
    else:
        print("--> The nonce did not return a confirmed status yet but is correct.\n\n")
        return True





def output_header():
    print(r'''
    Steroid v0.4a
    www.steroid.io''')


# END FUNCTIONS
output_header()




# CODE HERE
config = open('config.txt','r')
configsplit = ''
configarrayvalue = []

config = config.readlines()

for configlines in config:
    configlines = configlines.replace('\n', '')

    configsplit = configlines.split("=")
    configarrayvalue.append(configsplit[1])



publicKey = configarrayvalue[0]
privateKey = configarrayvalue[1]
node = "https://" + str(configarrayvalue[2]) + ".steroid.io/mine"
steroidtype = configarrayvalue[3]


worker = uuid.uuid4()

prepare(publicKey, privateKey, node, steroidtype, worker)

res = update()
if (not res) :
    print("ERROR: Could not get mining info from the node")

run()

# END OF CODE
