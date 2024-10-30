import tkinter as tk
import numpy as np
import random

class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Coloring Problem (Genetic Algorithm)")

        # Prompt user for number of vertices
        tk.Label(root, text="Enter number of vertices:").grid(row=0, column=0)
        self.vertex_entry = tk.Entry(root)
        self.vertex_entry.grid(row=0, column=1)

        # Button to create graph
        create_button = tk.Button(root, text="Create Graph", command=self.create_graph)
        create_button.grid(row=1, column=0, columnspan=2)

        # Canvas to visualize graph
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.grid(row=2, column=0, columnspan=2)

        # Label to display generation count
        self.generation_label = tk.Label(root, text="Generation: 0")
        self.generation_label.grid(row=3, column=0, columnspan=2)

        # Label to indicate solution status
        self.solution_label = tk.Label(root, text="", fg="green")
        self.solution_label.grid(row=4, column=0, columnspan=2)

        # Button to solve graph coloring
        solve_button = tk.Button(root, text="Find Solution",
                                 command=self.solve_with_genetic_algorithm)
        solve_button.grid(row=5, column=0, columnspan=2)

        # Parameters for genetic algorithm
        self.population_size = 100
        self.num_colors = None

    def create_graph(self):
        """Generate random adjacency matrix based on user input and start algorithm."""
        num_vertices = int(self.vertex_entry.get())
        self.num_colors = num_vertices
        self.adj_matrix = np.random.randint(0, 2, size=(num_vertices, num_vertices))
        np.fill_diagonal(self.adj_matrix, 0)  # No self-loops
        self.num_vertices = num_vertices
        self.vertices_positions = self.generate_vertices_positions()

        # Clear the solution message and canvas
        self.solution_label.config(text="")  # Reset solution status
        self.canvas.delete("all")  # Clear previous graph

        self.draw_graph()

        # Solve button for running genetic algorithm
        solve_button = tk.Button(self.root, text="Find Solution",
                                 command=self.solve_with_genetic_algorithm)
        solve_button.grid(row=5, column=0, columnspan=2)

    def generate_vertices_positions(self):
        radius = 150
        center_x, center_y = 200, 200
        positions = []
        for i in range(self.num_vertices):
            angle = 2 * np.pi * i / self.num_vertices
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            positions.append((x, y))
        return positions

    def draw_graph(self, solution=None):
        self.canvas.delete("all")
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]

        for i, (x, y) in enumerate(self.vertices_positions):
            color = colors[solution[i] % len(colors)] if solution else "gray"
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline="black")
            self.canvas.create_text(x, y, text=str(i + 1), font=("Arial", 14))

        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] == 1:
                    x1, y1 = self.vertices_positions[i]
                    x2, y2 = self.vertices_positions[j]
                    self.canvas.create_line(x1, y1, x2, y2, fill="black")

    def solve_with_genetic_algorithm(self):
        """Run the genetic algorithm to solve the graph coloring problem."""
        self.population = self.generate_population()
        self.evolve_graph_coloring()

    def generate_population(self):
        """Initialize a random population of color assignments."""
        return [[random.randint(0, self.num_colors - 1) for _ in range(self.num_vertices)]
                for _ in range(self.population_size)]

    def fitness(self, individual):
        """Calculate fitness based strictly on the number of conflicts."""
        conflicts = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] == 1 and individual[i] == individual[j]:
                    conflicts += 1
        return conflicts  # Lower is better; zero conflicts is ideal.

    def evolve_graph_coloring(self):
        generations = 1000
        for generation in range(generations):
            # Update generation label on UI
            self.generation_label.config(text=f"Generation: {generation}")
            self.root.update_idletasks()

            fitness_scores = [self.fitness(ind) for ind in self.population]
            best_fitness = min(fitness_scores)

            # Check if a solution has been found
            if best_fitness == 0:  # Ideal solution reached
                solution = self.population[fitness_scores.index(best_fitness)]
                self.draw_graph(solution)
                self.solution_label.config(text="Solution Found!")  # Update solution label
                return

            # Select parents and generate new population
            parents = self.select_parents(fitness_scores)
            new_population = parents[:]
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = self.multi_point_crossover(parent1, parent2)
                child = self.adaptive_mutate(child, generation)
                new_population.append(child)

            # Update population and show best solution found so far
            self.population = new_population
            self.draw_graph(self.population[fitness_scores.index(best_fitness)])

    def select_parents(self, fitness_scores):
        """Select individuals with the lowest fitness scores (less conflicts)."""
        sorted_population = [ind for _, ind in sorted(zip(fitness_scores, self.population), key=lambda x: x[0])]
        return sorted_population[:self.population_size // 2]

    def multi_point_crossover(self, parent1, parent2):
        """Perform multi-point crossover with two crossover points."""
        crossover_point1 = random.randint(1, self.num_vertices // 2)
        crossover_point2 = random.randint(crossover_point1, self.num_vertices - 1)
        return parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]

    def adaptive_mutate(self, individual, generation):
        """Adaptive mutation rate to allow more exploration in early generations."""
        mutation_rate = max(0.05, 0.5 - (generation * 0.0005))
        for i in range(self.num_vertices):
            if random.random() < mutation_rate:
                individual[i] = random.randint(0, self.num_colors - 1)
        return individual

# Run the app
root = tk.Tk()
app = GraphColoringApp(root)
root.mainloop()
