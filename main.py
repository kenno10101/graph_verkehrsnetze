import sys
import heapq

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
    def __init__(self, neighbour: Vertex, traveltime: int, line: str, next=None):
        super().__init__(next)
        self.neighbour_station_name = neighbour.station_name
        self.traveltime = traveltime  # weight
        self.line = line  # U-Bahn/Straßenbahn line


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

    def add_edge(self, first_station: str, second_station: str, weight: int, line: str):
        # Create vertex object and store in dictionary of vertices, if it's not in dictionary already
        if first_station not in self.vertices:
            self.vertices[first_station] = Vertex(first_station)
        if second_station not in self.vertices:
            self.vertices[second_station] = Vertex(second_station)

        # Access vertex objects of first and second station
        first_vertex = self.vertices[first_station]
        second_vertex = self.vertices[second_station]

        # Create edges
        first_edge = Edge(second_vertex, weight, line)
        second_edge = Edge(first_vertex, weight, line)

        # Add edges to vertices' list of edges
        first_vertex.neighbours.add(first_edge)
        second_vertex.neighbours.add(second_edge)

    def __iter__(self):
        return iter(self.vertices.values())

    def dijkstra(self, start, goal):
        # Dijkstra's algorithm to find shortest path from start to destination
        queue = [(0, start, [])]
        visited = set()
        min_times = {start: 0}

        while queue:
            (current_time, current_station, path) = heapq.heappop(queue)

            if current_station in visited:
                continue

            path = path + [current_station]

            if current_station == goal:
                return (current_time, path)

            visited.add(current_station)

            current_vertex = self.get_vertex(current_station)
            for edge in current_vertex.neighbours:
                neighbour = edge.neighbour_station_name
                time = current_time + edge.traveltime

                if neighbour not in visited or time < min_times.get(neighbour, float('inf')):
                    min_times[neighbour] = time
                    heapq.heappush(queue, (time, neighbour, path))

        return (float('inf'), [])

    def find_path(self, start, goal):
        total_time, path = self.dijkstra(start, goal)
        if total_time == float('inf'):
            return "No path found"

        result = []
        for i in range(len(path) - 1):
            current_station = path[i]
            next_station = path[i + 1]
            current_vertex = self.get_vertex(current_station)
            for edge in current_vertex.neighbours:
                if edge.neighbour_station_name == next_station:
                    result.append((current_station, next_station, edge.line, edge.traveltime))
                    break

        return total_time, result


def read_graph_from_file(filename):
    graph = Graph()

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            line_name = parts[0]
            segments = parts[1].split('"')[1::2]  # Extract station names
            times = [int(x) for x in parts[1].split('"')[2::2] if x.strip().isdigit()]  # Extract travel times

            for i in range(len(segments) - 1):
                graph.add_edge(segments[i], segments[i + 1], times[i], line_name)

    return graph


def main():
    if len(sys.argv) != 4:
        print("Usage: find_path filename_graph start_station end_station")
        return

    filename = sys.argv[1]
    start_station = sys.argv[2]
    end_station = sys.argv[3]

    graph = read_graph_from_file(filename)
    total_time, path = graph.find_path(start_station, end_station)

    if total_time == float('inf'):
        print("No path found")
    else:
        print(f"Total travel time: {total_time} minutes")
        for (current, next, line, time) in path:
            print(f"{current} -> {next} via {line} ({time} minutes)")


if __name__ == '__main__':
    main()
