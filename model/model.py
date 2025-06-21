
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()

        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f #associa l'id della fermata all'oggetto fermata

    def buildGraph(self):
        #aggiungo i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges3()


    def addEdges1(self):
        # aggiungo gli archi con doppio ciclo sui nodi e testando se per ogni coppia esiste una connesisone
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnessione(u, v) and u != v:
                    self._grafo.add_edge(u, v)
                    print(f"aggiunto arco tra: {u} e {v} ")


    def addEdges2(self):
        # ciclo SOLO UNA VOLTA, e faccio una query per trovare tutti i vicini
        for u in self._fermate:
            for conn in DAO.getVicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)



    def addEdges3(self):
        # faccio una query unica che prende tutti gli archi e poi ciclo qui
        allEdges = DAO.getAllEdges()
        for e in allEdges:
            u = self._idMapFermate[e.id_stazP]
            v = self._idMapFermate[e.id_stazA]
            self._grafo.add_edge(u, v)


    def addEdgesPesati(self):
        allEdges = DAO.getAllEdges()
        for e in allEdges:
            u = self._idMapFermate[e.id_stazP]
            v = self._idMapFermate[e.id_stazA]
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"]+=1
            else:
                self._grafo.add_edge(u, v, weight=1)


    def addEdgesPesatiV2(self):
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdgesPesati()
        for e in allEdges:
            u = self._idMapFermate[e.id_stazP]
            v = self._idMapFermate[e.id_stazA]
            self._grafo.add_edge(u, v, weight=e.peso)





    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getBFStree(self, source):
        #cerco l'albero di visita, partendo dal nodo source --> lo dice l'utente dal dropdown
        tree  = nx.bfs_tree(self._grafo, source) # è un grafo a tutti gli effetti, oreintato e costruito a partire da BFS partito da source
        archi = (tree.edges())
        nodes = list(tree.nodes())
        return nodes[1::]

    def getDFStree(self,source):
        tree = nx.dfs_tree(self._grafo, source)
        nodes = list(tree.nodes())
        return nodes[1::]

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        res = []
        for u,v in archi:
            res.append(v)
        return res

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()



    @property
    def fermate(self):
        return self._fermate