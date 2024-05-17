class Node:
    def __init__(self, next=None):
        self.next = next

    def set_next(self, new_next_node):
        self.next = new_next_node


class Vertex(Node):
    def __init__(self, station_name: str, next=None):
        super().__init__(next)
        self.station_name = station_name
        self.neighbours = LinkedList()  # linked list of edges


class Edge(Node):
    def __init__(self, neighbour: Vertex, traveltime: int, next=None):
        super().__init__(next)
        self.neighbour_station_name = neighbour.station_name
        self.traveltime = traveltime  # weight


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, value):
        newNode = value
        newNode.set_next(self.head)
        self.head = newNode

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next


class Graph:
    def __init__(self):
        self.vertices = {}  # dictionary of vertices by station name (key=station name, value=vertex object)

    def get_vertex(self, station_name):
        return self.vertices.get(station_name)

    def add_edge(self, first_station: str, second_station: str, weight: int):
        # Create vertex object and store in dictionary of vertices, if it's not in dictionary already
        if first_station not in self.vertices:
            self.vertices[first_station] = Vertex(first_station)
        if second_station not in self.vertices:
            self.vertices[second_station] = Vertex(second_station)

        # Access vertex objects of first and second station
        first_vertex = self.vertices[first_station]
        second_vertex = self.vertices[second_station]

        # Create edges
        first_edge = Edge(second_vertex, weight)
        second_edge = Edge(first_vertex, weight)

        # Add edges to vertices' list of edges
        first_vertex.neighbours.add(first_edge)
        second_vertex.neighbours.add(second_edge)

    def __iter__(self):
        return iter(self.vertices.values())


def main():
    ubahnnetz = Graph()
    ubahnnetz.add_edge("Leopoldau", "Grossfeldsiedlung", 2)
    ubahnnetz.add_edge("Grossfeldsiedlung", "Aderklaaer Strasse", 1)
    ubahnnetz.add_edge("Aderklaaer Strasse", "Rennbahnweg", 1)
    ubahnnetz.add_edge("Rennbahnweg", "Kagraner Platz", 2)

    # Example of iterating over the graph
    for vertex in ubahnnetz:
        print(f"Station: {vertex.station_name}")
        for edge in vertex.neighbours:
            print(f"  connects to {edge.neighbour_station_name} with travel time {edge.traveltime}")

    print(ubahnnetz.vertices["Leopoldau"].neighbours.head.neighbour_station_name)

if __name__ == '__main__':
    main()