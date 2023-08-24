import folium
import requests
import os
import openrouteservice as ors

with open("api-key.txt", "r") as file:
    api_key = file.readline().strip()

base_url = 'https://api.openrouteservice.org/optimization'

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

m = folium.Map(location=list(reversed(vehicle_start)), tiles="cartodbpositron", zoom_start=14)
for coord in coords:
    folium.Marker(location=list(reversed(coord))).add_to(m)

folium.Marker(location=list(reversed(vehicle_start)), icon=folium.Icon(color="red")).add_to(m)
vehicles = [{"id":1,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [2]},
            {"id":2,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [3]},
            {"id":3,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [2]}]

jobs = [{"id": index+1, "location": coords, "amount": [1]} for index, coords in enumerate(coords)]

# Requisição
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    "jobs": jobs,
    "vehicles": vehicles
}


response = requests.post(base_url, json=data, headers=headers)

if response.status_code == 200:
    optimized = response.json()
    print(optimized)
    line_colors = ['green', 'orange', 'blue', 'yellow']
    for route in optimized['routes']:
        print(route)
    #     folium.PolyLine(
    #         locations=[list(reversed(coords)) for coords in
    #                    ors.convert.decode_polyline(route['geometry'])['coordinates']],
    #         color=line_colors[route['vehicle']]).add_to(m)
    # m.save('mapa.html')
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)

