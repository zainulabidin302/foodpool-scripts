
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../')
import mysqlconnect
con = mysqlconnect.Connector("../env")






def get_users():
    usrs = con.query_to_list("select * from `user`")
    lst = map(
        lambda x : {
            "id": x[0],
            "first_name": x[1],
            "last_name": x[2],
            "username": x[3],
            "email": x[4],
        } , usrs)
    print(list(lst)[10])





def train():
    qry = """
        select 
            `user`.`id` ,
            concat(`user`.first_name, " ", `user`.last_name) `name`,
            `user_locations`.lat,
            `user_locations`.lon,
            `restaurant_comments`.comment,
            `restaurant_comments`.rating,
            `restaurant_comments`.label,
            `restaurant_comments`.restaurant_id
            
                 FROM `user`
            left join `user_locations` on `user_locations`.`user_id` = `user`.`id`
            left join `restaurant_comments` on `restaurant_comments`.`user_id` = `user`.`id`
            order by user.id
    """

    features = con.query_to_list(qry)

def predict():
    pass




train()

