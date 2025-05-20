from GetData import GetData
from Chromosome import Chromosome
from Population import Population
from Genetic import Genetic
import os
import folium
import random
import matplotlib.pyplot as plt

# Location parameters
DEPOT = "Hanoi University of Science and Technology, Vietnam"
NUM_POINTS = 40
MAX_DISTANCE = 10
NUM_VEHICLES = 8  # Reduced to 3 for clearer visualization

# GA parameters
POPULATION_SIZE = 500
MAX_GENERATIONS = 500
SELECTION_RATE = 0.9
MUTATION_RATE = 0.1
ELITISM_SIZE = 2

def draw_routes(map_obj, locations, routes):
    """
    Draw routes on the map with different colors for each route.
    
    Args:
        map_obj: folium Map object
        locations: List of (lat, lon) tuples including depot at index 0
        routes: List of routes, each containing location indices
    """
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
              'darkblue', 'darkgreen', 'cadetblue', 'darkpurple',
              'pink', 'lightblue', 'lightgreen', 'gray', 'black']
    
    # Debug information
    print("\nDebug - Drawing routes:")
    
    # Draw each route with a unique color
    for i, route in enumerate(routes):
        route_color = colors[i % len(colors)]
        route_points = []
        route_debug = []
        
        # Convert route indices to coordinates
        for loc_idx in route:
            if loc_idx == -1:
                # Depot is at index 0 in locations list
                actual_loc = locations[0]
                label = "D"
            else:
                # Location indices in chromosome (0, 1, 2...) 
                # correspond to locations[1], locations[2], locations[3]...
                actual_loc = locations[loc_idx + 1]
                label = str(loc_idx)
            
            route_points.append(actual_loc)
            route_debug.append(label)
        
        # Print debug info for this route
        print(f"Route {i+1}: {' → '.join(route_debug)}")
        
        # Only draw routes with at least 2 points
        if len(route_points) >= 2:
            folium.PolyLine(
                route_points,
                color=route_color,
                weight=4,
                opacity=0.7,
                tooltip=f'Route {i+1}: {" → ".join(route_debug)}'
            ).add_to(map_obj)

def plot_evolution_progress(best_history, avg_history):
    """Plot the evolution of fitness over generations"""
    plt.figure(figsize=(10, 6))
    generations = range(len(best_history))
    
    plt.plot(generations, best_history, 'b-', label='Best Fitness')
    plt.plot(generations, avg_history, 'r-', label='Average Fitness')
    
    plt.title('Fitness Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Total Distance)')
    plt.legend()
    plt.grid(True)
    
    return plt

def main():
    print("Starting VRP solution with Genetic Algorithm...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(script_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    # Step 1: Generate location data
    data_generator = GetData(
        location_name=DEPOT, 
        num_random_points=NUM_POINTS,  
        max_distance_km=MAX_DISTANCE,    
        output_dir=static_dir
    )
    
    locations, distance_matrix = data_generator.run()
    
    # Step 2: Initialize population
    print("\n---------------------------------------")
    print(f"Initializing population of {POPULATION_SIZE} chromosomes")
    population = Population(
        pop_size=POPULATION_SIZE,
        num_locations=NUM_POINTS,
        num_vehicles=NUM_VEHICLES,
        distance_matrix=distance_matrix
    )
    
    # Draw initial best solution
    initial_best = population.find_best_chromosome()
    print("\nInitial Best Solution:")
    print(f"Fitness (Total Distance): {initial_best.fitness:.2f} km")
    print(initial_best)
    
    initial_map = data_generator.create_map()
    data_generator.add_markers()
    draw_routes(initial_map, locations, initial_best.get_routes())
    initial_map_path = os.path.join(static_dir, "initial_solution.html")
    initial_map.save(initial_map_path)
    print(f"Initial solution map saved to {initial_map_path}")
    
    # Step 3: Run genetic algorithm
    print("\n---------------------------------------")
    print("Starting genetic algorithm evolution...")
    ga = Genetic(
        population=population,
        max_generations=MAX_GENERATIONS,
        selection_rate=SELECTION_RATE,
        mutation_rate=MUTATION_RATE,
        elitism_size=ELITISM_SIZE
    )
    
    final_solution = ga.run(verbose=True)
    
    # Step 4: Visualize final solution
    print("\n---------------------------------------")
    print("Final Solution:")
    print(f"Fitness (Total Distance): {final_solution.fitness:.2f} km")
    print(final_solution)
    
    final_map = data_generator.create_map()
    data_generator.add_markers()
    draw_routes(final_map, locations, final_solution.get_routes())
    final_map_path = os.path.join(static_dir, "final_solution.html")
    final_map.save(final_map_path)
    print(f"Final solution map saved to {final_map_path}")
    
    # Step 5: Plot fitness evolution
    print("\n---------------------------------------")
    print("Plotting fitness evolution...")
    progress = ga.get_progress()
    plt = plot_evolution_progress(
        progress["best_fitness_history"], 
        progress["avg_fitness_history"]
    )
    plot_path = os.path.join(static_dir, "fitness_evolution.png")
    plt.savefig(plot_path)
    print(f"Fitness evolution plot saved to {plot_path}")
    
    # Calculate improvement
    improvement = 1 - (final_solution.fitness / initial_best.fitness)
    print(f"\nImprovement: {improvement:.2%}")
    print("VRP solution completed successfully!")

if __name__ == "__main__":
    main()