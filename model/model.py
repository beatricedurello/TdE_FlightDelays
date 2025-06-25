import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestPath = []
        self._bestObjF = 0

    def getCamminoOttimo(self, v0, v1, t):
        self._bestPath = []
        self._bestObjF = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)

        return self._bestPath, self._bestObjF

    def _ricorsione(self, parziale, v1, t):
        #verificare se è una possibile soluzione
        if parziale[-1] == v1:
            #verificare se è meglio del best
            if self.getObjF(parziale) > self._bestObjF:
                self._bestPath = copy.deepcopy(parziale)
                self._bestObjF = self.getObjF(parziale)
        if len(parziale) == t+1:
            return
        #posso ancora aggiungere nodi
            #prendo i vicini e aggiungo un nodo alla volta
            #ricorsione
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def getObjF(self, listOfNodes):
        objval = 0
        for i in range(0, len(listOfNodes)-1):
            objval += self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return objval

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addAllArchiV1()
        print(f"Numero nodi: {len(self._graph.nodes)} Numero archi: {self._graph.number_of_edges()}")

    def addAllArchiV1(self):
        allEdges = DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def addAllArchiV2(self):
        allEdges = DAO.getAllEdgesV2(self._idMapAirports)
        self._graph.add_edges_from(allEdges)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes =  list(self._graph.nodes)
        nodes.sort(key= lambda x:x.IATA_CODE)
        return nodes

    def getSortedNeighbours(self, node):
        neighbours = self._graph.neighbors(node)
        neighbTuples = []
        for n in neighbours:
            neighbTuples.append((n, self._graph[node][n]["weight"]))
        neighbTuples.sort(key=lambda x:x[1], reverse=True)
        return neighbTuples

    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)
        # path = nx.shortest_path(self._graph, v0, v1)
        # myDict = nx.bfs_predecessors(self._graph, v0)
        # path = [v1]
        # while path[0]
        return path