#!/usr/bin/env python3

import requests
import getopt, sys
import os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:n:d:", [])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print('command -u http://example.com -n hello -d dirname')
        sys.exit(2)
    
    url = None
    name = None
    directory = ''
    
    for o, a in opts:
        if o == "-u":
            url = a
        elif o == "-n":
            name = a
        elif o == "-d":
            directory = a
        else:
            assert False, "unhandled option"

    if url is None :
        print('url  is not avaialbe')
        sys.exit(2)
    
    if name is None:
        name = url.replace(':', '_').replace('/', '_').replace('.', '_')
    
    if directory is None:
        directory = './'
    
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)
    file = os.path.join(directory, name)
    with open(file, 'w') as f:
        f.write(str(r.content))
    
    print(file)
    

if __name__ == "__main__":
    main()
    
