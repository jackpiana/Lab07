from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))   #costruttore oggetto situazione
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_situazioni_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                                FROM situazione s
                                WHERE month(data) = %s 
                                ORDER BY s.Data ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))  # costruttore oggetto situazione
            cursor.close()
            cnx.close()
        return result

    def get_situazioni_mese_15gg(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                                FROM situazione s
                                WHERE month(data) = %s 
                                AND day(data) <= 15
                                ORDER BY s.Data ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))  # costruttore oggetto situazione
            cursor.close()
            cnx.close()
        return result


if __name__ == '__main__':
    meteo = MeteoDao()
    for situazione in meteo.get_situazioni_mese(6):
        print(situazione)
