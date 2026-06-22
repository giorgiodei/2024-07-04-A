import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self, dd: ft.Dropdown()):
        years= self._model.getAllYears()
        for r in years:
            dd.options.append(ft.dropdown.Option(text=r))

    def fillDDShapes(self, dd: ft.Dropdown()):
        shapes= self._model.getAllShapes()
        for r in shapes:
            dd.options.append(ft.dropdown.Option(text=r))

    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value

        if year is None or shape is None:
            self._view.create_alert("Seleziona entrambi i dropdown")
            return

        self._model.creaGrafo(year, shape)

        n, m = self._model.getGraphDetails()

        num_componenti, componente_max = self._model.getComponentiConnesse()

        self._view.txt_result1.controls.clear()

        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {n}")
        )

        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di archi: {m}")
        )

        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {num_componenti} componenti connesse")
        )

        self._view.txt_result1.controls.append(
            ft.Text(
                f"La componente connessa più grande è costituita da "
                f"{len(componente_max)} nodi:"
            )
        )

        for nodo in componente_max:
            self._view.txt_result1.controls.append(
                ft.Text(
                    f"id:{nodo.id} - {nodo.city} [{nodo.state}], {nodo.datetime}"
                )
            )

        self._view.update_page()


    def handle_path(self, e):
        pass
