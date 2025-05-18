from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import random
import csv
import math
import os

class GetData:
    """A class for generating and managing location data for Vehicle Routing Problems."""
    
    def __init__(self, location_name="Hanoi University of Science, Vietnam", 
                 num_random_points=10, max_distance_km=10, output_dir="./static/"):
        """
        Initialize the GetData class.
        
        Args:
            location_name (str): Name of the central location to geocode
            num_random_points (int): Number of random points to generate
            max_distance_km (float): Maximum distance in km for random points
            output_dir (str): Directory to save output files
        """
        self.location_name = location_name
        self.num_random_points = num_random_points
        self.max_distance_km = max_distance_km
        self.output_dir = output_dir
        self.locations = []
        self.distance_matrix = []
        self.map = None
        self.lat = None
        self.lon = None
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def fetch_coordinates(self):
        """Get coordinates of the original location."""
        geolocator = Nominatim(user_agent="map-example")
        location = geolocator.geocode(self.location_name)
        self.lat, self.lon = location.latitude, location.longitude
        self.locations = [(self.lat, self.lon)]
        return self.lat, self.lon
    
    def generate_random_point(self, base_lat, base_lon):
      """
      Generate a random point within specified distance from base point
      using accurate geodesic calculations.
      """
      # Generate random distance (in km) within the maximum allowed distance
      dist = random.uniform(0, self.max_distance_km)
      
      # Generate random bearing/direction (0-360 degrees)
      bearing = random.uniform(0, 360)
      
      # Create a starting point
      start = (base_lat, base_lon)
      
      # Calculate destination point using geodesic calculations
      destination = geodesic(kilometers=dist).destination(point=start, bearing=bearing)
      
      # Return the latitude and longitude of the destination point
      return destination.latitude, destination.longitude
    
    def create_map(self):
        """Create a folium map centered on the main location."""
        if self.lat is None or self.lon is None:
            self.fetch_coordinates()
        self.map = folium.Map(location=[self.lat, self.lon], zoom_start=13)
        return self.map
    
    def add_markers(self):
        """Add markers to the map for all locations."""
        if self.map is None:
            self.create_map()
        
        # Add original marker
        folium.Marker(
            [self.lat, self.lon],
            popup=self.location_name,
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(self.map)
        
        # Add random point markers
        for i, (lat, lon) in enumerate(self.locations[1:], 1):
            folium.Marker(
                [lat, lon],
                popup=f"Random Point {i}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(self.map)
            
    def generate_random_locations(self):
        """Generate random locations around the main point."""
        if self.lat is None or self.lon is None:
            self.fetch_coordinates()
        
        for i in range(self.num_random_points):
            r_lat, r_lon = self.generate_random_point(self.lat, self.lon)
            self.locations.append((r_lat, r_lon))
            
        return self.locations
    
    def calculate_distance_matrix(self):
        """Calculate distance matrix between all locations."""
        n = len(self.locations)
        self.distance_matrix = [[0.0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.distance_matrix[i][j] = geodesic(self.locations[i], self.locations[j]).km
        
        return self.distance_matrix
    
    def save_map(self, filename="map.html"):
        """Save the map to an HTML file."""
        if self.map is None:
            self.add_markers()
        
        filepath = os.path.join(self.output_dir, filename)
        self.map.save(filepath)
        print(f"Map saved to {filepath}")
        
    def save_distance_matrix(self, filename="distance_matrix.csv"):
        """Save the distance matrix to a CSV file."""
        if not self.distance_matrix:
            self.calculate_distance_matrix()
            
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            # Write header
            headers = [""] + [f"P{i}" for i in range(len(self.locations))]
            writer.writerow(headers)
            # Write rows
            for i, row in enumerate(self.distance_matrix):
                writer.writerow([f"P{i}"] + [f"{dist:.2f}" for dist in row])
        
        print(f"Distance matrix saved to {filepath}")
    
    def run(self):
        """Execute the complete data generation process."""
        self.fetch_coordinates()
        self.generate_random_locations()
        self.create_map()
        self.add_markers()
        self.calculate_distance_matrix()
        self.save_map()
        self.save_distance_matrix()
        return self.locations, self.distance_matrix