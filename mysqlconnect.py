
import mysql.connector
cnx = None

def connect():
    with open('.env', 'r') as f:
        con_info = f.readlines()
    
    con_info = [a.replace('\n', '') for a in con_info]
    
    cnx = mysql.connector.connect(user=con_info[0], password=con_info[1],
                                  host=con_info[2],
                                  database='foodpool')
    return cnx
def close():
    cnx.close()


