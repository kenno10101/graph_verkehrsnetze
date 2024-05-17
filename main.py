import sys

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
    def __init__(self, line_name: str, neighbour: Vertex, traveltime: int, next=None):
        super().__init__(next)
        self.line_name = line_name
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

    def add_edge(self, line_name: str, first_station: str, weight: int, second_station: str):
        if first_station not in self.vertices:
            self.vertices[first_station] = Vertex(first_station)
        if second_station not in self.vertices:
            self.vertices[second_station] = Vertex(second_station)

        first_vertex = self.vertices[first_station]
        second_vertex = self.vertices[second_station]

        first_edge = Edge(line_name, second_vertex, weight)
        second_edge = Edge(line_name, first_vertex, weight)

        first_vertex.neighbours.add(first_edge)
        second_vertex.neighbours.add(second_edge)

    def __iter__(self):
        return iter(self.vertices.values())


def read_graph(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) < 2:
                continue
            line_name = parts[0].strip()
            stations = parts[1].strip().split('"')
            stations = [s for s in stations if s != '']
            for i in range(0, len(stations) - 2, 2):
                station_name = stations[i]
                travel_time = int(stations[i+1].strip())
                next_station = stations[i+2]
                graph.add_edge(line_name, station_name, travel_time, next_station)
    return graph


def find_min_distance_vertex(distances, visited):
    min_distance = float('infinity')
    min_vertex = None
    for vertex, distance in distances.items():
        if distance < min_distance and vertex not in visited:
            min_distance = distance
            min_vertex = vertex
    return min_vertex


def dijkstra(graph, start, goal):
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph.vertices}
    previous_lines = {vertex: None for vertex in graph.vertices}
    visited = []

    current_vertex = start
    while current_vertex is not None:
        visited.append(current_vertex)
        current_distance = distances[current_vertex]

        for edge in graph.get_vertex(current_vertex).neighbours:
            neighbor = edge.neighbour_station_name
            weight = edge.traveltime
            line = edge.line_name
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                previous_lines[neighbor] = line

        current_vertex = find_min_distance_vertex(distances, visited)
        if current_vertex == goal:
            break

    path = []
    lines = []
    total_cost = distances[goal]
    current_vertex = goal
    while previous_vertices[current_vertex]:
        path.append(current_vertex)
        lines.append(previous_lines[current_vertex])
        current_vertex = previous_vertices[current_vertex]
    path.append(start)
    path.reverse()
    lines.reverse()
    return path, lines, total_cost


def find_path(filename, start, goal):
    graph = read_graph(filename)
    path, lines, total_cost = dijkstra(graph, start, goal)

    if path:
        print(f"Path found from {start} to {goal} with total travel time of {total_cost} minutes:")
        current_line = lines[0]
        print(f"{path[0]} via {current_line}", end='')
        for i in range(1, len(path)):
            if lines[i - 1] != current_line:
                print(f" (change to {lines[i - 1]})", end='')
                current_line = lines[i - 1]
            print(f" -> {path[i]} via {current_line}", end='')
        print()
    else:
        print(f"No path found from {start} to {goal}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: find_path filename_graph start_station goal_station")
    else:
        filename_graph = sys.argv[1]
        start_station = sys.argv[2]
        goal_station = sys.argv[3]
        find_path(filename_graph, start_station, goal_station)
