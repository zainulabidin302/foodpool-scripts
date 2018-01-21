#!/usr/bin/env python3

import requests
import getopt, sys
import os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:n:d:f:", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print('command -u http://example.com -n hello -d dirname')
        sys.exit(2)
    
    url = None
    name = None
    filename = None
    directory = ''
    
    for o, a in opts:
        
        if o == "-f":
            filename = a
        elif o == "-u":
            url = a
        elif o == "-n":
            name = a
        elif o == "-d":
            directory = a
        else:
            assert False, "unhandled option"
    urls = None

    if filename is not None:
        # if filename list is found, then process all urls
        with open(filename, 'r') as f:
            content = f.readlines()
        urls = [x.strip() for x in content]
        
    elif url is None :
        print('url  is not avaialbe')
        sys.exit(2)
    
    if urls is None:
        urls = [url]
    
    get_name = lambda x: x.replace(':', '_').replace('/', '_').replace('.', '_')
    
    if directory is None:
        directory = './'
    
    for u in urls:
        
        headers = {'user-agent': 'my-app/0.0.1'}
        r = requests.get(u, headers=headers)
        file = os.path.join(directory, get_name(u))
        
        with open(file, 'w') as f:
            f.write(str(r.content))
        print(file)
    

if __name__ == "__main__":
    main()
    
