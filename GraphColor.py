import tkinter as tk
import numpy as np
import random
from random import randint

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
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.grid(row=2, column=0, columnspan=2)

        # Label to display generation count
        self.generation_label = tk.Label(root, text="Generation: 0")
        self.generation_label.grid(row=3, column=0, columnspan=2)

        # Label to indicate solution status
        self.solution_label = tk.Label(root, text="", fg="green")
        self.solution_label.grid(row=4, column=0, columnspan=2)

        # Button to solve graph coloring
        solve_button = tk.Button(root, text="Find Solution", command=self.solve_with_genetic_algorithm)
        solve_button.grid(row=5, column=0, columnspan=2)

        # Parameters for genetic algorithm
        self.population_size = 60
        self.max_num_colors = None
        self.graph = None

        # Color palette for vertices
        self.colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "brown", "gray"]

    def create_graph(self):
        """Generate random adjacency matrix based on user input and start algorithm."""
        self.n = int(self.vertex_entry.get())  # number of vertices
        self.graph = np.random.randint(0, 2, size=(self.n, self.n))
        np.fill_diagonal(self.graph, 0)  # No self-loop (diagonal 0)
        self.graph = np.triu(self.graph, 1)  # Make graph symmetric

        self.max_num_colors = self.get_max_colors()
        self.population = self.create_population()

        # Clear the solution message and canvas
        self.solution_label.config(text="")  # Reset solution status
        self.canvas.delete("all")  # Clear previous graph

        # Draw graph with empty coloring (vertices only, no solution)
        self.draw_graph(solution=None)

    def get_max_colors(self):
        """Get maximum number of colors based on graph structure."""
        return self.n  # Maximum colors needed could be the number of vertices in the worst case

    def create_chromosome(self):
        """Generate a random chromosome for a solution."""
        return np.random.randint(1, self.max_num_colors + 1, size=(self.n))

    def create_population(self):
        """Create a population of chromosomes."""
        return np.array([self.create_chromosome() for _ in range(self.population_size)])

    def calc_fitness(self, chromosome):
        """Calculate fitness based on penalty for adjacent vertices sharing the same color."""
        penalty = 0
        for vertex1 in range(self.n):
            for vertex2 in range(vertex1 + 1, self.n):
                if self.graph[vertex1][vertex2] == 1 and chromosome[vertex1] == chromosome[vertex2]:
                    penalty += 1
        return penalty

    def draw_graph(self, solution=None):
        """Draw the graph on the canvas, showing adjacency and highlighting conflicts if any."""
        self.canvas.delete("all")  # Clear previous graph

        # Generate positions for vertices
        positions = self.generate_vertices_positions()

        # Draw edges (connections between adjacent vertices)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.graph[i][j] == 1:  # Only draw if vertices i and j are adjacent
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]

                    # Check if the vertices share the same color in the solution
                    if solution is not None and solution[i] == solution[j]:
                        # Draw red line for conflict
                        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
                    else:
                        # Draw normal line for adjacency
                        self.canvas.create_line(x1, y1, x2, y2, fill="black", dash=(2, 2))

        # Draw vertices (nodes)
        for i in range(self.n):
            x, y = positions[i]

            # Determine the color for the node based on the solution (if available)
            color = self.colors[solution[i] % len(self.colors)] if solution is not None else "gray"

            # Draw node circle with color
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, outline="black")

            # Label the node with its index
            self.canvas.create_text(x, y, text=str(i), fill="white")

    def generate_vertices_positions(self):
        """Generate positions for the vertices on the canvas."""
        radius = 150
        center_x, center_y = 250, 250
        positions = []
        for i in range(self.n):
            angle = 2 * np.pi * i / self.n
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            positions.append((x, y))
        return positions

    def solve_with_genetic_algorithm(self):
        """Run the genetic algorithm to solve the graph coloring problem."""
        generations = 200
        best_fitness = float('inf')
        fittest = None

        for generation in range(generations):
            self.generation_label.config(text=f"Generation: {generation}")
            self.root.update_idletasks()

            # Selection
            population = self.tournament_selection()

            # Crossover
            children_population = []
            random.shuffle(population)
            for i in range(0, len(population) - 1, 2):
                child1, child2 = self.one_point_crossover(population[i], population[i + 1])
                children_population.append(child1)
                children_population.append(child2)

            # Mutation
            for chromosome in children_population:
                mutation_chance = 0.65 if generation < 100 else (0.5 if generation < 150 else 0.15)
                self.mutation(chromosome, mutation_chance)

            # Update population
            self.population = children_population
            best_fitness, fittest = self.get_best_fitness()

            if best_fitness == 0:
                self.draw_graph(fittest)
                self.solution_label.config(text="Solution Found!")
                return

        self.draw_graph(fittest)

    def tournament_selection(self):
        """Tournament selection to choose parents for crossover."""
        new_population = []
        while len(new_population) < self.population_size:
            random.shuffle(self.population)
            for i in range(0, self.population_size - 1, 2):
                if self.calc_fitness(self.population[i]) < self.calc_fitness(self.population[i + 1]):
                    new_population.append(self.population[i])
                else:
                    new_population.append(self.population[i + 1])
        return new_population

    def one_point_crossover(self, parent1, parent2):
        """One-point crossover between two parents."""
        split_point = randint(1, self.n - 1)
        child1 = np.concatenate((parent1[:split_point], parent2[split_point:]))
        child2 = np.concatenate((parent2[:split_point], parent1[split_point:]))
        return child1, child2

    def mutation(self, chromosome, chance):
        """Mutate a chromosome based on a given chance."""
        if random.uniform(0, 1) <= chance:
            vertex = randint(0, self.n - 1)
            chromosome[vertex] = randint(1, self.max_num_colors)

    def get_best_fitness(self):
        """Get the best fitness from the current population."""
        best_fitness = float('inf')
        fittest = None
        for individual in self.population:
            fitness = self.calc_fitness(individual)
            if fitness < best_fitness:
                best_fitness = fitness
                fittest = individual
        return best_fitness, fittest


# Run the app
root = tk.Tk()
app = GraphColoringApp(root)
root.mainloop()
