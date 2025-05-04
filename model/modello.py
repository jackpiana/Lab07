import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self._count = -1

    def get_all_situazioni(self):
        return MeteoDao.get_all_situazioni()

    def get_situazioni_mese(self, mese):
        return MeteoDao.get_situazioni_mese(mese)

    def get_situazioni_mese_15gg(self, mese):
        return MeteoDao.get_situazioni_mese_15gg(mese)

    def um_media(self, mese):
        situazioni = self.get_all_situazioni()
        sumGenova = 0
        sumTorino = 0
        sumMilano = 0
        countGenova = 0
        countTorino = 0
        countMilano = 0
        for situazione in situazioni:
            citta = situazione.localita
            match citta:
                case "Genova":
                    if situazione.data.month == mese:
                        countGenova += 1
                        sumGenova += situazione.umidita
                case "Torino":
                    if situazione.data.month == mese:
                        countTorino += 1
                        sumTorino += situazione.umidita
                case "Milano":
                    if situazione.data.month == mese:
                        countMilano += 1
                        sumMilano += situazione.umidita

        return sumGenova/countGenova, sumTorino/countTorino, sumMilano/countMilano

    def calcola_sequenza(self, mese):
        self.n_soluzione = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_situazioni_mese_15gg(mese)
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale) + 1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidate, parziale):
        # vincolo sui 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False

        # vincolo su permanenza
        # 1) lunghezza di parziale minore di 3
        if len(parziale) == 0:
            return True

        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False
        # 2) le tre situazioni precedenti non sono tutte uguali
        else:
            if parziale[-3].localita != parziale[-2].localita or parziale[-3].localita != parziale[-1].localita or \
                    parziale[-2].localita != parziale[-1].localita:
                if parziale[-1].localita != candidate.localita:
                    return False
        # altrimenti ok
        return True

    def _calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        # 2) costo su spostamenti
        for i in range(len(parziale)):
            # se i due giorni precedenti, non sono stato nella
            # stessa citta in cui sono ora, pago 100
            if (i >= 2 and
                    (parziale[i - 1].localita != parziale[i].localita or
                     parziale[i - 2].localita != parziale[i].localita)):
                costo += 100

        return costo

    def _ricorsione(self, parziale, lista_situazioni):
        # condizione terminale
        if len(parziale) == 15:
            self.n_soluzione += 1
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)
            # pass

        # condizione ricorsiva
        else:
            # cercare le città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale, lista_situazioni)
            # provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                # verifica_vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()

if __name__ == '__main__':
    m = Model()
    print(m.calcola_sequenza(5))


