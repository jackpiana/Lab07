import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Porcodio scegli un mese ritardato")
            return
        genova, torino, milano = self._model.um_media(self._mese) #genova, torino, milano
        self._view.load_result_umidita(genova, torino, milano)

    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Porcodio scegli un mese ritardato")
            return
        sequenza, costo = self._model.calcola_sequenza(self._mese)
        self._view.load_result_sequenza(sequenza, costo)

    def read_mese(self, e):
        self._mese = int(e.control.value)

