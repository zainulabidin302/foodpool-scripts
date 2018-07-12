
import mysql.connector

def connect(env = 'env'):
    with open(env, 'r') as f:
        con_info = f.readlines()
    
    con_info = [a.replace('\n', '') for a in con_info]
    
    cnx = mysql.connector.connect(user=con_info[0], password=con_info[1],
                                  host=con_info[2],
                                  database=con_info[3])
    return cnx

class Connector:
    def __init__(self, env = 'env'):
        self.cnx = connect(env)
    def __del__(self):
        self.cnx.commit()
        self.cnx.close()

    def query_to_list(self, qry):
        cursor = self.cnx.cursor()
        cursor.execute(qry)
        data = []
        for row in cursor:
            data.append(row)
        cursor.close()
        return data

    def count_rows(self, table):
        qry = "SELECT count(*) FROM `{}` ".format(table)
        cursor = self.cnx.cursor()
        cursor.execute(qry)
        row = cursor.next()
        cursor.close()
        return row[0]

    def query_insert(self, qry, data):
        cursor = self.cnx.cursor()
        result = cursor.execute(qry, data)
        id = cursor._last_insert_id
        cursor.close()
        return id


