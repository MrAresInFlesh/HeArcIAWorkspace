from heuristics.Heuristics import Heuristic


class AStar:

    def __init__(self, data, graph, start, goal, heuristic='h0'):
        self.heuristic = Heuristic(data, start, goal, heuristic)
        self.data = data
        self.graph = graph
        self.start = start
        self.goal = goal
        self.nodes_visited = set()

    def getNeighbours(self, n):
        neighbours  = [connection[1] for connection in self.graph if connection[0] == n]
        neighbours += [connection[0] for connection in self.graph if connection[1] == n]
        return neighbours

    def process(self):

        border = {self.start: (0, self.heuristic.process(self.data, self.start, self.goal))}
        history = {self.start: 0}
        counter = 0

        while border:
            n = list(border.keys())[0]
            (gn, hn) = border.pop(n)
            history[n] = (gn, hn)
            self.nodes_visited.add(n)

            counter += 1
            if n == self.goal:
                print(f"| >--Origin : {self.start}  |>-->>--> To >-->>--<>  Destination : {n}; \n|\n"
                      f"| [Visited cities / nodes] before finding the shortest path : \n| {self.nodes_visited}")
                return counter, gn
            for neighbor in self.getNeighbours(n):
                try:
                    dist = self.graph[(n, neighbor)]
                except:
                    dist = self.graph[(neighbor, n)]

                g = dist + gn
                h = self.heuristic.process(self.data, neighbor, self.goal)
                added = 0

                if neighbor not in border and neighbor not in history:
                    border[neighbor] = (g, h)
                    added = 1
                elif neighbor in border:
                    if g < border[neighbor][0]:
                        border[neighbor] = (g, h)
                        added = 1
                if added == 0 and neighbor in history:
                    if g < history[neighbor][0]:
                        border[neighbor] = (g, h)

                border = {k: v for k, v in sorted(border.items(), key=lambda item: item[1][0] + item[1][1])}

        return None
