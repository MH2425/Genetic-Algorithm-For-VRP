from GetData import GetData
from Chromosome import Chromosome
import os
import folium
import random

DEPOT = "Hanoi University of Science, Vietnam"
NUM_POINTS = 10
MAX_DISTANCE = 12
NUM_VEHICLES = 3  # Define number of vehicles

def draw_routes(map_obj, locations, routes):
    """
    Draw routes on the map with different colors for each route.
    
    Args:
        map_obj: folium Map object
        locations: List of (lat, lon) tuples including depot at index 0
        routes: List of routes, each containing location indices
    """
    # List of distinct colors for routes
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

def main():
    print("Starting data generation process...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(script_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    data_generator = GetData(
        location_name=DEPOT, 
        num_random_points=NUM_POINTS,  
        max_distance_km=MAX_DISTANCE,    
        output_dir=static_dir
    )
    
    locations, distance_matrix = data_generator.run()
    
    # print(f"\nTesting Chromosome class with {NUM_POINTS} locations and {NUM_VEHICLES} vehicles")
    
    # # Create 3 random chromosomes for testing
    # chromosomes = []
    # for i in range(3):
    #     chrom = Chromosome(NUM_POINTS, NUM_VEHICLES)
    #     fitness = chrom.calculate_fitness(distance_matrix)
    #     chromosomes.append(chrom)
    #     print(f"\nChromosome {i+1} - Fitness: {fitness:.2f} km")
    #     print(f"Genes: {chrom.genes}")
    #     print(chrom)
    
    # # Select the best chromosome to visualize
    # best_chrom = min(chromosomes, key=lambda x: x.fitness)
    # print(f"\nVisualizing best chromosome (Fitness: {best_chrom.fitness:.2f} km)")
    
    # # Create a new map for route visualization
    # route_map = data_generator.create_map()
    # data_generator.add_markers()
    
    # # Draw routes on map
    # draw_routes(route_map, locations, best_chrom.get_routes())
    
    # # Save the route map
    # route_map_path = os.path.join(static_dir, "route_map.html")
    # route_map.save(route_map_path)
    # print(f"Route map saved to {route_map_path}")

if __name__ == "__main__":
    main()