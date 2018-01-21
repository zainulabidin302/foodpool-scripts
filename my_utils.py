import os 

def file_to_urls(filename):
    # if filename list is found, then process all urls
    with open(filename, 'r') as f:
        content = f.readlines()
    urls = [x.strip() for x in content]
    return urls
    
def ls(dirname):
    # if filename list is found, then process all urls
    return [os.path.join(dirname, f) for f in os.listdir(dirname) if f != '.' or f != '..']


