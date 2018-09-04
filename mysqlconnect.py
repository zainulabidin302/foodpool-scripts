
import mysql.connector

def connect(env = 'env'):
    
    cnx = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='fp_new')
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


