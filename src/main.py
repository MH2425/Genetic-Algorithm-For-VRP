from GetData import GetData
import os

DEPOT = "Hanoi University of Science, Vietnam"
NUM_POINTS = 15
MAX_DISTANCE = 12

def main():
    """
    Main function to run the data generation process.
    Creates a GetData instance, runs it, and retrieves the results.
    """
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
    
    print(f"\nGeneration complete!")
    print(f"Generated {len(locations)} locations (1 origin + {len(locations)-1} destinations)")
    print(f"Distance matrix size: {len(distance_matrix)}×{len(distance_matrix[0])}")
    print(f"Map and distance matrix saved to {data_generator.output_dir}")

if __name__ == "__main__":
    main()