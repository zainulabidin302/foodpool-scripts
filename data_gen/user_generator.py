import sys
sys.path.insert(0, '../')
import mysqlconnect
con = mysqlconnect.Connector()

import random
import string
import sys
import os


def gen_phone():
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)

    last = (str(random.randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,9998)).zfill(4))

    return '{}-{}-{}'.format(first,second, last)

def generate_word(length):
    VOWELS = "aeiou"
    CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def generate(n):
    if n < 1:
        return 0
    dir_path = os.path.dirname(os.path.realpath(__file__))

    domains = []
    names = []
    images = []
    with open(os.path.join(dir_path, 'domains.txt'), 'r') as f:
        domains = f.readlines()
    with open(os.path.join(dir_path, 'names.txt'), 'r') as f:
        names = f.readlines()
    with open(os.path.join(dir_path, 'images.txt'), 'r') as f:
        images = f.readlines()

    ids = []
    for i in range(0, n):
        first_name = names[random.randint(0, len(names)-1)].replace('\n', '')
        last_name = names[random.randint(0, len(names)-1)].replace('\n', '')
        name = first_name + ' ' + last_name
        username = name.replace(' ', '_') + generate_word(5)
        username = username.lower()

        email = username + '@' + domains[random.randint(0, len(domains)-1)]
        password = generate_word(8)

        img_url = images[random.randint(0, len(images)-1)]
        phone = gen_phone()
        data = (first_name, last_name, username, email, img_url, password, phone)
        qry = """
            INSERT INTO `user` VALUES (NULL, %s,%s, %s, %s, %s, MD5(%s), %s)
        """

        ids.append(con.query_insert(qry, data))

    print("{} users were added successfully.".format((ids)))