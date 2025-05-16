from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import random
import csv
import math

# 1. Get coordinates of original location
geolocator = Nominatim(user_agent="map-example")
location = geolocator.geocode("Hanoi University of Science, Vietnam")
lat, lon = location.latitude, location.longitude

# 2. Create a map centered on the location
map = folium.Map(location=[lat, lon], zoom_start=13)

# 3. Add original marker
locations = [(lat, lon)]
folium.Marker(
    [lat, lon],
    popup="Hanoi University of Science",
    icon=folium.Icon(color="red", icon="flag")
).add_to(map)

# 4. Generate 10 random coordinates within 10 km
def generate_random_point(base_lat, base_lon, max_dist_km):
    # Convert distance in km to degrees roughly
    radius = max_dist_km / 111  # 1 degree ~ 111 km
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(0, radius)
    dlat = dist * math.cos(angle)
    dlon = dist * math.sin(angle) / math.cos(math.radians(base_lat))
    return base_lat + dlat, base_lon + dlon

for i in range(10):
    r_lat, r_lon = generate_random_point(lat, lon, 10)
    locations.append((r_lat, r_lon))
    folium.Marker(
        [r_lat, r_lon],
        popup=f"Random Point {i+1}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

# 5. Save map
map.save("./static/hus.html")
print(f"Map saved to hus.html with coordinates: {lat}, {lon} and 10 more points.")

# 6. Calculate distance matrix
n = len(locations)
distance_matrix = [[0.0]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        if i != j:
            distance_matrix[i][j] = geodesic(locations[i], locations[j]).km

# 7. Save distance matrix to CSV
with open("./static/distance_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write header
    headers = [""] + [f"P{i}" for i in range(n)]
    writer.writerow(headers)
    # Write rows
    for i, row in enumerate(distance_matrix):
        writer.writerow([f"P{i}"] + [f"{dist:.2f}" for dist in row])

print("Distance matrix saved to distance_matrix.csv")
