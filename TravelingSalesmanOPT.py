import math
import random
import tkinter as tk

# Parameters
num_cities = 25
city_scale = 5
road_width = 4
padding = 100
cooling_rate = 0.995
initial_temp = 1000

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, color='black'):
        canvas.create_oval(self.x - city_scale, self.y - city_scale,
                           self.x + city_scale, self.y + city_scale, fill=color)

class Edge:
    def __init__(self, a, b):
        self.city_a = a
        self.city_b = b
        self.length = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def draw(self, canvas, color='grey', style=(2, 4)):
        canvas.create_line(self.city_a.x, self.city_a.y,
                           self.city_b.x, self.city_b.y,
                           fill=color, width=road_width, dash=style)

class TravelingSalesman:
    def __init__(self, nodes):
        self.nodes = nodes
        self.best_path = list(range(len(nodes)))
        self.best_distance = self.calculate_total_distance(self.best_path)

    def calculate_total_distance(self, path):
        return sum(math.sqrt((self.nodes[path[i]].x - self.nodes[path[i - 1]].x) ** 2 +
                             (self.nodes[path[i]].y - self.nodes[path[i - 1]].y) ** 2)
                   for i in range(len(path)))

    def two_opt(self, path):
        best = path[:]
        improved = True
        while improved:
            improved = False
            for i in range(1, len(best) - 2):
                for j in range(i + 1, len(best)):
                    if j - i == 1: continue
                    new_path = best[:]
                    new_path[i:j] = best[j - 1:i - 1:-1]
                    new_distance = self.calculate_total_distance(new_path)
                    if new_distance < self.calculate_total_distance(best):
                        best = new_path
                        improved = True
            path = best
        return path

    def simulated_annealing(self):
        current_path = self.best_path[:]
        current_distance = self.best_distance
        temperature = initial_temp

        while temperature > 1:
            new_path = current_path[:]
            i, j = random.sample(range(len(self.nodes)), 2)
            new_path[i], new_path[j] = new_path[j], new_path[i]
            new_path = self.two_opt(new_path)  # Apply 2-opt optimization
            new_distance = self.calculate_total_distance(new_path)

            if (new_distance < current_distance or
                math.exp((current_distance - new_distance) / temperature) > random.random()):
                current_path, current_distance = new_path, new_distance
                if new_distance < self.best_distance:
                    self.best_path, self.best_distance = new_path, new_distance

            temperature *= cooling_rate
            yield self.best_path, self.best_distance  # Yield for real-time update

class UI(tk.Tk):
    def __init__(self, tsp_solver):
        super().__init__()
        self.tsp_solver = tsp_solver
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        self.distance_text = self.canvas.create_text(400, 20, text="Distance: 0", font=("Arial", 16))
        self.nodes = tsp_solver.nodes
        self.edges = [Edge(self.nodes[i], self.nodes[i + 1]) for i in range(len(self.nodes) - 1)]
        self.current_edges = []
        self.title("Enhanced Traveling Salesman Problem - Real-Time Solution")

    def draw_nodes(self):
        for i, node in enumerate(self.nodes):
            color = 'red' if i == 0 else 'black'
            node.draw(self.canvas, color=color)

    def draw_edges(self, path, distance):
        for edge in self.current_edges:
            self.canvas.delete(edge)
        self.current_edges = []

        for i in range(len(path)):
            a, b = self.nodes[path[i - 1]], self.nodes[path[i]]
            edge_id = self.canvas.create_line(a.x, a.y, b.x, b.y, fill="blue", width=road_width)
            self.current_edges.append(edge_id)

        self.canvas.itemconfig(self.distance_text, text=f"Distance: {distance:.2f}")
        self.canvas.update()

    def update_path(self):
        for path, distance in self.tsp_solver.simulated_annealing():
            self.draw_edges(path, distance)

if __name__ == "__main__":
    nodes = [Node(random.randint(padding, 700), random.randint(padding, 500)) for _ in range(num_cities)]
    tsp_solver = TravelingSalesman(nodes)
    ui = UI(tsp_solver)
    ui.draw_nodes()
    ui.update_path()
    ui.mainloop()
