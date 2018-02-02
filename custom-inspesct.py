#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import getopt, sys
import os
import mysqlconnect
import urllib 

def main():
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "u:n:d:", [])
    # except getopt.GetoptError as err:
    #     # print help information and exit:
    #     print(err) # will print something like "option -a not recognized"
    #     print('command -u http://example.com -n hello -d dirname')
    #     sys.exit(2)
    
    # url = None
    # name = None
    # directory = ''
    
    
    # for o, a in opts:
    #     if o == "-u":
    #         url = a
    #     elif o == "-n":
    #         name = a
    #     elif o == "-d":
    #         directory = a
    #     else:
    #         assert False, "unhandled option"
    
    # if url is None :
    #     print('url  is not avaialbe')
    #     sys.exit(2)
    
    # if name is None:
    #     name = url.replace(':', '_').replace('/', '_').replace('.', '_')
    
    # if directory is None:
    #     directory = './'
    
    # file = os.path.join(directory, name)
    # with open(file, 'w') as f:
    #     f.write(r.content)
    
    # print(len(r.content), ' Bytes written at ', file)
        
        
    #con = mysqlconnect.connect()
    #cursor = con.cursor()
    #query = 'INSERT INTO `intermediate_restaurants_urls` ( `foodpanda_url`) VALUES (%s)'
    #base_url = 'http://foodpanda.pk/city/lahore'

    with open(os.path.join('foodpool/restaurant_html_pages', 'https___foodpanda_pk_chain_cb0kl_nando-s'), 'r') as f:
        content = f.read()
        html = BeautifulSoup(content, 'html.parser')
        
        params = urllib.parse.urlparse(html.select('img.map')[0]['src']).query.split('&')
        for param in params:
            if param.split('=')[0] == 'center':
                lat, lon = param.split('=')[1].split(",")
                print(lat, lon)
                break
        
        #for vendor in vendors:
            #cursor.execute(query, (vendor,))
    
        #con.commit()
    #cursor.close()
    #con.close()



if __name__ == "__main__":
    main()
    
