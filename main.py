class Vertex:
    pass


class AdjListNode:
    def __init__(self, value: Vertex):
        self.value = value
        self.next = None

class Vertex:
    def __init__(self, station_name, trainline):
        self.station_name = station_name
        self.trainline = trainline
class Edge:
    def __init__(self, destination: Vertex, traveltime):
        self.destination = destination.station_name
        self.trainline = destination.trainline
        self.traveltime = traveltime # Weight
class Graph:
    def __init__(self, verticesNum: int):
        self.verticesNum = verticesNum
        self.graph = [None]  * self.verticesNum

    def addVertex(self, source: Vertex, destination: Vertex):
        newVertex = AdjListNode(destination)
        newVertex.next = self.graph[source]
        self.graph[source] = newVertex



def dijkstra(graph: Graph, nodesNum: int, startNode: Vertex):

def main():
    ubahnnetz = Graph()


if __name__ == '__main__':
    main()

