import sys
import random
sys.path.insert(0, '../')
import mysqlconnect

con = mysqlconnect.Connector()


import os
def generate(n):
    if n < 1:
        return 0
    qry = """
        SELECT `id` FROM `user`
    """
    uids = con.query_to_list(qry)
    qry = """
        SELECT `id` FROM `restaurants`
    """
    rids = con.query_to_list(qry)
    ids = []

    for i in range(0, n):
        user_id = uids[random.randint(0, len(uids)-1)][0]
        rest_id = rids[random.randint(0, len(rids)-1)][0]
        rating = 2.5
        qry = "INSERT INTO `user_restaurant_likes` (restaurant_id, user_id, rating) VALUES( %s, %s, %s)"

        id = con.query_insert(qry, (rest_id, user_id, rating))
        ids.append(id)

    print('{} likes were added '.format(len(ids)))