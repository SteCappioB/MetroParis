import flet as ft



class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model




    def handleCreaGrafo(self,e):
        # crea il grafo
        self._model.buildGraph()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("grafo correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f"grafo contiene {self._model.getNumNodi()} nodi "))
        self._view.lst_result.controls.append(ft.Text(f"grafo contiene {self._model.getNumArchi()} archi "))
        self._view._btnCalcola.disabled = False
        self._view.update_page()



    def handleCercaRaggiungibili(self,e):
        # metodo che posso chiamare solo se il grafo è stato creato -->  modifico il view per dire che il pulsante calcola comincia
        # da disabilitato, e lo riabilito quando creo il crafo

        if self._fermataPartenza is None:
            self._view.lst_result.controls.clear()      # VERIFICA CHE L'UTENTE ABBIA SELEZIONATO UNA FERMATA
            self._view.lst_result.controls.append(ft.Text("attenzione, non hai selezionato la fermata di partenza", color="red"))
            self._view.update_page()
            return

        nodes = self._model.getBFSNodesFromEdges(self._fermataPartenza) # nodi visitabili dalla fermata di partenza
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"di seguito le stazioni raggiungibili a partire da{self._fermataPartenza}"))
        for n in nodes:
            self._view.lst_result.controls.append(n)
        self._view.update_page()


    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
