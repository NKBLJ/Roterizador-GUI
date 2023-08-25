import folium
import requests
import os
import openrouteservice as ors

with open("api-key.txt", "r") as file:
    api_key = file.readline().strip()

base_url = 'https://api.openrouteservice.org/optimization'

coords = [('-5.0568026', '-42.8291832'), ('-5.062155', '-42.8202207'), ('-5.0622813', '-42.8202841'), ('-5.0565216', '-42.8147959'), ('-5.0662585', '-42.8121082'), ('-5.0641087', '-42.7982927'), ('-5.0864481', '-42.7865854'), ('-5.0961424', '-42.7944843'), ('-5.0849027', '-42.8156422'), ('-5.07617', '-42.8098266'), ('-5.0764541', '-42.8162912'), ('-5.0737711', '-42.8202524'), ('-5.0728557', '-42.8158793')]
coords = [[float(j), float(i)] for i, j in coords]

vehicle_start = [-42.8141138, -5.0775346]

m = folium.Map(location=list(reversed(vehicle_start)), tiles="cartodbpositron", zoom_start=14)
for coord in coords:
    folium.Marker(location=list(reversed(coord))).add_to(m)

folium.Marker(location=list(reversed(vehicle_start)), icon=folium.Icon(color="red")).add_to(m)
vehicles = [{"id":0,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [5]},
            {"id":1,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [5]},
            {"id":2,"profile":"driving-car","start":vehicle_start,"end":vehicle_start, "capacity": [5]}]

jobs = [{"id": index+1, "location": coords, "amount": [1]} for index, coords in enumerate(coords)]


# Requisição
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    "jobs": jobs,
    "vehicles": vehicles,
    "options": {
        "g": True  # Solicita a inclusão da geometria
    },
}


response = requests.post(base_url, json=data, headers=headers)

optimized = response.json()
print(optimized)

line_colors = ['green', 'orange', 'blue', 'yellow']
for route in optimized['routes']:
    folium.PolyLine(
        locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(route['geometry'])['coordinates']],
        color=line_colors[route['vehicle']]).add_to(m)

m.save('mapa.html')
