#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import getopt, sys
import os
import mysqlconnect
import datetime 
import my_utils
import urllib
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
        
        
        query_restaurant = 'update `restaurants` set `lat` = %(lat)s , `lon` = %(lon)s where `fp_url` = %(fp_url)s' 
       
        with open(file, 'r') as f:
            content = f.read()
            html = BeautifulSoup(content, 'html.parser')
            foodpanda_url = file.replace('restaurant_html_pages/https___foodpanda_pk_', 'https://foodpanda.pk/').replace('_', '/')
            lat = lon = 0

            try:

                params = urllib.parse.urlparse(html.select('img.map')[0]['src']).query.split('&')
                for param in params:
                    if param.split('=')[0] == 'center':
                        lat, lon = param.split('=')[1].split(",")
                        print(lat, lon)
            except Exception as e:
                print('log: ', e)
                
            
            query_params = {
                 'lat': float(lat),
                 'lon': float(lon),
                 'fp_url': foodpanda_url
                }
            
            cursor.execute(query_restaurant,  query_params)
            
            con.commit()
        
    cursor.close()
    con.close()



if __name__ == "__main__":
    main()
    
