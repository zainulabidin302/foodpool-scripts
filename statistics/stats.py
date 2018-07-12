import sys
sys.path.insert(0, '../')
import mysqlconnect
con = mysqlconnect.Connector()
def stats():

    print('{:<10}{:*^50}{:>10}'.format(10*'*', ' SYSTEM STATS ',  10*'*'))
    print('{:<10}{:*^50}{:>10}'.format(10*'*', ' TOTALS ',  10*'*'))
    print('TOTAL USERS {}'.format(con.count_rows('user')))


    print('-----> TOTAL USER RESTAURANT LIKES {}'.format(con.count_rows('user_restaurant_likes')))
    qry = """
    SELECT COUNT(*) FROM 
	    (SELECT COUNT(*) cnt FROM `user_restaurant_likes` GROUP BY user_id) AS t
	"""
    print('-----> ALL USERS WHO LIKED A RESTAURANT {}'.format(con.query_to_list(qry)[0][0]))

    qry = """
    SELECT * FROM 
        (SELECT /* user_id, */ COUNT(*) cnt FROM `user_restaurant_likes` GROUP BY user_id) AS t ORDER BY cnt DESC LIMIT 0, 10
    	"""
    print('-----> TOP 10 USERS WHO LIKED A RESTAURANT (BY COUNTS OF LIKES) {}'.format(con.query_to_list(qry)))

    qry = """
    SELECT AVG(cnt) FROM 
        (SELECT COUNT(*) cnt FROM `user_restaurant_likes` GROUP BY user_id) AS t 
    	"""
    print('-----> AVERAGE LIKES PER USER (ONLY USERS WHO LIKED SOMETHING) {}'.format(con.query_to_list(qry)))

    print('-----> USER LOCATIONS {}'.format(con.count_rows('user_locations')))

    print('')

    print('PRODUCTS {}'.format(con.count_rows('products')))
    print('-----> VARIATIONS {}'.format(con.count_rows('product_variations')))
    print('-----> VARIATION TOPPINGS {}'.format(con.count_rows('product_variation_toppings')))
    print('-----> VARIATION TOPPING OPTIONS {}'.format(con.count_rows('product_variation_topping_options')))
    print('-----> TOTAL PRODUCT LIKES BY USERS {}'.format(con.count_rows('user_product_likes')))

    qry = """
      SELECT * FROM 
          (SELECT COUNT(*) cnt FROM `user_product_likes` GROUP BY product_id) AS t ORDER BY cnt DESC LIMIT 0, 10
      	"""
    print('-----> TOP 10 PRODUCTS LIKED BY USERS (BY COUNTING LIKES) {}'.format(con.query_to_list(qry)))
    qry = """
      SELECT * FROM 
          (SELECT COUNT(*) cnt FROM `user_product_likes` GROUP BY user_id) AS t ORDER BY cnt DESC LIMIT 0, 10
      	"""
    print('-----> TOP 10 USERS WHO LIKED PRODUCTS (BY COUNTING LIKES) {}'.format(con.query_to_list(qry)))

    print('')

    print('RESTAURANTS {}'.format(con.count_rows('restaurants')))
    print('-----> RESTAURANTS CATEGORIES {}'.format(con.count_rows('restaurant_categories')))

    qry = """
    SELECT * FROM 
        (SELECT COUNT(*) cnt FROM `user_restaurant_likes` GROUP BY restaurant_id) AS t ORDER BY cnt DESC LIMIT 0, 10
    	"""
    print('-----> TOP 10 RESTAURANTS LIKED BY USERS (BY COUNTING LIKES) {}'.format(con.query_to_list(qry)))

    qry = """
    SELECT AVG(cnt) FROM 
        (SELECT COUNT(*) cnt FROM `user_restaurant_likes` GROUP BY restaurant_id) AS t 
    	"""
    print('-----> AVERAGE LIKES PER PER RESTAURANT {}'.format(con.query_to_list(qry)))