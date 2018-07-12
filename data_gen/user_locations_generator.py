import sys
sys.path.insert(0, '../')
import mysqlconnect
con = mysqlconnect.Connector()
import random

"""
        // Initialize and add the map
        // 1 deg is around 110 km
        // 0.1 deg is around 110/10 i.e 10 km
        // 0.1 is around 10 km radius (approx)
"""

def getNearby(n, loc, min=-0.1, max=0.1):
    locations = []
    lat, lng = loc['lat'], loc['lng']
    epsilon = 0.0
    for i in range(0, n):
        epsilon = random.random() * (max - min) + min;
        lat += epsilon;
        epsilon = random.random() * (max - min) + min;
        lng += epsilon;
        locations.append({
            'lat': lat, 'lng': lng
        })
    return locations


_LAHORE_LOCATION = {
        'lat': 31.474221,
        'lng': 74.376440
}

def generator(n):
    if (n < 1):
        return
    user_list = con.query_to_list('select id from user')

    BUNCH_CENTER = [{
        'lat': 31.538009,
        'lng': 74.328593,
        'label': 'Shadman'
    }, {
        'lat': 31.501749,
        'lng': 74.361698,
        'label': 'Cavlary Ground'
    }, {
        'lat': 31.474221,
        'lng': 74.376440,
        'label': 'DHA Phase 4'
    }];


    locations = []
    n = int((1/3)*n)
    for l in BUNCH_CENTER:
        locations += getNearby(n, l)

    print('generating ', n * len(BUNCH_CENTER), ' locations')
    users = []
    for loc in locations:
        user_pick_index = random.randint(0, len(user_list) - 1)
        user_id = user_list[user_pick_index][0]
        users.append(user_id)

        qry = """
            INSERT INTO user_locations VALUES(NULL, %s, %s, NULL, %s)
        """
        con.query_insert(qry, (loc['lat'], loc['lng'], user_id))

    print("for ", len(set(users)), " users")