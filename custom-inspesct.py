#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import getopt, sys
import os
import mysqlconnect

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
        
        
    con = mysqlconnect.connect()
    cursor = con.cursor()
    query = 'INSERT INTO `intermediate_restaurants_urls` ( `foodpanda_url`) VALUES (%s)'
    base_url = 'http://foodpanda.pk/city/lahore'

    with open(os.path.join('foodpool/html', 'https___www_foodpanda_pk_city_lahore'), 'r') as f:
        content = f.read()
        html = BeautifulSoup(content, 'html.parser')
        vendors = html.select('.vendor-list li a')
        
        vendors = map(lambda x: x['href'], vendors)
        
        for vendor in vendors:
            cursor.execute(query, (vendor,))
    
        con.commit()
    cursor.close()
    con.close()



if __name__ == "__main__":
    main()
    
