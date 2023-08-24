import folium
import openrouteservice as ors
import math

client = ors.Client(key='5b3ce3597851110001cf62482b4eac78da7b4dd2af533430ff8b926f')
coords = [
    [-87.7898356, 41.8879452],
    [-87.7808524, 41.8906422],
    [-87.7552925, 41.8809087],
    [-87.7728134, 41.8804058],
    [-87.7702890, 41.8802231],
    [-87.7787924, 41.8944518],
    [-87.7732345, 41.8770663],
    [-87.800701, 41.876214]
]

vehicle_start = [-87.7895149, 41.8933762]
m = folium.Map(location=list(reversed([-87.787984, 41.8871616])), tiles="cartodbpositron", zoom_start=14)
for coord in coords:
    folium.Marker(location=list(reversed(coord))).add_to(m)

folium.Marker(location=list(reversed(vehicle_start)), icon=folium.Icon(color="red")).add_to(m)
vehicles = [
    ors.optimization.Vehicle(id=0, profile='driving-car', start=vehicle_start, end=vehicle_start, capacity=[2]),
    ors.optimization.Vehicle(id=1, profile='driving-car', start=vehicle_start, end=vehicle_start, capacity=[4]),
    ors.optimization.Vehicle(id=2, profile='driving-car', start=vehicle_start, end=vehicle_start, capacity=[2]),
]
jobs = [ors.optimization.Job(id=index, location=coords, amount=[1]) for index, coords in enumerate(coords)]
optimized = client.optimization(jobs=jobs, vehicles=vehicles, geometry=True)
print(optimized)
line_colors = ['green', 'orange', 'blue', 'yellow']
for route in optimized['routes']:
    print(route)
    folium.PolyLine(
        locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(route['geometry'])['coordinates']],
        color=line_colors[route['vehicle']]).add_to(m)
m.save('mapa.html')
