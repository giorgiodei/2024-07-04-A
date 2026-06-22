from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._avvistamenti=[]
        self._idMapAvvistamenti = None


    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self):
        return DAO.getAllShapes()

    def creaGrafo(self, year, shape):

        self._grafo.clear()
        self._avvistamenti = DAO.getAllNodes(year, shape)
        self._idMapAvvistamenti = {a.id: a for a in self._avvistamenti}
        self._grafo.add_nodes_from(self._avvistamenti)
        data = DAO.getConnessione(year, shape)
        coppie = DAO.getEdges(year, shape)

        self.addEdges(coppie, data)

    def addEdges(self, coppie, data):
        for c in coppie:
            idA = c["idA"]
            idB = c["idB"]

            avvistamentoA = self._idMapAvvistamenti[idA]
            avvistamentoB = self._idMapAvvistamenti[idB]

            dataA = data[idA]
            dataB = data[idB]

            if dataA < dataB:
                self._grafo.add_edge(avvistamentoA, avvistamentoB)
            elif dataB < dataA:
                self._grafo.add_edge(avvistamentoB, avvistamentoA)
            else:
                # caso di stessa data/ora: aggiungo UN SOLO arco
                # scelgo una direzione convenzionale, ad esempio da id minore a id maggiore
                self._grafo.add_edge(avvistamentoA, avvistamentoB)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getComponentiConnesse(self):
        componenti = list(nx.weakly_connected_components(self._grafo))

        numero_componenti = len(componenti)

        componente_max = max(componenti, key=len)

        return numero_componenti, componente_max