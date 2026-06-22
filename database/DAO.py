from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime` ) as anno
from sighting s 
order by anno desc"""
            cursor.execute(query)

            res = []
            for row in cursor:
                res.append(row['anno'])

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getAllShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as forme
from sighting s 
where s.shape is not null and s.shape <>''
order by s.shape """
            cursor.execute(query)

            res = []
            for row in cursor:
                res.append(row['forme'])

            cursor.close()
            cnx.close()
            return res

    @staticmethod
    def getAllNodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
from sighting s 
where year(s.`datetime`)=%s and s.shape=%s """
            cursor.execute(query, (year, shape,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getEdges(year, shape):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT e1.id AS idA, e2.id AS idB
            FROM (
                SELECT s.id, s.state, s.datetime
                FROM sighting s
                WHERE YEAR(s.datetime) = %s
                  AND s.shape = %s
                  AND s.state IS NOT NULL
                  AND s.state <> ''
                  AND s.shape IS NOT NULL
                  AND s.shape <> ''
            ) AS e1,
            (
                SELECT s.id, s.state, s.datetime
                FROM sighting s
                WHERE YEAR(s.datetime) = %s
                  AND s.shape = %s
                  AND s.state IS NOT NULL
                  AND s.state <> ''
                  AND s.shape IS NOT NULL
                  AND s.shape <> ''
            ) AS e2
            WHERE e1.state = e2.state
              AND e1.id < e2.id
              AND e1.datetime <> e2.datetime
        """

        cursor.execute(query, (year, shape, year, shape))

        result = []
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getConnessione(year, shape):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)

        query = """
select s.id as id, s.`datetime` as data
from sighting s 
where year(s.`datetime`)=%s and s.shape=%s AND s.state IS NOT NULL
AND s.state <> ''
and  s.shape is not null and s.shape <>''"""
        cursor.execute(query, (year,shape,))

        for row in cursor:
            result[row["id"]] = row["data"]

        cursor.close()
        conn.close()
        return result