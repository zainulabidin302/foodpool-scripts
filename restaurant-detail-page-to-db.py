#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import getopt, sys
import os
import mysqlconnect
import datetime 
import my_utils
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print('command -f filename')
        sys.exit(2)
    
    file = None
    dir_name = None
    
    
    for o, a in opts:
        if o == "-f":
            file = a
        elif o == "-d":
            dir_name = a
        
        else:
            assert False, "unhandled option"
    
    files = None
    if dir_name is not None :
        files = my_utils.ls(dir_name)
        
        
    elif file is None :
        print('file  is not avaialbe')
        sys.exit(2)
    
    if files is None:
        files = [file]
    
    con = mysqlconnect.connect()
    cursor = con.cursor()  
    
    for file in files:
        

        query_restaurant = 'INSERT INTO `restaurants` ( `title`, `logo_url`, `rating`, `timing`, `cuisines`, `fp_url`) VALUES (%s, %s, %s, %s, %s, %s)'
        
        query_comment = 'INSERT INTO `restaurant_comments` ( `username`, `date`, `comment`, `rating`, `restaurant_id`) VALUES (%(username)s, %(date)s, %(comment)s, %(rating)s, %(restaurant_id)s)'
        
        with open(file, 'r') as f:
            content = f.read()
            
            html = BeautifulSoup(content, 'html.parser')
            
            foodpanda_url = file.replace('restaurant_html_pages/https___foodpanda_pk_', 'https://foodpanda.pk/').replace('_', '/')
            print(file, foodpanda_url)
            title = count = timing = vendor_cuisines = logo_url = ''
            rating = -1
            
            try:
                
                title = html.select('h1')[0].get_text()
                logo_url = html.select('.vendor-logo')[0]['src']
                timing = html.select('.schedule-times')[0].get_text().replace('\\n', '').strip()
                vendor_cuisines = map(lambda x: x.get_text(), html.select('.vendor-cuisines li'))
                reviews_count = html.select('.review-count-title')[0].get_text().replace('\\n', '').strip()
                rating = html.select('.hero-banner-wrapper.redesign-vendor-info .rating')[0].get_text()
                count = html.select('.hero-banner-wrapper.redesign-vendor-info .count')[0].get_text()
            except Exception as e:
                print((title, logo_url, rating, timing, ','.join(list(vendor_cuisines)),))
                print('log: ', e)
                
                
            query_params = (title, logo_url, rating, timing, ','.join(list(vendor_cuisines)), foodpanda_url,  )
            
            cursor.execute(query_restaurant,  query_params)
            restaurant_id = cursor.lastrowid
    
            reviews = html.select('.review-component.hreview')
            for review in reviews:
                dt = review.select('.review-date.dtreviewed')[0].get_text().replace('\\n', '').strip()
                formated_date = datetime.datetime.strptime(dt, '%d-%b-%Y')
                
                comment = {
                    'username': review.select('.reviewer.vcard .fn')[0].get_text(),
                    'date': formated_date,
                    'rating': int(review.select('.rating')[0].get_text()),
                    'comment': review.select('.description')[0].get_text().replace('\\n', '').strip(),
                    'restaurant_id': restaurant_id
                }
                
                cursor.execute(query_comment, comment)
        con.commit()
    cursor.close()
    con.close()



if __name__ == "__main__":
    main()
    
