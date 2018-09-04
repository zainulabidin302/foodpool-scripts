
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, '../')
sys.path.insert(0, './')
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





def predict(id, n=10):
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

    df = pd.DataFrame(con.query_to_list(qry), columns=['id', 'name', 'lat', 'lon','comment','rating', 'label', 'rid'])
    # will this effect the final result?
    from collections import defaultdict
    d = defaultdict(LabelEncoder)
    # Encoding the variable
    fit = df.astype(str).apply(lambda x: d[x.name].fit_transform(x))

    # Inverse the encoded
    fit_inv = fit.apply(lambda x: d[x.name].inverse_transform(x))

    nbrs = NearestNeighbors(n_neighbors=n).fit(fit)
    print(id)
    print(fit[fit['id']==20].apply(lambda x: d[x.name].inverse_transform(x)))
    user_fit = fit[fit['id'] == id] # 0 == id
    print(user_fit)
    print(user_fit.apply(lambda x: d[x.name].inverse_transform(x)))

    distances, indices = nbrs.kneighbors(user_fit)
    print(indices)