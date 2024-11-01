# UTPB-COSC-6389-Project1

# Project Title

### Overview
This project addresses three classic computational problems using optimization algorithms: the Traveling Salesman Problem (TSP), the Knapsack Problem, and the Graph Coloring Problem. Each algorithm has been enhanced and optimized for improved solution quality, efficiency, interactivity, and user experience.

## Problem Summaries and Enhancements

### Traveling Salesman Problem (TSP)

**Description**  
The TSP seeks the shortest possible route that visits a list of cities and returns to the starting point. This project implements a simulated annealing-based approach, optimized for more efficient and accurate results.

**Enhancements and Contributions**  
- **Solution Quality**: Originally used only basic Simulated Annealing, now enhanced with 2-Opt optimization to improve local adjustments and path quality.
- **Initialization**: Updated from a random path to a Nearest-Neighbor Heuristic for a high-quality starting path.
- **Efficiency**: Optimized the cooling rate and temperature settings, which reduces the iteration count for faster convergence.
- **Interactivity**: Added a feature allowing users to dynamically generate points and observe real-time updates.
- **Solver Selection**: Implemented an option to choose between Simulated Annealing and Ant Colony Optimization.
- **Readability and Modularity**: Restructured code to be modular, making it more organized and easier to read.

### Knapsack Problem

**Description**  
The Knapsack Problem involves selecting items with given weights and values to maximize the total value without exceeding a weight limit. This project utilizes genetic algorithms with several enhancements for optimal performance.

**Enhancements and Contributions**  
- **Fitness Function**: Changed from an absolute difference from the target value to a scaled normalization, reducing bias and improving consistency in the search.
- **Selection Method**: Transitioned from weighted to tournament selection to promote diversity and prevent convergence to local optima.
- **Crossover Method**: Updated from single-point crossover to uniform crossover, increasing genetic diversity and improving trait mixing.
- **Mutation Method**: Enhanced with multi-point mutation for broader search exploration and effective local minima escape.
- **Elitism**: Modified from simple to selective elitism, balancing best-solution retention with population diversity.
- **UI Updates**: Replaced standard updates with asynchronous updates using `self.after()`, making the interface smoother and more responsive.

### Graph Coloring Problem

**Description**  
This program applies a genetic algorithm to solve the Graph Coloring Problem, where the goal is to assign colors to vertices such that no adjacent vertices share the same color.

**Algorithm Details and Contributions**  
- **Initialization**: Begins with a randomly generated population with color assignments for all vertices.
- **Fitness Evaluation**: Measures fitness based on the number of edge conflicts, with a goal to minimize conflicts.
- **Selection**: Selects the top half of individuals based on fitness to ensure the best solutions progress.
- **Crossover**: Uses a multi-point crossover for diverse trait mixing, helping the algorithm to escape local optima.
- **Adaptive Mutation**: Implements a probabilistic mutation that adapts over generations, shifting from exploration to refinement as the algorithm progresses.
- **Termination and Real-Time Feedback**: Terminates early if a solution with zero conflicts is found, providing visual feedback and generation tracking.

# Graph Coloring Problem Solver - UI Navigation

This document provides a guide for navigating the user interface of the **Graph Coloring Problem Solver** application. The app utilizes a genetic algorithm to solve the graph coloring problem, where the goal is to assign colors to vertices such that no two adjacent vertices share the same color.

## User Interface Components

1. **Vertex Input Field**:
   - **Label**: "Enter number of vertices:"
   - **Input Box**: Enter the desired number of vertices for your graph.
   
2. **Create Graph Button**:
   - **Button**: **Create Graph**
   - Click this button to generate a random graph based on the number of vertices specified. This action resets the canvas, allowing for new graph inputs.

3. **Graph Visualization Canvas**:
   - **Canvas**: Displays the graph visually with vertices and edges.
   - Initially, vertices are shown in gray, indicating that they have not been colored.

4. **Generation Counter**:
   - **Label**: "Generation: 0"
   - Displays the current generation count as the genetic algorithm runs.

5. **Solution Status Label**:
   - **Label**: (initially empty, will display solution status)
   - This label shows messages such as "Solution Found!" when a valid coloring solution is achieved.

6. **Find Solution Button**:
   - **Button**: **Find Solution**
   - Click this button to start the genetic algorithm. The algorithm will attempt to find a valid color assignment for the graph, updating the visualization as it progresses.

## Using the Application

1. **Input the Number of Vertices**:
   - Type in the desired number of vertices in the input field.

2. **Generate the Graph**:
   - Press the **Create Graph** button. The canvas will refresh and display a new random graph.

3. **Start the Coloring Algorithm**:
   - Click the **Find Solution** button to begin the genetic algorithm process. The generation count will update in real-time.

4. **Monitor the Progress**:
   - Observe the graph as the algorithm works towards finding a solution. If a solution is found, the canvas will update to show the colored vertices, and the solution status label will indicate success.

---





