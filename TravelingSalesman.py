import math
import random
import tkinter as tk

# Parameters
num_cities = 50
city_scale = 5
road_width = 3
padding = 100
cooling_rate = 0.995
initial_temp = 1000
best_edge_color = "blue"
excluded_edge_color = "grey"
node_color = "black"
start_node_color = "red"


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, color=node_color):
        canvas.create_oval(self.x - city_scale, self.y - city_scale,
                           self.x + city_scale, self.y + city_scale, fill=color)


class TravelingSalesman:
    def __init__(self, nodes):
        self.nodes = nodes
        self.best_path = list(range(len(nodes)))
        self.best_distance = self.calculate_total_distance(self.best_path)

    def calculate_total_distance(self, path):
        # Total distance including returning to the starting city
        return sum(math.sqrt((self.nodes[path[i]].x - self.nodes[path[i - 1]].x) ** 2 +
                             (self.nodes[path[i]].y - self.nodes[path[i - 1]].y) ** 2)
                   for i in range(len(path))) + math.sqrt((self.nodes[path[-1]].x - self.nodes[path[0]].x) ** 2 +
                                                          (self.nodes[path[-1]].y - self.nodes[path[0]].y) ** 2)

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
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        self.tsp_solver = None
        self.current_edges = []
        self.distance_text = None

        # Generate new cities button
        self.generate_button = tk.Button(self, text="Generate New Cities", command=self.generate_new_cities)
        self.generate_button.pack(pady=10)

        # Initialize UI elements with blank canvas
        self.initialize_ui(blank=True)

    def initialize_ui(self, blank=False):
        self.title("Traveling Salesman Problem - Real-Time Solution")
        if not blank:
            self.distance_text = self.canvas.create_text(400, 20, text="Distance: 0", font=("Arial", 12))
        else:
            self.distance_text = None  # Start without any distance text

    def generate_new_cities(self):
        # Clear canvas and generate a new set of nodes
        self.canvas.delete("all")  # Clear all previous drawings
        nodes = [Node(random.randint(padding, 700), random.randint(padding, 500)) for _ in range(num_cities)]
        self.tsp_solver = TravelingSalesman(nodes)

        # Initialize UI to display distance text after generation
        if not self.distance_text:
            self.distance_text = self.canvas.create_text(400, 20, text="Distance: 0", font=("Arial", 12))

        self.update_path()  # Start solving and drawing path

    def draw_nodes(self):
        self.canvas.delete("node")  # Clear previous nodes
        for i, node in enumerate(self.tsp_solver.nodes):
            color = start_node_color if i == 0 else node_color
            node.draw(self.canvas, color=color)

    def draw_edges(self, path, distance):
        # Clear previous edges
        for edge in self.current_edges:
            self.canvas.delete(edge)
        self.current_edges = []

        # Draw edges in the path
        for i in range(len(path)):
            a, b = self.tsp_solver.nodes[path[i - 1]], self.tsp_solver.nodes[path[i]]
            color = best_edge_color if i < len(path) else excluded_edge_color
            edge_id = self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color, width=road_width)
            self.current_edges.append(edge_id)

        # Close the loop by connecting the last node back to the first
        start_node = self.tsp_solver.nodes[path[0]]
        end_node = self.tsp_solver.nodes[path[-1]]
        loop_edge_id = self.canvas.create_line(end_node.x, end_node.y, start_node.x, start_node.y, fill=best_edge_color,
                                               width=road_width)
        self.current_edges.append(loop_edge_id)

        # Update distance display
        self.canvas.itemconfig(self.distance_text, text=f"Distance: {distance:.2f}")
        self.canvas.update()

    def update_path(self):
        self.draw_nodes()  # Draw new nodes
        for path, distance in self.tsp_solver.simulated_annealing():
            self.draw_edges(path, distance)


if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
