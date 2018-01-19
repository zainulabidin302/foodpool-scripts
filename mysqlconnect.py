
import mysql.connector
cnx = None

def connect():
    cnx = mysql.connector.connect(user='root', password='{(ajl:s)}df:<:<vlsd|l',
                                  host='dawndb.ciledregqogy.us-east-2.rds.amazonaws.com',
                                  database='foodpool')
    return cnx
def close():
    cnx.close()


