from database.DB_connect import DBConnect
from model.connessione import Connessione

from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row)) #lista d oggetti di tipo Fermata
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnessione(u:Fermata,v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    from connessione c 
                    where c.id_stazP = %s and c.id_stazA = %s"""
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row) # lista d oggetti di tipo Fermata
        cursor.close()
        conn.close()
        return len(result)>0

    @staticmethod
    def getVicini(u):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from connessione c
                    where c.id_stazP = %s"""
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row))  # lista d oggetti di tipo Fermata
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from connessione c
                   """
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))  # lista d oggetti di tipo Fermata
        cursor.close()
        conn.close()
        return result


    @staticmethod

    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select id_stazP as P , id_stazA as A , count(*) as n
                    from connessione c 
                    group by id_stazP , id_stazA 
                    order by n as DESC  """
        cursor.execute(query)

        for row in cursor:
            result.append((row["P"], row["A"], row["n"]))  # lista d oggetti di tipo Fermata
        cursor.close()
        conn.close()
        return result





