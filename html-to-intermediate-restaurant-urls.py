#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import getopt, sys
import os
import mysqlconnect
import datetime 
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print('command -f filename')
        sys.exit(2)
    
    file = None
    name = None
    directory = ''
    
    
    for o, a in opts:
        if o == "-f":
            file = a
        else:
            assert False, "unhandled option"
    
    if file is None :
        print('file  is not avaialbe')
        sys.exit(2)
        
        
    con = mysqlconnect.connect()
    cursor = con.cursor()
    query = 'INSERT INTO `intermediate_restaurants_urls` ( `foodpanda_url`, `dt`) VALUES (%s, %s)'
    base_url = 'http://foodpanda.pk/city/lahore'

    with open(file, 'r') as f:
        content = f.read()
        html = BeautifulSoup(content, 'html.parser')
        vendors = html.select('.vendor-list li a')
        vendors = map(lambda x: x['href'], vendors)
        
        for vendor in vendors:
            cursor.execute(query, (vendor, datetime.datetime.now()) )
    
        con.commit()
    cursor.close()
    con.close()



if __name__ == "__main__":
    main()
    
